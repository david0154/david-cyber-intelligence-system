"""
Automation & Scheduler Layer
Auto scans, alerts, patch suggestions
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import threading
import time
import smtplib
import os
import json
from email.mime.text import MIMEText
from datetime import datetime
from loguru import logger


class AlertManager:
    """
    Multi-channel alerting:
    - Email (SMTP)
    - Telegram Bot
    - Log file
    """

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_pass = os.getenv("SMTP_PASS", "")
        self.alert_email = os.getenv("ALERT_EMAIL", "")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.telegram_chat = os.getenv("TELEGRAM_CHAT_ID", "")

    def send_email(self, subject: str, body: str) -> bool:
        if not self.smtp_user or not self.alert_email:
            logger.warning("[Alert] Email not configured (SMTP_USER / ALERT_EMAIL missing).")
            return False
        try:
            msg = MIMEText(body)
            msg["Subject"] = f"[DAVID CIS] {subject}"
            msg["From"] = self.smtp_user
            msg["To"] = self.alert_email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as s:
                s.starttls()
                s.login(self.smtp_user, self.smtp_pass)
                s.send_message(msg)
            logger.success(f"[Alert] Email sent: {subject}")
            return True
        except Exception as e:
            logger.error(f"[Alert] Email failed: {e}")
            return False

    def send_telegram(self, message: str) -> bool:
        if not self.telegram_token or not self.telegram_chat:
            logger.warning("[Alert] Telegram not configured.")
            return False
        try:
            import requests
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            resp = requests.post(url, json={
                "chat_id": self.telegram_chat,
                "text": f"🛡️ DAVID CIS Alert\n{message}",
                "parse_mode": "Markdown",
            }, timeout=5)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"[Alert] Telegram failed: {e}")
            return False

    def alert(self, subject: str, body: str, channels=("email", "telegram", "log")):
        if "log" in channels:
            logger.warning(f"[ALERT] {subject}: {body[:200]}")
        if "email" in channels:
            threading.Thread(target=self.send_email,
                             args=(subject, body), daemon=True).start()
        if "telegram" in channels:
            threading.Thread(target=self.send_telegram,
                             args=(f"*{subject}*\n{body[:500]}",), daemon=True).start()


class ScanScheduler:
    """
    Scheduled automated scans.
    Runs background scan jobs at defined intervals.
    """

    def __init__(self):
        self.jobs = []
        self.alert_manager = AlertManager()
        self._running = False
        self._thread = None

    def add_job(self, name: str, target: str, scan_type: str,
                interval_seconds: int = 3600):
        self.jobs.append({
            "name": name,
            "target": target,
            "scan_type": scan_type,
            "interval": interval_seconds,
            "last_run": 0,
            "enabled": True,
        })
        logger.info(f"[Scheduler] Job added: {name} -> {target} every {interval_seconds}s")

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.success("[Scheduler] Started.")

    def stop(self):
        self._running = False
        logger.info("[Scheduler] Stopped.")

    def _loop(self):
        while self._running:
            now = time.time()
            for job in self.jobs:
                if not job["enabled"]:
                    continue
                if now - job["last_run"] >= job["interval"]:
                    job["last_run"] = now
                    threading.Thread(
                        target=self._run_job,
                        args=(job,), daemon=True
                    ).start()
            time.sleep(30)

    def _run_job(self, job: dict):
        logger.info(f"[Scheduler] Running job: {job['name']}")
        try:
            from core.task_router import TaskRouter
            router = TaskRouter()
            if job["scan_type"] == "vuln":
                result = router.route("vuln_scan",
                                      {"target": job["target"]})
            elif job["scan_type"] == "pentest":
                result = router.route("pentest",
                                      {"target": job["target"]})
            else:
                result = router.route(job["scan_type"],
                                      {"target": job["target"]})

            risk = result.get("risk_level", "LOW")
            if risk in ("HIGH", "CRITICAL"):
                self.alert_manager.alert(
                    f"{risk} Threat: {job['target']}",
                    f"Job: {job['name']}\nRisk: {risk}\n"
                    f"Details: {str(result)[:500]}"
                )
        except Exception as e:
            logger.error(f"[Scheduler] Job failed: {e}")
