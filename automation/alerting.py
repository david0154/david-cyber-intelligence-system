#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM
Alerting Module — automation/alerting.py

Sends alerts via:
  - Telegram Bot (instant push notification)
  - SMTP Email   (with HTML report attached)
  - Desktop popup (Tkinter, no external service)
  - Log file     (always, as fallback)

Required .env variables:
  TELEGRAM_BOT_TOKEN  — from t.me/botfather
  TELEGRAM_CHAT_ID    — your chat ID
  SMTP_HOST           — e.g. smtp.gmail.com
  SMTP_PORT           — e.g. 587
  SMTP_USER           — your email
  SMTP_PASS           — app password
  ALERT_EMAIL         — destination email

Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import smtplib
import threading
import requests
from email.mime.text      import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime             import datetime
from loguru               import logger
from typing               import Optional

# ── Env
TELEGRAM_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
SMTP_HOST        = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT        = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER        = os.getenv("SMTP_USER", "")
SMTP_PASS        = os.getenv("SMTP_PASS", "")
ALERT_EMAIL      = os.getenv("ALERT_EMAIL", SMTP_USER)

SEVERITY_EMOJI = {
    "CRITICAL": "🔴",
    "HIGH":     "🟠",
    "MEDIUM":   "🟡",
    "LOW":      "🟢",
    "INFO":     "ℹ️",
}


class AlertManager:
    """
    Central alerting hub. Call send() from any module.
    All sends are non-blocking (background thread).
    """

    def __init__(self):
        self._session = requests.Session()

    # ── Public API ────────────────────────────────────────────────────────────
    def send(self, title: str, body: str, severity: str = "HIGH",
             source: str = "", extra: dict = None):
        """
        Send alert via all configured channels.
        Non-blocking — fires in background thread.
        """
        event = {
            "title":     title,
            "body":      body,
            "severity":  severity.upper(),
            "source":    source,
            "extra":     extra or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        logger.warning(f"[Alert] {severity} | {title} | {body[:80]}")
        threading.Thread(
            target=self._dispatch, args=(event,), daemon=True
        ).start()

    # ── Dispatch ──────────────────────────────────────────────────────────────
    def _dispatch(self, event: dict):
        if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
            self._send_telegram(event)
        if SMTP_USER and SMTP_PASS and ALERT_EMAIL:
            self._send_email(event)
        # Desktop popup — always works, no config needed
        self._send_desktop(event)

    # ── Telegram ──────────────────────────────────────────────────────────────
    def _send_telegram(self, event: dict):
        emoji = SEVERITY_EMOJI.get(event["severity"], "⚠️")
        text  = (
            f"{emoji} *DAVID CIS Alert*\n"
            f"*{event['title']}*\n"
            f"Severity: `{event['severity']}`\n"
            f"Source: `{event['source'] or 'System'}`\n"
            f"Time: `{event['timestamp']}`\n\n"
            f"{event['body'][:800]}"
        )
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            r   = self._session.post(url, json={
                "chat_id":    TELEGRAM_CHAT_ID,
                "text":       text,
                "parse_mode": "Markdown"
            }, timeout=10)
            if r.status_code == 200:
                logger.info("[Alert] Telegram sent ✓")
            else:
                logger.warning(f"[Alert] Telegram failed: {r.status_code} {r.text[:100]}")
        except Exception as e:
            logger.error(f"[Alert] Telegram error: {e}")

    # ── Email ─────────────────────────────────────────────────────────────────
    def _send_email(self, event: dict):
        emoji = SEVERITY_EMOJI.get(event["severity"], "⚠️")
        subject = f"[DAVID CIS] {emoji} {event['severity']}: {event['title']}"
        html = f"""
        <html><body style="font-family:monospace;background:#0a0a0f;color:#ccc;padding:20px">
          <h2 style="color:#ff4444">{emoji} DAVID CIS Security Alert</h2>
          <table style="width:100%;border-collapse:collapse">
            <tr><td style="color:#888;width:120px">Title</td>
                <td style="color:#fff">{event['title']}</td></tr>
            <tr><td style="color:#888">Severity</td>
                <td style="color:#ff8800">{event['severity']}</td></tr>
            <tr><td style="color:#888">Source</td>
                <td>{event['source'] or 'System'}</td></tr>
            <tr><td style="color:#888">Time</td>
                <td>{event['timestamp']}</td></tr>
          </table>
          <hr style="border-color:#333">
          <pre style="color:#aaffaa;white-space:pre-wrap">{event['body']}</pre>
          <hr style="border-color:#333">
          <small style="color:#555">DAVID Cyber Intelligence System — Nexuzy Tech Pvt Ltd</small>
        </body></html>
        """
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = SMTP_USER
        msg["To"]      = ALERT_EMAIL
        msg.attach(MIMEText(html, "html"))
        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as s:
                s.ehlo()
                s.starttls()
                s.login(SMTP_USER, SMTP_PASS)
                s.sendmail(SMTP_USER, ALERT_EMAIL, msg.as_string())
            logger.info("[Alert] Email sent ✓")
        except smtplib.SMTPAuthenticationError:
            logger.error("[Alert] SMTP auth failed — check SMTP_USER/SMTP_PASS in .env")
        except Exception as e:
            logger.error(f"[Alert] Email error: {e}")

    # ── Desktop popup ─────────────────────────────────────────────────────────
    def _send_desktop(self, event: dict):
        """Non-blocking Tkinter popup."""
        def show():
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                emoji = SEVERITY_EMOJI.get(event["severity"], "⚠️")
                messagebox.showwarning(
                    title=f"{emoji} {event['severity']}: {event['title']}",
                    message=event["body"][:300]
                )
                root.destroy()
            except Exception:
                pass
        # Only show popups for HIGH/CRITICAL
        if event["severity"] in ("CRITICAL", "HIGH"):
            threading.Thread(target=show, daemon=True).start()


# ── Convenience singleton
_manager = None

def get_alert_manager() -> AlertManager:
    global _manager
    if _manager is None:
        _manager = AlertManager()
    return _manager

def alert(title: str, body: str, severity: str = "HIGH",
          source: str = "", extra: dict = None):
    """Module-level shortcut: from automation.alerting import alert."""
    get_alert_manager().send(title, body, severity, source, extra)


if __name__ == "__main__":
    a = AlertManager()
    a.send(
        title="Test Alert",
        body="This is a test from DAVID CIS alerting module.",
        severity="HIGH",
        source="test"
    )
    import time; time.sleep(3)
