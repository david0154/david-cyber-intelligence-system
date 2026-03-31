"""
OSINT Engine — Full Implementation
Shodan + theHarvester + SpiderFoot + WHOIS + Breach + DNS + NER
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import re
import json
import socket
import subprocess
import shutil
import requests
from datetime import datetime
from loguru import logger


class OSINTEngine:
    """
    Full OSINT investigation: IP, domain, email, username, phone.
    Aggregates Shodan, geolocation, WHOIS, DNS, breach checks,
    theHarvester, AbuseIPDB, OTX feeds, and NER extraction.
    """

    def __init__(self):
        self.shodan_key       = os.getenv("SHODAN_API_KEY", "")
        self.hibp_key         = os.getenv("HIBP_API_KEY", "")
        self.sectrails_key    = os.getenv("SECURITYTRAILS_KEY", "")
        self.abuseipdb_key    = os.getenv("ABUSEIPDB_API_KEY", "")
        self.otx_key          = os.getenv("OTX_API_KEY", "")
        self.virustotal_key   = os.getenv("VIRUSTOTAL_API_KEY", "")

    # ─────────────────────────────────────────
    #  MAIN INVESTIGATE
    # ─────────────────────────────────────────
    def investigate(self, target: str) -> dict:
        result = {
            "status": "ok",
            "target": target,
            "type": self._detect_type(target),
            "timestamp": datetime.utcnow().isoformat(),
            "geolocation": {},
            "shodan": {},
            "whois": {},
            "dns": {},
            "breach": {},
            "abuseipdb": {},
            "otx": {},
            "virustotal": {},
            "harvester": {},
            "reverse_dns": "",
            "entities": [],
            "risk": "UNKNOWN",
            "summary": "",
        }

        t = result["type"]

        if t in ("ip", "domain"):
            result["geolocation"]  = self._geolocate(target)
            result["shodan"]       = self._shodan_lookup(target)
            result["abuseipdb"]    = self._abuseipdb(target)
            result["otx"]          = self._otx_lookup(target)
            result["dns"]          = self._dns_lookup(target)
            result["reverse_dns"]  = self._reverse_dns(target)
            result["virustotal"]   = self._virustotal(target, "ip" if t == "ip" else "domain")

        if t == "domain":
            result["whois"]        = self._whois(target)
            result["harvester"]    = self._run_harvester(target)
            result["sectrails"]    = self._securitytrails(target)

        if t == "email":
            result["breach"]       = self._breach_check(target)

        result["entities"] = self._extract_entities(
            json.dumps(result, default=str)[:6000]
        )
        result["risk"] = self._score_risk(result)
        result["summary"] = self._llm_summary(result)
        return result

    # ─────────────────────────────────────────
    #  TARGET TYPE DETECTION
    # ─────────────────────────────────────────
    def _detect_type(self, target: str) -> str:
        ip_re = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
        email_re = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]+$")
        if ip_re.match(target):    return "ip"
        if email_re.match(target): return "email"
        if "." in target:          return "domain"
        return "username"

    # ─────────────────────────────────────────
    #  GEOLOCATION
    # ─────────────────────────────────────────
    def _geolocate(self, ip: str) -> dict:
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=6)
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    # ─────────────────────────────────────────
    #  SHODAN
    # ─────────────────────────────────────────
    def _shodan_lookup(self, target: str) -> dict:
        if not self.shodan_key:
            return {"message": "SHODAN_API_KEY not set"}
        try:
            import shodan
            api = shodan.Shodan(self.shodan_key)
            host = api.host(target)
            return {
                "ip": host.get("ip_str"),
                "org": host.get("org"),
                "os": host.get("os"),
                "ports": host.get("ports", []),
                "vulns": list(host.get("vulns", [])),
                "hostnames": host.get("hostnames", []),
                "country": host.get("country_name"),
                "tags": host.get("tags", []),
            }
        except ImportError:
            return {"message": "shodan library not installed — pip install shodan"}
        except Exception as e:
            return {"message": str(e)}

    # ─────────────────────────────────────────
    #  DNS
    # ─────────────────────────────────────────
    def _dns_lookup(self, target: str) -> dict:
        records = {}
        try:
            import dns.resolver
            for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]:
                try:
                    answers = dns.resolver.resolve(target, rtype, lifetime=5)
                    records[rtype] = [str(r) for r in answers]
                except Exception:
                    pass
        except ImportError:
            try:
                ip = socket.gethostbyname(target)
                records["A"] = [ip]
            except Exception:
                pass
        return records

    def _reverse_dns(self, ip: str) -> str:
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return ""

    # ─────────────────────────────────────────
    #  WHOIS
    # ─────────────────────────────────────────
    def _whois(self, domain: str) -> dict:
        try:
            import whois
            w = whois.whois(domain)
            return {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "name_servers": w.name_servers,
                "org": w.org,
                "country": w.country,
                "emails": w.emails,
            }
        except ImportError:
            if shutil.which("whois"):
                try:
                    out = subprocess.run(["whois", domain],
                        capture_output=True, text=True, timeout=15)
                    return {"raw": out.stdout[:3000]}
                except Exception:
                    pass
            return {"message": "python-whois not installed — pip install python-whois"}
        except Exception as e:
            return {"message": str(e)}

    # ─────────────────────────────────────────
    #  ABUSEIPDB
    # ─────────────────────────────────────────
    def _abuseipdb(self, ip: str) -> dict:
        if not self.abuseipdb_key:
            return {"message": "ABUSEIPDB_API_KEY not set"}
        try:
            r = requests.get(
                "https://api.abuseipdb.com/api/v2/check",
                headers={"Key": self.abuseipdb_key, "Accept": "application/json"},
                params={"ipAddress": ip, "maxAgeInDays": 90, "verbose": True},
                timeout=8,
            )
            return r.json().get("data", {})
        except Exception as e:
            return {"error": str(e)}

    # ─────────────────────────────────────────
    #  OTX
    # ─────────────────────────────────────────
    def _otx_lookup(self, target: str) -> dict:
        if not self.otx_key:
            return {"message": "OTX_API_KEY not set"}
        try:
            section = "IPv4" if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", target) else "domain"
            url = f"https://otx.alienvault.com/api/v1/indicators/{section}/{target}/general"
            r = requests.get(url, headers={"X-OTX-API-KEY": self.otx_key}, timeout=8)
            d = r.json()
            return {
                "pulse_count": d.get("pulse_info", {}).get("count", 0),
                "reputation": d.get("reputation", 0),
                "country": d.get("country_name"),
                "malware_families": d.get("malware_families", []),
                "tags": [p.get("name") for p in
                         d.get("pulse_info", {}).get("pulses", [])[:5]],
            }
        except Exception as e:
            return {"error": str(e)}

    # ─────────────────────────────────────────
    #  VIRUSTOTAL
    # ─────────────────────────────────────────
    def _virustotal(self, target: str, kind: str) -> dict:
        if not self.virustotal_key:
            return {"message": "VIRUSTOTAL_API_KEY not set"}
        try:
            url = f"https://www.virustotal.com/api/v3/{kind}s/{target}"
            r = requests.get(url,
                headers={"x-apikey": self.virustotal_key}, timeout=8)
            attrs = r.json().get("data", {}).get("attributes", {})
            stats = attrs.get("last_analysis_stats", {})
            return {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "reputation": attrs.get("reputation", 0),
            }
        except Exception as e:
            return {"error": str(e)}

    # ─────────────────────────────────────────
    #  SECURITY TRAILS
    # ─────────────────────────────────────────
    def _securitytrails(self, domain: str) -> dict:
        if not self.sectrails_key:
            return {"message": "SECURITYTRAILS_KEY not set"}
        try:
            r = requests.get(
                f"https://api.securitytrails.com/v1/domain/{domain}",
                headers={"APIKEY": self.sectrails_key},
                timeout=8,
            )
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    # ─────────────────────────────────────────
    #  BREACH CHECK (HIBP)
    # ─────────────────────────────────────────
    def _breach_check(self, email: str) -> dict:
        if not self.hibp_key:
            return {"message": "HIBP_API_KEY not set"}
        try:
            r = requests.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                headers={"hibp-api-key": self.hibp_key, "User-Agent": "DAVID-CIS"},
                timeout=8,
            )
            if r.status_code == 404:
                return {"breached": False, "message": "No breaches found"}
            breaches = r.json()
            return {
                "breached": True,
                "count": len(breaches),
                "breaches": [b.get("Name") for b in breaches],
            }
        except Exception as e:
            return {"error": str(e)}

    # ─────────────────────────────────────────
    #  THE HARVESTER
    # ─────────────────────────────────────────
    def _run_harvester(self, domain: str) -> dict:
        harvester = shutil.which("theHarvester") or shutil.which("theharvester")
        if not harvester:
            return {"message": "theHarvester not installed. pip install theHarvester"}
        try:
            cmd = [harvester, "-d", domain, "-b", "google,bing,yahoo", "-l", "100"]
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            raw = out.stdout
            emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", raw)
            subdomains = re.findall(r"[\w.-]+\." + re.escape(domain), raw)
            return {
                "emails": list(set(emails))[:30],
                "subdomains": list(set(subdomains))[:50],
                "raw": raw[:2000],
            }
        except subprocess.TimeoutExpired:
            return {"message": "theHarvester timed out"}
        except Exception as e:
            return {"message": str(e)}

    # ─────────────────────────────────────────
    #  NER ENTITY EXTRACTION
    # ─────────────────────────────────────────
    def _extract_entities(self, text: str) -> list:
        entities = []
        # Regex-based fallback
        ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
        emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
        cves = re.findall(r"CVE-\d{4}-\d{4,7}", text)
        domains = re.findall(r"\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b", text)
        for ip in set(ips):      entities.append({"text": ip,    "type": "IP"})
        for e in set(emails):    entities.append({"text": e,     "type": "EMAIL"})
        for c in set(cves):      entities.append({"text": c,     "type": "CVE"})
        for d in list(set(domains))[:20]: entities.append({"text": d, "type": "DOMAIN"})
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text[:4000])
            for ent in doc.ents:
                entities.append({"text": ent.text, "type": ent.label_})
        except Exception:
            pass
        return entities[:80]

    # ─────────────────────────────────────────
    #  RISK SCORING
    # ─────────────────────────────────────────
    def _score_risk(self, result: dict) -> str:
        score = 0
        abuse = result.get("abuseipdb", {})
        score += min(int(abuse.get("abuseConfidenceScore", 0)), 50)
        otx = result.get("otx", {})
        score += min(int(otx.get("pulse_count", 0)) * 3, 30)
        vt = result.get("virustotal", {})
        score += min(int(vt.get("malicious", 0)) * 5, 20)
        if score >= 75: return "CRITICAL"
        if score >= 50: return "HIGH"
        if score >= 25: return "MEDIUM"
        if score > 0:   return "LOW"
        return "CLEAN"

    # ─────────────────────────────────────────
    #  LLM SUMMARY
    # ─────────────────────────────────────────
    def _llm_summary(self, result: dict) -> str:
        try:
            from core.llm_brain import LLMBrain
            brain = LLMBrain()
            snippet = json.dumps({
                "target": result["target"],
                "risk": result["risk"],
                "geo": result.get("geolocation", {}).get("country", ""),
                "shodan_ports": result.get("shodan", {}).get("ports", []),
                "shodan_vulns": result.get("shodan", {}).get("vulns", []),
                "abuse_score": result.get("abuseipdb", {}).get("abuseConfidenceScore", 0),
                "otx_pulses": result.get("otx", {}).get("pulse_count", 0),
            }, default=str)[:800]
            return brain.explain_threat({"osint_summary": snippet})
        except Exception as e:
            return f"LLM summary unavailable: {e}"
