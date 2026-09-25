import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import time
import threading
from core.camera import EphemeralCamera
from core.screen_monitor import ScreenMonitor
from core.audio_monitor import AudioMonitor
from core.emotion_engine import EmotionEngine
from core.content_classifier import ContentClassifier
from core.distraction_tracker import DistractionTracker
from core.alert_dispatcher import AlertDispatcher
from config import FRAME_INTERVAL_SECONDS, NOISE_THRESHOLD_DB
from ui.dashboard import Dashboard

state = {
    "emotion":        "focused",
    "content_type":   "neutral",
    "phone_detected": False,
    "face_present":   True,
    "noise_db":       0,
    "timers":         {},
    "window_title":   "",
    "running":        True
}

camera  = EphemeralCamera()
screen  = ScreenMonitor()
audio   = AudioMonitor()
emotion = EmotionEngine()
content = ContentClassifier()
tracker = DistractionTracker()
alerter = AlertDispatcher()

def analysis_loop():
    camera.start()
    audio.start()
    while state["running"]:
        try:
            title    = screen.get_browser_tab_title()
            noise_db = audio.get_noise_db()

            state["window_title"] = title
            state["noise_db"]     = noise_db
            state["content_type"] = content.classify(title)

            frame = camera.get_frame()
            if frame is not None:
                state["emotion"]        = emotion.analyze(frame)
                state["phone_detected"] = emotion.detect_phone(frame)
                state["face_present"]   = emotion.is_face_present()
                del frame

            alerts = tracker.update(
                state["content_type"],
                state["phone_detected"],
                noise_db,
                NOISE_THRESHOLD_DB,
                face_present=state["face_present"]
            )
            state["timers"] = tracker.get_timers()

            for alert_type in alerts:
                alerter.send_alert(alert_type)

            alerter.send_emotion_alert(state["emotion"])

        except Exception as e:
            print(f"[Loop error] {e}")

        time.sleep(FRAME_INTERVAL_SECONDS)

    print("[EduSentinel] Stopping...")
    camera.stop()
    audio.stop()
    print("[EduSentinel] Shutdown complete.")

def on_close():
    state["running"] = False
    time.sleep(1)

if __name__ == "__main__":
    t = threading.Thread(target=analysis_loop, daemon=True)
    t.start()
    Dashboard(state, on_close=on_close).run()
    on_close()