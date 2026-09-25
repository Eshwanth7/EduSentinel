import subprocess
import platform

try:
    import pygetwindow as gw
except ImportError:
    gw = None

class ScreenMonitor:
    def get_active_window_title(self):
        """Returns the full raw window title including browser name."""
        try:
            if platform.system() == "Windows":
                if gw:
                    win = gw.getActiveWindow()
                    return win.title if win else ""
            elif platform.system() == "Darwin":
                script = 'tell application "System Events" to get name of first application process whose frontmost is true'
                return subprocess.check_output(["osascript", "-e", script]).decode().strip()
            else:
                return subprocess.check_output(
                    ["xdotool", "getactivewindow", "getwindowname"]
                ).decode().strip()
        except Exception:
            return ""

    def get_browser_tab_title(self):
        """
        Returns full title string — DO NOT strip browser name.
        We need 'YouTube' and 'Netflix' in the title for classification.
        """
        return self.get_active_window_title()