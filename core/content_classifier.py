import re

ENTERTAINMENT = [
    "youtube", "netflix", "prime video", "hotstar", "disney+", "hulu",
    "twitch", "voot", "zee5", "sonyliv", "jiocinema", "mxplayer",
    "dailymotion", "vimeo", "crunchyroll", "funimation", "anime planet",
    "vlc media player", "windows media player", "mpc-hc",
    "media player", "movies & tv", "groove music",
    "kmplayer", "pot player", "potplayer", "gom player",
    "instagram", "facebook", "twitter", "snapchat", "tiktok",
    "reddit", "9gag", "pinterest", "tumblr",
    "buzzfeed", "meme", "funny", "reels", "shorts",
    "web series", "movie", "series", "anime", "manga",
    "pubg", "free fire", "valorant", "minecraft", "steam",
    "epic games", "roblox", "gta", "fortnite", "bgmi", "call of duty",
    "esports", "streamer", "streaming",
    "youtube gaming", "facebook gaming",
    "soundcloud", "pandora", "deezer", "tidal", "amazon music",
    "food vlog", "travel vlog", "vlogger", "vlog",
    "football", "soccer", "cricket", "tennis", "basketball", "hockey",
    "baseball", "golf", "formula 1", "nba", "nfl", "mlb",
    "uefa", "champions league",
    "prank", "comedy video", "stand-up comedy", "comedian",
    "vlc", "potplayer", "kmplayer", "gom player",
    "spotify", "gaana", "wynk", "jiosaavn", "apple music",
    "fun","funny","entertainment","meme","comedy","movie",
    "series","anime","gaming","music","sports","vlog","prank","streaming",
]

EDUCATIONAL = [
    "coursera", "udemy", "khan academy", "nptel", "edx", "brilliant",
    "codecademy", "unacademy", "byju", "vedantu", "toppr",
    "duolingo", "skillshare", "linkedin learning", "udacity",
    "futurelearn", "swayam", "researchgate",
    "google scholar", "arxiv", "springer", "ieee", "acm",
    "stackoverflow", "github", "gitlab", "w3schools", "geeksforgeeks",
    "leetcode", "hackerrank", "codechef", "codeforces",
    "documentation", "tutorial", "wikipedia",
    "medium", "dev.to", "hashnode", "freecodecamp",
    "google classroom", "google docs", "google sheets",
    "google slides", "google forms", "google meet", "google drive",
    "microsoft teams", "onenote", "sharepoint",
    "lecture", "assignment", "textbook", "syllabus",
    "exam", "quiz", "study", "course", "chapter",
    "mathematics", "physics", "chemistry", "biology",
    "history", "geography", "engineering",
    "research paper", "thesis", "journal",
    "university", "college", "professor",
    "homework", "project", "lab report",
    # Programming — whole words only (handled separately below)
    "python tutorial", "python course", "python lecture",
    "java tutorial", "java course",
    "javascript tutorial", "javascript course",
    "machine learning", "deep learning", "data science",
    "artificial intelligence", "computer vision",
    "natural language processing", "blockchain",
    "cybersecurity", "cloud computing", "devops",
    "docker", "kubernetes", "aws tutorial", "azure tutorial",
    "visual studio code", "vs code", "pycharm", "jupyter notebook",
    "android studio", "eclipse", "intellij", "sublime text",
    "algorithm", "data structure",
]

# These are programming languages — only educational when combined with study context
PROGRAMMING_LANGUAGES = [
    "python", "java", "javascript", "c++", "c#", "ruby", "php",
    "swift", "kotlin", "golang", "rust", "typescript",
]

# Study context words — if any of these appear with a programming language = educational
STUDY_CONTEXT = [
    "tutorial", "course", "learn", "lecture", "study",
    "documentation", "docs", "guide", "how to", "beginner",
    "advanced", "practice", "exercise", "project", "assignment",
    "stackoverflow", "github", "geeksforgeeks", "w3schools",
    "codecademy", "udemy", "coursera", "nptel", "freecodecamp",
    "notebook", "jupyter", "pycharm", "vs code", "ide",
]

# Entertainment apps — classified immediately even without video title
ENTERTAINMENT_APPS = [
    "youtube", "netflix", "prime video", "hotstar", "twitch",
    "vlc", "potplayer", "kmplayer", "mpc", "movies & tv",
    "windows media player", "media player", "gom player",
    "spotify", "gaana", "wynk", "jiosaavn", "apple music",
    "soundcloud", "pandora", "deezer", "tidal", "amazon music",
    "instagram", "facebook", "twitter", "snapchat", "tiktok",
    "reddit", "9gag", "pinterest", "tumblr",
    "buzzfeed", "reels", "shorts",
]

# These apps are always educational regardless of title
EDUCATIONAL_APPS = [
    "visual studio code", "vs code", "pycharm", "jupyter",
    "android studio", "eclipse", "intellij", "spyder",
    "google classroom", "microsoft teams", "zoom",
]


class ContentClassifier:

    def classify(self, window_title: str) -> str:
        if not window_title:
            return "neutral"

        t = window_title.lower()

        # ── Step 1: Educational app check — highest priority ──────────────
        for app in EDUCATIONAL_APPS:
            if app in t:
                return "educational"

        # ── Step 2: Entertainment app check ───────────────────────────────
        for app in ENTERTAINMENT_APPS:
            if app in t:
                return "entertainment"

        # ── Step 3: Programming language + study context check ────────────
        # e.g. "Python tutorial", "Learn Java", "Python - Stack Overflow"
        has_lang = any(
            re.search(rf"\b{re.escape(lang)}\b", t)
            for lang in PROGRAMMING_LANGUAGES
        )
        has_study = any(ctx in t for ctx in STUDY_CONTEXT)
        if has_lang and has_study:
            return "educational"

        # ── Step 4: Keyword scoring ────────────────────────────────────────
        ent_score = sum(1 for kw in ENTERTAINMENT if kw in t)
        edu_score = sum(1 for kw in EDUCATIONAL   if kw in t)

        if ent_score > edu_score:
            return "entertainment"
        elif edu_score > 0:
            return "educational"

        return "neutral"

    def get_video_name(self, title: str) -> str:
        """Extracts clean video/tab name — strips browser and platform names."""
        if not title:
            return "Unknown"
        for suffix in [
            " - Google Chrome", " - Microsoft Edge",
            " - Firefox", " - Brave", " - Opera",
            " - YouTube", " | Netflix", " | Prime Video",
            " | Hotstar", " - Hotstar", " - Twitch",
            " - SonyLIV", " - ZEE5", " - Voot",
        ]:
            title = title.replace(suffix, "").strip()
        title = re.sub(r"^\(\d+\)\s*", "", title).strip()
        return title if title else "Unknown"

    def get_matched_keywords(self, window_title: str) -> dict:
        t = window_title.lower()
        return {
            "educational":   [kw for kw in EDUCATIONAL   if kw in t],
            "entertainment": [kw for kw in ENTERTAINMENT if kw in t],
        }