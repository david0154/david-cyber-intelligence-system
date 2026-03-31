"""
CVSS v3.1 Scorer
Auto-scores vulnerabilities based on type and impact
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""


CVSS_BASE = {
    "rce":               {"score": 9.8, "severity": "CRITICAL", "reward": 500},
    "sql_injection":     {"score": 8.5, "severity": "HIGH",     "reward": 300},
    "xss":               {"score": 6.1, "severity": "MEDIUM",   "reward": 150},
    "csrf":              {"score": 5.4, "severity": "MEDIUM",   "reward": 100},
    "idor":              {"score": 7.5, "severity": "HIGH",     "reward": 250},
    "ssrf":              {"score": 8.6, "severity": "HIGH",     "reward": 350},
    "lfi":               {"score": 7.2, "severity": "HIGH",     "reward": 200},
    "rfi":               {"score": 8.0, "severity": "HIGH",     "reward": 300},
    "xxe":               {"score": 7.5, "severity": "HIGH",     "reward": 250},
    "auth_bypass":       {"score": 9.1, "severity": "CRITICAL", "reward": 450},
    "privilege_escalation": {"score": 8.8, "severity": "HIGH", "reward": 400},
    "open_redirect":     {"score": 4.3, "severity": "LOW",      "reward": 50},
    "info_disclosure":   {"score": 5.3, "severity": "MEDIUM",   "reward": 75},
    "broken_auth":       {"score": 7.5, "severity": "HIGH",     "reward": 200},
    "path_traversal":    {"score": 6.5, "severity": "MEDIUM",   "reward": 150},
    "other":             {"score": 3.0, "severity": "LOW",      "reward": 25},
}

VULN_KEYWORDS = {
    "rce":            ["remote code", "rce", "code execution", "command injection"],
    "sql_injection":  ["sql", "injection", "sqli", "union select"],
    "xss":            ["xss", "cross-site scripting", "script injection"],
    "csrf":           ["csrf", "cross-site request"],
    "idor":           ["idor", "insecure direct", "object reference"],
    "ssrf":           ["ssrf", "server-side request"],
    "lfi":            ["lfi", "local file", "path inclusion"],
    "rfi":            ["rfi", "remote file"],
    "xxe":            ["xxe", "xml external"],
    "auth_bypass":    ["auth bypass", "authentication bypass", "bypass login"],
    "privilege_escalation": ["privilege", "escalation", "root access"],
    "open_redirect":  ["open redirect", "url redirect"],
    "info_disclosure":["information disclosure", "sensitive data", "leak"],
    "broken_auth":    ["broken authentication", "session", "token"],
    "path_traversal": ["path traversal", "directory traversal", "../"],
}


class CVSSScorer:
    def classify(self, title: str, description: str) -> dict:
        text = (title + " " + description).lower()
        for vuln_type, keywords in VULN_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                data = CVSS_BASE[vuln_type].copy()
                data["vuln_type"] = vuln_type
                return data
        return {**CVSS_BASE["other"], "vuln_type": "other"}

    def score(self, vuln_type: str) -> dict:
        return CVSS_BASE.get(vuln_type, CVSS_BASE["other"])
