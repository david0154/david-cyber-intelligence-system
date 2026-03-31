"""
CAI - Cybersecurity AI Engine
Based on aliasrobotics/cai concepts
AI-driven offensive + defensive automation
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import subprocess
import shutil
from loguru import logger
from core.llm_brain import LLMBrain


class CAIEngine:
    """
    Cybersecurity AI (CAI) Engine:
    - Automated threat detection pipelines
    - AI-driven offensive simulation
    - Defensive recommendation engine
    - LLM-guided attack/defense reasoning
    """

    def __init__(self):
        self.llm = LLMBrain()

    def run_pipeline(self, target: str, mode: str = "defensive") -> dict:
        """
        Run full AI security pipeline.
        mode: 'offensive' (pentest) or 'defensive' (hardening)
        """
        result = {
            "status": "ok",
            "target": target,
            "mode": mode,
            "steps": [],
            "ai_analysis": "",
            "recommendations": [],
        }

        if mode == "offensive":
            result["steps"] = self._offensive_pipeline(target)
        else:
            result["steps"] = self._defensive_pipeline(target)

        # LLM analysis
        result["ai_analysis"] = self.llm.explain_threat({
            "target": target,
            "mode": mode,
            "steps": result["steps"],
        })

        result["recommendations"] = self._generate_recommendations(result["steps"])
        return result

    def _offensive_pipeline(self, target: str) -> list:
        steps = []
        # Step 1: Recon
        steps.append({"step": "recon", "tool": "nmap", "status": self._run_nmap(target)})
        # Step 2: Vulnerability scan
        steps.append({"step": "vuln_scan", "tool": "nmap_vulners", "status": self._run_vulners(target)})
        # Step 3: Web test (if HTTP)
        steps.append({"step": "web_test", "tool": "curl_check", "status": self._check_web(target)})
        return steps

    def _defensive_pipeline(self, target: str) -> list:
        steps = []
        steps.append({"step": "port_audit", "tool": "nmap", "status": self._run_nmap(target)})
        steps.append({"step": "ssl_check", "tool": "curl", "status": self._check_ssl(target)})
        steps.append({"step": "header_check", "tool": "http_headers", "status": self._check_headers(target)})
        return steps

    def _run_nmap(self, target: str) -> str:
        if not shutil.which("nmap"):
            return "nmap not installed"
        try:
            out = subprocess.run(["nmap", "-T4", "--top-ports", "20", target],
                                 capture_output=True, text=True, timeout=30)
            return out.stdout[:500]
        except Exception as e:
            return str(e)

    def _run_vulners(self, target: str) -> str:
        if not shutil.which("nmap"):
            return "nmap not installed"
        try:
            out = subprocess.run(["nmap", "-sV", "--script", "vulners", target],
                                 capture_output=True, text=True, timeout=60)
            return out.stdout[:500]
        except Exception as e:
            return str(e)

    def _check_web(self, target: str) -> str:
        import requests
        try:
            url = target if target.startswith("http") else f"http://{target}"
            r = requests.get(url, timeout=5)
            return f"HTTP {r.status_code}, server: {r.headers.get('Server', 'unknown')}"
        except Exception as e:
            return str(e)

    def _check_ssl(self, target: str) -> str:
        try:
            import ssl, socket
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=target) as s:
                s.connect((target, 443))
                cert = s.getpeercert()
                return f"SSL valid until: {cert.get('notAfter', 'unknown')}"
        except Exception as e:
            return f"SSL check: {e}"

    def _check_headers(self, target: str) -> dict:
        import requests
        try:
            url = target if target.startswith("http") else f"https://{target}"
            r = requests.get(url, timeout=5)
            important = ["Strict-Transport-Security", "X-Frame-Options",
                         "X-Content-Type-Options", "Content-Security-Policy"]
            present = {h: r.headers.get(h, "MISSING") for h in important}
            return present
        except Exception as e:
            return {"error": str(e)}

    def _generate_recommendations(self, steps: list) -> list:
        recs = []
        for step in steps:
            status = str(step.get("status", ""))
            if "open" in status.lower():
                recs.append(f"Close unnecessary ports detected in {step['step']}")
            if "CVE" in status:
                recs.append(f"Patch CVEs found in {step['step']}")
            if "MISSING" in status:
                recs.append(f"Add missing security headers found in {step['step']}")
        return recs or ["No critical issues found."]
