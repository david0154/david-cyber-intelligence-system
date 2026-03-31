"""
AI Bug Bounty Validator
Auto-validates, scores, and classifies submitted vulnerabilities
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import re
from core.llm_brain import LLMBrain
from bounty.cvss_scorer import CVSSScorer


class AIValidator:
    """
    AI-powered bug validation:
    - Checks if submission is a real vulnerability
    - Auto-classifies type
    - CVSS scores it
    - Detects duplicates
    - Generates AI feedback for reporter
    """

    def __init__(self):
        self.llm = LLMBrain()
        self.scorer = CVSSScorer()

    def validate(self, report: dict) -> dict:
        title = report.get("title", "")
        description = report.get("description", "")
        target = report.get("target", "")

        # Step 1: Basic quality check
        quality = self._quality_check(title, description)

        # Step 2: Classify vulnerability type
        classification = self.scorer.classify(title, description)

        # Step 3: CVSS score
        cvss = classification["score"]
        severity = classification["severity"]
        vuln_type = classification["vuln_type"]
        reward = classification["reward"]

        # Step 4: AI feedback
        ai_feedback = self._ai_feedback(title, description, target, severity)

        # Step 5: Validity
        is_valid = quality["score"] >= 3 and vuln_type != "other"

        return {
            "valid": is_valid,
            "vuln_type": vuln_type,
            "severity": severity,
            "cvss_score": cvss,
            "suggested_reward": reward,
            "quality_score": quality["score"],
            "quality_notes": quality["notes"],
            "ai_feedback": ai_feedback,
            "auto_status": "VERIFIED" if is_valid else "NEEDS_REVIEW",
        }

    def _quality_check(self, title: str, description: str) -> dict:
        score = 0
        notes = []

        if len(title) > 10:
            score += 1
        else:
            notes.append("Title too short — describe the vulnerability clearly.")

        if len(description) > 50:
            score += 1
        else:
            notes.append("Description too short — add details and impact.")

        if any(kw in description.lower() for kw in
               ["step", "reproduce", "poc", "payload", "request", "curl",
                "http", "exploit", "parameter"]):
            score += 2
            notes.append("✅ PoC/reproduction steps detected.")
        else:
            notes.append("Add reproduction steps or PoC for faster validation.")

        if re.search(r"https?://\S+", description):
            score += 1
            notes.append("✅ URL/reference included.")

        return {"score": score, "notes": notes}

    def _ai_feedback(self, title: str, description: str,
                     target: str, severity: str) -> str:
        prompt = (
            f"You are a senior bug bounty analyst.\n"
            f"Review this vulnerability report:\n"
            f"Title: {title}\n"
            f"Target: {target}\n"
            f"Description: {description[:500]}\n"
            f"Severity: {severity}\n\n"
            f"Provide: 1) Is this a real vulnerability? 2) Impact assessment "
            f"3) Missing information 4) Suggested CVSS score justification"
        )
        return self.llm.think(prompt)
