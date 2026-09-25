import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from winotify import Notification, audio

toast = Notification(
    app_id="EduSentinel",
    title="Test Alert",
    msg="This is a test from EduSentinel",
    duration="long"
)
toast.set_audio(audio.Default, loop=False)
toast.show()
print("Notification sent!")