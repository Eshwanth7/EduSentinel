import platform
import threading
import time

APP_ID = "EduSentinel"

ALERT_CONFIGS = {
    "entertainment": {
        "title": "EduSentinel — Focus Alert 🎬",
        "body":  "You have been watching entertainment for 1+ minute. Please switch back to learning!"
    },
    "phone": {
        "title": "EduSentinel — Phone Detected 📱",
        "body":  "Phone usage detected for 2+ minutes! Keep your phone away and focus on studies."
    },
    "no_face": {
        "title": "EduSentinel — Are you there? 👤",
        "body":  "No face detected for 2+ minutes. Please return to your desk."
    },
    "noise": {
        "title": "EduSentinel — Noise Alert 🔊",
        "body":  "High background noise detected. Find a quieter spot."
    },
}

EMOTION_CONFIGS = {
    "stressed": {
        "title": "EduSentinel — Wellness Check 😰",
        "body":  "You seem stressed. Take a short break and breathe deeply."
    },
    "bored": {
        "title": "EduSentinel — Engagement Tip 😴",
        "body":  "Feeling bored? Try flashcards or switch topics!"
    },
}


# ── Sound functions ────────────────────────────────────────────────────────

def _beep_long():
    """2 second buzzer for phone alert."""
    if platform.system() == "Windows":
        try:
            import winsound
            winsound.Beep(1000, 1000)
            winsound.Beep(1000, 1000)
        except:
            pass

def _beep_short():
    """Short 3-beep for other alerts."""
    if platform.system() == "Windows":
        try:
            import winsound
            winsound.Beep(1000, 300)
            winsound.Beep(1000, 300)
            winsound.Beep(1000, 300)
        except:
            pass

def _chime():
    """Soft single chime for emotion alerts."""
    if platform.system() == "Windows":
        try:
            import winsound
            winsound.Beep(800, 200)
        except:
            pass

def _toast(title, body):
    """Non-blocking Windows toast notification."""
    def _show():
        try:
            from winotify import Notification, audio
            n = Notification(
                app_id=APP_ID,
                title=title,
                msg=body,
                duration="long"
            )
            n.set_audio(audio.Default, loop=False)
            n.show()
        except:
            pass
    threading.Thread(target=_show, daemon=True).start()


# ── Alert Dispatcher ───────────────────────────────────────────────────────

class AlertDispatcher:
    def __init__(self):
        self._dist_cd = {}   # distraction cooldowns
        self._emo_cd  = {}   # emotion cooldowns

    def send_alert(self, alert_type: str):
        """
        Sends Windows toast + buzzer for distraction alerts.
        Cooldown: 2 minutes per alert type.
        Phone gets 2 second buzzer.
        All others get short 3-beep sound.
        """
        now = time.time()
        if now - self._dist_cd.get(alert_type, 0) < 120:
            return
        self._dist_cd[alert_type] = now

        cfg = ALERT_CONFIGS.get(alert_type)
        if not cfg:
            return

        # Phone = long buzzer, others = short beep
        if alert_type == "phone":
            threading.Thread(target=_beep_long,  daemon=True).start()
        else:
            threading.Thread(target=_beep_short, daemon=True).start()

        # Toast notification
        _toast(cfg["title"], cfg["body"])

    def send_emotion_alert(self, emotion: str):
        """
        Sends emotion tip notification.
        Only for stressed and bored.
        Cooldown: 5 minutes per emotion.
        """
        now = time.time()
        if emotion not in EMOTION_CONFIGS:
            return
        if now - self._emo_cd.get(emotion, 0) < 300:
            return
        self._emo_cd[emotion] = now

        cfg = EMOTION_CONFIGS[emotion]
        threading.Thread(target=_chime, daemon=True).start()
        _toast(cfg["title"], cfg["body"])