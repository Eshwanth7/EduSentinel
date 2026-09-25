import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

EDUCATION_KEYWORDS = [
    "lecture", "tutorial", "coursera", "khan academy", "udemy", "nptel",
    "notes", "assignment", "textbook", "study", "exam prep", "python tutorial",
    "mathematics", "physics", "chemistry", "biology", "history", "geography",
    "stackoverflow", "github", "documentation", "research paper", "classroom",
    "google classroom", "moodle", "edx", "brilliant", "codecademy"
]

ENTERTAINMENT_KEYWORDS = [
    "youtube shorts", "reels", "tiktok", "netflix", "prime video", "hotstar",
    "instagram", "twitter", "facebook", "meme", "movie", "series", "web series",
    "gaming", "twitch", "pubg", "free fire", "valorant", "minecraft", "spotify",
    "snapchat", "reddit", "9gag", "buzzfeed", "entertainment", "trending"
]

# Timing
DISTRACTION_THRESHOLD_SECONDS = 120   # 2 minutes before alert
FRAME_INTERVAL_SECONDS        = 5     # analyze every 5 seconds
EMOTION_ALERT_COOLDOWN        = 120   # emotion alerts max once per 2 mins
DISTRACTION_ALERT_COOLDOWN    = 120   # distraction alerts max once per 2 mins
PHONE_THRESHOLD_SECONDS       = 30   # 2 minutes on phone before buzzer

# Audio
NOISE_THRESHOLD_DB = 65

# Emotion messages shown in dashboard
EMOTION_MESSAGES = {
    "focused":    "You are in the zone! Keep it up.",
    "bored":      "Feeling bored? Try the Pomodoro technique — 25 min on, 5 min off.",
    "distracted": "Let us refocus! Close distracting tabs and come back.",
    "stressed":   "Take a 2-minute deep breath break. You have got this.",
    "active":     "Great energy! Channel it into your study session.",
    "passive":    "Try active recall — quiz yourself on what you just read."
}