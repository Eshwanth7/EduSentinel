import cv2
import time

from core.cv_support import resolve_haar_cascade_path

FACE_CASCADE_PATH = resolve_haar_cascade_path("haarcascade_frontalface_default.xml")
FACE_CASCADE = cv2.CascadeClassifier(FACE_CASCADE_PATH) if FACE_CASCADE_PATH else None

cap = cv2.VideoCapture(0)
print("Testing face detection...")
print("Round 1-5:  sit normally in front of camera")
print("Round 6-10: move away OR look down at your phone")
print("-" * 50)

no_face_count = 0

for i in range(10):
    ret, frame = cap.read()
    if not ret:
        print("Camera error!")
        break

    if FACE_CASCADE is None:
        print("Face cascade XML not available; skipping detection.")
        break

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray  = cv2.equalizeHist(gray)   # improves detection in low light

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(50, 50)
    )

    face_found = len(faces) > 0

    if not face_found:
        no_face_count += 1
    else:
        no_face_count = 0

    status = "✓ FACE PRESENT" if face_found else f"✗ NO FACE (count={no_face_count})"
    print(f"[{i+1:02d}] Faces={len(faces)}  →  {status}")
    time.sleep(1)

cap.release()
print("\nDone!")
print(f"Total no-face detections: {no_face_count}")