import time
from core.screen_monitor import ScreenMonitor
from core.content_classifier import ContentClassifier

scr = ScreenMonitor()
cnt = ContentClassifier()

print("Reading active window every 3 seconds...")
print("Open YouTube, Netflix, Google in browser now")
print("-" * 60)

for i in range(10):
    title = scr.get_browser_tab_title()
    result = cnt.classify(title)
    print(f"[{i+1}] Title: {title}")
    print(f"     Result: {result}")
    print("-" * 60)
    time.sleep(3)

print("Done!")