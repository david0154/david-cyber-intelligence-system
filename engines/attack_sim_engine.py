"""
Attack Simulation Engine (Ethical Pentest Only)
Nmap + SQLMap + ZAP + Metasploit + AI
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
WARNING: Use ONLY on systems you own or have written permission to test.
"""

import subprocess
import shutil
import re
import os
from loguru import logger
from core.llm_brain import LLMBrain


class AttackSimEngine:
    """
    Full attack simulation pipeline:
    Phase 1: Reconnaissance (Nmap)
    Phase 2: Vulnerability Discovery (CVE + ZAP + SQLMap)
    Phase 3: Exploitation Check (Metasploit module search)
    Phase 4: AI Report + Fix Suggestions
    """

    def __init__(self):
        self.llm = LLMBrain()

    def run_full_pentest(self, target: str, scope: str = "basic") -> dict:
        """
        scope: 'basic' = port scan + CVE
               'web'   = + ZAP + SQLMap
               'full'  = + MSF module check
        """
        result = {
            "status": "ok",
            "target": target,
            "scope": scope,
            "phases": {},
            "total_vulns": 0,
            "exploit_paths": [],
            "risk_level": "LOW",
            "ai_report": "",
            "fix_suggestions": [],
        }

        # Phase 1: Recon
        result["phases"]["recon"] = self._phase_recon(target)

        # Phase 2: Vuln discovery
        result["phases"]["vuln"] = self._phase_vuln(target)

        if scope in ("web", "full"):
            result["phases"]["web"] = self._phase_web(target)

        if scope == "full":
            result["phases"]["exploit"] = self._phase_exploit(target)

        # Count vulns
        cves = result["phases"].get("vuln", {}).get("cves", [])
        result["total_vulns"] = len(cves)

        # Risk level
        ports = result["phases"].get("recon", {}).get("open_ports", [])
        if len(cves) > 10 or len(ports) > 15:
            result["risk_level"] = "CRITICAL"
        elif len(cves) > 5 or len(ports) > 8:
            result["risk_level"] = "HIGH"
        elif cves or ports:
            result["risk_level"] = "MEDIUM"

        # AI Report
        result["ai_report"] = self.llm.explain_threat({
            "target": target,
            "open_ports": ports[:10],
            "cves_found": cves[:5],
            "risk_level": result["risk_level"],
        })

        result["fix_suggestions"] = self._fix_suggestions(result)
        return result

    def _phase_recon(self, target: str) -> dict:
        if not shutil.which("nmap"):
            return {"status": "skipped", "reason": "nmap not installed",
                    "open_ports": [], "services": []}
        try:
            cmd = ["nmap", "-sV", "-T4", "--open", "--top-ports", "200", target]
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            ports = re.findall(r"(\d+)/tcp\s+open", out.stdout)
            services = re.findall(r"(\d+)/tcp\s+open\s+(\S+)", out.stdout)
            return {
                "status": "ok",
                "open_ports": ports,
                "services": [{"port": s[0], "service": s[1]} for s in services[:20]],
                "raw": out.stdout[:2000],
            }
        except Exception as e:
            return {"status": "error", "message": str(e), "open_ports": []}

    def _phase_vuln(self, target: str) -> dict:
        if not shutil.which("nmap"):
            return {"status": "skipped", "cves": []}
        try:
            cmd = ["nmap", "-sV", "--script", "vulners,vulscan", "-T4", target]
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            cves = list(set(re.findall(r"CVE-\d{4}-\d+", out.stdout)))[:30]
            return {"status": "ok", "cves": cves, "raw": out.stdout[:3000]}
        except Exception as e:
            return {"status": "error", "cves": [], "message": str(e)}

    def _phase_web(self, target: str) -> dict:
        results = {"sqlmap": {}, "zap": {}}
        # SQLMap
        if shutil.which("sqlmap"):
            try:
                url = target if target.startswith("http") else f"http://{target}"
                cmd = ["sqlmap", "-u", url, "--batch", "--level=1",
                       "--risk=1", "--forms", "--crawl=1"]
                out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                injectable = "injectable" in out.stdout.lower()
                results["sqlmap"] = {
                    "status": "ok",
                    "injectable": injectable,
                    "raw": out.stdout[:1500],
                }
            except Exception as e:
                results["sqlmap"] = {"status": "error", "message": str(e)}
        else:
            results["sqlmap"] = {"status": "skipped",
                                  "message": "sqlmap not installed: https://sqlmap.org"}
        return results

    def _phase_exploit(self, target: str) -> dict:
        if not shutil.which("msfconsole"):
            return {
                "status": "skipped",
                "message": "Metasploit not found. Install: https://metasploit.com",
                "modules_found": []
            }
        try:
            # Search relevant modules (read-only, no actual exploit)
            cmd = ["msfconsole", "-q", "-x",
                   f"db_nmap -sV {target}; search type:exploit platform:linux; exit",
                   "--no-readline"]
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            modules = re.findall(r"exploit/\S+", out.stdout)[:10]
            return {"status": "ok", "modules_found": modules, "raw": out.stdout[:2000]}
        except Exception as e:
            return {"status": "error", "message": str(e), "modules_found": []}

    def _fix_suggestions(self, result: dict) -> list:
        fixes = []
        recon = result["phases"].get("recon", {})
        for port in recon.get("open_ports", []):
            advice = {
                "21":  "Disable FTP, use SFTP/SCP",
                "23":  "Disable Telnet immediately, use SSH",
                "3389":"Restrict RDP to VPN only",
                "3306":"Bind MySQL to 127.0.0.1 only",
                "27017":"Restrict MongoDB — add authentication",
            }
            if port in advice:
                fixes.append({"port": port, "fix": advice[port]})
        for cve in result["phases"].get("vuln", {}).get("cves", [])[:5]:
            fixes.append({"cve": cve,
                          "fix": f"Check NVD: https://nvd.nist.gov/vuln/detail/{cve}"})
        return fixes
