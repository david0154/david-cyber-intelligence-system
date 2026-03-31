"""
Wazuh SIEM Integration
Log collection + attack detection + alerting
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import os
import requests
from loguru import logger
from requests.auth import HTTPBasicAuth

WAZUH_URL = os.getenv("WAZUH_URL", "https://localhost:55000")
WAZUH_USER = os.getenv("WAZUH_USER", "wazuh")
WAZUH_PASS = os.getenv("WAZUH_PASS", "wazuh")


class WazuhClient:
    """
    Wazuh SIEM integration for:
    - Live security alerts
    - Failed login detection
    - Unusual location alerts
    - Traffic spike detection
    Setup: https://documentation.wazuh.com/current/installation-guide/
    """

    def __init__(self):
        self.base = WAZUH_URL
        self.auth = HTTPBasicAuth(WAZUH_USER, WAZUH_PASS)
        self.token = None
        self._authenticate()

    def _authenticate(self):
        try:
            resp = requests.post(
                f"{self.base}/security/user/authenticate",
                auth=self.auth,
                verify=False,
                timeout=5
            )
            if resp.status_code == 200:
                self.token = resp.json().get("data", {}).get("token")
                logger.success("[Wazuh] Authenticated.")
            else:
                logger.warning(f"[Wazuh] Auth failed: {resp.status_code}")
        except Exception as e:
            logger.warning(f"[Wazuh] Not reachable: {e}")

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def get_alerts(self, limit: int = 20) -> dict:
        result = {"status": "ok", "alerts": [], "failed_logins": [], "suspicious_ips": []}
        if not self.token:
            result["status"] = "offline"
            result["message"] = "Wazuh not connected. Install: https://documentation.wazuh.com"
            return result
        try:
            resp = requests.get(
                f"{self.base}/security/events",
                headers=self._headers(),
                params={"limit": limit, "sort": "-timestamp"},
                verify=False,
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json().get("data", {}).get("affected_items", [])
                result["alerts"] = data[:limit]
                # Extract failed logins
                result["failed_logins"] = [
                    a for a in data if "authentication" in str(a).lower() and "failure" in str(a).lower()
                ][:10]
                # Suspicious IPs (rule level >= 10)
                result["suspicious_ips"] = [
                    a.get("agent", {}).get("ip", "") for a in data
                    if a.get("rule", {}).get("level", 0) >= 10
                ][:10]
        except Exception as e:
            logger.error(f"[Wazuh] Get alerts error: {e}")
            result["status"] = "error"
            result["message"] = str(e)
        return result

    def get_agents(self) -> dict:
        if not self.token:
            return {"status": "offline"}
        try:
            resp = requests.get(
                f"{self.base}/agents",
                headers=self._headers(),
                verify=False, timeout=5
            )
            return resp.json() if resp.status_code == 200 else {}
        except Exception as e:
            return {"status": "error", "message": str(e)}
