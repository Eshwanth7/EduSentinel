import os, sys, time, threading, tkinter as tk
from tkinter import ttk
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# ── Shared state ──────────────────────────────────────────────────────────────
state = {
    "emotion":"focused","content_type":"neutral",
    "phone_detected":False,"face_present":True,
    "noise_db":0.0,"timers":{"entertainment":0,"phone":0,"no_face":0,"noise":0},
    "window_title":"","running":False,"status":"stopped",
    "alert_log":[],"load_msg":"",
}
EMOTION_COLORS  = {"focused":"#00d4aa","active":"#4f9eff","bored":"#ffb347",
                   "passive":"#aaaaaa","stressed":"#ff5c5c","distracted":"#ff8c42"}
EMOTION_ICONS   = {"focused":"🎯","active":"⚡","bored":"😴",
                   "passive":"😐","stressed":"😰","distracted":"😵"}
EMOTION_MSGS    = {"focused":"Deep focus detected — excellent work!",
                   "active":"High energy! Great time for hard problems.",
                   "bored":"Boredom detected — try switching study method.",
                   "passive":"Low engagement — try active recall or quizzing.",
                   "stressed":"Stress detected — take 3 deep breaths now.",
                   "distracted":"Distraction detected — close extra tabs."}
CONTENT_COLORS  = {"educational":"#00d4aa","entertainment":"#ff5c5c","neutral":"#aaaaaa"}
CONTENT_ICONS   = {"educational":"📚","entertainment":"🎬","neutral":"💻"}

_cam=_scr=_aud=_emo=_cnt=_trk=_alt=None

def _load_and_run():
    global _cam,_scr,_aud,_emo,_cnt,_trk,_alt
    state["status"]="loading"
    try:
        state["load_msg"]="Importing modules..."
        from core.camera              import EphemeralCamera
        from core.screen_monitor      import ScreenMonitor
        from core.audio_monitor       import AudioMonitor
        from core.emotion_engine      import EmotionEngine
        from core.content_classifier  import ContentClassifier
        from core.distraction_tracker import DistractionTracker
        from core.alert_dispatcher    import AlertDispatcher

        state["load_msg"]="Starting camera & microphone..."
        _cam=EphemeralCamera(); _scr=ScreenMonitor(); _aud=AudioMonitor()
        _emo=EmotionEngine();   _cnt=ContentClassifier()
        _trk=DistractionTracker(); _alt=AlertDispatcher()
        _cam.start(); _aud.start()

        state["load_msg"]="Warming up AI model — please wait (~15 sec)..."
        warm=_cam.get_frame()
        if warm is not None:
            _emo.analyze(warm)
            del warm

        state["load_msg"]="Ready!"
        state["status"]="running"
    except Exception as e:
        print(f"[Load error] {e}")
        state["load_msg"]=f"Error: {e}"
        state["status"]="error"
        state["running"]=False
        return

    from config import FRAME_INTERVAL_SECONDS, NOISE_THRESHOLD_DB
    while state["running"]:
        try:
            title    = _scr.get_browser_tab_title()
            noise_db = _aud.get_noise_db()
            state["window_title"]=title
            state["noise_db"]=round(noise_db,1)
            state["content_type"]=_cnt.classify(title)

            frame=_cam.get_frame()
            if frame is not None:
                state["emotion"]       =_emo.analyze(frame)
                state["phone_detected"]=_emo.detect_phone(frame)
                state["face_present"]  =_emo.is_face_present()
                del frame

            alerts=_trk.update(state["content_type"],state["phone_detected"],
                               noise_db,NOISE_THRESHOLD_DB,
                               face_present=state["face_present"])
            state["timers"]=_trk.get_timers()

            for a in alerts:
                _alt.send_alert(a)
                ts=time.strftime("%H:%M:%S")
                msg={"entertainment":"Entertainment alert — go back to work!",
                     "phone":        "Phone usage detected for 2+ mins",
                     "no_face":      "Away from desk for 2+ mins",
                     "noise":        "High background noise detected"}.get(a,a)
                state["alert_log"].insert(0,f"{ts}   {msg}")
                state["alert_log"]=state["alert_log"][:6]
            _alt.send_emotion_alert(state["emotion"])
        except Exception as e:
            print(f"[Loop] {e}")
        time.sleep(FRAME_INTERVAL_SECONDS)

    try: _cam.stop(); _aud.stop()
    except: pass
    state["status"]="stopped"

# ── UI ────────────────────────────────────────────────────────────────────────
class App:
    BG="#0a0f1e"; BG2="#111827"; BG3="#1a2332"
    ACC="#00d4aa"; ACC2="#4f9eff"
    FG="#ffffff";  FG2="#8892a4"
    DNG="#ff5c5c"; WRN="#ffb347"

    def __init__(self):
        self.root=tk.Tk()
        self.root.title("EduSentinel — Student Focus Monitor")
        self.root.configure(bg=self.BG)
        self.root.state("zoomed")          # ← MAXIMIZED on startup
        self.root.minsize(700,600)
        self.root.protocol("WM_DELETE_WINDOW",self._quit)
        self._pulse=0
        self._build()
        self._styles()

    def _styles(self):
        s=ttk.Style(); s.theme_use("default")
        for n,c in [("teal","#00d4aa"),("red","#ff5c5c"),
                    ("amber","#ffb347"),("blue","#4f9eff")]:
            s.configure(f"{n}.Horizontal.TProgressbar",
                        troughcolor=self.BG2,background=c,thickness=10,borderwidth=0)

    def _build(self):
        # ── Header ────────────────────────────────────────────────────────
        hdr=tk.Frame(self.root,bg=self.BG2,pady=18)
        hdr.pack(fill="x")
        lf=tk.Frame(hdr,bg=self.BG2); lf.pack(side="left",padx=28)
        tk.Label(lf,text="🛡  EduSentinel",font=("Courier New",26,"bold"),
                 bg=self.BG2,fg=self.ACC).pack(anchor="w")
        tk.Label(lf,text="AI-Powered Student Focus Monitor  ·  ICAP Framework  ·  Privacy First",
                 font=("Courier New",10),bg=self.BG2,fg=self.FG2).pack(anchor="w")
        rf=tk.Frame(hdr,bg=self.BG2); rf.pack(side="right",padx=28)
        self.clock=tk.Label(rf,text="",font=("Courier New",18,"bold"),
                            bg=self.BG2,fg=self.ACC)
        self.clock.pack(anchor="e")
        self.datl=tk.Label(rf,text="",font=("Courier New",10),
                           bg=self.BG2,fg=self.FG2)
        self.datl.pack(anchor="e")

        # ── Status bar ────────────────────────────────────────────────────
        sb=tk.Frame(self.root,bg=self.BG3,pady=10)
        sb.pack(fill="x")
        self.dot=tk.Label(sb,text=" ● ",font=("Courier New",14),
                          bg=self.BG3,fg=self.DNG)
        self.dot.pack(side="left",padx=(20,4))
        self.slbl=tk.Label(sb,text="SYSTEM OFFLINE",
                           font=("Courier New",12,"bold"),
                           bg=self.BG3,fg=self.DNG)
        self.slbl.pack(side="left")
        self.llbl=tk.Label(sb,text="",font=("Courier New",10),
                           bg=self.BG3,fg=self.WRN)
        self.llbl.pack(side="left",padx=16)
        tk.Label(sb,text="S = Start     Q = Stop     Esc = Quit",
                 font=("Courier New",10),bg=self.BG3,fg=self.FG2,
                 padx=20).pack(side="right")

        # ── Buttons ───────────────────────────────────────────────────────
        bf=tk.Frame(self.root,bg=self.BG,pady=16)
        bf.pack(fill="x",padx=28)
        self.sbtn=tk.Button(bf,text="▶   START   (S)",
            font=("Courier New",13,"bold"),bg=self.ACC,fg=self.BG,
            activebackground="#00ffcc",activeforeground=self.BG,
            relief="flat",padx=32,pady=14,cursor="hand2",bd=0,
            command=self._start)
        self.sbtn.pack(side="left",padx=(0,14))
        self.qbtn=tk.Button(bf,text="■   STOP   (Q)",
            font=("Courier New",13,"bold"),bg=self.BG3,fg=self.FG2,
            activebackground=self.DNG,activeforeground="white",
            relief="flat",padx=32,pady=14,cursor="hand2",bd=0,
            state="disabled",command=self._stop)
        self.qbtn.pack(side="left")
        self.root.bind("<s>",    lambda e:self._start())
        self.root.bind("<S>",    lambda e:self._start())
        self.root.bind("<q>",    lambda e:self._stop())
        self.root.bind("<Q>",    lambda e:self._stop())
        self.root.bind("<Escape>",lambda e:self._quit())

        # ── 4 metric cards ────────────────────────────────────────────────
        cf=tk.Frame(self.root,bg=self.BG)
        cf.pack(fill="x",padx=28,pady=(0,14))
        for i in range(4): cf.columnconfigure(i,weight=1)
        self.c_emo =self._card(cf,"EMOTION STATE","🎯","—",0)
        self.c_cnt =self._card(cf,"CONTENT TYPE", "💻","—",1)
        self.c_face=self._card(cf,"FACE PRESENCE","👤","—",2)
        self.c_noi =self._card(cf,"NOISE LEVEL",  "🔇","—",3)

        # ── Active window ─────────────────────────────────────────────────
        wf=tk.Frame(self.root,bg=self.BG3,pady=8)
        wf.pack(fill="x",padx=28,pady=(0,12))
        tk.Label(wf,text="  ACTIVE WINDOW",font=("Courier New",9,"bold"),
                 bg=self.BG3,fg=self.FG2).pack(side="left")
        self.wlbl=tk.Label(wf,text="Not monitoring",
                           font=("Courier New",10),bg=self.BG3,
                           fg=self.ACC2,padx=10)
        self.wlbl.pack(side="left")

        # ── Timers ────────────────────────────────────────────────────────
        tk.Label(self.root,
                 text="  DISTRACTION TIMERS  —  Windows notification fires at 2:00",
                 font=("Courier New",10),bg=self.BG,fg=self.FG2,
                 anchor="w").pack(fill="x",padx=28)
        tf=tk.Frame(self.root,bg=self.BG3,padx=20,pady=14)
        tf.pack(fill="x",padx=28,pady=(4,12))
        self.t_ent =self._trow(tf,"🎬  Entertainment","teal", 0)
        self.t_ph  =self._trow(tf,"📱  Phone usage",  "red",  1)
        self.t_fce =self._trow(tf,"👤  Away from desk","amber",2)
        self.t_noi =self._trow(tf,"🔊  High noise",    "blue", 3)

        # ── Tip banner ────────────────────────────────────────────────────
        tipf=tk.Frame(self.root,bg=self.BG3,pady=12)
        tipf.pack(fill="x",padx=28,pady=(0,12))
        self.tipico=tk.Label(tipf,text="💡",font=("Segoe UI Emoji",20),bg=self.BG3)
        self.tipico.pack(side="left",padx=(14,8))
        self.tiplbl=tk.Label(tipf,text="Press S or click START to begin monitoring",
                             font=("Courier New",11,"bold"),bg=self.BG3,fg=self.ACC,
                             wraplength=900,justify="left")
        self.tiplbl.pack(side="left")

        # ── Alert log ─────────────────────────────────────────────────────
        tk.Label(self.root,text="  ALERT LOG",
                 font=("Courier New",10),bg=self.BG,fg=self.FG2,
                 anchor="w").pack(fill="x",padx=28)
        lf=tk.Frame(self.root,bg=self.BG2,padx=16,pady=10)
        lf.pack(fill="x",padx=28,pady=(4,14))
        self.logs=[]
        for _ in range(5):
            l=tk.Label(lf,text="  —",font=("Courier New",10),
                       bg=self.BG2,fg=self.FG2,anchor="w")
            l.pack(fill="x",pady=1)
            self.logs.append(l)

        # ── Footer ────────────────────────────────────────────────────────
        ft=tk.Frame(self.root,bg=self.BG2,pady=7)
        ft.pack(fill="x",side="bottom")
        tk.Label(ft,text="EduSentinel v1.0   |   No data stored — Privacy First   |   ICAP Framework   |   Hackathon Edition",
                 font=("Courier New",9),bg=self.BG2,fg=self.FG2).pack()

    def _card(self,p,label,icon,val,col):
        f=tk.Frame(p,bg=self.BG3,padx=12,pady=16)
        f.grid(row=0,column=col,padx=5,sticky="ew")
        tk.Label(f,text=label,font=("Courier New",9,"bold"),
                 bg=self.BG3,fg=self.FG2).pack()
        ic=tk.Label(f,text=icon,font=("Segoe UI Emoji",26),bg=self.BG3)
        ic.pack(pady=(6,3))
        vl=tk.Label(f,text=val,font=("Courier New",13,"bold"),
                    bg=self.BG3,fg=self.FG)
        vl.pack()
        return ic,vl

    def _trow(self,p,label,color,row):
        tk.Label(p,text=label,font=("Courier New",10),bg=self.BG3,
                 fg=self.FG2,width=20,anchor="w").grid(row=row,column=0,padx=6,pady=6)
        bar=ttk.Progressbar(p,length=400,maximum=120,
                            style=f"{color}.Horizontal.TProgressbar")
        bar.grid(row=row,column=1,padx=12)
        tl=tk.Label(p,text="0:00",font=("Courier New",11,"bold"),
                    bg=self.BG3,fg=self.FG,width=5)
        tl.grid(row=row,column=2,padx=6)
        al=tk.Label(p,text="",font=("Courier New",9,"bold"),
                    bg=self.BG3,fg=self.DNG,width=12)
        al.grid(row=row,column=3,padx=4)
        return bar,tl,al

    # ── Start / Stop ──────────────────────────────────────────────────────
    def _start(self):
        if state["running"]: return
        state["running"]=True
        state["alert_log"]=[]
        self._setstatus("loading")
        self.sbtn.config(state="disabled",bg=self.BG3,fg=self.FG2)
        self.qbtn.config(state="disabled")
        self.tiplbl.config(text="Loading AI models — please wait (~15 seconds)...")
        threading.Thread(target=_load_and_run,daemon=True).start()
        self._poll()

    def _poll(self):
        s=state["status"]
        self.llbl.config(text=state.get("load_msg",""))
        if s=="loading":
            self.root.after(400,self._poll)
        elif s=="running":
            self.llbl.config(text="")
            self._setstatus("running")
            self.qbtn.config(state="normal",bg=self.DNG,fg="white",
                             activebackground="#cc3333")
            self._refresh()
        elif s=="error":
            self._setstatus("error")
            self.sbtn.config(state="normal",bg=self.ACC,fg=self.BG)
            self.tiplbl.config(
                text=f"Error: {state.get('load_msg','')}  — check CMD window",
                fg=self.DNG)

    def _stop(self):
        if not state["running"]: return
        state["running"]=False
        self._setstatus("stopped")
        self.llbl.config(text="")
        self.sbtn.config(state="normal",bg=self.ACC,fg=self.BG)
        self.qbtn.config(state="disabled",bg=self.BG3,fg=self.FG2)
        self.tiplbl.config(text="Monitoring stopped. Press S to restart.",fg=self.ACC)
        self.tipico.config(text="💡")
        self.wlbl.config(text="Not monitoring")
        for w in [self.c_emo,self.c_cnt,self.c_face,self.c_noi]:
            w[0].config(text="—"); w[1].config(text="—",fg=self.FG)
        for bar,tl,al in [self.t_ent,self.t_ph,self.t_fce,self.t_noi]:
            bar["value"]=0; tl.config(text="0:00",fg=self.FG); al.config(text="")
        for l in self.logs: l.config(text="  —",fg=self.FG2)

    def _setstatus(self,s):
        c={"running":(f"● MONITORING ACTIVE",self.ACC),
           "loading":(f"● LOADING MODELS...",self.WRN),
           "stopped":(f"● SYSTEM OFFLINE",   self.DNG),
           "error":  (f"● ERROR",            self.DNG)}.get(s,("● OFFLINE",self.DNG))
        self.dot.config(fg=c[1]); self.slbl.config(text=c[0],fg=c[1])

    # ── Refresh every 2 seconds ───────────────────────────────────────────
    def _refresh(self):
        if not state["running"]: return

        emo   =state.get("emotion","focused")
        ctype =state.get("content_type","neutral")
        face  =state.get("face_present",True)
        noise =state.get("noise_db",0.0)
        timers=state.get("timers",{})
        title =state.get("window_title","")
        logs  =state.get("alert_log",[])

        # Cards
        self.c_emo[0].config(text=EMOTION_ICONS.get(emo,"🎯"))
        self.c_emo[1].config(text=emo.upper(),fg=EMOTION_COLORS.get(emo,self.FG))

        self.c_cnt[0].config(text=CONTENT_ICONS.get(ctype,"💻"))
        self.c_cnt[1].config(text=ctype.upper(),fg=CONTENT_COLORS.get(ctype,self.FG))

        self.c_face[0].config(text="👤" if face else "❌")
        self.c_face[1].config(text="PRESENT" if face else "AWAY",
                              fg=self.ACC if face else self.DNG)

        nc=self.DNG if noise>=65 else self.ACC
        self.c_noi[0].config(text="🔊" if noise>=65 else "🔇")
        self.c_noi[1].config(text=f"{noise:.0f} dB  {'HIGH' if noise>=65 else 'NORMAL'}",fg=nc)

        # Tip
        self.tiplbl.config(text=EMOTION_MSGS.get(emo,"Stay focused!"),
                           fg=EMOTION_COLORS.get(emo,self.ACC))
        self.tipico.config(text=EMOTION_ICONS.get(emo,"💡"))

        # Window
        self.wlbl.config(text=title[:90] if title else "Desktop")

        # Timers
        for key,(bar,tl,al) in [("entertainment",self.t_ent),
                                  ("phone",        self.t_ph),
                                  ("no_face",      self.t_fce),
                                  ("noise",        self.t_noi)]:
            s=timers.get(key,0)
            bar["value"]=min(s,120)
            tl.config(text=f"{s//60}:{s%60:02d}")
            if s>=120:   al.config(text="⚠ ALERT SENT!"); tl.config(fg=self.DNG)
            elif s>=60:  al.config(text="⚡ WARNING");    tl.config(fg=self.WRN)
            else:        al.config(text="");               tl.config(fg=self.FG)

        # Logs
        for i,l in enumerate(self.logs):
            if i<len(logs): l.config(text=f"  ⚠  {logs[i]}",fg=self.WRN)
            else:           l.config(text="  —",fg=self.FG2)

        # Pulse dot
        self._pulse=1-self._pulse
        if state["status"]=="running":
            self.dot.config(fg=self.ACC if self._pulse else "#007755")

        self.root.after(2000,self._refresh)

    def _quit(self):
        try:
            state["running"] = False
            self.root.quit()
            self.root.destroy()
        except:
            pass
        finally:
            os._exit(0)  # force clean exit — returns CMD prompt immediately

    def run(self):
        self._tick()
        self.root.mainloop()

    def _tick(self):
        self.clock.config(text=time.strftime("%H:%M:%S"))
        self.datl.config(text=time.strftime("%A, %d %B %Y"))
        self.root.after(1000,self._tick)

if __name__ == "__main__":
    try:
        App().run()
    except Exception as e:
        print(f"[Error] {e}")
    finally:
        os._exit(0)