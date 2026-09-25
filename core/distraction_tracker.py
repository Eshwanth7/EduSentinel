import time
from config import (
    DISTRACTION_THRESHOLD_SECONDS,
    PHONE_THRESHOLD_SECONDS,
    DISTRACTION_ALERT_COOLDOWN
)

class DistractionTracker:
    def __init__(self):
        self.entertainment_start = None
        self.phone_start         = None
        self.noise_start         = None
        self.no_face_start       = None
        self.alert_cooldown      = {}

    def update(self, content_type, phone_detected, noise_db, noise_threshold, face_present=True):
        alerts = []
        now = time.time()

        # Entertainment timer
        if content_type == "entertainment":
            if self.entertainment_start is None:
                self.entertainment_start = now
            elif now - self.entertainment_start >= DISTRACTION_THRESHOLD_SECONDS:
                if self._can_alert("entertainment", now):
                    alerts.append("entertainment")
        else:
            self.entertainment_start = None

        # Phone timer — 2 minutes
        if phone_detected:
            if self.phone_start is None:
                self.phone_start = now
            elif now - self.phone_start >= PHONE_THRESHOLD_SECONDS:
                if self._can_alert("phone", now):
                    alerts.append("phone")
        else:
            self.phone_start = None

        # No face timer — buzzer if away for 2 minutes
        if not face_present:
            if self.no_face_start is None:
                self.no_face_start = now
            elif now - self.no_face_start >= DISTRACTION_THRESHOLD_SECONDS:
                if self._can_alert("no_face", now):
                    alerts.append("no_face")
        else:
            self.no_face_start = None

        # Noise timer
        if noise_db > noise_threshold:
            if self.noise_start is None:
                self.noise_start = now
            elif now - self.noise_start >= DISTRACTION_THRESHOLD_SECONDS:
                if self._can_alert("noise", now):
                    alerts.append("noise")
        else:
            self.noise_start = None

        return alerts

    def get_timers(self):
        now = time.time()
        return {
            "entertainment": int(now - self.entertainment_start) if self.entertainment_start else 0,
            "phone":         int(now - self.phone_start)         if self.phone_start         else 0,
            "noise":         int(now - self.noise_start)         if self.noise_start         else 0,
            "no_face":       int(now - self.no_face_start)       if self.no_face_start       else 0,
        }

    def _can_alert(self, category, now):
        last = self.alert_cooldown.get(category, 0)
        if now - last >= DISTRACTION_ALERT_COOLDOWN:
            self.alert_cooldown[category] = now
            return True
        return False