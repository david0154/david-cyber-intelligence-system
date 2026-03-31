#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM
Bug Analyzer GUI Tab — drop-in Tkinter frame
Add to gui_app.py by importing and calling build_bug_analyzer_tab(parent)

Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import threading
import json
import os
import webbrowser
from datetime import datetime

# Colors (match main GUI)
BG        = "#0a0a0a"
BG2       = "#111111"
BG3       = "#1a1a1a"
ACCENT    = "#00ff41"
ACCENT2   = "#41b3ff"
DANGER    = "#ff4141"
WARN      = "#ffd700"
FG        = "#e0e0e0"
FG_DIM    = "#555555"
FONT_MONO = ("Courier New", 10)
FONT_H2   = ("Courier New", 11, "bold")
FONT_SMALL= ("Courier New", 9)
FONT_MENU = ("Courier New", 10, "bold")

SEV_COLORS = {
    "CRITICAL": "#ff4141",
    "HIGH":     "#ff8800",
    "MEDIUM":   "#ffd700",
    "LOW":      "#41b3ff",
    "INFO":     "#888888",
    "CLEAN":    "#00ff41",
}


class BugAnalyzerTab(tk.Frame):
    """
    Self-contained Bug Analyzer tab.
    Usage:
        tab = BugAnalyzerTab(parent)
        tab.pack(fill='both', expand=True)
    """

    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG, **kw)
        self._engine   = None
        self._report   = None
        self._last_html = None
        self._build()

    def _build(self):
        # ── Title row
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=18, pady=(14, 4))
        tk.Label(hdr,
                 text="\U0001f41b  APP BUG ANALYZER  \u2014  Find & Fix Bugs in Any Application",
                 font=FONT_H2, fg=ACCENT, bg=BG).pack(side="left")

        tk.Label(hdr,
                 text="Supports: APK  EXE/DLL  PHP  Python  JS  Java  URL  ZIP  Folder",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG).pack(side="right")

        tk.Frame(self, bg="#1a1a1a", height=1).pack(fill="x")

        # ── Input row
        inp = tk.Frame(self, bg=BG2)
        inp.pack(fill="x", padx=0)

        tk.Label(inp, text="  Target:",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG2).pack(side="left", pady=10)

        self._target_var = tk.StringVar()
        self._target_entry = tk.Entry(
            inp, textvariable=self._target_var,
            font=FONT_MONO, fg=ACCENT, bg=BG3,
            insertbackground=ACCENT, bd=0, relief="flat",
            highlightthickness=1, highlightbackground="#2a2a2a",
            highlightcolor=ACCENT, width=55
        )
        self._target_entry.pack(side="left", padx=8, pady=10)
        self._target_entry.insert(0, "Path to file/folder/APK/EXE  or  https://target.com")
        self._target_entry.bind("<FocusIn>", self._clear_hint)
        self._target_entry.bind("<Return>",  lambda e: self._run_scan())

        # Browse buttons
        for label, cmd in [
            ("\U0001f4c1 File",   self._browse_file),
            ("\U0001f4c2 Folder", self._browse_folder),
        ]:
            tk.Button(
                inp, text=label,
                font=FONT_SMALL, fg=FG, bg=BG3,
                activeforeground=ACCENT, activebackground=BG3,
                bd=0, relief="flat", cursor="hand2", padx=8, pady=6,
                command=cmd
            ).pack(side="left", padx=2)

        # Run button
        self._run_btn = tk.Button(
            inp, text="\u25b6  SCAN",
            font=FONT_MENU, fg="#000", bg=ACCENT,
            activeforeground="#000", activebackground="#00cc33",
            bd=0, relief="flat", cursor="hand2", padx=16, pady=6,
            command=self._run_scan
        )
        self._run_btn.pack(side="left", padx=10)

        tk.Frame(self, bg="#1a1a1a", height=1).pack(fill="x")

        # ── Main area: results table (left) + detail panel (right)
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=10, pady=8)

        # Left: score + bug table
        left = tk.Frame(main, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        # Score strip
        score_strip = tk.Frame(left, bg=BG2, height=58)
        score_strip.pack(fill="x")
        score_strip.pack_propagate(False)

        self._score_lbl = tk.Label(
            score_strip, text="Score: —",
            font=("Courier New", 20, "bold"), fg=ACCENT, bg=BG2)
        self._score_lbl.pack(side="left", padx=18, pady=10)

        self._level_lbl = tk.Label(
            score_strip, text="",
            font=("Courier New", 14, "bold"), fg=FG_DIM, bg=BG2)
        self._level_lbl.pack(side="left", padx=8)

        self._summary_lbl = tk.Label(
            score_strip, text="",
            font=FONT_SMALL, fg=FG_DIM, bg=BG2, wraplength=500, justify="left")
        self._summary_lbl.pack(side="left", padx=14)

        # Export buttons
        exp = tk.Frame(score_strip, bg=BG2)
        exp.pack(side="right", padx=12)
        tk.Button(exp, text="\U0001f4be JSON",
                  font=FONT_SMALL, fg=FG, bg=BG3,
                  activeforeground=ACCENT, activebackground=BG3,
                  bd=0, relief="flat", cursor="hand2", padx=8, pady=4,
                  command=self._export_json).pack(side="left", padx=2)
        tk.Button(exp, text="\U0001f4c4 HTML",
                  font=FONT_SMALL, fg=FG, bg=BG3,
                  activeforeground=ACCENT2, activebackground=BG3,
                  bd=0, relief="flat", cursor="hand2", padx=8, pady=4,
                  command=self._export_html).pack(side="left", padx=2)
        tk.Button(exp, text="\U0001f310 Open Report",
                  font=FONT_SMALL, fg="#000", bg=ACCENT2,
                  activeforeground="#000", activebackground="#3399cc",
                  bd=0, relief="flat", cursor="hand2", padx=8, pady=4,
                  command=self._open_html).pack(side="left", padx=2)

        # Bug table
        cols = ("Severity", "Issue", "File", "Line", "Fix")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                        background=BG3, foreground=FG,
                        fieldbackground=BG3, rowheight=24,
                        font=("Courier New", 9))
        style.configure("Dark.Treeview.Heading",
                        background=BG2, foreground=ACCENT,
                        font=("Courier New", 9, "bold"))
        style.map("Dark.Treeview",
                  background=[("selected", "#1a2a1a")],
                  foreground=[("selected", ACCENT)])

        tree_frame = tk.Frame(left, bg=BG3)
        tree_frame.pack(fill="both", expand=True, pady=(6, 0))

        self._tree = ttk.Treeview(
            tree_frame, columns=cols, show="headings",
            style="Dark.Treeview", selectmode="browse")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._tree.pack(fill="both", expand=True)

        widths = {"Severity": 90, "Issue": 240, "File": 160,
                  "Line": 55, "Fix": 300}
        for col in cols:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=widths.get(col, 120), anchor="w")

        # Color tags per severity
        for sev, color in SEV_COLORS.items():
            self._tree.tag_configure(sev, foreground=color)

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        # Right: detail panel
        right = tk.Frame(main, bg=BG2, width=320)
        right.pack(side="right", fill="y", padx=(10, 0))
        right.pack_propagate(False)

        tk.Label(right, text="Bug Detail",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG2).pack(
                     pady=(12, 4), anchor="w", padx=12)

        self._detail_text = scrolledtext.ScrolledText(
            right, font=FONT_MONO, fg=FG, bg=BG3,
            bd=0, relief="flat", wrap="word", state="disabled",
            height=20)
        self._detail_text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._detail_text.tag_config("sev",   foreground=DANGER,  font=("Courier New", 10, "bold"))
        self._detail_text.tag_config("fix",   foreground=ACCENT)
        self._detail_text.tag_config("code",  foreground=WARN)
        self._detail_text.tag_config("label", foreground=FG_DIM)
        self._detail_text.tag_config("cvss",  foreground=ACCENT2)

        # Log panel (bottom)
        tk.Frame(self, bg="#111", height=1).pack(fill="x")
        tk.Label(self, text="  Scan Log:",
                 font=FONT_SMALL, fg=FG_DIM, bg=BG).pack(
                     anchor="w", padx=18, pady=(4, 0))
        self._log = scrolledtext.ScrolledText(
            self, font=("Courier New", 8), fg=FG_DIM, bg="#080808",
            bd=0, relief="flat", wrap="word", state="disabled", height=6)
        self._log.pack(fill="x", padx=10, pady=(0, 8))

    # ── Actions ─────────────────────────────────────────────────────────────
    def _clear_hint(self, event):
        hints = ["Path to file/folder/APK/EXE  or  https://target.com"]
        if self._target_var.get() in hints:
            self._target_entry.delete(0, "end")

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Select file to analyze",
            filetypes=[
                ("All files",     "*.*"),
                ("Android APK",   "*.apk"),
                ("Executables",   "*.exe *.dll *.bin"),
                ("PHP",           "*.php"),
                ("Python",        "*.py"),
                ("JavaScript",    "*.js *.ts"),
                ("Java",          "*.java *.kt"),
                ("ZIP Archive",   "*.zip"),
            ])
        if path:
            self._target_var.set(path)

    def _browse_folder(self):
        path = filedialog.askdirectory(title="Select project folder")
        if path:
            self._target_var.set(path)

    def _run_scan(self):
        target = self._target_var.get().strip()
        if not target or target.startswith("Path to"):
            return
        self._run_btn.config(state="disabled", text="\u23f3 Scanning...")
        self._clear_tree()
        self._log_clear()
        self._log_write(f"[{datetime.now().strftime('%H:%M:%S')}] Starting scan: {target}\n")
        threading.Thread(
            target=self._do_scan, args=(target,), daemon=True).start()

    def _do_scan(self, target: str):
        try:
            from engines.bug_analyzer import BugAnalyzerEngine
            engine = BugAnalyzerEngine()
            report = engine.analyze(
                target,
                progress_cb=lambda m: self.after(0, self._log_write, m)
            )
            self._report = report
            self._engine = engine
            self.after(0, self._display_report, report)
        except Exception as e:
            self.after(0, self._log_write, f"\u2716 Error: {e}\n")
        finally:
            self.after(0, lambda: self._run_btn.config(
                state="normal", text="\u25b6  SCAN"))

    def _display_report(self, report: dict):
        level = report.get("risk_level", "CLEAN")
        score = report.get("risk_score", 0)
        color = SEV_COLORS.get(level, ACCENT)

        self._score_lbl.config(
            text=f"Score: {score}/100", fg=color)
        self._level_lbl.config(
            text=level, fg=color)
        self._summary_lbl.config(
            text=report.get("summary", ""))

        # Populate tree
        for bug in report.get("bugs", []):
            sev  = bug["severity"]
            line = str(bug["line"]) if bug["line"] else "—"
            fix  = bug["fix"][:80]
            self._tree.insert(
                "", "end",
                values=(sev, bug["name"], bug["source"], line, fix),
                tags=(sev,)
            )

        self._log_write(
            f"\u2714 Done | {report['total_bugs']} bugs | "
            f"Risk: {level} ({score}/100) | "
            f"Files: {report['files_scanned']}\n"
        )

    def _on_select(self, event):
        sel = self._tree.selection()
        if not sel or not self._report:
            return
        item  = self._tree.item(sel[0])
        vals  = item["values"]
        # Find matching bug
        name  = vals[1] if len(vals) > 1 else ""
        bugs  = [b for b in self._report["bugs"] if b["name"] == name]
        bug   = bugs[0] if bugs else {}

        self._detail_text.config(state="normal")
        self._detail_text.delete("1.0", "end")
        if bug:
            self._detail_text.insert("end", f"  {bug['severity']}\n", "sev")
            self._detail_text.insert("end", f"\n", "label")
            self._detail_text.insert("end", "Issue:\n", "label")
            self._detail_text.insert("end", f"  {bug['name']}\n\n")
            self._detail_text.insert("end", "File:\n", "label")
            self._detail_text.insert("end",
                f"  {bug.get('source_full', bug.get('source',''))}")
            if bug.get("line"):
                self._detail_text.insert("end", f"  :  line {bug['line']}")
            self._detail_text.insert("end", "\n\n")
            if bug.get("detail"):
                self._detail_text.insert("end", "Code:\n", "label")
                self._detail_text.insert(
                    "end", f"  {bug['detail']}\n\n", "code")
            self._detail_text.insert("end", "Fix:\n", "label")
            self._detail_text.insert("end", f"  {bug['fix']}\n\n", "fix")
            self._detail_text.insert("end", "CVSS Estimate:\n", "label")
            self._detail_text.insert(
                "end", f"  {bug.get('cvss','N/A')}\n", "cvss")
        self._detail_text.config(state="disabled")

    # ── Export ──────────────────────────────────────────────────────────────
    def _export_json(self):
        if not self._report:
            return
        from engines.bug_analyzer import BugAnalyzerEngine
        path = self._engine.save_report_json(self._report) if self._engine else None
        if path:
            self._log_write(f"\u2714 JSON saved: {path}\n")

    def _export_html(self):
        if not self._report:
            return
        from engines.bug_analyzer import BugAnalyzerEngine
        path = self._engine.save_report_html(self._report) if self._engine else None
        if path:
            self._last_html = path
            self._log_write(f"\u2714 HTML saved: {path}\n")

    def _open_html(self):
        if not self._report:
            return
        if not self._last_html:
            self._export_html()
        if self._last_html and os.path.exists(self._last_html):
            webbrowser.open(f"file://{os.path.abspath(self._last_html)}")

    # ── Helpers ─────────────────────────────────────────────────────────────
    def _clear_tree(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._score_lbl.config(text="Score: —", fg=ACCENT)
        self._level_lbl.config(text="", fg=FG_DIM)
        self._summary_lbl.config(text="")

    def _log_write(self, msg: str):
        self._log.config(state="normal")
        self._log.insert("end", msg)
        self._log.see("end")
        self._log.config(state="disabled")

    def _log_clear(self):
        self._log.config(state="normal")
        self._log.delete("1.0", "end")
        self._log.config(state="disabled")
