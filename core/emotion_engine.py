import numpy as np
import cv2
from collections import Counter

EMOTION_MAP = {
    "happy":   "active",
    "surprise":"active",
    "neutral": "focused",
    "sad":     "bored",
    "fear":    "stressed",
    "angry":   "stressed",
    "disgust": "passive"
}

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

class EmotionEngine:
    def __init__(self):
        self._history             = []
        self._cached              = "focused"
        self._face_present        = True
        self._consecutive_no_face = 0
        self._consecutive_face    = 0

    def _has_face(self, frame: np.ndarray) -> bool:
        """OpenCV face detection — fast and reliable."""
        try:
            gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray  = cv2.equalizeHist(gray)
            faces = FACE_CASCADE.detectMultiScale(
                gray,
                scaleFactor=1.05,
                minNeighbors=3,
                minSize=(50, 50)
            )
            return len(faces) > 0
        except:
            return True

    def analyze(self, frame: np.ndarray) -> str:
        """Detects emotion. Also tracks face presence as a side effect."""
        face_found = self._has_face(frame)

        if face_found:
            self._consecutive_no_face = 0
            self._consecutive_face   += 1
            # Confirm face present after 2 consecutive detections
            if self._consecutive_face >= 2:
                self._face_present = True
        else:
            self._consecutive_face    = 0
            self._consecutive_no_face += 1
            # Confirm away after 3 consecutive no-face frames (~9 seconds)
            if self._consecutive_no_face >= 3:
                self._face_present = False
            return self._cached

        # Only run DeepFace if face is confirmed present
        try:
            from deepface import DeepFace
            result = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False,
                detector_backend="opencv",
                silent=True
            )
            raw        = result[0]["dominant_emotion"]
            emotions   = result[0]["emotion"]
            confidence = emotions[raw]

            if confidence < 55:
                mapped = "focused"
            else:
                mapped = EMOTION_MAP.get(raw, "focused")

            if mapped == "stressed":
                if emotions.get("fear", 0) + emotions.get("angry", 0) < 65:
                    mapped = "focused"

            self._history.append(mapped)
            if len(self._history) > 7:
                self._history.pop(0)

            self._cached = Counter(self._history).most_common(1)[0][0]
            return self._cached

        except:
            return self._cached

    def detect_phone(self, frame: np.ndarray) -> bool:
        """Returns True if no face detected for 3+ consecutive frames."""
        return not self._face_present

    def is_face_present(self) -> bool:
        return self._face_present