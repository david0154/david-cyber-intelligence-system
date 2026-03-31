"""
SOC / Defensive AI Engine
Real-time Threat Detection + Log Analysis + Anomaly Detection
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import os
import json
import re
from datetime import datetime
from loguru import logger
from core.llm_brain import LLMBrain


class SOCEngine:
    """
    Security Operations Center AI:
    - Log ingestion and analysis
    - Anomaly detection
    - Attack pattern recognition
    - AI-driven threat prediction
    - Auto response recommendations
    """

    ATTACK_PATTERNS = {
        "brute_force": r"(failed password|authentication failure|invalid user)",
        "sql_injection": r"(union select|or 1=1|drop table|' or '|xp_cmdshell)",
        "xss": r"(<script|javascript:|onerror=|onload=)",
        "path_traversal": r"(\.\./|\.\\|%2e%2e)",
        "port_scan": r"(nmap|masscan|zmap|syn flood)",
        "ddos": r"(flood|dos attack|high request rate)",
        "malware": r"(trojan|ransomware|backdoor|rootkit|exploit)",
        "privilege_escalation": r"(sudo|su root|privilege|escalat)",
    }

    def __init__(self):
        self.llm = LLMBrain()
        self.event_log = []
        self.blocked_ips = set()
        self.alert_thresholds = {"brute_force": 5, "port_scan": 10, "ddos": 100}
        self.ip_counters = {}

    def analyze_log(self, log_text: str, source: str = "system") -> dict:
        """
        Analyze raw log text for threats.
        """
        result = {
            "status": "ok",
            "source": source,
            "timestamp": datetime.utcnow().isoformat(),
            "lines_analyzed": len(log_text.splitlines()),
            "threats_found": [],
            "blocked_ips": [],
            "risk_level": "LOW",
            "ai_analysis": "",
            "recommended_actions": [],
        }

        threats = self._detect_patterns(log_text)
        result["threats_found"] = threats

        ips = self._extract_ips(log_text)
        suspicious = self._score_ips(ips, threats)
        result["suspicious_ips"] = suspicious

        for ip_info in suspicious:
            if ip_info["score"] >= 10:
                self.blocked_ips.add(ip_info["ip"])
                result["blocked_ips"].append(ip_info["ip"])

        result["risk_level"] = self._calc_risk_level(threats)

        if threats:
            result["ai_analysis"] = self.llm.explain_threat({
                "log_source": source,
                "threats": [t["type"] for t in threats[:5]],
                "suspicious_ips": [i["ip"] for i in suspicious[:3]],
            })
            result["recommended_actions"] = self._get_actions(threats)

        self.event_log.append(result)
        return result

    def analyze_log_file(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}
        try:
            with open(file_path, "r", errors="ignore") as f:
                content = f.read()
            return self.analyze_log(content, source=file_path)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _detect_patterns(self, text: str) -> list:
        found = []
        text_lower = text.lower()
        for attack_type, pattern in self.ATTACK_PATTERNS.items():
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                found.append({
                    "type": attack_type,
                    "count": len(matches),
                    "sample": matches[0] if matches else "",
                    "severity": self._get_severity(attack_type),
                })
        return found

    def _extract_ips(self, text: str) -> list:
        return list(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)))

    def _score_ips(self, ips: list, threats: list) -> list:
        result = []
        threat_types = [t["type"] for t in threats]
        for ip in ips[:50]:
            score = 0
            if "brute_force" in threat_types: score += 5
            if "port_scan" in threat_types: score += 7
            if "sql_injection" in threat_types: score += 10
            if ip in self.blocked_ips: score += 15
            if score > 0:
                result.append({"ip": ip, "score": score,
                                "flagged": ip in self.blocked_ips})
        return sorted(result, key=lambda x: x["score"], reverse=True)[:20]

    def _get_severity(self, attack_type: str) -> str:
        critical = {"sql_injection", "malware", "privilege_escalation"}
        high = {"brute_force", "port_scan", "ddos"}
        if attack_type in critical: return "CRITICAL"
        if attack_type in high: return "HIGH"
        return "MEDIUM"

    def _calc_risk_level(self, threats: list) -> str:
        if not threats: return "LOW"
        severities = [t["severity"] for t in threats]
        if "CRITICAL" in severities: return "CRITICAL"
        if "HIGH" in severities: return "HIGH"
        return "MEDIUM"

    def _get_actions(self, threats: list) -> list:
        actions = []
        for t in threats:
            action_map = {
                "brute_force": "Enable account lockout after 5 failed attempts. Add CAPTCHA.",
                "sql_injection": "Use parameterized queries. Enable WAF rules.",
                "xss": "Sanitize all user inputs. Add Content-Security-Policy header.",
                "path_traversal": "Validate file paths server-side. Restrict directory access.",
                "port_scan": "Enable firewall rate limiting. Alert on SYN flood.",
                "ddos": "Enable Cloudflare DDoS protection. Rate-limit IPs.",
                "malware": "Isolate affected system. Run malware scan. Check persistence.",
                "privilege_escalation": "Audit sudo rules. Check SUID binaries. Review user roles.",
            }
            if t["type"] in action_map:
                actions.append(action_map[t["type"]])
        return list(set(actions))

    def get_dashboard_data(self) -> dict:
        total_events = len(self.event_log)
        all_threats = []
        for evt in self.event_log:
            all_threats.extend(evt.get("threats_found", []))
        return {
            "total_events_analyzed": total_events,
            "total_threats": len(all_threats),
            "blocked_ips": list(self.blocked_ips),
            "threat_types": list({t["type"] for t in all_threats}),
            "recent_events": self.event_log[-5:],
        }
