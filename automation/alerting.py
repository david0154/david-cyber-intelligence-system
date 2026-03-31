"""
Alerting Module — Full Implementation
Telegram + Email (SMTP) + Desktop notifications
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from loguru import logger


class AlertManager:
    """
    Sends alerts via Telegram bot, SMTP email, and desktop toast.
    Reads from .env:
      TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
      SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ALERT_EMAIL
    """

    SEVERITY_EMOJI = {
        "CRITICAL": "\U0001f534",
        "HIGH":     "\U0001f7e0",
        "MEDIUM":   "\U0001f7e1",
        "LOW":      "\U0001f7e2",
        "INFO":     "\u2139\ufe0f",
    }

    def __init__(self):
        self.tg_token   = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        self.smtp_host  = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port  = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user  = os.getenv("SMTP_USER", "")
        self.smtp_pass  = os.getenv("SMTP_PASS", "")
        self.alert_email= os.getenv("ALERT_EMAIL", self.smtp_user)
        self._history: list = []
        logger.success("AlertManager ready.")

    # ─────────────────────────────────────────
    #  MAIN SEND
    # ─────────────────────────────────────────
    def send(self, title: str, message: str,
             severity: str = "HIGH", attachment_path: str = "") -> dict:
        """Send alert via all configured channels."""
        severity = severity.upper()
        emoji = self.SEVERITY_EMOJI.get(severity, "\u26a0\ufe0f")
        full_title = f"{emoji} DAVID CIS [{severity}] — {title}"

        entry = {
            "title": full_title,
            "message": message[:500],
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat(),
            "channels": [],
        }

        # Telegram
        tg_ok = self._send_telegram(full_title, message)
        if tg_ok:  entry["channels"].append("telegram")

        # Email
        if severity in ("CRITICAL", "HIGH"):
            mail_ok = self._send_email(full_title, message, attachment_path)
            if mail_ok: entry["channels"].append("email")

        # Desktop notification
        self._desktop_notify(full_title, message)
        entry["channels"].append("desktop")

        self._history.append(entry)
        return entry

    # ─────────────────────────────────────────
    #  TELEGRAM
    # ─────────────────────────────────────────
    def _send_telegram(self, title: str, message: str) -> bool:
        if not self.tg_token or not self.tg_chat_id:
            return False
        try:
            import requests
            text = f"*{title}*\n\n{message[:3000]}"
            r = requests.post(
                f"https://api.telegram.org/bot{self.tg_token}/sendMessage",
                json={
                    "chat_id": self.tg_chat_id,
                    "text": text,
                    "parse_mode": "Markdown",
                },
                timeout=8,
            )
            ok = r.json().get("ok", False)
            if ok:
                logger.success(f"Telegram alert sent: {title[:50]}")
            else:
                logger.warning(f"Telegram error: {r.json().get('description')}")
            return ok
        except Exception as e:
            logger.error(f"Telegram send failed: {e}")
            return False

    # ─────────────────────────────────────────
    #  EMAIL
    # ─────────────────────────────────────────
    def _send_email(self, subject: str, body: str,
                    attachment_path: str = "") -> bool:
        if not self.smtp_user or not self.smtp_pass:
            logger.warning("Email not configured — set SMTP_USER and SMTP_PASS")
            return False
        if not self.alert_email:
            logger.warning("ALERT_EMAIL not set")
            return False
        try:
            msg = MIMEMultipart()
            msg["From"]    = self.smtp_user
            msg["To"]      = self.alert_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                fname = os.path.basename(attachment_path)
                part.add_header("Content-Disposition",
                                f"attachment; filename={fname}")
                msg.attach(part)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.smtp_user, self.alert_email,
                                msg.as_string())
            logger.success(f"Email alert sent to {self.alert_email}")
            return True
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP auth failed — check SMTP_USER/SMTP_PASS")
            return False
        except smtplib.SMTPConnectError:
            logger.error(f"SMTP connect failed — check SMTP_HOST={self.smtp_host} SMTP_PORT={self.smtp_port}")
            return False
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False

    # ─────────────────────────────────────────
    #  DESKTOP NOTIFICATION
    # ─────────────────────────────────────────
    def _desktop_notify(self, title: str, message: str):
        try:
            import platform
            system = platform.system()
            if system == "Windows":
                try:
                    from win10toast import ToastNotifier
                    ToastNotifier().show_toast(
                        title, message[:200], duration=6, threaded=True)
                except ImportError:
                    pass
            elif system == "Linux":
                import subprocess
                subprocess.run(["notify-send", title[:80], message[:200]],
                               capture_output=True, timeout=3)
            elif system == "Darwin":
                import subprocess
                script = f'display notification "{message[:200]}" with title "{title[:80]}"'
                subprocess.run(["osascript", "-e", script],
                               capture_output=True, timeout=3)
        except Exception:
            pass

    # ─────────────────────────────────────────
    #  ALERT HISTORY
    # ─────────────────────────────────────────
    def get_history(self, limit: int = 50) -> list:
        return self._history[-limit:]

    def clear_history(self):
        self._history = []

    def test_channels(self) -> dict:
        """Send a test alert to verify all channels work."""
        return self.send(
            title="Test Alert",
            message="DAVID CIS alerting system is working correctly.",
            severity="INFO",
        )
