#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM
Tkinter GUI Desktop Application v3.1
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
import platform

# ─── Color Theme ─────────────────────────────────────────────────────────────
BG        = "#0a0a0a"
BG2       = "#111111"
BG3       = "#1a1a1a"
BG4       = "#0d1a0d"
ACCENT    = "#00ff41"
ACCENT2   = "#41b3ff"
DANGER    = "#ff4141"
WARN      = "#ffd700"
SUCCESS   = "#00ff41"
FG        = "#e0e0e0"
FG_DIM    = "#555555"
FONT_MONO = ("Courier New", 10)
FONT_TITLE= ("Courier New", 13, "bold")
FONT_MENU = ("Courier New", 10, "bold")
FONT_SMALL= ("Courier New", 9)
FONT_H2   = ("Courier New", 11, "bold")

# ─── Module Definitions ──────────────────────────────────────────────────────
MODULES = [
    # ── Offensive ──
    {"id": "vuln_scan",   "icon": "🔍", "label": "Vulnerability Scan",   "group": "Offensive",
     "param": "target",     "hint": "IP or hostname (e.g. 192.168.1.1)"},
    {"id": "attack_sim",  "icon": "💥", "label": "Attack Simulation",    "group": "Offensive",
     "param": "target",     "hint": "Target IP / Host"},
    {"id": "pentest",     "icon": "🧪", "label": "Pentest Engine",        "group": "Offensive",
     "param": "target",     "hint": "Target IP / Host"},
    {"id": "zap",         "icon": "🕳️", "label": "OWASP ZAP Web Scan",   "group": "Offensive",
     "param": "url",        "hint": "Target URL (https://...)"},
    {"id": "openvas",     "icon": "🔭", "label": "OpenVAS CVE Scan",      "group": "Offensive",
     "param": "target",     "hint": "Target IP / Host"},
    {"id": "hydra",       "icon": "🔑", "label": "Hydra Brute Test",      "group": "Offensive",
     "param": "target",     "hint": "Target host for brute test"},
    {"id": "deepexploit", "icon": "🤖", "label": "DeepExploit (RL AI)",   "group": "Offensive",
     "param": "target",     "hint": "Target IP / Host"},
    # ── Defensive ──
    {"id": "malware",     "icon": "🦠", "label": "Malware Analysis",     "group": "Defensive",
     "param": "file_path",  "hint": "File path to analyze"},
    {"id": "network",     "icon": "🌐", "label": "Network IDS",           "group": "Defensive",
     "param": "interface",  "hint": "Network interface (eth0 / Wi-Fi)"},
    {"id": "defense",     "icon": "🛡️", "label": "Defense WAF",          "group": "Defensive",
     "param": None,         "hint": "No input needed"},
    {"id": "soc",         "icon": "📊", "label": "SOC Log Analysis",      "group": "Defensive",
     "param": "log_text",   "hint": "Paste log text or enter file path"},
    {"id": "wazuh",       "icon": "📡", "label": "Wazuh SIEM Alerts",     "group": "Defensive",
     "param": "limit",      "hint": "Alert limit (default: 20)"},
    {"id": "cloudflare",  "icon": "☁️", "label": "Cloudflare WAF Stats",  "group": "Defensive",
     "param": "zone_id",    "hint": "Zone ID (leave blank for first zone)"},
    # ── Intelligence ──
    {"id": "osint",       "icon": "🕵️", "label": "OSINT Recon",          "group": "Intelligence",
     "param": "target",     "hint": "IP / Domain / Email / Username"},
    {"id": "intel",       "icon": "🧠", "label": "Threat Intelligence",   "group": "Intelligence",
     "param": "ioc",        "hint": "IOC: IP / Hash / Domain"},
    # ── Tracking ──
    {"id": "flight",      "icon": "✈️", "label": "Flight Tracker",        "group": "Tracking",
     "param": "callsign",   "hint": "ICAO24 or Callsign"},
    {"id": "ship",        "icon": "🚢", "label": "Ship Tracker",          "group": "Tracking",
     "param": "mmsi",       "hint": "Vessel MMSI number"},
    {"id": "satellite",   "icon": "🛰️", "label": "Satellite Tracker",     "group": "Tracking",
     "param": "sat_id",     "hint": "NORAD Satellite ID"},
    {"id": "geo",         "icon": "🗺️", "label": "IP Geo Intelligence",   "group": "Tracking",
     "param": "ip",         "hint": "IP address to geolocate"},
    # ── Bug Bounty ──
    {"id": "_bounty",     "icon": "🐞", "label": "Bug Bounty Submit",     "group": "Bug Bounty",
     "param": "title",      "hint": "Bug title (then fill form below)"},
    # ── AI ──
    {"id": "chat",        "icon": "💬", "label": "AI Brain Chat",         "group": "AI",
     "param": "query",      "hint": "Ask any cybersecurity question"},
]

GROUP_ICONS = {
    "Offensive":    "🔴",
    "Defensive":    "🛡️",
    "Intelligence": "🥷",
    "Tracking":     "📍",
    "Bug Bounty":   "🐞",
    "AI":           "🧠",
}


class CyberApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DAVID CYBER INTELLIGENCE SYSTEM  |  Devil Pvt Ltd & Nexuzy Tech Pvt Ltd")
        self.configure(bg=BG)
        self.geometry("1350x820")
        self.minsize(1100, 660)
        self.resizable(True, True)
        self._set_icon()
        self._router = None
        self._current_mod = MODULES[0]
        self._active_tab = tk.StringVar(value="modules")
        self._build_ui()
        self._load_router_async()

    def _set_icon(self):
        try:
            for name in ("logo.jpg", "icon.png", "icon.ico"):
                p = os.path.join("assets", name)
                if os.path.exists(p) and p.endswith(".png"):
                    img = tk.PhotoImage(file=p)
                    self.iconphoto(True, img)
                    break
        except Exception:
            pass

    # ─── BUILD UI ──────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg="#0d0d0d", height=54)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="  ◼ DAVID CYBER INTELLIGENCE SYSTEM  v3.1",
                 font=FONT_TITLE, fg=ACCENT, bg="#0d0d0d").pack(side="left", pady=14)
        tk.Label(hdr, text=f"OS: {platform.system()}  |  Python {sys.version[:6]}  |  Devil Pvt Ltd & Nexuzy Tech Pvt Ltd  ",
                 font=FONT_SMALL, fg=FG_DIM, bg="#0d0d0d").pack(side="right", pady=14)

        # Tab bar
        tab_bar = tk.Frame(self, bg="#0a0a0a", height=38)
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)
        self._tab_btns = {}
        tabs = [
            ("modules",   "🔧 Modules"),
            ("installer", "📦 Tool Installer"),
            ("bounty",    "🐞 Bug Bounty"),
            ("settings",  "⚙️ Settings"),
        ]
        for tab_id, tab_label in tabs:
            btn = tk.Button(
                tab_bar, text=tab_label,
                font=FONT_MENU, fg=FG_DIM, bg="#0a0a0a",
                activeforeground=ACCENT, activebackground="#111",
                bd=0, relief="flat", cursor="hand2", padx=18, pady=6,
                command=lambda t=tab_id: self._switch_tab(t)
            )
            btn.pack(side="left")
            self._tab_btns[tab_id] = btn
        tk.Frame(self, bg="#1a1a1a", height=1).pack(fill="x")

        # Status bar
        self._status_var = tk.StringVar(value="● Initializing...")
        sb = tk.Frame(self, bg="#080808", height=26)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)
        tk.Label(sb, textvariable=self._status_var,
                 font=FONT_SMALL, fg=WARN, bg="#080808").pack(side="left", padx=12, pady=4)
        self._threat_var = tk.StringVar(value="Threat: --")
        tk.Label(sb, textvariable=self._threat_var,
                 font=FONT_SMALL, fg=DANGER, bg="#080808").pack(side="right", padx=12)

        # Page container
        self._pages = {}
        self._container = tk.Frame(self, bg=BG)
        self._container.pack(fill="both", expand=True)

        self._pages["modules"]   = self._build_modules_page()
        self._pages["installer"] = self._build_installer_page()
        self._pages["bounty"]    = self._build_bounty_page()
        self._pages["settings"]  = self._build_settings_page()

        self._switch_tab("modules")

    def _switch_tab(self, tab_id: str):
        for tid, page in self._pages.items():
            page.pack_forget()
        self._pages[tab_id].pack(fill="both", expand=True)
        self._active_tab.set(tab_id)
        for tid, btn in self._tab_btns.items():
            btn.config(
                fg=ACCENT if tid == tab_id else FG_DIM,
                bg="#111" if tid == tab_id else "#0a0a0a"
            )

    # ─── MODULES PAGE ─────────────────────────────────────────────────────
    def _build_modules_page(self) -> tk.Frame:
        page = tk.Frame(self._container, bg=BG)

        # Sidebar (grouped)
        sidebar = tk.Frame(page, bg=BG2, width=230)
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        sb_canvas = tk.Canvas(sidebar, bg=BG2, bd=0,
                              highlightthickness=0, width=228)
        sb_scroll = tk.Scrollbar(sidebar, orient="vertical",
                                 command=sb_canvas.yview)
        sb_canvas.configure(yscrollcommand=sb_scroll.set)
        sb_scroll.pack(side="right", fill="y")
        sb_canvas.pack(side="left", fill="both", expand=True)
        sb_inner = tk.Frame(sb_canvas, bg=BG2)
        sb_canvas.create_window((0, 0), window=sb_inner, anchor="nw")
        sb_inner.bind("<Configure>",
            lambda e: sb_canvas.configure(scrollregion=sb_canvas.bbox("all")))

        self._sidebar_btns = {}
        current_group = None
        for mod in MODULES:
            if mod["group"] != current_group:
                current_group = mod["group"]
                ico = GROUP_ICONS.get(current_group, "")
                tk.Label(sb_inner,
                         text=f"  {ico} {current_group.upper()}",
                         font=FONT_SMALL, fg=FG_DIM, bg=BG2,
                         anchor="w").pack(fill="x", pady=(10, 2))
            btn = tk.Button(
                sb_inner,
                text=f"   {mod['icon']}  {mod['label']}",
                font=FONT_SMALL, fg=FG, bg=BG2,
                activeforeground=ACCENT, activebackground=BG3,
                bd=0, relief="flat", anchor="w", padx=8, pady=5,
                cursor="hand2",
                command=lambda m=mod: self._select_module(m),
            )
            btn.pack(fill="x", padx=4, pady=1)
            self._sidebar_btns[mod["id"]] = btn

        # Separator
        tk.Frame(page, bg="#1e1e1e", width=1).pack(fill="y", side="left")

        # Content area
        content = tk.Frame(page, bg=BG)
        content.pack(fill="both", expand=True)

        # Input row
        inp_row = tk.Frame(content, bg=BG2, height=86)
        inp_row.pack(fill="x")
        inp_row.pack_propagate(False)

        self._mod_title = tk.Label(inp_row, text="▶ Select a module from the left",
                                   font=FONT_H2, fg=ACCENT, bg=BG2)
        self._mod_title.place(x=18, y=10)

        self._hint_lbl = tk.Label(inp_row, text="",
                                  font=FONT_SMALL, fg=FG_DIM, bg=BG2)
        self._hint_lbl.place(x=18, y=36)

        self._input_var = tk.StringVar()
        self._input_entry = tk.Entry(
            inp_row, textvariable=self._input_var,
            font=FONT_MONO, fg=ACCENT, bg=BG3,
            insertbackground=ACCENT, bd=0, relief="flat",
            highlightthickness=1, highlightbackground="#2a2a2a",
            highlightcolor=ACCENT, width=46
        )
        self._input_entry.place(x=18, y=56)
        self._input_entry.bind("<Return>", lambda e: self._run_module())

        self._browse_btn = tk.Button(
            inp_row, text="📂 Browse",
            font=FONT_SMALL, fg=FG, bg=BG3,
            activeforeground=ACCENT, activebackground=BG3,
            bd=0, relief="flat", cursor="hand2", padx=8,
            command=self._browse_file
        )

        btn_frame = tk.Frame(inp_row, bg=BG2)
        btn_frame.place(x=620, y=48)

        self._run_btn = tk.Button(
            btn_frame, text="▶  RUN",
            font=FONT_MENU, fg="#000", bg=ACCENT,
            activeforeground="#000", activebackground="#00cc33",
            bd=0, relief="flat", cursor="hand2", padx=18, pady=5,
            command=self._run_module
        )
        self._run_btn.pack(side="left", padx=(0, 8))

        tk.Button(
            btn_frame, text="✕ Clear",
            font=FONT_SMALL, fg=FG_DIM, bg=BG2,
            activeforeground=DANGER, activebackground=BG2,
            bd=0, relief="flat", cursor="hand2", padx=8, pady=5,
            command=self._clear_output
        ).pack(side="left")

        tk.Button(
            btn_frame, text="💾 Save",
            font=FONT_SMALL, fg=FG_DIM, bg=BG2,
            activeforeground=ACCENT2, activebackground=BG2,
            bd=0, relief="flat", cursor="hand2", padx=8, pady=5,
            command=self._save_output
        ).pack(side="left", padx=(8, 0))

        tk.Frame(content, bg="#1a1a1a", height=1).pack(fill="x")

        # Output + score panel
        out_frame = tk.Frame(content, bg=BG)
        out_frame.pack(fill="both", expand=True, padx=10, pady=8)

        # Score panel
        score_panel = tk.Frame(out_frame, bg=BG2, width=190)
        score_panel.pack(side="right", fill="y", padx=(8, 0))
        score_panel.pack_propagate(False)

        tk.Label(score_panel, text="THREAT SCORE",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG2).pack(pady=(18, 4))
        self._score_val = tk.Label(score_panel, text="0",
                                   font=("Courier New", 38, "bold"),
                                   fg=ACCENT, bg=BG2)
        self._score_val.pack()
        tk.Label(score_panel, text="/ 100",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG2).pack()
        self._level_lbl = tk.Label(score_panel, text="LOW",
                                   font=("Courier New", 14, "bold"),
                                   fg=ACCENT, bg=BG2)
        self._level_lbl.pack(pady=(6, 0))

        tk.Frame(score_panel, bg="#222", height=1).pack(fill="x", pady=10, padx=8)

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
        tk.Button(score_panel, text="↺ Reset",
                  font=FONT_SMALL, fg=FG_DIM, bg=BG2,
                  activeforeground=DANGER, activebackground=BG2,
                  bd=0, relief="flat", cursor="hand2",
                  command=self._reset_score).pack(pady=4)

        # Output text
        self._output = scrolledtext.ScrolledText(
            out_frame, font=FONT_MONO, fg=ACCENT, bg=BG3,
            insertbackground=ACCENT, bd=0, relief="flat",
            wrap="word", state="disabled"
        )
        self._output.pack(fill="both", expand=True)
        for tag, fg_col in [("header", ACCENT), ("error", DANGER),
                             ("warn", WARN), ("info", ACCENT2),
                             ("dim", FG_DIM), ("normal", FG),
                             ("success", SUCCESS)]:
            self._output.tag_config(tag, foreground=fg_col)

        self._select_module(MODULES[0])
        return page

    # ─── INSTALLER PAGE ────────────────────────────────────────────────────
    def _build_installer_page(self) -> tk.Frame:
        page = tk.Frame(self._container, bg=BG)

        # Title
        tk.Label(page,
                 text="  📦  TOOL INSTALLER  —  One-Click Install All Required Tools",
                 font=FONT_H2, fg=ACCENT, bg=BG).pack(
                     anchor="w", padx=18, pady=(14, 4))
        tk.Label(page,
                 text=f"  OS Detected: {platform.system()} {platform.release()}  |  Auto-installs via winget/choco (Windows), apt/dnf (Linux), brew (macOS)",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG).pack(anchor="w", padx=18, pady=(0, 8))
        tk.Frame(page, bg="#1a1a1a", height=1).pack(fill="x")

        # Main area: tool list left + log right
        main = tk.Frame(page, bg=BG)
        main.pack(fill="both", expand=True, padx=12, pady=10)

        # Left: tool list
        left = tk.Frame(main, bg=BG2, width=420)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        # Buttons row
        btn_row = tk.Frame(left, bg=BG2)
        btn_row.pack(fill="x", pady=8, padx=8)

        tk.Button(btn_row, text="▶ INSTALL ALL",
                  font=FONT_MENU, fg="#000", bg=ACCENT,
                  activeforeground="#000", activebackground="#00cc33",
                  bd=0, relief="flat", cursor="hand2", padx=14, pady=6,
                  command=self._install_all_tools).pack(side="left", padx=(0, 8))

        tk.Button(btn_row, text="🔄 Check Status",
                  font=FONT_SMALL, fg=FG, bg=BG3,
                  activeforeground=ACCENT, activebackground=BG3,
                  bd=0, relief="flat", cursor="hand2", padx=10, pady=6,
                  command=self._check_all_tools).pack(side="left")

        tk.Frame(left, bg="#222", height=1).pack(fill="x", padx=8)

        # Scrollable tool list
        tool_canvas = tk.Canvas(left, bg=BG2, bd=0, highlightthickness=0)
        tool_scroll = tk.Scrollbar(left, orient="vertical",
                                   command=tool_canvas.yview)
        tool_canvas.configure(yscrollcommand=tool_scroll.set)
        tool_scroll.pack(side="right", fill="y")
        tool_canvas.pack(side="left", fill="both", expand=True)
        tool_inner = tk.Frame(tool_canvas, bg=BG2)
        tool_canvas.create_window((0, 0), window=tool_inner, anchor="nw")
        tool_inner.bind("<Configure>",
            lambda e: tool_canvas.configure(
                scrollregion=tool_canvas.bbox("all")))

        self._tool_rows = {}
        from tools_installer import TOOLS
        current_cat = None
        for tool in TOOLS:
            if tool["category"] != current_cat:
                current_cat = tool["category"]
                tk.Label(tool_inner,
                         text=f"  {current_cat.upper()}",
                         font=FONT_SMALL, fg=FG_DIM, bg=BG2,
                         anchor="w").pack(fill="x", pady=(10, 2), padx=8)

            row = tk.Frame(tool_inner, bg=BG3)
            row.pack(fill="x", padx=8, pady=2)

            status_lbl = tk.Label(row, text="☐", font=FONT_MONO,
                                  fg=FG_DIM, bg=BG3, width=2)
            status_lbl.pack(side="left", padx=(8, 4), pady=6)

            info = tk.Frame(row, bg=BG3)
            info.pack(side="left", fill="x", expand=True, pady=4)
            tk.Label(info, text=tool["name"],
                     font=("Courier New", 9, "bold"),
                     fg=FG, bg=BG3, anchor="w").pack(fill="x")
            tk.Label(info, text=tool["desc"],
                     font=("Courier New", 8),
                     fg=FG_DIM, bg=BG3, anchor="w").pack(fill="x")

            install_btn = tk.Button(
                row, text="Install",
                font=("Courier New", 8), fg="#000", bg="#555",
                activeforeground="#000", activebackground=ACCENT,
                bd=0, relief="flat", cursor="hand2", padx=8, pady=4,
                command=lambda t=tool: self._install_single_tool(t)
            )
            install_btn.pack(side="right", padx=8, pady=6)

            self._tool_rows[tool["id"]] = {
                "status": status_lbl,
                "btn": install_btn,
                "row": row,
            }

        # Right: install log
        right = tk.Frame(main, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Install Log",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG).pack(
                     anchor="w", padx=4, pady=(0, 4))

        self._install_log = scrolledtext.ScrolledText(
            right, font=("Courier New", 9), fg=ACCENT, bg=BG3,
            bd=0, relief="flat", wrap="word", state="disabled"
        )
        self._install_log.pack(fill="both", expand=True)
        self._install_log.tag_config("ok",   foreground=SUCCESS)
        self._install_log.tag_config("err",  foreground=DANGER)
        self._install_log.tag_config("warn", foreground=WARN)
        self._install_log.tag_config("info", foreground=ACCENT2)
        self._install_log.tag_config("dim",  foreground=FG_DIM)

        # Auto-check on tab open
        self.after(500, self._check_all_tools)
        return page

    # ─── BUG BOUNTY PAGE ──────────────────────────────────────────────────
    def _build_bounty_page(self) -> tk.Frame:
        page = tk.Frame(self._container, bg=BG)
        tk.Label(page,
                 text="  🐞  BUG BOUNTY PLATFORM  —  Submit & Track Vulnerabilities",
                 font=FONT_H2, fg=ACCENT, bg=BG).pack(
                     anchor="w", padx=18, pady=(14, 4))
        tk.Label(page,
                 text="  Submit bugs → AI validates → CVSS scored → Admin approves → Reward issued",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG).pack(
                     anchor="w", padx=18, pady=(0, 8))
        tk.Frame(page, bg="#1a1a1a", height=1).pack(fill="x")

        form = tk.Frame(page, bg=BG2)
        form.pack(fill="x", padx=18, pady=14)

        fields = [
            ("Title",       "_b_title",       "Short vulnerability title"),
            ("Target",      "_b_target",      "URL / IP / App name"),
            ("Reporter",    "_b_reporter",    "Your name / handle"),
            ("Vuln Type",   "_b_vuln",        "e.g. XSS / SQLi / RCE / IDOR"),
        ]
        for i, (lbl, attr, hint) in enumerate(fields):
            tk.Label(form, text=f"{lbl}:", font=FONT_SMALL,
                     fg=FG_DIM, bg=BG2, width=10, anchor="e").grid(
                         row=i, column=0, padx=(8, 4), pady=5, sticky="e")
            var = tk.StringVar()
            setattr(self, f"{attr}_var", var)
            entry = tk.Entry(form, textvariable=var,
                             font=FONT_MONO, fg=ACCENT, bg=BG3,
                             insertbackground=ACCENT, bd=0, relief="flat",
                             highlightthickness=1, highlightbackground="#333",
                             highlightcolor=ACCENT, width=50)
            entry.insert(0, hint)
            entry.bind("<FocusIn>", lambda e, h=hint, w=entry: 
                       (w.delete(0, "end") if w.get() == h else None))
            entry.grid(row=i, column=1, padx=4, pady=5, sticky="w")

        tk.Label(form, text="Description:",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG2,
                 width=10, anchor="ne").grid(
                     row=4, column=0, padx=(8, 4), pady=5, sticky="ne")
        self._b_desc_text = tk.Text(
            form, font=FONT_MONO, fg=FG, bg=BG3,
            insertbackground=ACCENT, bd=0, relief="flat",
            highlightthickness=1, highlightbackground="#333",
            highlightcolor=ACCENT, width=50, height=6
        )
        self._b_desc_text.insert("1.0",
            "Describe the vulnerability, reproduction steps, and impact...")
        self._b_desc_text.grid(row=4, column=1, padx=4, pady=5, sticky="w")

        btn_row = tk.Frame(form, bg=BG2)
        btn_row.grid(row=5, column=1, sticky="w", padx=4, pady=8)

        tk.Button(btn_row, text="🚀 Submit Bug Report",
                  font=FONT_MENU, fg="#000", bg=ACCENT,
                  activeforeground="#000", activebackground="#00cc33",
                  bd=0, relief="flat", cursor="hand2", padx=14, pady=6,
                  command=self._submit_bug).pack(side="left", padx=(0, 12))

        tk.Button(btn_row, text="📸 Attach Screenshot",
                  font=FONT_SMALL, fg=FG, bg=BG3,
                  activeforeground=ACCENT, activebackground=BG3,
                  bd=0, relief="flat", cursor="hand2", padx=10, pady=6,
                  command=self._attach_screenshot).pack(side="left")

        self._b_attach_lbl = tk.Label(btn_row, text="",
                                      font=FONT_SMALL, fg=FG_DIM, bg=BG2)
        self._b_attach_lbl.pack(side="left", padx=8)
        self._b_screenshot = None

        tk.Frame(page, bg="#1a1a1a", height=1).pack(fill="x")

        tk.Label(page, text="  Submission Result:",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG).pack(
                     anchor="w", padx=18, pady=(8, 2))
        self._bounty_result = scrolledtext.ScrolledText(
            page, font=FONT_MONO, fg=ACCENT, bg=BG3,
            bd=0, relief="flat", wrap="word", state="disabled", height=12
        )
        self._bounty_result.pack(fill="both", expand=True, padx=18, pady=(0, 10))
        return page

    # ─── SETTINGS PAGE ────────────────────────────────────────────────────
    def _build_settings_page(self) -> tk.Frame:
        page = tk.Frame(self._container, bg=BG)
        tk.Label(page,
                 text="  ⚙️  SETTINGS  —  API Keys & Configuration",
                 font=FONT_H2, fg=ACCENT, bg=BG).pack(
                     anchor="w", padx=18, pady=(14, 4))
        tk.Label(page,
                 text="  These settings are saved to your .env file",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG).pack(
                     anchor="w", padx=18, pady=(0, 8))
        tk.Frame(page, bg="#1a1a1a", height=1).pack(fill="x")

        canvas = tk.Canvas(page, bg=BG, bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(page, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        form = tk.Frame(canvas, bg=BG)
        canvas.create_window((0, 0), window=form, anchor="nw")
        form.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self._settings_vars = {}
        env_fields = [
            ("LLM Settings",     None, None),
            ("LLM Model Path",   "LLM_MODEL_PATH",   "models/mixtral.gguf"),
            ("LLM Model Type",   "LLM_MODEL_TYPE",   "mistral"),
            ("Security Tools",   None, None),
            ("ZAP URL",          "ZAP_URL",           "http://localhost:8080"),
            ("ZAP API Key",      "ZAP_API_KEY",       ""),
            ("Wazuh URL",        "WAZUH_URL",         "https://localhost:55000"),
            ("Wazuh User",       "WAZUH_USER",        "wazuh"),
            ("Wazuh Password",   "WAZUH_PASS",        ""),
            ("Threat Intel",     None, None),
            ("Shodan API Key",   "SHODAN_API_KEY",    ""),
            ("MISP URL",         "MISP_URL",          ""),
            ("MISP Key",         "MISP_KEY",          ""),
            ("Cloudflare Token", "CLOUDFLARE_API_TOKEN", ""),
            ("Tracking",         None, None),
            ("N2YO API Key",     "N2YO_API_KEY",      ""),
            ("Alerts",           None, None),
            ("SMTP User",        "SMTP_USER",         ""),
            ("SMTP Password",    "SMTP_PASS",         ""),
            ("Alert Email",      "ALERT_EMAIL",       ""),
            ("Telegram Token",   "TELEGRAM_BOT_TOKEN",""),
            ("Telegram Chat ID", "TELEGRAM_CHAT_ID",  ""),
        ]

        row_idx = 0
        for label, key, default in env_fields:
            if key is None:
                tk.Label(form, text=f"  {label.upper()}",
                         font=FONT_SMALL, fg=FG_DIM, bg=BG,
                         anchor="w").grid(
                             row=row_idx, column=0, columnspan=2,
                             sticky="w", padx=18, pady=(14, 2))
            else:
                tk.Label(form, text=f"{label}:",
                         font=FONT_SMALL, fg=FG, bg=BG,
                         width=18, anchor="e").grid(
                             row=row_idx, column=0,
                             sticky="e", padx=(18, 6), pady=4)
                # Read from .env if exists
                current = os.getenv(key, default)
                var = tk.StringVar(value=current)
                self._settings_vars[key] = var
                show = "*" if "PASS" in key or "KEY" in key or "TOKEN" in key else ""
                entry = tk.Entry(
                    form, textvariable=var,
                    font=FONT_MONO, fg=ACCENT, bg=BG3,
                    insertbackground=ACCENT, bd=0, relief="flat",
                    highlightthickness=1, highlightbackground="#333",
                    highlightcolor=ACCENT, width=45, show=show
                )
                entry.grid(row=row_idx, column=1,
                           sticky="w", padx=(0, 18), pady=4)
            row_idx += 1

        save_frame = tk.Frame(form, bg=BG)
        save_frame.grid(row=row_idx, column=0, columnspan=2,
                        pady=16, padx=18, sticky="w")
        tk.Button(save_frame, text="💾 Save Settings to .env",
                  font=FONT_MENU, fg="#000", bg=ACCENT,
                  activeforeground="#000", activebackground="#00cc33",
                  bd=0, relief="flat", cursor="hand2", padx=14, pady=6,
                  command=self._save_settings).pack(side="left", padx=(0, 12))
        tk.Button(save_frame, text="📂 Load .env",
                  font=FONT_SMALL, fg=FG, bg=BG3,
                  activeforeground=ACCENT, activebackground=BG3,
                  bd=0, relief="flat", cursor="hand2", padx=10, pady=6,
                  command=self._load_settings).pack(side="left")
        return page

    # ─── INSTALLER LOGIC ──────────────────────────────────────────────────
    def _ilog(self, text: str, tag: str = "info"):
        """Write to install log."""
        self._install_log.config(state="normal")
        if "\u2714" in text or "Already" in text:
            tag = "ok"
        elif "✖" in text or "Error" in text or "Failed" in text:
            tag = "err"
        elif "⚠" in text or "Warning" in text:
            tag = "warn"
        elif text.startswith("$") or text.startswith("="):
            tag = "dim"
        self._install_log.insert("end", text, tag)
        self._install_log.see("end")
        self._install_log.config(state="disabled")
        self._install_log.update_idletasks()

    def _set_tool_status(self, tool_id: str, ok: bool):
        row = self._tool_rows.get(tool_id)
        if row:
            if ok:
                row["status"].config(text="✔", fg=SUCCESS)
                row["btn"].config(bg="#1a3a1a", text="✔ OK")
                row["row"].config(bg="#0d1a0d")
            else:
                row["status"].config(text="✖", fg=DANGER)
                row["btn"].config(bg=BG3, text="Install", fg="#fff")

    def _check_all_tools(self):
        def _check():
            self._ilog("\n─── Checking tool status...\n", "dim")
            try:
                from tools_installer import TOOLS, check_tool
                for tool in TOOLS:
                    ok = check_tool(tool["id"])
                    icon = "✔" if ok else "✖"
                    col = "ok" if ok else "err"
                    self._ilog(f"  {icon} {tool['name']}\n", col)
                    self.after(0, self._set_tool_status, tool["id"], ok)
            except Exception as e:
                self._ilog(f"Check error: {e}\n", "err")
            self._ilog("─── Done checking.\n", "dim")
        threading.Thread(target=_check, daemon=True).start()

    def _install_all_tools(self):
        if not messagebox.askyesno(
                "Install All Tools",
                "This will install ALL required tools.\n"
                "Some tools require admin/sudo.\n\n"
                "Continue?"):
            return

        def _do_install():
            try:
                from tools_installer import install_all
                install_all(callback=lambda t: self.after(0, self._ilog, t))
                self.after(0, self._check_all_tools)
                self.after(0, self._status, "● All tools installation complete.")
            except Exception as e:
                self.after(0, self._ilog, f"✖ {e}\n", "err")
        threading.Thread(target=_do_install, daemon=True).start()

    def _install_single_tool(self, tool: dict):
        def _do():
            self.after(0, self._ilog, f"\n▶ Installing: {tool['name']}\n", "info")
            try:
                ok = tool["install"](lambda t: self.after(0, self._ilog, t))
                self.after(0, self._set_tool_status, tool["id"], ok)
                msg = f"✔ {tool['name']} installed!" if ok else f"⚠ {tool['name']} needs manual install"
                self.after(0, self._ilog, msg + "\n",
                           "ok" if ok else "warn")
            except Exception as e:
                self.after(0, self._ilog, f"✖ {e}\n", "err")
        threading.Thread(target=_do, daemon=True).start()

    # ─── SETTINGS LOGIC ───────────────────────────────────────────────────
    def _save_settings(self):
        try:
            lines = []
            env_path = ".env"
            existing = {}
            if os.path.exists(env_path):
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if "=" in line and not line.startswith("#"):
                            k, v = line.split("=", 1)
                            existing[k.strip()] = v.strip()
            existing.update({k: v.get() for k, v in self._settings_vars.items()})
            with open(env_path, "w") as f:
                f.write("# DAVID CYBER INTELLIGENCE SYSTEM .env\n")
                for k, v in existing.items():
                    f.write(f"{k}={v}\n")
            messagebox.showinfo("Saved", ".env saved successfully!\nRestart app to apply.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _load_settings(self):
        try:
            from dotenv import dotenv_values
            vals = dotenv_values(".env")
            for k, var in self._settings_vars.items():
                if k in vals:
                    var.set(vals[k])
            messagebox.showinfo("Loaded", ".env loaded!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ─── BUG BOUNTY LOGIC ─────────────────────────────────────────────────
    def _attach_screenshot(self):
        path = filedialog.askopenfilename(
            title="Select Screenshot",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif"),
                       ("All", "*.*")]
        )
        if path:
            self._b_screenshot = path
            self._b_attach_lbl.config(
                text=f"✔ {os.path.basename(path)}", fg=SUCCESS)

    def _submit_bug(self):
        title = getattr(self, "_b_title_var", tk.StringVar()).get().strip()
        target = getattr(self, "_b_target_var", tk.StringVar()).get().strip()
        reporter = getattr(self, "_b_reporter_var", tk.StringVar()).get().strip()
        vuln_type = getattr(self, "_b_vuln_var", tk.StringVar()).get().strip()
        desc = self._b_desc_text.get("1.0", "end").strip()

        hints = ["Short vulnerability title", "URL / IP / App name",
                 "Your name / handle", "e.g. XSS / SQLi / RCE / IDOR"]
        if not title or title in hints:
            messagebox.showwarning("Missing", "Please enter a title.")
            return

        def _do():
            try:
                import requests
                payload = {
                    "title": title, "description": desc,
                    "target": target, "reporter": reporter,
                    "vuln_type": vuln_type.lower(),
                }
                resp = requests.post(
                    "http://localhost:8001/report/submit",
                    json=payload, timeout=10)
                result = resp.json()
                text = json.dumps(result, indent=2)
                self.after(0, self._write_bounty_result, text)
            except Exception as e:
                self.after(0, self._write_bounty_result,
                           f"Bug Bounty API not running.\n"
                           f"Start with: uvicorn bounty.api:app --port 8001\n\n"
                           f"Error: {e}")
        threading.Thread(target=_do, daemon=True).start()

    def _write_bounty_result(self, text: str):
        self._bounty_result.config(state="normal")
        self._bounty_result.delete("1.0", "end")
        self._bounty_result.insert("end", text)
        self._bounty_result.config(state="disabled")

    # ─── MODULE LOGIC ─────────────────────────────────────────────────────
    def _select_module(self, mod: dict):
        self._current_mod = mod
        for mid, btn in self._sidebar_btns.items():
            btn.config(fg=ACCENT if mid == mod["id"] else FG,
                       bg=BG3 if mid == mod["id"] else BG2)
        self._mod_title.config(text=f"{mod['icon']}  {mod['label']}")
        self._hint_lbl.config(text=f"Input: {mod['hint']}")
        self._input_var.set("")
        if mod["param"] == "file_path":
            self._browse_btn.place(x=440, y=56)
        else:
            self._browse_btn.place_forget()
        if mod["param"] is None:
            self._input_entry.config(state="disabled")
        else:
            self._input_entry.config(state="normal")
            self._input_entry.focus()

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Select file to analyze",
            filetypes=[("All files", "*.*"),
                       ("Executables", "*.exe *.dll *.bin")])
        if path:
            self._input_var.set(path)

    def _run_module(self):
        mod = self._current_mod
        if mod["id"] == "_bounty":
            self._switch_tab("bounty")
            return
        param_val = self._input_var.get().strip()
        if mod["param"] and not param_val:
            self._write(f"⚠ Please enter: {mod['hint']}\n", "warn")
            return
        params = {}
        if mod["param"]:
            key = mod["param"]
            params[key] = int(param_val) if key == "limit" and param_val.isdigit() else param_val
        if mod["id"] == "hydra":
            params["service"] = "ssh"
        if mod["id"] == "soc" and os.path.isfile(param_val):
            try:
                with open(param_val, errors="ignore") as f:
                    params["log_text"] = f.read()[:10000]
                    params["source"] = param_val
            except Exception:
                pass
        self._run_btn.config(state="disabled", text="⏳ Running...")
        self._status(f"● Running: {mod['label']}...")
        self._write(f"\n{'─'*60}\n", "dim")
        self._write(f"▶ {mod['icon']}  {mod['label']}", "header")
        if param_val:
            self._write(f"  →  {param_val}\n", "info")
        else:
            self._write("\n", "normal")
        self._write(f"{'─'*60}\n", "dim")
        threading.Thread(
            target=self._run_in_thread,
            args=(mod["id"], params), daemon=True).start()

    def _run_in_thread(self, module_id: str, params: dict):
        try:
            router = self._get_router()
            if router is None:
                self.after(0, self._write,
                           "✖ Router not loaded. Check requirements.\n"
                           "   Go to: Tool Installer tab → Install All\n",
                           "error")
                self.after(0, self._restore_btn)
                return
            result = router.route(module_id, params)
            fmt = json.dumps(result, indent=2, default=str)
            self.after(0, self._display_result, result, fmt)
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
            self._write("✔ Success\n", "success")
        self._write(formatted + "\n", "normal")
        self._status(f"● Done: {self._current_mod['label']}")
        if "threat_level" in result:
            self._update_score_display(result)
        elif "risk_score" in result:
            self._update_bar("malware", result["risk_score"])

    def _update_score_display(self, data: dict):
        level = data.get("threat_level", "LOW")
        total = data.get("total_score", 0)
        self._score_val.config(text=str(int(total)))
        self._threat_var.set(f"Threat: {level}")
        colors = {"LOW": ACCENT, "MEDIUM": WARN, "HIGH": "#ff8800", "CRITICAL": DANGER}
        c = colors.get(level, ACCENT)
        self._level_lbl.config(text=level, fg=c)
        self._score_val.config(fg=c)
        for key in ("malware", "network", "osint", "intel"):
            self._update_bar(key, data.get("scores", {}).get(key, 0))

    def _update_bar(self, key: str, val: float):
        bar = getattr(self, f"_bar_{key}", None)
        if bar:
            bar.config(width=max(0, min(int((val / 25) * 150), 150)))

    def _reset_score(self):
        self._score_val.config(text="0", fg=ACCENT)
        self._level_lbl.config(text="LOW", fg=ACCENT)
        self._threat_var.set("Threat: --")
        for key in ("malware", "network", "osint", "intel"):
            self._update_bar(key, 0)

    def _write(self, text: str, tag: str = "normal"):
        self._output.config(state="normal")
        self._output.insert("end", text, tag)
        self._output.see("end")
        self._output.config(state="disabled")

    def _clear_output(self):
        self._output.config(state="normal")
        self._output.delete("1.0", "end")
        self._output.config(state="disabled")

    def _save_output(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("JSON", "*.json"), ("All", "*.*")])
        if path:
            content = self._output.get("1.0", "end")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Output saved to:\n{path}")

    def _restore_btn(self):
        self._run_btn.config(state="normal", text="▶  RUN")

    def _status(self, msg: str):
        self._status_var.set(msg)

    def _get_router(self):
        if self._router is None:
            try:
                from core.task_router import TaskRouter
                self._router = TaskRouter()
            except Exception:
                return None
        return self._router

    def _load_router_async(self):
        def _load():
            r = self._get_router()
            msg = (f"● Ready  |  {len(r._engines)} modules loaded"
                   if r else
                   "⚠ Router failed — Go to Tool Installer tab")
            self.after(0, self._status, msg)
        threading.Thread(target=_load, daemon=True).start()


# ─── Entry Point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    # Load .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    app = CyberApp()
    app.mainloop()
