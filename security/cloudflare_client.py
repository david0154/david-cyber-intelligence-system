"""
Cloudflare API Integration
Blocked IPs, traffic stats, WAF events
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import os
import requests
from loguru import logger

CF_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
CF_EMAIL = os.getenv("CLOUDFLARE_EMAIL", "")
CF_BASE = "https://api.cloudflare.com/client/v4"


class CloudflareClient:
    """
    Cloudflare integration:
    - WAF events
    - Blocked IPs
    - Traffic analytics
    - Firewall rules
    Setup: https://dash.cloudflare.com/profile/api-tokens
    """

    def __init__(self):
        self.token = CF_API_TOKEN
        self.email = CF_EMAIL
        if not self.token:
            logger.warning("[Cloudflare] CLOUDFLARE_API_TOKEN not set.")

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        return {}

    def get_zones(self) -> list:
        try:
            resp = requests.get(f"{CF_BASE}/zones", headers=self._headers(), timeout=10)
            if resp.status_code == 200:
                return resp.json().get("result", [])
        except Exception as e:
            logger.error(f"[Cloudflare] Zones error: {e}")
        return []

    def get_stats(self, zone_id: str = "") -> dict:
        result = {"status": "ok", "zones": [], "waf_events": [], "blocked_ips": [], "traffic": {}}
        if not self.token:
            result["status"] = "offline"
            result["message"] = "Set CLOUDFLARE_API_TOKEN in .env"
            return result

        zones = self.get_zones()
        result["zones"] = [{"id": z["id"], "name": z["name"]} for z in zones[:5]]

        target_zone = zone_id or (zones[0]["id"] if zones else None)
        if not target_zone:
            return result

        # WAF events
        try:
            resp = requests.get(
                f"{CF_BASE}/zones/{target_zone}/firewall/events",
                headers=self._headers(), timeout=10
            )
            if resp.status_code == 200:
                events = resp.json().get("result", [])
                result["waf_events"] = events[:10]
                result["blocked_ips"] = list({e.get("clientIP", "") for e in events if e.get("action") == "block"})[:20]
        except Exception as e:
            logger.error(f"[Cloudflare] WAF events error: {e}")

        # Analytics
        try:
            resp = requests.get(
                f"{CF_BASE}/zones/{target_zone}/analytics/dashboard",
                headers=self._headers(),
                params={"since": "-1440", "until": "0"},
                timeout=10
            )
            if resp.status_code == 200:
                result["traffic"] = resp.json().get("result", {}).get("totals", {})
        except Exception as e:
            logger.error(f"[Cloudflare] Analytics error: {e}")

        return result

    def block_ip(self, zone_id: str, ip: str, notes: str = "Blocked by DAVID CIS") -> dict:
        try:
            resp = requests.post(
                f"{CF_BASE}/zones/{zone_id}/firewall/access_rules/rules",
                headers=self._headers(),
                json={"mode": "block", "configuration": {"target": "ip", "value": ip}, "notes": notes},
                timeout=10
            )
            return resp.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
