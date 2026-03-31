"""
CAI Engine — Full Cybersecurity AI Pipeline
Dual mode: Offensive recon + Defensive hardening auditor
SSL inspector + HTTP security-header checker + LLM recommendations
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import os
import re
import ssl
import json
import socket
import subprocess
import shutil
import requests
from datetime import datetime
from loguru import logger


class CAIEngine:
    """
    Cybersecurity AI (CAI) Engine — dual-mode pipeline.

    mode='offensive'  →  Nmap recon → Vulners CVE scan → Web check → LLM report
    mode='defensive'  →  Port audit → SSL certificate inspect → HTTP security
                          header check → LLM hardening recommendations
    """

    # Security headers that MUST be present on any hardened server
    REQUIRED_HEADERS = [
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Content-Security-Policy",
        "Referrer-Policy",
        "Permissions-Policy",
        "X-XSS-Protection",
    ]

    # Port-specific risk advisories used in offensive mode
    PORT_RISK = {
        21:    "FTP — plaintext, anonymous login risk",
        22:    "SSH — brute-force vector; ensure key-based auth",
        23:    "Telnet — plaintext protocol; replace with SSH immediately",
        25:    "SMTP — open relay abuse risk",
        53:    "DNS — zone-transfer or amplification attack surface",
        80:    "HTTP — no TLS; upgrade to HTTPS",
        110:   "POP3 — plaintext email",
        143:   "IMAP — plaintext email",
        445:   "SMB — EternalBlue / ransomware vector",
        1433:  "MSSQL — exposed database",
        3306:  "MySQL — restrict to localhost",
        3389:  "RDP — BlueKeep / brute-force; enable NLA + VPN",
        5432:  "PostgreSQL — restrict to localhost",
        5900:  "VNC — no-auth / weak password risk",
        6379:  "Redis — unauthenticated access; bind to 127.0.0.1",
        8080:  "HTTP alt — check for exposed admin panels",
        27017: "MongoDB — unauthenticated access; restrict binding",
    }

    def __init__(self):
        try:
            from core.llm_brain import LLMBrain
            self.llm = LLMBrain()
        except Exception as e:
            self.llm = None
            logger.warning(f"LLM unavailable: {e}")
        logger.success("CAIEngine ready.")

    # ─────────────────────────────────────────────────
    #  MAIN ENTRY POINT
    # ─────────────────────────────────────────────────
    def run_pipeline(self, target: str, mode: str = "defensive") -> dict:
        """
        Run full AI security pipeline.
        mode: 'offensive' or 'defensive'
        """
        logger.info(f"[CAIEngine] Starting {mode} pipeline on {target}")
        result = {
            "status": "ok",
            "target": target,
            "mode": mode,
            "timestamp": datetime.utcnow().isoformat(),
            "steps": [],
            "risk_level": "UNKNOWN",
            "ai_analysis": "",
            "recommendations": [],
        }

        if mode == "offensive":
            result["steps"] = self._offensive_pipeline(target)
        else:
            result["steps"] = self._defensive_pipeline(target)

        result["risk_level"] = self._assess_risk(result["steps"])
        result["ai_analysis"] = self._llm_summary(result)
        result["recommendations"] = self._generate_recommendations(result["steps"])

        logger.success(f"[CAIEngine] Done — risk: {result['risk_level']}")
        return result

    # ─────────────────────────────────────────────────
    #  OFFENSIVE PIPELINE
    # ─────────────────────────────────────────────────
    def _offensive_pipeline(self, target: str) -> list:
        steps = []

        # Step 1 — Nmap recon
        logger.info("[CAI-Offensive] Step 1: Nmap recon")
        nmap_result = self._run_nmap_recon(target)
        steps.append({"step": "nmap_recon", "tool": "nmap",
                       "result": nmap_result})

        # Step 2 — Vulners CVE scan
        logger.info("[CAI-Offensive] Step 2: Vulners CVE scan")
        vuln_result = self._run_vulners(target)
        steps.append({"step": "cve_scan", "tool": "nmap_vulners",
                       "result": vuln_result})

        # Step 3 — Web check
        logger.info("[CAI-Offensive] Step 3: Web check")
        web_result = self._check_web(target)
        steps.append({"step": "web_check", "tool": "requests",
                       "result": web_result})

        # Step 4 — AbuseIPDB reputation
        logger.info("[CAI-Offensive] Step 4: IP reputation")
        rep_result = self._ip_reputation(target)
        steps.append({"step": "ip_reputation", "tool": "abuseipdb",
                       "result": rep_result})

        return steps

    # ─────────────────────────────────────────────────
    #  DEFENSIVE PIPELINE
    # ─────────────────────────────────────────────────
    def _defensive_pipeline(self, target: str) -> list:
        steps = []

        # Step 1 — Port audit
        logger.info("[CAI-Defensive] Step 1: Port audit")
        port_result = self._run_nmap_recon(target)
        steps.append({"step": "port_audit", "tool": "nmap",
                       "result": port_result})

        # Step 2 — SSL certificate inspection
        logger.info("[CAI-Defensive] Step 2: SSL certificate")
        ssl_result = self._check_ssl(target)
        steps.append({"step": "ssl_check", "tool": "ssl_socket",
                       "result": ssl_result})

        # Step 3 — HTTP security headers
        logger.info("[CAI-Defensive] Step 3: HTTP security headers")
        header_result = self._check_headers(target)
        steps.append({"step": "header_audit", "tool": "http_headers",
                       "result": header_result})

        # Step 4 — TLS version check
        logger.info("[CAI-Defensive] Step 4: TLS version")
        tls_result = self._check_tls_version(target)
        steps.append({"step": "tls_version", "tool": "openssl",
                       "result": tls_result})

        # Step 5 — Open dangerous ports
        logger.info("[CAI-Defensive] Step 5: Dangerous port check")
        dangerous = self._check_dangerous_ports(port_result)
        steps.append({"step": "dangerous_ports", "tool": "analysis",
                       "result": dangerous})

        return steps

    # ─────────────────────────────────────────────────
    #  NMAP RECON
    # ─────────────────────────────────────────────────
    def _run_nmap_recon(self, target: str) -> dict:
        if not shutil.which("nmap"):
            return {"status": "error",
                    "message": "nmap not installed — https://nmap.org"}
        try:
            cmd = ["nmap", "-sV", "-sC", "-T4", "--open",
                   "--top-ports", "100", target]
            out = subprocess.run(cmd, capture_output=True,
                                 text=True, timeout=120)
            raw = out.stdout
            # Parse open ports
            ports = re.findall(r"(\d+)/tcp\s+open\s+(\S+)", raw)
            open_ports = [int(p[0]) for p in ports]
            cves = re.findall(r"CVE-\d{4}-\d{4,7}", raw)
            return {
                "status": "ok",
                "open_ports": open_ports,
                "services": [{"port": p[0], "service": p[1]} for p in ports],
                "cves_found": list(set(cves))[:20],
                "raw": raw[:3000],
            }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "message": "nmap timed out"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────────────
    #  VULNERS CVE SCAN
    # ─────────────────────────────────────────────────
    def _run_vulners(self, target: str) -> dict:
        if not shutil.which("nmap"):
            return {"status": "error",
                    "message": "nmap not installed"}
        try:
            cmd = ["nmap", "-sV", "--script", "vulners",
                   "-T4", "--top-ports", "50", target]
            out = subprocess.run(cmd, capture_output=True,
                                 text=True, timeout=120)
            raw = out.stdout
            cves = list(set(re.findall(r"CVE-\d{4}-\d{4,7}", raw)))
            cve_details = [
                {"cve": c,
                 "nvd": f"https://nvd.nist.gov/vuln/detail/{c}"}
                for c in cves[:20]
            ]
            return {
                "status": "ok",
                "cves": cve_details,
                "cve_count": len(cve_details),
                "raw": raw[:2000],
            }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "message": "vulners scan timed out"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────────────
    #  WEB CHECK
    # ─────────────────────────────────────────────────
    def _check_web(self, target: str) -> dict:
        url = target if target.startswith("http") else f"http://{target}"
        try:
            r = requests.get(url, timeout=8, allow_redirects=True)
            return {
                "status": "ok",
                "http_status": r.status_code,
                "server": r.headers.get("Server", "unknown"),
                "x_powered_by": r.headers.get("X-Powered-By", "not set"),
                "redirect_url": r.url if r.url != url else None,
                "content_length": len(r.content),
            }
        except requests.exceptions.ConnectionError:
            return {"status": "unreachable",
                    "message": f"{url} is not reachable"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────────────
    #  SSL CERTIFICATE INSPECTOR
    # ─────────────────────────────────────────────────
    def _check_ssl(self, target: str) -> dict:
        """
        Full SSL certificate inspection:
        - Validity dates
        - Issuer and subject
        - SANs
        - Self-signed detection
        - Days until expiry
        """
        hostname = target.replace("https://", "").replace("http://", "").split("/")[0]
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(
                socket.create_connection((hostname, 443), timeout=10),
                server_hostname=hostname,
            ) as s:
                cert = s.getpeercert()

            # Parse expiry
            not_after_str = cert.get("notAfter", "")
            not_before_str = cert.get("notBefore", "")
            expiry = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z") \
                     if not_after_str else None
            days_left = (expiry - datetime.utcnow()).days if expiry else None

            # Subject / issuer
            subject  = dict(x[0] for x in cert.get("subject", []))
            issuer   = dict(x[0] for x in cert.get("issuer", []))
            san_list = [
                v for _, v in cert.get("subjectAltName", [])
            ]

            self_signed = subject.get("organizationName") == \
                          issuer.get("organizationName")

            return {
                "status": "ok",
                "valid": True,
                "subject": subject,
                "issuer": issuer,
                "not_before": not_before_str,
                "not_after": not_after_str,
                "days_until_expiry": days_left,
                "san": san_list,
                "self_signed": self_signed,
                "warning": "Certificate expires soon!" if days_left and days_left < 30 else None,
            }
        except ssl.SSLCertVerificationError as e:
            return {"status": "invalid", "valid": False,
                    "error": f"SSL verification failed: {e}"}
        except ConnectionRefusedError:
            return {"status": "no_ssl",
                    "message": f"{hostname}:443 refused — HTTPS not available"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────────────
    #  HTTP SECURITY HEADER AUDITOR
    # ─────────────────────────────────────────────────
    def _check_headers(self, target: str) -> dict:
        """
        Audits all critical HTTP security headers:
        Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options,
        Content-Security-Policy, Referrer-Policy, Permissions-Policy,
        X-XSS-Protection.
        Returns present values, missing list, and per-header advice.
        """
        url = target if target.startswith("http") else f"https://{target}"
        try:
            r = requests.get(url, timeout=8, allow_redirects=True)
        except Exception as e:
            return {"status": "error", "message": str(e)}

        header_advice = {
            "Strict-Transport-Security":  "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload",
            "X-Frame-Options":            "Add: X-Frame-Options: DENY  (prevents clickjacking)",
            "X-Content-Type-Options":     "Add: X-Content-Type-Options: nosniff",
            "Content-Security-Policy":    "Add a strict Content-Security-Policy to prevent XSS",
            "Referrer-Policy":            "Add: Referrer-Policy: strict-origin-when-cross-origin",
            "Permissions-Policy":         "Add: Permissions-Policy: geolocation=(), microphone=()",
            "X-XSS-Protection":           "Add: X-XSS-Protection: 1; mode=block",
        }

        present = {}
        missing = []
        advice  = []

        for h in self.REQUIRED_HEADERS:
            val = r.headers.get(h)
            if val:
                present[h] = val
            else:
                missing.append(h)
                advice.append(header_advice.get(h, f"Add {h}"))

        score = int((len(present) / len(self.REQUIRED_HEADERS)) * 100)
        grade = (
            "A" if score >= 90 else
            "B" if score >= 70 else
            "C" if score >= 50 else
            "D" if score >= 30 else
            "F"
        )

        return {
            "status": "ok",
            "url": r.url,
            "http_status": r.status_code,
            "present": present,
            "missing": missing,
            "advice": advice,
            "score": score,
            "grade": grade,
            "total_checked": len(self.REQUIRED_HEADERS),
            "present_count": len(present),
            "missing_count": len(missing),
        }

    # ─────────────────────────────────────────────────
    #  TLS VERSION CHECK
    # ─────────────────────────────────────────────────
    def _check_tls_version(self, target: str) -> dict:
        hostname = target.replace("https://", "").replace("http://", "").split("/")[0]
        tls_results = {}
        for proto, const in [
            ("TLSv1.0",  ssl.TLSVersion.TLSv1   if hasattr(ssl.TLSVersion, "TLSv1")   else None),
            ("TLSv1.1",  ssl.TLSVersion.TLSv1_1 if hasattr(ssl.TLSVersion, "TLSv1_1") else None),
            ("TLSv1.2",  ssl.TLSVersion.TLSv1_2),
            ("TLSv1.3",  ssl.TLSVersion.TLSv1_3 if hasattr(ssl.TLSVersion, "TLSv1_3") else None),
        ]:
            if const is None:
                continue
            try:
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.minimum_version = const
                ctx.maximum_version = const
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                with ctx.wrap_socket(
                    socket.create_connection((hostname, 443), timeout=5),
                    server_hostname=hostname,
                ):
                    tls_results[proto] = "SUPPORTED"
            except Exception:
                tls_results[proto] = "NOT_SUPPORTED"

        deprecated = [p for p, v in tls_results.items()
                      if v == "SUPPORTED" and p in ("TLSv1.0", "TLSv1.1")]
        return {
            "status": "ok",
            "tls_support": tls_results,
            "deprecated_enabled": deprecated,
            "warning": f"Disable deprecated TLS: {deprecated}" if deprecated else None,
        }

    # ─────────────────────────────────────────────────
    #  IP REPUTATION
    # ─────────────────────────────────────────────────
    def _ip_reputation(self, target: str) -> dict:
        abuseipdb_key = os.getenv("ABUSEIPDB_API_KEY", "")
        otx_key       = os.getenv("OTX_API_KEY", "")
        result = {"target": target}

        if abuseipdb_key:
            try:
                r = requests.get(
                    "https://api.abuseipdb.com/api/v2/check",
                    headers={"Key": abuseipdb_key, "Accept": "application/json"},
                    params={"ipAddress": target, "maxAgeInDays": 30},
                    timeout=8,
                )
                d = r.json().get("data", {})
                result["abuseipdb_score"] = d.get("abuseConfidenceScore", 0)
                result["total_reports"]   = d.get("totalReports", 0)
            except Exception as e:
                result["abuseipdb_error"] = str(e)
        else:
            result["abuseipdb"] = "ABUSEIPDB_API_KEY not set"

        if otx_key:
            try:
                r = requests.get(
                    f"https://otx.alienvault.com/api/v1/indicators/IPv4/{target}/general",
                    headers={"X-OTX-API-KEY": otx_key},
                    timeout=8,
                )
                d = r.json()
                result["otx_pulse_count"] = d.get("pulse_info", {}).get("count", 0)
            except Exception as e:
                result["otx_error"] = str(e)
        else:
            result["otx"] = "OTX_API_KEY not set"

        return result

    # ─────────────────────────────────────────────────
    #  DANGEROUS PORT ANALYSIS
    # ─────────────────────────────────────────────────
    def _check_dangerous_ports(self, nmap_result: dict) -> dict:
        open_ports = nmap_result.get("open_ports", [])
        findings = []
        for port in open_ports:
            if port in self.PORT_RISK:
                findings.append({
                    "port": port,
                    "risk": self.PORT_RISK[port],
                    "severity": "HIGH" if port in (23, 3389, 445, 6379, 27017)
                                else "MEDIUM",
                })
        return {
            "status": "ok",
            "total_open": len(open_ports),
            "dangerous_count": len(findings),
            "findings": findings,
        }

    # ─────────────────────────────────────────────────
    #  RISK ASSESSMENT
    # ─────────────────────────────────────────────────
    def _assess_risk(self, steps: list) -> str:
        score = 0
        for step in steps:
            r = step.get("result", {})
            if isinstance(r, dict):
                score += len(r.get("cves", [])) * 10
                score += len(r.get("cves_found", [])) * 10
                score += len(r.get("missing", [])) * 5
                score += len(r.get("deprecated_enabled", [])) * 15
                score += len(r.get("findings", [])) * 8
                abuse = r.get("abuseipdb_score", 0) or 0
                score += min(int(abuse), 20)
        if score >= 80: return "CRITICAL"
        if score >= 50: return "HIGH"
        if score >= 25: return "MEDIUM"
        if score > 0:   return "LOW"
        return "CLEAN"

    # ─────────────────────────────────────────────────
    #  LLM SUMMARY
    # ─────────────────────────────────────────────────
    def _llm_summary(self, result: dict) -> str:
        if not self.llm:
            return "LLM unavailable — install ctransformers and download mixtral.gguf"
        try:
            snippet = json.dumps({
                "target":     result["target"],
                "mode":       result["mode"],
                "risk":       result["risk_level"],
                "step_names": [s["step"] for s in result["steps"]],
                "summary": [
                    {
                        "step": s["step"],
                        "missing_headers": s["result"].get("missing", [])[:5]
                        if isinstance(s["result"], dict) else [],
                        "cves": s["result"].get("cves_found", [])[:5]
                        if isinstance(s["result"], dict) else [],
                    }
                    for s in result["steps"]
                ],
            }, default=str)[:900]
            return self.llm.explain_threat({"cai_pipeline": snippet})
        except Exception as e:
            return f"LLM summary unavailable: {e}"

    # ─────────────────────────────────────────────────
    #  RECOMMENDATION GENERATOR
    # ─────────────────────────────────────────────────
    def _generate_recommendations(self, steps: list) -> list:
        recs = []
        for step in steps:
            r = step.get("result", {})
            if not isinstance(r, dict):
                continue

            # Header recommendations
            for adv in r.get("advice", []):
                recs.append({"type": "header",    "advice": adv})

            # CVE recommendations
            for cve in r.get("cves", [])[:10]:
                c = cve if isinstance(cve, str) else cve.get("cve", "")
                recs.append({"type": "cve",
                             "advice": f"Patch {c} — https://nvd.nist.gov/vuln/detail/{c}"})
            for c in r.get("cves_found", [])[:10]:
                recs.append({"type": "cve",
                             "advice": f"Patch {c} — https://nvd.nist.gov/vuln/detail/{c}"})

            # SSL warnings
            if r.get("warning"):
                recs.append({"type": "ssl", "advice": r["warning"]})

            # TLS deprecated
            for dep in r.get("deprecated_enabled", []):
                recs.append({"type": "tls",
                             "advice": f"Disable {dep} on your server — use TLS 1.2+ only"})

            # Dangerous ports
            for f in r.get("findings", []):
                recs.append({"type": "port",
                             "severity": f.get("severity", "MEDIUM"),
                             "advice": f"Port {f['port']}: {f['risk']}"})

        return recs if recs else [{"type": "info",
                                   "advice": "No critical issues detected."}]
