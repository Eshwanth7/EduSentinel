import os, time
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

print("Step 1: importing modules...")
from core.camera import EphemeralCamera
from core.screen_monitor import ScreenMonitor
from core.audio_monitor import AudioMonitor
from core.emotion_engine import EmotionEngine
from core.content_classifier import ContentClassifier
from core.distraction_tracker import DistractionTracker
from core.alert_dispatcher import AlertDispatcher
print("Step 2: all imports done")

print("Step 3: creating objects...")
cam = EphemeralCamera()
scr = ScreenMonitor()
aud = AudioMonitor()
emo = EmotionEngine()
cnt = ContentClassifier()
trk = DistractionTracker()
alt = AlertDispatcher()
print("Step 4: objects created")

print("Step 5: starting camera...")
cam.start()
print("Step 6: camera started")

print("Step 7: starting audio...")
aud.start()
print("Step 8: audio started")

print("Step 9: getting frame...")
frame = cam.get_frame()
print(f"Step 10: frame shape = {frame.shape if frame is not None else 'None'}")

print("Step 11: analyzing emotion...")
emotion = emo.analyze(frame)
print(f"Step 12: emotion = {emotion}")

print("Step 13: stopping...")
cam.stop()
aud.stop()
print("All done!")