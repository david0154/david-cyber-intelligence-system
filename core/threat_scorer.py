"""
Unified Threat Scoring System
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""


class ThreatScorer:
    """
    Combines scores from all engines into a unified threat score.
    Threat Score = Malware + Network + OSINT + Intel Match
    """

    THRESHOLDS = {
        "LOW": (0, 25),
        "MEDIUM": (26, 50),
        "HIGH": (51, 75),
        "CRITICAL": (76, 100),
    }

    def __init__(self):
        self.scores = {
            "malware": 0,
            "network": 0,
            "osint": 0,
            "intel": 0,
        }

    def update(self, module: str, score: float):
        """Update individual module score (0-25 each)."""
        if module in self.scores:
            self.scores[module] = max(0, min(25, score))

    def total(self) -> float:
        return sum(self.scores.values())

    def level(self) -> str:
        total = self.total()
        for level, (low, high) in self.THRESHOLDS.items():
            if low <= total <= high:
                return level
        return "UNKNOWN"

    def report(self) -> dict:
        total = self.total()
        return {
            "scores": self.scores,
            "total_score": total,
            "threat_level": self.level(),
            "breakdown": {
                k: f"{v}/25" for k, v in self.scores.items()
            }
        }

    def reset(self):
        for k in self.scores:
            self.scores[k] = 0
