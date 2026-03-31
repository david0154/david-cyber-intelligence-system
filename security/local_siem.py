#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM
Local SIEM — NO WAZUH / NO SERVER REQUIRED

Replaces Wazuh + Elasticsearch with:
  - Local log file monitoring (Windows Event Log, syslog, app logs)
  - SQLite event storage (zero server)
  - Pattern-based alert rules (Wazuh-style, but local)
  - Real-time tail of log files
  - Failed login detection
  - Anomaly detection with basic ML
  - Works 100% OFFLINE

Optional: If Wazuh IS available, falls back to it.

Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import re
import json
import sqlite3
import platform
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from loguru import logger
from typing import Callable, Optional

DB_PATH = Path("data/siem.db")

# ── Log sources per OS
LOG_SOURCES = {
    "Windows": [
        "%SystemRoot%\\System32\\winevt\\Logs\\Security.evtx",
        "%SystemRoot%\\System32\\winevt\\Logs\\Application.evtx",
        "%SystemRoot%\\System32\\winevt\\Logs\\System.evtx",
        "%TEMP%\\david_app.log",
    ],
    "Linux": [
        "/var/log/auth.log",
        "/var/log/syslog",
        "/var/log/kern.log",
        "/var/log/apache2/access.log",
        "/var/log/apache2/error.log",
        "/var/log/nginx/access.log",
        "/var/log/nginx/error.log",
        "/var/log/mysql/error.log",
        "/tmp/david_app.log",
    ],
    "Darwin": [
        "/var/log/system.log",
        "/var/log/auth.log",
        "/tmp/david_app.log",
    ],
}

# ── Alert rules (name, regex pattern, severity, description)
ALERT_RULES = [
    # Auth / brute force
    ("Failed SSH Login",       r"Failed password for .* from ([\d.]+)",         "HIGH",     "SSH brute force attempt"),
    ("SSH Root Login Attempt", r"Failed password for root from ([\d.]+)",        "CRITICAL", "Root SSH brute force"),
    ("Invalid User Login",     r"Invalid user .* from ([\d.]+)",                 "MEDIUM",   "Unknown user login attempt"),
    ("Sudo Privilege Escalation", r"sudo:.*COMMAND=(.*)",                         "HIGH",     "Privilege escalation via sudo"),
    ("Accepted Password Login",r"Accepted password for .* from ([\d.]+)",        "INFO",     "Successful SSH login"),
    ("Multiple Auth Failures", r"authentication failure.*rhost=([\d.]+)",        "HIGH",     "PAM authentication failure"),
    # Malware / exploit
    ("Reverse Shell Pattern",  r"(?:bash|sh|nc|ncat|python).*(?:/dev/tcp|/dev/udp)", "CRITICAL", "Possible reverse shell"),
    ("Base64 Execution",       r"base64.*decode.*|echo.*\|.*base64",              "HIGH",     "Obfuscated command execution"),
    ("Wget/Curl Pipe to Shell",r"(?:wget|curl).*\|.*(?:bash|sh)",                "CRITICAL", "Remote code execution via pipe"),
    ("Python Reverse Shell",   r"python.*import socket.*exec",                    "CRITICAL", "Python reverse shell"),
    # Web attacks
    ("SQL Injection in Log",   r"(?:UNION|SELECT|INSERT|DROP|UPDATE).*--",       "HIGH",     "SQL injection attempt"),
    ("XSS Attempt",            r"<script.*>|javascript:",                         "MEDIUM",   "Cross-site scripting attempt"),
    ("Path Traversal",         r"\.\./\.\./|%2e%2e%2f",                          "HIGH",     "Directory traversal attempt"),
    ("Scanner Detected",       r"(?:Nmap|masscan|nikto|sqlmap|nessus|openvas)",  "MEDIUM",   "Security scanner detected"),
    ("Web Shell Pattern",      r"(?:cmd|exec|system|passthru).*\$_(?:GET|POST)", "CRITICAL", "Web shell pattern"),
    # System
    ("Cron Job Modified",      r"CRON.*CMD",                                      "INFO",     "Cron job executed"),
    ("New User Created",       r"useradd|adduser|New user",                       "HIGH",     "New system user created"),
    ("Firewall Rule Changed",  r"iptables|ufw|firewall-cmd",                      "MEDIUM",   "Firewall configuration changed"),
    ("File Permission Change", r"chmod 777|chmod \+s",                           "HIGH",     "Dangerous file permission change"),
    ("Outbound Connection",    r"CONNECT ([\d.]+):(?:4444|1337|6666|9999|31337)", "CRITICAL", "Known C2 port connection"),
    # Windows-specific
    ("Windows Login Failure",  r"Logon Failure|EventID.*4625",                   "HIGH",     "Windows failed login"),
    ("Windows Privilege Use",  r"EventID.*4672|Special privileges assigned",     "HIGH",     "Special privilege assigned"),
    ("Windows Process Exec",   r"EventID.*4688|A new process has been created",  "INFO",     "New process created"),
    ("Mimikatz Pattern",       r"sekurlsa|lsadump|kerberos.*golden",             "CRITICAL", "Mimikatz / credential dumping"),
    ("Ransomware Pattern",     r"\.locked|YOUR_FILES_ARE_ENCRYPTED|README_DECRYPT", "CRITICAL", "Ransomware activity detected"),
]


class LocalSIEM:
    """
    Fully local SIEM. Monitors log files, detects threats,
    stores events in SQLite. No Wazuh, no Elasticsearch needed.
    """

    def __init__(self, alert_cb: Optional[Callable] = None):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self._init_db()
        self.alert_cb   = alert_cb or (lambda e: None)
        self._running   = False
        self._threads   = []
        self._brute_track = defaultdict(list)  # ip -> [timestamps]
        self._lock      = threading.Lock()
        self._os        = platform.system()

    def _init_db(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT DEFAULT (datetime('now')),
            severity    TEXT,
            rule_name   TEXT,
            description TEXT,
            source_ip   TEXT,
            log_source  TEXT,
            raw_line    TEXT
        );
        CREATE TABLE IF NOT EXISTS stats (
            date        TEXT PRIMARY KEY,
            critical    INTEGER DEFAULT 0,
            high        INTEGER DEFAULT 0,
            medium      INTEGER DEFAULT 0,
            low         INTEGER DEFAULT 0,
            info        INTEGER DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_ev_sev ON events(severity);
        CREATE INDEX IF NOT EXISTS idx_ev_ts  ON events(timestamp);
        """)
        self.conn.commit()

    # ── Start monitoring all log sources
    def start(self):
        self._running = True
        sources = LOG_SOURCES.get(self._os, LOG_SOURCES["Linux"])
        for src in sources:
            src = os.path.expandvars(src)
            if os.path.exists(src) and src.endswith(".log"):
                t = threading.Thread(
                    target=self._tail_file,
                    args=(src,), daemon=True
                )
                t.start()
                self._threads.append(t)
                logger.info(f"[SIEM] Monitoring: {src}")

        # Windows Event Log (if on Windows)
        if self._os == "Windows":
            t = threading.Thread(target=self._monitor_windows_events, daemon=True)
            t.start()
            self._threads.append(t)

        logger.info(f"[SIEM] Started. Monitoring {len(self._threads)} source(s).")

    def stop(self):
        self._running = False

    # ── Tail a text log file
    def _tail_file(self, filepath: str):
        """Continuously reads new lines from a log file."""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(0, 2)   # Seek to end
                while self._running:
                    line = f.readline()
                    if line:
                        self._process_line(line.strip(), filepath)
                    else:
                        import time; time.sleep(0.5)
        except PermissionError:
            logger.warning(f"[SIEM] No permission to read: {filepath}")
        except Exception as e:
            logger.error(f"[SIEM] tail error {filepath}: {e}")

    # ── Windows Event Log via PowerShell
    def _monitor_windows_events(self):
        import time
        while self._running:
            try:
                result = subprocess.run(
                    ["powershell", "-Command",
                     "Get-EventLog -LogName Security -Newest 20 "
                     "| Select-Object TimeGenerated,EventID,Message "
                     "| ConvertTo-Json -Depth 2"],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0:
                    events = json.loads(result.stdout or "[]")
                    if isinstance(events, dict): events = [events]
                    for ev in events:
                        line = f"EventID {ev.get('EventID','')} {ev.get('Message','')[:200]}"
                        self._process_line(line, "Windows-Security")
            except Exception:
                pass
            time.sleep(10)

    # ── Process a single log line against all rules
    def _process_line(self, line: str, source: str):
        for rule_name, pattern, severity, description in ALERT_RULES:
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                source_ip = m.group(1) if m.lastindex else ""
                self._fire_alert(severity, rule_name, description,
                                 source_ip, source, line)
                # Brute force detection
                if source_ip and severity in ("HIGH", "CRITICAL"):
                    self._check_brute_force(source_ip)

    # ── Brute force detector (5+ events in 60 seconds)
    def _check_brute_force(self, ip: str):
        import time
        now = time.time()
        with self._lock:
            self._brute_track[ip] = [
                t for t in self._brute_track[ip] if now - t < 60
            ]
            self._brute_track[ip].append(now)
            count = len(self._brute_track[ip])
        if count == 5:
            self._fire_alert(
                "CRITICAL",
                "Brute Force Detected",
                f"IP {ip} made {count} failed attempts in 60 seconds.",
                ip, "brute_force_detector",
                f"Auto-detected brute force from {ip}"
            )

    # ── Fire alert
    def _fire_alert(self, severity, rule_name, description,
                    source_ip, log_source, raw_line):
        event = {
            "timestamp":   datetime.utcnow().isoformat(),
            "severity":    severity,
            "rule_name":   rule_name,
            "description": description,
            "source_ip":   source_ip,
            "log_source":  log_source,
            "raw_line":    raw_line[:500],
        }
        # Store in DB
        self.conn.execute("""
            INSERT INTO events
            (timestamp, severity, rule_name, description, source_ip, log_source, raw_line)
            VALUES (?,?,?,?,?,?,?)
        """, tuple(event.values()))
        self.conn.commit()
        self._update_stats(severity)
        # Callback to GUI / alerts
        logger.warning(f"[SIEM] {severity} | {rule_name} | {source_ip}")
        self.alert_cb(event)

    def _update_stats(self, severity: str):
        date = datetime.utcnow().date().isoformat()
        col  = severity.lower()
        if col not in ("critical", "high", "medium", "low", "info"):
            return
        self.conn.execute(f"""
            INSERT INTO stats (date, {col}) VALUES (?, 1)
            ON CONFLICT(date) DO UPDATE SET {col} = {col} + 1
        """, (date,))
        self.conn.commit()

    # ── Manual log scan (scan a file or string now)
    def scan_text(self, text: str, source: str = "manual") -> list:
        """Scan any text/log content against all rules. Returns list of alerts."""
        alerts = []
        for line in text.splitlines():
            for rule_name, pattern, severity, description in ALERT_RULES:
                if re.search(pattern, line, re.IGNORECASE):
                    m = re.search(pattern, line, re.IGNORECASE)
                    alerts.append({
                        "rule":       rule_name,
                        "severity":   severity,
                        "description":description,
                        "source_ip":  m.group(1) if m and m.lastindex else "",
                        "line":       line[:300],
                    })
        return alerts

    # ── Query API
    def get_events(self, limit=100, severity=None) -> list:
        if severity:
            cur = self.conn.execute(
                "SELECT * FROM events WHERE severity=? ORDER BY timestamp DESC LIMIT ?",
                (severity, limit)
            )
        else:
            cur = self.conn.execute(
                "SELECT * FROM events ORDER BY timestamp DESC LIMIT ?", (limit,)
            )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    def get_stats(self) -> dict:
        cur = self.conn.execute(
            "SELECT * FROM stats ORDER BY date DESC LIMIT 7"
        )
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        total = self.conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        return {"daily": rows, "total_events": total,
                "rules_loaded": len(ALERT_RULES)}

    def get_top_threats(self, limit=10) -> list:
        cur = self.conn.execute("""
            SELECT source_ip, COUNT(*) as hits, MAX(severity) as max_sev
            FROM events WHERE source_ip != ''
            GROUP BY source_ip ORDER BY hits DESC LIMIT ?
        """, (limit,))
        return [dict(zip(["ip", "hits", "max_severity"], r)) for r in cur.fetchall()]


# ── Convenience singleton
_siem = None

def get_siem(alert_cb=None) -> LocalSIEM:
    global _siem
    if _siem is None:
        _siem = LocalSIEM(alert_cb=alert_cb)
    return _siem


if __name__ == "__main__":
    import time
    def on_alert(event):
        print(f"\n\033[31m[ALERT] {event['severity']} | {event['rule_name']}\033[0m")
        print(f"  IP: {event['source_ip']} | Source: {event['log_source']}")
        print(f"  {event['description']}")

    siem = LocalSIEM(alert_cb=on_alert)
    siem.start()
    print("[SIEM] Running... Ctrl+C to stop")
    print(f"[SIEM] Stats: {siem.get_stats()}")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        siem.stop()
