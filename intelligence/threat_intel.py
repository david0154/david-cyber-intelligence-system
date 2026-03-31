#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM
Threat Intelligence Engine — NO SERVER REQUIRED

Replaces MISP + OpenCTI with FREE public APIs:
  - AlienVault OTX       (free, no credit card)
  - AbuseIPDB            (free, 1000/day)
  - ThreatFox (abuse.ch) (free, no key needed)
  - URLhaus (abuse.ch)   (free, no key needed)
  - VirusTotal           (free, 500/day)
  - MalwareBazaar        (free, no key needed)
  - Shodan               (free tier)
  - Local SQLite cache   (offline, instant)

All results cached locally in data/threat_intel.db
No Docker, no server, no self-hosting required.

Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import json
import sqlite3
import hashlib
import requests
import ipaddress
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger
from typing import Optional

# ── Config
DB_PATH      = Path("data/threat_intel.db")
CACHE_HOURS  = 24        # Re-query after 24h
REQUEST_TO   = 10        # seconds

OTX_KEY      = os.getenv("OTX_API_KEY", "")
ABUSE_KEY    = os.getenv("ABUSEIPDB_API_KEY", "")
VT_KEY       = os.getenv("VIRUSTOTAL_API_KEY", "")
SHODAN_KEY   = os.getenv("SHODAN_API_KEY", "")


# ────────────────────────────────────────────────────────────────────
class LocalThreatDB:
    """SQLite-based local IOC cache. Zero server requirement."""

    def __init__(self, db_path: Path = DB_PATH):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS ioc (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ioc_type    TEXT NOT NULL,   -- ip, domain, hash, url, email
            value       TEXT NOT NULL,
            threat_type TEXT,           -- malware, botnet, phishing, etc.
            confidence  INTEGER DEFAULT 0,
            source      TEXT,           -- otx, abuseipdb, threatfox, etc.
            country     TEXT,
            asn         TEXT,
            tags        TEXT,           -- JSON list
            raw         TEXT,           -- full JSON from source
            first_seen  TEXT,
            last_seen   TEXT,
            created_at  TEXT DEFAULT (datetime('now')),
            UNIQUE(ioc_type, value, source)
        );

        CREATE TABLE IF NOT EXISTS cache (
            key         TEXT PRIMARY KEY,
            result      TEXT NOT NULL,
            expires_at  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS local_events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type  TEXT,
            severity    TEXT,
            source_ip   TEXT,
            details     TEXT,
            created_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_ioc_value ON ioc(value);
        CREATE INDEX IF NOT EXISTS idx_ioc_type  ON ioc(ioc_type);
        """)
        self.conn.commit()

    def store_ioc(self, ioc_type, value, threat_type="",
                  confidence=50, source="manual", country="",
                  asn="", tags=None, raw=None, first_seen="", last_seen=""):
        try:
            self.conn.execute("""
                INSERT OR REPLACE INTO ioc
                (ioc_type, value, threat_type, confidence, source,
                 country, asn, tags, raw, first_seen, last_seen)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                ioc_type, value.lower().strip(), threat_type,
                confidence, source, country, asn,
                json.dumps(tags or []),
                json.dumps(raw) if raw else "",
                first_seen, last_seen
            ))
            self.conn.commit()
        except Exception as e:
            logger.debug(f"store_ioc: {e}")

    def lookup(self, value: str) -> list:
        cur = self.conn.execute(
            "SELECT * FROM ioc WHERE value = ? ORDER BY confidence DESC",
            (value.lower().strip(),)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    def set_cache(self, key: str, result: dict, hours: int = CACHE_HOURS):
        expires = (datetime.utcnow() + timedelta(hours=hours)).isoformat()
        self.conn.execute(
            "INSERT OR REPLACE INTO cache (key, result, expires_at) VALUES (?,?,?)",
            (key, json.dumps(result), expires)
        )
        self.conn.commit()

    def get_cache(self, key: str) -> Optional[dict]:
        cur = self.conn.execute(
            "SELECT result, expires_at FROM cache WHERE key = ?", (key,)
        )
        row = cur.fetchone()
        if row:
            if datetime.utcnow().isoformat() < row[1]:  # not expired
                return json.loads(row[0])
        return None

    def log_event(self, event_type, severity, source_ip="", details=""):
        self.conn.execute(
            "INSERT INTO local_events (event_type, severity, source_ip, details) VALUES (?,?,?,?)",
            (event_type, severity, source_ip, details)
        )
        self.conn.commit()

    def recent_events(self, limit=50) -> list:
        cur = self.conn.execute(
            "SELECT * FROM local_events ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    def stats(self) -> dict:
        c = self.conn.execute("SELECT COUNT(*) FROM ioc").fetchone()[0]
        e = self.conn.execute("SELECT COUNT(*) FROM local_events").fetchone()[0]
        s = self.conn.execute(
            "SELECT source, COUNT(*) as n FROM ioc GROUP BY source"
        ).fetchall()
        return {"total_iocs": c, "total_events": e,
                "by_source": {r[0]: r[1] for r in s}}


# ────────────────────────────────────────────────────────────────────
class ThreatIntelEngine:
    """
    Aggregates threat intel from multiple FREE sources.
    No server, no Docker, no self-hosting required.
    All data cached in local SQLite.
    """

    def __init__(self):
        self.db = LocalThreatDB()
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "DAVID-CIS/1.0"

    # ────────────────────────────────────────────────────────────────
    #  MAIN LOOKUP — call this for any IP/domain/hash/URL
    # ────────────────────────────────────────────────────────────────
    def lookup(self, value: str) -> dict:
        """
        Looks up any IOC: IP, domain, file hash (MD5/SHA256), or URL.
        Returns combined result from all available sources.
        """
        value = value.strip().lower()
        cache_key = f"lookup:{value}"
        cached = self.db.get_cache(cache_key)
        if cached:
            logger.debug(f"[ThreatIntel] Cache hit: {value}")
            return cached

        ioc_type = self._detect_type(value)
        logger.info(f"[ThreatIntel] Querying {ioc_type}: {value}")

        result = {
            "value":    value,
            "ioc_type": ioc_type,
            "is_threat": False,
            "confidence": 0,
            "threat_types": [],
            "sources": {},
            "tags": [],
            "country": "",
            "asn": "",
            "summary": "",
            "local_hits": self.db.lookup(value),
        }

        # Query each source
        if ioc_type == "ip":
            result["sources"]["abuseipdb"] = self._query_abuseipdb(value)
            result["sources"]["otx"]        = self._query_otx_ip(value)
            result["sources"]["shodan"]      = self._query_shodan_ip(value)
            result["sources"]["ipapi"]       = self._query_ipapi(value)

        elif ioc_type == "domain":
            result["sources"]["otx"]         = self._query_otx_domain(value)
            result["sources"]["urlhaus"]      = self._query_urlhaus(value)

        elif ioc_type == "hash":
            result["sources"]["virustotal"]   = self._query_vt_hash(value)
            result["sources"]["malwarebazaar"] = self._query_malwarebazaar(value)
            result["sources"]["threatfox"]    = self._query_threatfox_hash(value)

        elif ioc_type == "url":
            result["sources"]["urlhaus"]      = self._query_urlhaus(value)
            result["sources"]["virustotal"]   = self._query_vt_url(value)

        # Aggregate confidence + threat flags
        self._aggregate(result)

        # Cache + store IOC if threat found
        self.db.set_cache(cache_key, result)
        if result["is_threat"]:
            self.db.store_ioc(
                ioc_type=ioc_type,
                value=value,
                threat_type=", ".join(result["threat_types"]),
                confidence=result["confidence"],
                source="aggregated",
                country=result.get("country", ""),
                asn=result.get("asn", ""),
                tags=result["tags"],
                raw=result["sources"]
            )
        return result

    # ── AbuseIPDB — free, 1000 req/day ─────────────────────────────────
    def _query_abuseipdb(self, ip: str) -> dict:
        if not ABUSE_KEY:
            return {"error": "No ABUSEIPDB_API_KEY in .env"}
        try:
            r = self._session.get(
                "https://api.abuseipdb.com/api/v2/check",
                params={"ipAddress": ip, "maxAgeInDays": 90, "verbose": True},
                headers={"Key": ABUSE_KEY, "Accept": "application/json"},
                timeout=REQUEST_TO
            )
            d = r.json().get("data", {})
            return {
                "abuse_score":   d.get("abuseConfidenceScore", 0),
                "is_public":     d.get("isPublic"),
                "country":       d.get("countryCode", ""),
                "isp":           d.get("isp", ""),
                "domain":        d.get("domain", ""),
                "total_reports": d.get("totalReports", 0),
                "last_reported": d.get("lastReportedAt", ""),
                "usage_type":    d.get("usageType", ""),
                "is_tor":        d.get("isTor", False),
            }
        except Exception as e:
            return {"error": str(e)}

    # ── AlienVault OTX — free, no limit ────────────────────────────────
    def _query_otx_ip(self, ip: str) -> dict:
        try:
            headers = {"X-OTX-API-KEY": OTX_KEY} if OTX_KEY else {}
            r = self._session.get(
                f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general",
                headers=headers, timeout=REQUEST_TO
            )
            d = r.json()
            pulses = d.get("pulse_info", {}).get("count", 0)
            tags   = []
            for p in d.get("pulse_info", {}).get("pulses", [])[:5]:
                tags += p.get("tags", [])
            return {
                "pulse_count":  pulses,
                "reputation":   d.get("reputation", 0),
                "country":      d.get("country_name", ""),
                "asn":          d.get("asn", ""),
                "tags":         list(set(tags))[:10],
                "malware_fams": [p.get("name", "") for p in
                                  d.get("pulse_info", {}).get("pulses", [])[:5]],
            }
        except Exception as e:
            return {"error": str(e)}

    def _query_otx_domain(self, domain: str) -> dict:
        try:
            headers = {"X-OTX-API-KEY": OTX_KEY} if OTX_KEY else {}
            r = self._session.get(
                f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general",
                headers=headers, timeout=REQUEST_TO
            )
            d = r.json()
            return {
                "pulse_count": d.get("pulse_info", {}).get("count", 0),
                "alexa_rank":  d.get("alexa", ""),
                "whois":       d.get("whois", ""),
                "tags":        [p.get("name") for p in
                                d.get("pulse_info", {}).get("pulses", [])[:5]],
            }
        except Exception as e:
            return {"error": str(e)}

    # ── ThreatFox (abuse.ch) — free, NO KEY NEEDED ─────────────────────
    def _query_threatfox_hash(self, hash_val: str) -> dict:
        try:
            r = self._session.post(
                "https://threatfox-api.abuse.ch/api/v1/",
                json={"query": "search_hash", "hash": hash_val},
                timeout=REQUEST_TO
            )
            d = r.json()
            if d.get("query_status") == "ok" and d.get("data"):
                hit = d["data"][0]
                return {
                    "malware":      hit.get("malware", ""),
                    "malware_alias":hit.get("malware_alias", ""),
                    "confidence":   hit.get("confidence_level", 0),
                    "threat_type":  hit.get("threat_type", ""),
                    "first_seen":   hit.get("first_seen", ""),
                    "tags":         hit.get("tags") or [],
                }
            return {"status": "clean"}
        except Exception as e:
            return {"error": str(e)}

    # ── URLhaus (abuse.ch) — free, NO KEY NEEDED ──────────────────────
    def _query_urlhaus(self, url_or_domain: str) -> dict:
        try:
            r = self._session.post(
                "https://urlhaus-api.abuse.ch/v1/url/",
                data={"url": url_or_domain},
                timeout=REQUEST_TO
            )
            d = r.json()
            if d.get("query_status") == "is_listed":
                return {
                    "status":      "malicious",
                    "threat":      d.get("threat", ""),
                    "tags":        d.get("tags") or [],
                    "date_added":  d.get("date_added", ""),
                    "url_status":  d.get("url_status", ""),
                    "reporter":    d.get("reporter", ""),
                }
            return {"status": "clean"}
        except Exception as e:
            return {"error": str(e)}

    # ── MalwareBazaar (abuse.ch) — free, NO KEY NEEDED ────────────────
    def _query_malwarebazaar(self, hash_val: str) -> dict:
        try:
            r = self._session.post(
                "https://mb-api.abuse.ch/api/v1/",
                data={"query": "get_info", "hash": hash_val},
                timeout=REQUEST_TO
            )
            d = r.json()
            if d.get("query_status") == "ok" and d.get("data"):
                hit = d["data"][0]
                return {
                    "file_name":  hit.get("file_name", ""),
                    "file_type":  hit.get("file_type", ""),
                    "malware":    hit.get("tags") or [],
                    "signature":  hit.get("signature", ""),
                    "first_seen": hit.get("first_seen", ""),
                    "reporter":   hit.get("reporter", ""),
                }
            return {"status": "not_found"}
        except Exception as e:
            return {"error": str(e)}

    # ── VirusTotal — free 500 req/day ─────────────────────────────────
    def _query_vt_hash(self, hash_val: str) -> dict:
        if not VT_KEY:
            return {"error": "No VIRUSTOTAL_API_KEY in .env"}
        try:
            r = self._session.get(
                f"https://www.virustotal.com/api/v3/files/{hash_val}",
                headers={"x-apikey": VT_KEY},
                timeout=REQUEST_TO
            )
            if r.status_code == 200:
                d = r.json()["data"]["attributes"]
                stats = d.get("last_analysis_stats", {})
                return {
                    "malicious":  stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless":   stats.get("harmless", 0),
                    "name":       d.get("meaningful_name", ""),
                    "type":       d.get("type_description", ""),
                    "tags":       d.get("tags", []),
                }
            return {"status": "not_found"}
        except Exception as e:
            return {"error": str(e)}

    def _query_vt_url(self, url: str) -> dict:
        if not VT_KEY:
            return {"error": "No VIRUSTOTAL_API_KEY in .env"}
        try:
            import base64
            url_id = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
            r = self._session.get(
                f"https://www.virustotal.com/api/v3/urls/{url_id}",
                headers={"x-apikey": VT_KEY},
                timeout=REQUEST_TO
            )
            if r.status_code == 200:
                d = r.json()["data"]["attributes"]
                stats = d.get("last_analysis_stats", {})
                return {
                    "malicious":  stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "categories": d.get("categories", {}),
                }
            return {"status": "not_found"}
        except Exception as e:
            return {"error": str(e)}

    # ── Shodan — free tier ───────────────────────────────────────────────
    def _query_shodan_ip(self, ip: str) -> dict:
        if not SHODAN_KEY:
            return {"error": "No SHODAN_API_KEY in .env (get free at shodan.io)"}
        try:
            r = self._session.get(
                f"https://api.shodan.io/shodan/host/{ip}",
                params={"key": SHODAN_KEY},
                timeout=REQUEST_TO
            )
            if r.status_code == 200:
                d = r.json()
                return {
                    "open_ports": d.get("ports", []),
                    "org":        d.get("org", ""),
                    "isp":        d.get("isp", ""),
                    "country":    d.get("country_name", ""),
                    "city":       d.get("city", ""),
                    "vulns":      list(d.get("vulns", {}).keys()),
                    "tags":       d.get("tags", []),
                    "hostnames":  d.get("hostnames", []),
                    "os":         d.get("os", ""),
                }
            return {"error": f"Shodan: HTTP {r.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    # ── ip-api.com — completely free, no key ──────────────────────────
    def _query_ipapi(self, ip: str) -> dict:
        try:
            r = self._session.get(
                f"http://ip-api.com/json/{ip}",
                params={"fields": "status,country,countryCode,regionName,city,isp,org,as,proxy,hosting"},
                timeout=REQUEST_TO
            )
            d = r.json()
            if d.get("status") == "success":
                return {
                    "country":  d.get("country", ""),
                    "city":     d.get("city", ""),
                    "isp":      d.get("isp", ""),
                    "org":      d.get("org", ""),
                    "asn":      d.get("as", ""),
                    "is_proxy": d.get("proxy", False),
                    "is_hosting": d.get("hosting", False),
                }
            return {}
        except Exception as e:
            return {"error": str(e)}

    # ── Aggregator ─────────────────────────────────────────────────────
    def _aggregate(self, result: dict):
        score = 0
        tags  = []
        types = []

        # AbuseIPDB
        ab = result["sources"].get("abuseipdb", {})
        if isinstance(ab, dict) and not ab.get("error"):
            score += ab.get("abuse_score", 0)
            if ab.get("country"): result["country"] = ab["country"]
            if ab.get("is_tor"):  tags.append("tor")
            if ab.get("total_reports", 0) > 0: types.append("abuse")

        # OTX
        otx = result["sources"].get("otx", {})
        if isinstance(otx, dict) and not otx.get("error"):
            score += min(otx.get("pulse_count", 0) * 5, 50)
            tags  += otx.get("tags", [])
            if otx.get("country") and not result["country"]:
                result["country"] = otx["country"]
            if otx.get("asn"): result["asn"] = otx["asn"]

        # ThreatFox
        tf = result["sources"].get("threatfox", {})
        if isinstance(tf, dict) and tf.get("malware"):
            score += 80
            types.append(f"malware:{tf['malware']}")
            tags  += tf.get("tags", [])

        # MalwareBazaar
        mb = result["sources"].get("malwarebazaar", {})
        if isinstance(mb, dict) and mb.get("signature"):
            score += 70
            types.append(f"malware:{mb['signature']}")

        # VirusTotal
        vt = result["sources"].get("virustotal", {})
        if isinstance(vt, dict) and not vt.get("error"):
            mal = vt.get("malicious", 0)
            if mal > 0:
                score += min(mal * 5, 60)
                types.append(f"virustotal:{mal}_engines")
            tags += vt.get("tags", [])

        # URLhaus
        uh = result["sources"].get("urlhaus", {})
        if isinstance(uh, dict) and uh.get("status") == "malicious":
            score += 75
            types.append(f"malware_url:{uh.get('threat','')}")
            tags  += uh.get("tags", [])

        # Shodan
        sh = result["sources"].get("shodan", {})
        if isinstance(sh, dict) and sh.get("vulns"):
            score += len(sh["vulns"]) * 10
            types += sh["vulns"]
            if sh.get("country") and not result["country"]:
                result["country"] = sh["country"]

        result["confidence"]   = min(score, 100)
        result["is_threat"]    = score >= 30
        result["threat_types"] = list(set(types))
        result["tags"]         = list(set(tags))[:15]
        result["summary"]      = self._make_summary(result)

    def _make_summary(self, r: dict) -> str:
        if not r["is_threat"]:
            return f"{r['value']} — No threats found in any database."
        tt = ", ".join(r["threat_types"][:3]) or "suspicious activity"
        return (
            f"{r['value']} is MALICIOUS (confidence {r['confidence']}%). "
            f"Threat type: {tt}. Country: {r.get('country','unknown')}."
        )

    # ── Bulk feed download (run once to pre-populate DB) ────────────────
    def update_feeds(self, progress_cb=None):
        """
        Downloads free threat intel bulk feeds and stores in local DB.
        Run once to pre-populate — future lookups are instant (offline).
        No API key needed for any of these feeds.
        """
        cb = progress_cb or print
        feeds = [
            # (name, url, parser_func)
            ("ThreatFox IOC dump",
             "https://threatfox.abuse.ch/export/json/recent/",
             self._parse_threatfox_feed),
            ("URLhaus malware URLs",
             "https://urlhaus.abuse.ch/downloads/json_recent/",
             self._parse_urlhaus_feed),
            ("FeodoTracker C2 IPs",
             "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
             self._parse_feodo_feed),
            ("Emerging Threats IP blocklist",
             "https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt",
             self._parse_et_feed),
        ]
        for name, url, parser in feeds:
            cb(f"[Feed] Downloading {name}...\n")
            try:
                r = self._session.get(url, timeout=30)
                count = parser(r)
                cb(f"[Feed] {name}: {count} IOCs stored.\n")
            except Exception as e:
                cb(f"[Feed] {name} failed: {e}\n")

    def _parse_threatfox_feed(self, r) -> int:
        data = r.json()
        count = 0
        for ioc_list in data.get("data", {}).values():
            for item in (ioc_list if isinstance(ioc_list, list) else []):
                self.db.store_ioc(
                    ioc_type=item.get("ioc_type", "unknown"),
                    value=item.get("ioc", ""),
                    threat_type=item.get("malware", ""),
                    confidence=item.get("confidence_level", 50),
                    source="threatfox",
                    tags=item.get("tags") or [],
                    first_seen=item.get("first_seen", ""),
                    last_seen=item.get("last_seen", "")
                )
                count += 1
        return count

    def _parse_urlhaus_feed(self, r) -> int:
        data = r.json()
        count = 0
        for item in data.get("urls", []):
            if item.get("url_status") == "online":
                self.db.store_ioc(
                    ioc_type="url", value=item.get("url", ""),
                    threat_type=item.get("threat", ""),
                    confidence=80, source="urlhaus",
                    tags=item.get("tags") or [],
                    first_seen=item.get("dateadded", "")
                )
                count += 1
        return count

    def _parse_feodo_feed(self, r) -> int:
        count = 0
        for line in r.text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                ip = line.split(",")[0].strip()
                self.db.store_ioc(
                    ioc_type="ip", value=ip,
                    threat_type="c2_server",
                    confidence=95, source="feodotracker"
                )
                count += 1
        return count

    def _parse_et_feed(self, r) -> int:
        count = 0
        for line in r.text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                self.db.store_ioc(
                    ioc_type="ip", value=line,
                    threat_type="emerging_threat",
                    confidence=70, source="emerging_threats"
                )
                count += 1
        return count

    # ── Type detector ───────────────────────────────────────────────────
    @staticmethod
    def _detect_type(value: str) -> str:
        import re
        value = value.strip()
        # IP address
        try:
            ipaddress.ip_address(value)
            return "ip"
        except ValueError:
            pass
        # MD5 / SHA1 / SHA256
        if re.fullmatch(r"[0-9a-f]{32}", value): return "hash"
        if re.fullmatch(r"[0-9a-f]{40}", value): return "hash"
        if re.fullmatch(r"[0-9a-f]{64}", value): return "hash"
        # URL
        if value.startswith("http://") or value.startswith("https://"): return "url"
        # Email
        if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", value): return "email"
        # Domain (default)
        return "domain"


# ── Convenience singleton
_engine = None

def get_engine() -> ThreatIntelEngine:
    global _engine
    if _engine is None:
        _engine = ThreatIntelEngine()
    return _engine


if __name__ == "__main__":
    import sys
    engine = ThreatIntelEngine()
    if len(sys.argv) > 1:
        r = engine.lookup(sys.argv[1])
        print(json.dumps(r, indent=2))
    else:
        print("Usage: python threat_intel.py <ip|domain|hash|url>")
        print("  e.g. python threat_intel.py 1.2.3.4")
        print("  e.g. python threat_intel.py malware.exe.sha256hash")
        print()
        engine.update_feeds()
        print("Feeds updated. Stats:", engine.db.stats())
