import tkinter as tk
from tkinter import ttk
import threading, time
from config import EMOTION_MESSAGES, DISTRACTION_THRESHOLD_SECONDS

STATUS_COLORS = {
    "focused": "#22c55e",
    "active":  "#3b82f6",
    "bored":   "#f59e0b",
    "passive": "#94a3b8",
    "stressed":"#ef4444",
    "distracted":"#f97316"
}

class Dashboard:
    def __init__(self, state: dict, on_close=None):
        state = state
        self.on_close = on_close
        self.root = tk.Tk()
        self.root.title("EduSentinel — Student Focus Monitor")
        self.root.geometry("720x500")
        self.root.configure(bg="#0f172a")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)  # intercept X button
        self._build_ui()

    def _on_close(self):
        self.state["running"] = False
        if self.on_close:
            self.on_close()
        self.root.destroy()

    def _build_ui(self):
        # Title bar
        tk.Label(self.root, text="EduSentinel", font=("Segoe UI", 22, "bold"),
                 bg="#0f172a", fg="#f8fafc").pack(pady=(20, 4))
        tk.Label(self.root, text="Student Focus Monitor",
                 font=("Segoe UI", 11), bg="#0f172a", fg="#64748b").pack()

        # Status card grid
        card_frame = tk.Frame(self.root, bg="#0f172a")
        card_frame.pack(fill="x", padx=24, pady=16)

        self.emotion_card   = self._make_card(card_frame, "Emotion State", "focused", 0)
        self.content_card   = self._make_card(card_frame, "Content Type", "neutral",  1)
        self.noise_card     = self._make_card(card_frame, "Noise Level",  "0 dB",     2)
        self.phone_card     = self._make_card(card_frame, "Phone Status", "On Laptop",3)

        # Timer bars
        timer_frame = tk.LabelFrame(self.root, text=" Distraction Timers ",
                                    font=("Segoe UI", 10),
                                    bg="#1e293b", fg="#94a3b8",
                                    bd=1, relief="flat", padx=12, pady=8)
        timer_frame.pack(fill="x", padx=24, pady=4)

        self.ent_bar   = self._make_timer_row(timer_frame, "Entertainment", "#f97316", 0)
        self.phone_bar = self._make_timer_row(timer_frame, "Phone",         "#8b5cf6", 1)
        self.noise_bar = self._make_timer_row(timer_frame, "High Noise",    "#06b6d4", 2)

        # Emotion tip
        self.tip_label = tk.Label(self.root,
                                  text="Initializing EduSentinel...",
                                  font=("Segoe UI", 11, "italic"),
                                  bg="#0f172a", fg="#94a3b8",
                                  wraplength=680, justify="center")
        self.tip_label.pack(pady=12)

        # Window title
        self.title_label = tk.Label(self.root, text="", font=("Segoe UI", 9),
                                    bg="#0f172a", fg="#475569")
        self.title_label.pack()

    def _make_card(self, parent, label, value, col):
        frame = tk.Frame(parent, bg="#1e293b", padx=14, pady=10)
        frame.grid(row=0, column=col, padx=6, sticky="ew")
        parent.columnconfigure(col, weight=1)
        tk.Label(frame, text=label, font=("Segoe UI", 9),
                 bg="#1e293b", fg="#64748b").pack()
        val = tk.Label(frame, text=value, font=("Segoe UI", 13, "bold"),
                       bg="#1e293b", fg="#f8fafc")
        val.pack()
        return val

    def _make_timer_row(self, parent, label, color, row):
        tk.Label(parent, text=label, font=("Segoe UI", 9),
                 bg="#1e293b", fg="#94a3b8", width=16, anchor="w").grid(row=row, column=0, padx=4, pady=3)
        bar = ttk.Progressbar(parent, length=380, maximum=DISTRACTION_THRESHOLD_SECONDS)
        bar.grid(row=row, column=1, padx=8)
        time_lbl = tk.Label(parent, text="0:00", font=("Segoe UI", 9),
                            bg="#1e293b", fg=color, width=6)
        time_lbl.grid(row=row, column=2)
        return bar, time_lbl

    def _refresh(self):
        s = self.state
        emotion = s.get("emotion", "focused")
        color = STATUS_COLORS.get(emotion, "#f8fafc")
        self.emotion_card.config(text=emotion.capitalize(), fg=color)
        self.content_card.config(text=s.get("content_type","neutral").capitalize())
        self.noise_card.config(text=f'{s.get("noise_db",0):.0f} dB')
        self.phone_card.config(text="On Phone" if s.get("phone_detected") else "On Laptop")
        self.tip_label.config(text=EMOTION_MESSAGES.get(emotion, ""))
        self.title_label.config(text=f"Active: {s.get('window_title','')[:80]}")

        timers = s.get("timers", {})
        for key, (bar, lbl) in [("entertainment", self.ent_bar),
                                  ("phone",        self.phone_bar),
                                  ("noise",        self.noise_bar)]:
            secs = timers.get(key, 0)
            bar["value"] = min(secs, DISTRACTION_THRESHOLD_SECONDS)
            lbl.config(text=f"{secs//60}:{secs%60:02d}")

        if s["running"]:
            self.root.after(1500, self._refresh)

    def run(self):
        self.root.after(1500, self._refresh)
        self.root.mainloop()