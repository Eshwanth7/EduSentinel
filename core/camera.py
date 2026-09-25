import cv2
import numpy as np

class EphemeralCamera:
    def __init__(self):
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        """Returns a single frame as numpy array. No file written, no disk I/O."""
        if self.cap is None or not self.cap.isOpened():
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        # Frame lives only in RAM. Previous frame is GC'd when this returns.
        return frame  

    def stop(self):
        if self.cap:
            self.cap.release()
        self.cap = None