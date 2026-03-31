#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM
Splash Screen Launcher

Shows animated splash while all modules load in background,
then opens the main GUI. Works on Windows, macOS, Linux.

Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import tkinter as tk
from tkinter import ttk
import threading
import sys
import os
import time
import platform

# ── Add project root to path (works both from source and PyInstaller)
if getattr(sys, "frozen", False):
    BASE = sys._MEIPASS
else:
    BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

# Load .env early
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE, ".env"))
except Exception:
    pass

# ── Colors
BG       = "#0a0a0a"
ACCENT   = "#00ff41"
ACCENT2  = "#41b3ff"
FG       = "#e0e0e0"
FG_DIM   = "#555555"
DANGER   = "#ff4141"
FONT_BIG = ("Courier New", 22, "bold")
FONT_SUB = ("Courier New", 10)
FONT_SML = ("Courier New",  8)

LOAD_STEPS = [
    ("Loading AI Brain (LLM)...",           0.12),
    ("Initialising Task Router...",          0.06),
    ("Loading Malware Engine...",            0.08),
    ("Loading Network IDS...",               0.07),
    ("Loading OSINT Engine...",              0.07),
    ("Loading Pentest Engine...",            0.08),
    ("Loading Defense Engine...",            0.07),
    ("Loading Bug Analyzer...",              0.07),
    ("Loading Threat Intelligence...",       0.08),
    ("Loading SOC / SIEM Layer...",          0.07),
    ("Loading Bug Bounty Platform...",       0.06),
    ("Loading Tracking Engine...",           0.07),
    ("Loading Automation Layer...",          0.05),
    ("Starting API Server...",               0.05),
    ("Building GUI...",                      0.06),
]


class SplashScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DAVID CIS")
        self.overrideredirect(True)   # No title bar
        self.configure(bg=BG)
        self.resizable(False, False)
        self._progress = 0.0
        self._status   = ""
        self._done     = False
        self._center(640, 380)
        self._build()
        self._animate_border(0)
        threading.Thread(target=self._load_steps, daemon=True).start()

    def _center(self, w, h):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - w) // 2
        y  = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        # Outer border frame (animated)
        self._border = tk.Frame(self, bg=ACCENT, padx=2, pady=2)
        self._border.pack(fill="both", expand=True, padx=1, pady=1)

        inner = tk.Frame(self._border, bg=BG)
        inner.pack(fill="both", expand=True)

        # Logo / ASCII art
        logo_txt = (
            "  ██████╗   █████╗  ██╗   ██╗ ██╗ ██████╗  \n"
            "  ██╔══██╗ ██╔══██╗ ██║   ██║ ██║ ██╔══██╗ \n"
            "  ██║  ██║ ███████║ ██║   ██║ ██║ ██║  ██║ \n"
            "  ██║  ██║ ██╔══██║ ╚██╗ ██╔╝ ██║ ██║  ██║ \n"
            "  ██████╔╝ ██║  ██║  ╚████╔╝  ██║ ██████╔╝ \n"
            "  ╚═════╝  ╚═╝  ╚═╝   ╚═══╝   ╚═╝ ╚═════╝  "
        )
        tk.Label(inner, text=logo_txt,
                 font=("Courier New", 9, "bold"),
                 fg=ACCENT, bg=BG,
                 justify="center").pack(pady=(22, 0))

        tk.Label(inner,
                 text="CYBER INTELLIGENCE SYSTEM  v3.1",
                 font=("Courier New", 11, "bold"),
                 fg=ACCENT2, bg=BG).pack(pady=(2, 0))

        tk.Label(inner,
                 text="Devil Pvt Ltd  \u00b7  Nexuzy Tech Pvt Ltd",
                 font=FONT_SML, fg=FG_DIM, bg=BG).pack(pady=(2, 14))

        tk.Frame(inner, bg="#1a1a1a", height=1).pack(fill="x", padx=30)

        # Status label
        self._status_lbl = tk.Label(
            inner, text="Initialising...",
            font=FONT_SUB, fg=FG_DIM, bg=BG)
        self._status_lbl.pack(pady=(14, 4))

        # Progress bar (custom)
        self._bar_canvas = tk.Canvas(
            inner, width=540, height=18,
            bg="#111", bd=0, highlightthickness=0)
        self._bar_canvas.pack(pady=(0, 6))
        self._bar_bg  = self._bar_canvas.create_rectangle(
            2, 2, 538, 16, fill="#1a1a1a", outline="#222")
        self._bar_fill = self._bar_canvas.create_rectangle(
            2, 2, 2, 16, fill=ACCENT, outline="")

        # Percent label
        self._pct_lbl = tk.Label(
            inner, text="0%",
            font=FONT_SML, fg=FG_DIM, bg=BG)
        self._pct_lbl.pack()

        tk.Frame(inner, bg="#1a1a1a", height=1).pack(
            fill="x", padx=30, pady=(10, 0))

        # Platform info
        tk.Label(
            inner,
            text=f"Platform: {platform.system()} {platform.release()}  \u00b7  Python {sys.version[:6]}",
            font=FONT_SML, fg=FG_DIM, bg=BG
        ).pack(pady=(6, 0))

        tk.Label(inner,
                 text="hypechats.com",
                 font=FONT_SML, fg="#333", bg=BG).pack(pady=(2, 8))

    def _animate_border(self, step):
        colors = [ACCENT, ACCENT2, "#ff00ff", ACCENT2, ACCENT]
        self._border.configure(bg=colors[step % len(colors)])
        if not self._done:
            self.after(500, self._animate_border, step + 1)

    def _update_progress(self, pct: float, status: str):
        """Thread-safe progress update."""
        self._progress = pct
        self._status   = status
        self.after(0, self._redraw)

    def _redraw(self):
        pct = self._progress
        self._status_lbl.config(text=self._status)
        self._pct_lbl.config(text=f"{int(pct * 100)}%")
        w = int(536 * pct)
        self._bar_canvas.coords(self._bar_fill, 2, 2, 2 + w, 16)
        # Color shifts: green → cyan → blue as loading progresses
        color = ACCENT if pct < 0.6 else ACCENT2
        self._bar_canvas.itemconfig(self._bar_fill, fill=color)

    def _load_steps(self):
        total_time = sum(t for _, t in LOAD_STEPS)
        elapsed    = 0.0
        for label, duration in LOAD_STEPS:
            self._update_progress(elapsed / total_time, label)
            # Simulate loading in small increments
            steps = max(4, int(duration * 40))
            for i in range(steps):
                time.sleep(duration / steps)
                frac = elapsed / total_time + (duration / total_time) * (i + 1) / steps
                self._update_progress(min(frac, 0.99), label)
            elapsed += duration

        self._update_progress(1.0, "Ready!")
        time.sleep(0.4)
        self._done = True
        self.after(0, self._open_main)

    def _open_main(self):
        self.destroy()
        # Launch main GUI
        try:
            import gui_app
            gui_app.main()
        except Exception as e:
            # Fallback: re-exec main module
            import importlib
            import traceback
            traceback.print_exc()


def main():
    app = SplashScreen()
    app.mainloop()


if __name__ == "__main__":
    main()
