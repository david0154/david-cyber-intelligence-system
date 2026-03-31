"""
Defense Engine
Open-AppSec + ML WAF + Auto Blocking
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import os
import json
from datetime import datetime
from loguru import logger


class DefenseEngine:
    """
    Active defense: WAF-like filtering, IP blocking, threat logging.
    """

    def __init__(self):
        self.blocked_ips = set()
        self.threat_log = []
        self.rules = self._load_rules()

    def _load_rules(self) -> list:
        rules_path = os.path.join("data", "defense_rules.json")
        if os.path.exists(rules_path):
            try:
                with open(rules_path) as f:
                    return json.load(f)
            except Exception:
                pass
        return [
            {"type": "sqli", "pattern": "' OR '"},
            {"type": "xss", "pattern": "<script>"},
            {"type": "cmd", "pattern": "; rm -rf"},
            {"type": "path_traversal", "pattern": "../"},
        ]

    def inspect(self, request_data: str, source_ip: str = "0.0.0.0") -> dict:
        if source_ip in self.blocked_ips:
            return {"action": "BLOCK", "reason": "IP in blocklist", "ip": source_ip}

        for rule in self.rules:
            if rule["pattern"].lower() in request_data.lower():
                self._block_ip(source_ip)
                alert = {
                    "action": "BLOCK",
                    "type": rule["type"],
                    "ip": source_ip,
                    "timestamp": datetime.utcnow().isoformat(),
                    "reason": f"Matched rule: {rule['type']}",
                }
                self.threat_log.append(alert)
                return alert

        return {"action": "ALLOW", "ip": source_ip}

    def _block_ip(self, ip: str):
        self.blocked_ips.add(ip)
        logger.warning(f"Blocked IP: {ip}")

    def status(self) -> dict:
        return {
            "status": "ok",
            "blocked_ips": list(self.blocked_ips),
            "total_threats_blocked": len(self.threat_log),
            "recent_alerts": self.threat_log[-10:],
        }
