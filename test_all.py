import os, time
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from core.camera             import EphemeralCamera
from core.emotion_engine     import EmotionEngine
from core.screen_monitor     import ScreenMonitor
from core.content_classifier import ContentClassifier

cam = EphemeralCamera()
cam.start()
eng = EmotionEngine()
scr = ScreenMonitor()
cls = ContentClassifier()

print("EduSentinel — Module Test")
print("Sit in front of camera with good lighting")
print("Open YouTube or Netflix in browser during test")
print("=" * 60)

for i in range(5):
    t     = time.time()
    frame = cam.get_frame()

    emotion = eng.analyze(frame)
    phone   = eng.detect_phone(frame)
    face    = eng.is_face_present()
    title   = scr.get_browser_tab_title()
    content = cls.classify(title)
    del frame

    elapsed = time.time() - t

    print(f"\nRound {i+1}  ({elapsed:.1f}s)")
    print(f"  Emotion  :  {emotion.upper()}")
    print(f"  Face     :  {'PRESENT' if face else 'AWAY'}")
    print(f"  Phone    :  {'YES' if phone else 'NO'}")
    print(f"  Content  :  {content.upper()}")
    print(f"  Window   :  {title[:65]}")
    print("-" * 60)
    time.sleep(3)

cam.stop()
print("\nAll tests done!")