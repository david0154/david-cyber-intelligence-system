"""
Phishing Detection — DQN Model
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import re
import numpy as np
from loguru import logger


SUSPICIOUS_PATTERNS = [
    r"paypa[l1]", r"[a@]mazon", r"secure.*login", r"verify.*account",
    r"bank.*update", r"click.*here", r"limited.*offer", r".tk$", r".ml$"
]


class PhishingDQN:
    """
    Lightweight phishing URL/content detector.
    Uses rule-based heuristics + optional DQN model.
    """

    def __init__(self):
        self.model = None

    def predict(self, url: str) -> dict:
        score = 0
        matched = []
        url_lower = url.lower()
        for pat in SUSPICIOUS_PATTERNS:
            if re.search(pat, url_lower):
                score += 15
                matched.append(pat)

        # Length heuristic
        if len(url) > 100:
            score += 10
            matched.append("long_url")

        # IP in URL
        if re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url):
            score += 20
            matched.append("ip_in_url")

        verdict = "PHISHING" if score >= 30 else "SUSPICIOUS" if score >= 15 else "SAFE"
        return {
            "url": url,
            "score": min(score, 100),
            "verdict": verdict,
            "matched_patterns": matched,
        }
