"""
OWASP ZAP Integration Engine
Auto web app vulnerability scanning
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import os
import requests
from loguru import logger

ZAP_BASE = os.getenv("ZAP_URL", "http://localhost:8080")
ZAP_API_KEY = os.getenv("ZAP_API_KEY", "")


class ZAPEngine:
    """
    OWASP ZAP automated scanner integration.
    Detects XSS, SQLi, auth issues, and more.
    Setup: Download ZAP from https://zaproxy.org and run in daemon mode:
      zap.sh -daemon -port 8080 -config api.key=YOUR_KEY
    """

    def __init__(self):
        self.base = ZAP_BASE
        self.api_key = ZAP_API_KEY
        self._check_connection()

    def _check_connection(self):
        try:
            resp = requests.get(f"{self.base}/JSON/core/view/version/", timeout=3)
            if resp.status_code == 200:
                logger.success(f"[ZAP] Connected at {self.base}")
        except Exception:
            logger.warning("[ZAP] Not running. Start ZAP daemon first.")

    def scan(self, url: str) -> dict:
        if not url:
            return {"status": "error", "message": "URL required"}
        result = {"status": "ok", "url": url, "spider": {}, "alerts": [], "risk_summary": {}}
        try:
            # Spider first
            spider_resp = requests.get(
                f"{self.base}/JSON/spider/action/scan/",
                params={"apikey": self.api_key, "url": url, "recurse": True},
                timeout=10
            )
            result["spider"] = spider_resp.json() if spider_resp.status_code == 200 else {}

            # Active scan
            scan_resp = requests.get(
                f"{self.base}/JSON/ascan/action/scan/",
                params={"apikey": self.api_key, "url": url, "recurse": True, "inScopeOnly": False},
                timeout=10
            )
            scan_data = scan_resp.json() if scan_resp.status_code == 200 else {}
            scan_id = scan_data.get("scan", "0")

            # Get alerts
            alerts_resp = requests.get(
                f"{self.base}/JSON/core/view/alerts/",
                params={"apikey": self.api_key, "baseurl": url, "start": 0, "count": 50},
                timeout=10
            )
            if alerts_resp.status_code == 200:
                alerts = alerts_resp.json().get("alerts", [])
                result["alerts"] = alerts[:20]
                # Risk summary
                risks = {"High": 0, "Medium": 0, "Low": 0, "Informational": 0}
                for a in alerts:
                    risk = a.get("risk", "Informational")
                    risks[risk] = risks.get(risk, 0) + 1
                result["risk_summary"] = risks
                result["scan_id"] = scan_id
        except requests.exceptions.ConnectionError:
            result["status"] = "offline"
            result["message"] = "ZAP not running. Start: zap.sh -daemon -port 8080"
        except Exception as e:
            logger.error(f"[ZAP] Scan error: {e}")
            result["status"] = "error"
            result["message"] = str(e)
        return result

    def get_alerts(self, base_url: str = "") -> list:
        try:
            resp = requests.get(
                f"{self.base}/JSON/core/view/alerts/",
                params={"apikey": self.api_key, "baseurl": base_url, "count": 100},
                timeout=5
            )
            if resp.status_code == 200:
                return resp.json().get("alerts", [])
        except Exception as e:
            logger.error(f"[ZAP] Get alerts error: {e}")
        return []
