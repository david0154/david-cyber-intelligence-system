#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM
Tkinter GUI Desktop Application
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
Run: python gui_app.py
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import json
import sys
import os

# ─── Color Theme ────────────────────────────────────────────────────────────
BG        = "#0a0a0a"
BG2       = "#111111"
BG3       = "#1a1a1a"
ACCENT    = "#00ff41"       # matrix green
ACCENT2   = "#41b3ff"       # blue
DANGER    = "#ff4141"       # red
WARN      = "#ffd700"       # yellow
FG        = "#e0e0e0"
FG_DIM    = "#555555"
FONT_MONO = ("Courier New", 10)
FONT_TITLE= ("Courier New", 13, "bold")
FONT_MENU = ("Courier New", 10, "bold")
FONT_SMALL= ("Courier New", 9)

# ─── Module Definitions ─────────────────────────────────────────────────────
MODULES = [
    {"id": "malware",     "icon": "🦠", "label": "Malware Analysis",    "param": "file_path",  "hint": "File path to analyze"},
    {"id": "network",     "icon": "🌐", "label": "Network IDS",          "param": "interface",  "hint": "Network interface (eth0 / Wi-Fi)"},
    {"id": "osint",       "icon": "🔍", "label": "OSINT Investigation",  "param": "target",     "hint": "IP / Domain / Email"},
    {"id": "pentest",     "icon": "🧪", "label": "Pentest Engine",        "param": "target",     "hint": "Target IP / Host"},
    {"id": "defense",     "icon": "🛡️", "label": "Defense Engine",       "param": None,         "hint": "No input needed"},
    {"id": "intel",       "icon": "🧠", "label": "Threat Intelligence",   "param": "ioc",        "hint": "IOC: IP / Hash / Domain"},
    {"id": "flight",      "icon": "✈️", "label": "Flight Tracker",        "param": "callsign",   "hint": "ICAO24 or Callsign"},
    {"id": "ship",        "icon": "🚢", "label": "Ship Tracker",          "param": "mmsi",       "hint": "Vessel MMSI number"},
    {"id": "satellite",   "icon": "🛰️", "label": "Satellite Tracker",     "param": "sat_id",     "hint": "NORAD Satellite ID"},
    {"id": "geo",         "icon": "🗺️", "label": "Geo Intelligence",      "param": "ip",         "hint": "IP address to geolocate"},
    {"id": "zap",         "icon": "🔎", "label": "OWASP ZAP Scan",        "param": "url",        "hint": "Target URL (https://...)"},
    {"id": "wazuh",       "icon": "📊", "label": "Wazuh SIEM Alerts",     "param": "limit",      "hint": "Alert limit (default: 20)"},
    {"id": "openvas",     "icon": "🔭", "label": "OpenVAS CVE Scan",      "param": "target",     "hint": "Target IP / Host"},
    {"id": "hydra",       "icon": "🔑", "label": "Hydra Brute Test",      "param": "target",     "hint": "Target host for brute test"},
    {"id": "cloudflare",  "icon": "☁️", "label": "Cloudflare Stats",      "param": "zone_id",    "hint": "Zone ID (leave blank for first zone)"},
    {"id": "deepexploit", "icon": "🤖", "label": "DeepExploit (RL)",      "param": "target",     "hint": "Target IP / Host"},
    {"id": "chat",        "icon": "💬", "label": "AI Brain Chat",         "param": "query",      "hint": "Ask any cybersecurity question"},
]


class CyberApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DAVID CYBER INTELLIGENCE SYSTEM  |  Devil Pvt Ltd & Nexuzy Tech Pvt Ltd")
        self.configure(bg=BG)
        self.geometry("1280x780")
        self.minsize(1024, 640)
        self.resizable(True, True)
        self._set_icon()
        self._router = None
        self._active_module = tk.StringVar(value="malware")
        self._build_ui()
        self._load_router_async()

    # ── Icon (optional, no crash if missing) ──────────────────────────────
    def _set_icon(self):
        try:
            ico = os.path.join("assets", "icon.png")
            if os.path.exists(ico):
                img = tk.PhotoImage(file=ico)
                self.iconphoto(True, img)
        except Exception:
            pass

    # ── Build full UI ──────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header ──
        hdr = tk.Frame(self, bg="#111", height=52)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="◼ DAVID CYBER INTELLIGENCE SYSTEM",
                 font=FONT_TITLE, fg=ACCENT, bg="#111").pack(side="left", padx=20, pady=12)
        tk.Label(hdr, text="Devil Pvt Ltd  ◆  Nexuzy Tech Pvt Ltd",
                 font=FONT_SMALL, fg=FG_DIM, bg="#111").pack(side="right", padx=20)

        # ── Status bar ──
        self._status_var = tk.StringVar(value="● Initializing...")
        sb = tk.Frame(self, bg="#0d0d0d", height=26)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)
        tk.Label(sb, textvariable=self._status_var,
                 font=FONT_SMALL, fg=WARN, bg="#0d0d0d").pack(side="left", padx=12, pady=4)
        self._threat_var = tk.StringVar(value="Threat: --")
        tk.Label(sb, textvariable=self._threat_var,
                 font=FONT_SMALL, fg=DANGER, bg="#0d0d0d").pack(side="right", padx=12)

        # ── Main pane: sidebar + content ──
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(main, bg=BG2, width=220)
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="MODULES", font=FONT_SMALL,
                 fg=FG_DIM, bg=BG2).pack(pady=(14, 4), padx=12, anchor="w")

        self._sidebar_btns = {}
        for mod in MODULES:
            btn = tk.Button(
                sidebar,
                text=f"  {mod['icon']}  {mod['label']}",
                font=FONT_MENU,
                fg=FG, bg=BG2,
                activeforeground=ACCENT, activebackground=BG3,
                bd=0, relief="flat",
                anchor="w", padx=8, pady=6,
                cursor="hand2",
                command=lambda m=mod: self._select_module(m),
            )
            btn.pack(fill="x", padx=4, pady=1)
            self._sidebar_btns[mod["id"]] = btn

        # Separator
        tk.Frame(main, bg="#222", width=1).pack(fill="y", side="left")

        # Content area
        content = tk.Frame(main, bg=BG)
        content.pack(fill="both", expand=True)

        # Top: module title + input row
        self._top_frame = tk.Frame(content, bg=BG2, height=80)
        self._top_frame.pack(fill="x", padx=0)
        self._top_frame.pack_propagate(False)

        self._mod_title = tk.Label(self._top_frame, text="Select a module",
                                   font=FONT_TITLE, fg=ACCENT, bg=BG2)
        self._mod_title.place(x=20, y=10)

        self._hint_lbl = tk.Label(self._top_frame, text="",
                                  font=FONT_SMALL, fg=FG_DIM, bg=BG2)
        self._hint_lbl.place(x=20, y=38)

        self._input_var = tk.StringVar()
        self._input_entry = tk.Entry(
            self._top_frame, textvariable=self._input_var,
            font=FONT_MONO, fg=ACCENT, bg=BG3,
            insertbackground=ACCENT, bd=0, relief="flat",
            highlightthickness=1, highlightbackground="#333",
            highlightcolor=ACCENT, width=42
        )
        self._input_entry.place(x=20, y=52)
        self._input_entry.bind("<Return>", lambda e: self._run_module())

        self._browse_btn = tk.Button(
            self._top_frame, text="Browse",
            font=FONT_SMALL, fg=FG, bg=BG3,
            activeforeground=ACCENT, activebackground=BG3,
            bd=0, relief="flat", cursor="hand2", padx=8,
            command=self._browse_file
        )

        self._run_btn = tk.Button(
            self._top_frame, text="▶  RUN",
            font=FONT_MENU, fg="#000", bg=ACCENT,
            activeforeground="#000", activebackground="#00cc33",
            bd=0, relief="flat", cursor="hand2", padx=16, pady=4,
            command=self._run_module
        )
        self._run_btn.place(x=580, y=46)

        self._clear_btn = tk.Button(
            self._top_frame, text="✕ Clear",
            font=FONT_SMALL, fg=FG_DIM, bg=BG2,
            activeforeground=DANGER, activebackground=BG2,
            bd=0, relief="flat", cursor="hand2", padx=8,
            command=self._clear_output
        )
        self._clear_btn.place(x=660, y=50)

        # Separator
        tk.Frame(content, bg="#1e1e1e", height=1).pack(fill="x")

        # Output area
        out_frame = tk.Frame(content, bg=BG)
        out_frame.pack(fill="both", expand=True, padx=12, pady=10)

        # Threat score sidebar panel
        score_panel = tk.Frame(out_frame, bg=BG2, width=180)
        score_panel.pack(side="right", fill="y", padx=(8, 0))
        score_panel.pack_propagate(False)

        tk.Label(score_panel, text="THREAT SCORE",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG2).pack(pady=(16, 4))
        self._score_val = tk.Label(score_panel, text="0",
                                   font=("Courier New", 36, "bold"),
                                   fg=ACCENT, bg=BG2)
        self._score_val.pack()
        tk.Label(score_panel, text="/ 100",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG2).pack()

        self._level_lbl = tk.Label(score_panel, text="LOW",
                                   font=("Courier New", 14, "bold"),
                                   fg=ACCENT, bg=BG2)
        self._level_lbl.pack(pady=(8, 0))

        tk.Frame(score_panel, bg="#222", height=1).pack(fill="x", pady=12, padx=8)

        # Score bars
        for lbl, key in [("Malware", "malware"), ("Network", "network"),
                         ("OSINT", "osint"), ("Intel", "intel")]:
            tk.Label(score_panel, text=lbl, font=FONT_SMALL,
                     fg=FG_DIM, bg=BG2).pack(anchor="w", padx=12)
            bar_bg = tk.Frame(score_panel, bg="#222", height=6)
            bar_bg.pack(fill="x", padx=12, pady=(0, 6))
            bar_fill = tk.Frame(bar_bg, bg=ACCENT, height=6, width=0)
            bar_fill.place(x=0, y=0)
            setattr(self, f"_bar_{key}", bar_fill)

        tk.Frame(score_panel, bg="#222", height=1).pack(fill="x", pady=8, padx=8)
        tk.Button(score_panel, text="Reset Score",
                  font=FONT_SMALL, fg=FG_DIM, bg=BG2,
                  activeforeground=DANGER, activebackground=BG2,
                  bd=0, relief="flat", cursor="hand2",
                  command=self._reset_score).pack(pady=4)

        # Output text widget
        self._output = scrolledtext.ScrolledText(
            out_frame,
            font=FONT_MONO, fg=ACCENT, bg=BG3,
            insertbackground=ACCENT,
            bd=0, relief="flat",
            wrap="word",
            state="disabled",
        )
        self._output.pack(fill="both", expand=True)

        # Configure text tags
        self._output.tag_config("header",  foreground=ACCENT,  font=("Courier New", 10, "bold"))
        self._output.tag_config("error",   foreground=DANGER)
        self._output.tag_config("warn",    foreground=WARN)
        self._output.tag_config("info",    foreground=ACCENT2)
        self._output.tag_config("dim",     foreground=FG_DIM)
        self._output.tag_config("normal",  foreground=FG)

        # Select first module
        self._select_module(MODULES[0])

    # ── Module Selection ──────────────────────────────────────────────────
    def _select_module(self, mod: dict):
        self._current_mod = mod
        self._active_module.set(mod["id"])

        # Sidebar highlight
        for mid, btn in self._sidebar_btns.items():
            btn.config(fg=FG if mid != mod["id"] else ACCENT,
                       bg=BG2 if mid != mod["id"] else BG3)

        self._mod_title.config(text=f"{mod['icon']}  {mod['label']}")
        self._hint_lbl.config(text=f"Input: {mod['hint']}")
        self._input_var.set("")

        # Show/hide browse button for file inputs
        if mod["param"] == "file_path":
            self._browse_btn.place(x=400, y=50)
        else:
            self._browse_btn.place_forget()

        # Disable input if no param needed
        if mod["param"] is None:
            self._input_entry.config(state="disabled")
        else:
            self._input_entry.config(state="normal")
            self._input_entry.focus()

    # ── Browse file ───────────────────────────────────────────────────────
    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Select file to analyze",
            filetypes=[("All files", "*.*"), ("Executables", "*.exe *.dll *.bin")]
        )
        if path:
            self._input_var.set(path)

    # ── Run Module ────────────────────────────────────────────────────────
    def _run_module(self):
        mod = self._current_mod
        param_val = self._input_var.get().strip()

        if mod["param"] and not param_val:
            self._write(f"⚠ Please enter: {mod['hint']}\n", "warn")
            return

        params = {}
        if mod["param"]:
            if mod["param"] == "limit":
                try:
                    params[mod["param"]] = int(param_val)
                except ValueError:
                    params[mod["param"]] = 20
            else:
                params[mod["param"]] = param_val

        # Add extra param for hydra
        if mod["id"] == "hydra":
            params["service"] = "ssh"

        self._run_btn.config(state="disabled", text="⏳ Running...")
        self._status(f"● Running: {mod['label']}...")
        self._write(f"\n{'─'*60}\n", "dim")
        self._write(f"▶ {mod['icon']} {mod['label']}", "header")
        if param_val:
            self._write(f"  →  {param_val}\n", "info")
        else:
            self._write("\n", "normal")
        self._write(f"{'─'*60}\n", "dim")

        thread = threading.Thread(
            target=self._run_in_thread,
            args=(mod["id"], params),
            daemon=True
        )
        thread.start()

    def _run_in_thread(self, module_id: str, params: dict):
        try:
            router = self._get_router()
            if router is None:
                self.after(0, self._write, "✖ Router not loaded. Check your Python environment.\n", "error")
                self.after(0, self._restore_btn)
                return
            result = router.route(module_id, params)
            formatted = json.dumps(result, indent=2, default=str)
            self.after(0, self._display_result, result, formatted)
        except Exception as e:
            self.after(0, self._write, f"✖ Error: {e}\n", "error")
        finally:
            self.after(0, self._restore_btn)

    def _display_result(self, result: dict, formatted: str):
        status = result.get("status", "ok")
        if status == "error":
            self._write(f"✖ {result.get('message', 'Unknown error')}\n", "error")
        elif status in ("warning", "offline"):
            self._write(f"⚠ {result.get('message', 'Warning')}\n", "warn")
        else:
            self._write("✔ Success\n", "header")

        self._write(formatted + "\n", "normal")
        self._status(f"● Done: {self._current_mod['label']}")

        # Update threat score if present
        if "threat_level" in result:
            self._update_score_display(result)
        elif "risk_score" in result:
            self._update_bar("malware", result["risk_score"])

    # ── Score display ─────────────────────────────────────────────────────
    def _update_score_display(self, data: dict):
        level = data.get("threat_level", "LOW")
        total = data.get("total_score", 0)
        self._score_val.config(text=str(int(total)))
        self._threat_var.set(f"Threat: {level}")
        colors = {"LOW": ACCENT, "MEDIUM": WARN, "HIGH": "#ff8800", "CRITICAL": DANGER}
        self._level_lbl.config(text=level, fg=colors.get(level, ACCENT))
        self._score_val.config(fg=colors.get(level, ACCENT))
        scores = data.get("scores", {})
        for key in ("malware", "network", "osint", "intel"):
            self._update_bar(key, scores.get(key, 0))

    def _update_bar(self, key: str, val: float):
        bar = getattr(self, f"_bar_{key}", None)
        if bar:
            w = int((val / 25) * 140)
            bar.config(width=max(0, min(w, 140)))

    def _reset_score(self):
        self._score_val.config(text="0", fg=ACCENT)
        self._level_lbl.config(text="LOW", fg=ACCENT)
        self._threat_var.set("Threat: --")
        for key in ("malware", "network", "osint", "intel"):
            self._update_bar(key, 0)

    # ── Output helpers ────────────────────────────────────────────────────
    def _write(self, text: str, tag: str = "normal"):
        self._output.config(state="normal")
        self._output.insert("end", text, tag)
        self._output.see("end")
        self._output.config(state="disabled")

    def _clear_output(self):
        self._output.config(state="normal")
        self._output.delete("1.0", "end")
        self._output.config(state="disabled")

    def _restore_btn(self):
        self._run_btn.config(state="normal", text="▶  RUN")

    def _status(self, msg: str):
        self._status_var.set(msg)

    # ── Router lazy load ──────────────────────────────────────────────────
    def _get_router(self):
        if self._router is None:
            try:
                from core.task_router import TaskRouter
                self._router = TaskRouter()
            except Exception as e:
                return None
        return self._router

    def _load_router_async(self):
        def _load():
            r = self._get_router()
            if r:
                mods = list(r._engines.keys())
                self.after(0, self._status, f"● Ready  |  Modules: {', '.join(mods)}")
            else:
                self.after(0, self._status, "⚠ Router failed. Check requirements.")
        threading.Thread(target=_load, daemon=True).start()


# ─── Entry Point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Make sure we can import from project root
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    app = CyberApp()
    app.mainloop()
