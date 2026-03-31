"""
Defense Engine — Full Implementation
Open-AppSec ML WAF + AbuseIPDB + Cloudflare + Rate Limiting + Geo-Blocking
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import json
import time
import requests
import subprocess
import shutil
from datetime import datetime
from collections import defaultdict
from loguru import logger


class DefenseEngine:
    """
    Active defense: WAF filtering, IP reputation blocking,
    rate limiting, geo-blocking, Cloudflare push, alerting.
    """

    DANGEROUS_PATTERNS = [
        {"type": "sqli",          "patterns": ["' OR '", "1=1", "UNION SELECT", "DROP TABLE", "--", "';--", "xp_cmdshell"]},
        {"type": "xss",           "patterns": ["<script", "javascript:", "onerror=", "onload=", "alert(", "document.cookie"]},
        {"type": "rce",           "patterns": ["; rm -rf", "| cat /etc", "&& wget", "`id`", "$(id)", "eval("]},
        {"type": "path_traversal","patterns": ["../", "..%2F", "%2e%2e", "/etc/passwd", "C:\\Windows"]},
        {"type": "ssrf",          "patterns": ["169.254.169.254", "localhost", "127.0.0.1", "::1"]},
        {"type": "lfi",           "patterns": ["php://filter", "php://input", "data://text", "file://"]},
    ]

    def __init__(self):
        self.blocked_ips: set = set()
        self.whitelist_ips: set = set()
        self.threat_log: list = []
        self.rate_tracker: dict = defaultdict(list)   # ip -> [timestamps]
        self.rate_limit = int(os.getenv("RATE_LIMIT_RPM", "60"))  # requests per minute
        self.abuseipdb_key = os.getenv("ABUSEIPDB_API_KEY", "")
        self.cloudflare_token = os.getenv("CLOUDFLARE_API_TOKEN", "")
        self.geo_block_countries: list = os.getenv("GEO_BLOCK_COUNTRIES", "").split(",")
        self._load_saved_blocklist()
        logger.success("DefenseEngine ready.")

    # ─────────────────────────────────────────
    #  MAIN INSPECTION ENTRY POINT
    # ─────────────────────────────────────────
    def inspect(self, request_data: str, source_ip: str = "0.0.0.0",
                path: str = "/", method: str = "GET") -> dict:
        """Inspect incoming request. Returns action ALLOW / BLOCK / RATE_LIMIT."""

        if source_ip in self.whitelist_ips:
            return {"action": "ALLOW", "ip": source_ip, "reason": "whitelisted"}

        if source_ip in self.blocked_ips:
            return self._build_block(source_ip, "IP in blocklist")

        # Rate limiting
        rate_result = self._check_rate(source_ip)
        if rate_result:
            return rate_result

        # Geo-blocking
        geo_result = self._check_geo(source_ip)
        if geo_result:
            return geo_result

        # AbuseIPDB reputation check
        abuse_result = self._check_abuseipdb(source_ip)
        if abuse_result:
            return abuse_result

        # WAF pattern matching
        payload = f"{path} {method} {request_data}"
        for rule_group in self.DANGEROUS_PATTERNS:
            for pattern in rule_group["patterns"]:
                if pattern.lower() in payload.lower():
                    self._block_ip(source_ip, rule_group["type"])
                    return self._build_block(source_ip, f"WAF rule: {rule_group['type']}")

        return {"action": "ALLOW", "ip": source_ip}

    # ─────────────────────────────────────────
    #  RATE LIMITING
    # ─────────────────────────────────────────
    def _check_rate(self, ip: str) -> dict | None:
        now = time.time()
        window = 60
        self.rate_tracker[ip] = [t for t in self.rate_tracker[ip] if now - t < window]
        self.rate_tracker[ip].append(now)
        if len(self.rate_tracker[ip]) > self.rate_limit:
            self._block_ip(ip, "rate_limit")
            return self._build_block(ip, f"Rate limit exceeded: {self.rate_limit} req/min")
        return None

    # ─────────────────────────────────────────
    #  GEO BLOCKING
    # ─────────────────────────────────────────
    def _check_geo(self, ip: str) -> dict | None:
        if not any(c.strip() for c in self.geo_block_countries):
            return None
        try:
            resp = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode",
                                timeout=4)
            cc = resp.json().get("countryCode", "")
            if cc in [c.strip().upper() for c in self.geo_block_countries if c.strip()]:
                self._block_ip(ip, "geo_block")
                return self._build_block(ip, f"Geo-blocked country: {cc}")
        except Exception:
            pass
        return None

    # ─────────────────────────────────────────
    #  ABUSEIPDB REPUTATION
    # ─────────────────────────────────────────
    def _check_abuseipdb(self, ip: str) -> dict | None:
        if not self.abuseipdb_key:
            return None
        try:
            resp = requests.get(
                "https://api.abuseipdb.com/api/v2/check",
                headers={"Key": self.abuseipdb_key, "Accept": "application/json"},
                params={"ipAddress": ip, "maxAgeInDays": 30},
                timeout=5,
            )
            data = resp.json().get("data", {})
            score = data.get("abuseConfidenceScore", 0)
            if score >= 80:
                self._block_ip(ip, "abuseipdb")
                return self._build_block(ip, f"AbuseIPDB score: {score}")
        except Exception as e:
            logger.debug(f"AbuseIPDB check failed: {e}")
        return None

    # ─────────────────────────────────────────
    #  IP MANAGEMENT
    # ─────────────────────────────────────────
    def _block_ip(self, ip: str, reason: str = ""):
        self.blocked_ips.add(ip)
        entry = {"ip": ip, "reason": reason, "timestamp": datetime.utcnow().isoformat()}
        self.threat_log.append(entry)
        logger.warning(f"[DefenseEngine] Blocked {ip} — {reason}")
        self._try_os_block(ip)

    def _try_os_block(self, ip: str):
        """Attempt OS-level firewall block (requires admin/root)."""
        try:
            if shutil.which("iptables"):
                subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
                               capture_output=True, timeout=5)
        except Exception:
            pass

    def unblock_ip(self, ip: str):
        self.blocked_ips.discard(ip)
        logger.info(f"Unblocked: {ip}")

    def whitelist_ip(self, ip: str):
        self.whitelist_ips.add(ip)

    def _build_block(self, ip: str, reason: str) -> dict:
        return {
            "action": "BLOCK",
            "ip": ip,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
        }

    # ─────────────────────────────────────────
    #  CLOUDFLARE INTEGRATION
    # ─────────────────────────────────────────
    def cloudflare_block_ip(self, zone_id: str, ip: str) -> dict:
        """Push block rule to Cloudflare WAF for a given zone."""
        if not self.cloudflare_token:
            return {"status": "error", "message": "CLOUDFLARE_API_TOKEN not set"}
        try:
            resp = requests.post(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/access_rules/rules",
                headers={
                    "Authorization": f"Bearer {self.cloudflare_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "mode": "block",
                    "configuration": {"target": "ip", "value": ip},
                    "notes": f"DAVID CIS auto-block {datetime.utcnow().isoformat()}",
                },
                timeout=8,
            )
            return resp.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def cloudflare_get_zones(self) -> list:
        """Auto-discover all Cloudflare zones for this account."""
        if not self.cloudflare_token:
            return []
        try:
            resp = requests.get(
                "https://api.cloudflare.com/client/v4/zones",
                headers={"Authorization": f"Bearer {self.cloudflare_token}"},
                timeout=8,
            )
            return resp.json().get("result", [])
        except Exception:
            return []

    # ─────────────────────────────────────────
    #  PERSISTENCE
    # ─────────────────────────────────────────
    def _load_saved_blocklist(self):
        path = os.path.join("data", "blocked_ips.json")
        if os.path.exists(path):
            try:
                with open(path) as f:
                    self.blocked_ips = set(json.load(f))
            except Exception:
                pass

    def save_blocklist(self):
        os.makedirs("data", exist_ok=True)
        with open(os.path.join("data", "blocked_ips.json"), "w") as f:
            json.dump(list(self.blocked_ips), f)

    def status(self) -> dict:
        return {
            "status": "ok",
            "blocked_ips_count": len(self.blocked_ips),
            "blocked_ips": list(self.blocked_ips)[:50],
            "total_threats_blocked": len(self.threat_log),
            "recent_alerts": self.threat_log[-20:],
            "rate_limit_rpm": self.rate_limit,
            "geo_blocked_countries": self.geo_block_countries,
        }
