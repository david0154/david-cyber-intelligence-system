# DAVID CYBER INTELLIGENCE SYSTEM

<div align="center">

![DAVID CIS Logo](assets/logo.png)

**Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green?style=for-the-badge)](#-quick-start)
[![Version](https://img.shields.io/badge/Version-2.0.0-red?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-Proprietary-orange?style=for-the-badge)](#️-legal-disclaimer)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)](#)

```
██████╗  █████╗ ██╗   ██╗██╗██████╗
██╔══██╗██╔══██╗██║   ██║██║██╔══██╗
██║  ██║███████║██║   ██║██║██║  ██║
██║  ██║██╔══██║╚██╗ ██╔╝██║██║  ██║
██████╔╝██║  ██║ ╚████╔╝ ██║██████╔╝
╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═════╝
  CYBER INTELLIGENCE SYSTEM  v2.0
```

> **A TRUE AI-Powered Cybersecurity Platform**
> Security Analysis · Real-Time Defense · Bug Hunting · Live Global Tracking

</div>

---

## 🗺️ Table of Contents

1. [What Is DAVID?](#-what-is-david)
2. [Core Architecture](#-core-architecture)
3. [All Features](#-all-features)
   - [Offensive Security](#-1-offensive-security-engine)
   - [Malware Analysis](#-2-malware-analysis-engine)
   - [Network IDS](#-3-network-ids--live-attack-map)
   - [OSINT Investigation](#-4-osint-investigation-engine)
   - [Defense / WAF](#-5-defense-engine--waf)
   - [Threat Intelligence](#-6-threat-intelligence-engine)
   - [SOC / SIEM](#-7-soc--siem-layer)
   - [Bug Bounty Platform](#-8-bug-bounty-platform)
   - [App Bug Analyzer](#-9-app-bug-analyzer)
   - [Live Cyber Attack Map](#-10-live-cyber-attack-map)
   - [Flight Tracking](#-11-live-flight-tracking)
   - [Ship Tracking](#-12-live-ship-tracking)
   - [Satellite Tracking](#-13-live-satellite-tracking)
   - [IP Geolocation](#-14-ip-geolocation)
   - [Automation & Alerts](#-15-automation--alerting)
4. [Web Dashboard](#-web-dashboard)
5. [Required API Keys](#-required-api-keys)
6. [Complete .env Template](#-complete-env-template)
7. [Project Directories](#-project-directories)
8. [Roadmap / Status](#-roadmap--status)
9. [REST API Endpoints](#-rest-api-endpoints)
10. [Running Without LLM](#-running-without-llm)
11. [Data Layer](#-data-layer)
12. [Quick Start](#-quick-start)
13. [Install as Normal Software](#-install-as-normal-software)
14. [AI Commands](#-ai-natural-language-commands)
15. [Version History](#-version-history)
16. [Contributing](#-contributing)
17. [Legal Disclaimer](#️-legal-disclaimer)

---

## 🧠 What Is DAVID?

DAVID (Defense & Attack Versatile Intelligence Daemon) is a complete AI-powered cybersecurity platform that runs on your desktop — **Windows, macOS, or Linux** — like any normal software. It combines:

- 🔴 **Offensive tools** — Nmap, SQLMap, Hydra, Metasploit, OWASP ZAP, OpenVAS, attack simulation
- 🦠 **Malware analysis** — YARA, pefile, capstone, AI behavior analysis
- 🌐 **Network monitoring** — Scapy, Suricata IDS, anomaly detection, SOC scoring
- 🕵️ **OSINT** — SpiderFoot, Shodan, theHarvester, CyNER AI
- 🛡️ **Defense** — Open-AppSec ML WAF, Cloudflare automation, auto IP blocking
- 🧠 **AI brain** — Local Mixtral LLM (runs offline, no API cost)
- ✈️ **Live tracking** — Flights, ships, satellites, IP geolocation, dashboard views
- 🐛 **Bug finder** — Analyzes any APK/EXE/PHP/Python/JS for security bugs
- 🏆 **Bug bounty** — Full platform with CVSS scoring and rewards

All controlled from **one GUI application** with a dark cyberpunk interface, plus a browser-accessible dashboard served by FastAPI.

---

## 🏗️ Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│               LLM BRAIN  (Mixtral-8x7B GGUF)                   │
│               via ctransformers  ─  runs 100% OFFLINE           │
│         Intent · Reasoning · Explanation · Task Routing         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
               ┌────────────▼────────────┐
               │       TASK ROUTER       │
               │  Routes input to module │
               └────────────┬────────────┘
                            │
┌──────────┬──────────┬─────┴────┬──────────┬──────────┬─────────┐
│ Offensive│ Malware  │ Network  │  OSINT   │ Defense  │Tracking │
│ Engine   │ Engine   │   IDS    │ Engine   │  WAF     │ Engine  │
│ Nmap     │ YARA     │ Scapy    │SpiderFoot│Open-AppSc│Flights  │
│ SQLMap   │ pefile   │Suricata  │ Shodan   │ Cloudflare│ Ships  │
│ Hydra    │capstone  │ LSTM     │theHarves │ Auto-IP  │Satellite│
│ ZAP      │ XGen-Q   │  ML IDS  │ CyNER    │  Block   │Cyber Map│
│ OpenVAS  │          │          │          │ CAI      │         │
└──────────┴──────────┴──────────┴──────────┴──────────┴─────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
  ┌─────▼──────┐    ┌───────▼──────┐    ┌──────▼──────┐
  │Threat Intel│    │  SOC / SIEM  │    │ Bug Bounty  │
  │MISP+OpenCTI│    │Wazuh + ELK   │    │  Platform   │
  │   Neo4j    │    │  Real-time   │    │ CVSS Scorer │
  └────────────┘    └──────────────┘    └─────────────┘
                            │
         PostgreSQL · Elasticsearch · Neo4j · SQLite
```

---

## ✅ All Features

### 🔴 1. Offensive Security Engine

Run penetration tests, vulnerability scans, and attack simulations against a target IP or web app. The AI guides each step, explains findings, and generates fix suggestions.

| Feature | Tool | What It Does |
|---------|------|--------------|
| Port & Service Scan | **Nmap** `-sV -sC` | Service detection and recon workflows |
| Standalone Vulnerability Scanner | `engines/vulnerability_scanner.py` | Top-1000 port scan, OS detection, CVE enrichment, raw Nmap output, patch links |
| CVE Detection | Nmap + vulners.nse | Auto-matches services to known CVEs |
| SQL Injection | **SQLMap** | Tests parameters for SQL injection |
| Full Web App Scan | **OWASP ZAP** API | DAST scan for XSS, CSRF, injections, and misconfigurations |
| Brute Force | **Hydra** | Tests SSH, FTP, and HTTP login flows |
| OpenVAS Scan | `security/openvas_client.py` | Launches authenticated vulnerability scans through OpenVAS |
| Attack Simulation | `engines/attack_sim_engine.py` | Simulates `basic`, `web`, or `full` attack paths with escalating checks |
| Auto Exploitation | **Metasploit + DeepExploit** | Maps findings to exploit options |
| Pentest Workflow | PentestGPT logic + LLM | Recon → scan → exploit → report |
| Fix Suggestions | Mixtral LLM | Patch recommendation for every finding |

**Attack Simulation scopes**
- `basic` — Nmap top-200 ports plus CVE matching.
- `web` — Adds SQLMap injection testing and OWASP ZAP DAST.
- `full` — Adds Metasploit module discovery for deeper validation.

**Flow:**
```
Target IP/URL → Recon → Vulnerability scan → CVE match → SQLMap/ZAP/OpenVAS
      → Attack simulation → DeepExploit → LLM explanation → Risk report
```

---

### 🦠 2. Malware Analysis Engine

Upload any file and analyze it without executing it. DAVID looks for trojans, ransomware, spyware, and backdoors.

| Feature | Tool | What It Does |
|---------|------|--------------|
| Signature Scan | **YARA** (1000+ rules) | Matches known malware families |
| Binary Parsing | **pefile** | PE headers, imports, exports, sections, entropy |
| Disassembly | **capstone** | Readable assembly output |
| String Extraction | Custom extractor | Finds URLs, IPs, registry keys, and secrets |
| Behavior Analysis | **XGen-Q** model | Identifies ransomware, keylogger, and botnet patterns |
| ASLR / DEP check | pefile flags | Checks exploit mitigations |
| Risk Score | Weighted scorer | 0–100 score: CLEAN / LOW / MEDIUM / HIGH / CRITICAL |
| AI Explanation | Mixtral LLM | Plain-English malware summary |

**Supported:** `.exe` `.dll` `.bin` `.so` `.apk` `.py` `.js` `.php` `.docx` `.pdf`

---

### 🌐 3. Network IDS & Live Attack Map

Monitors the network in real time, detects suspicious activity, and links detections to map and defense workflows.

| Feature | Tool | What It Does |
|---------|------|--------------|
| Packet Capture | **Scapy** | Sniffs packets on the selected interface |
| IDS Rules Engine | **Suricata** | Rule-based detection for scans, DDoS, and exploits |
| Traffic Logging | **Zeek** | Structured network activity logs |
| Anomaly Detection | LSTM / ML IDS | Flags traffic that deviates from learned patterns |
| Phishing Detection | RL / ML model | Scores suspicious URLs |
| Live Attack Map | `tracking/attack_map.py` | Animated world map for attacker → target visualization |
| Auto Block | Defense Engine | Blocks attacker IPs through local or Cloudflare controls |
| AI Explanation | Mixtral LLM | Explains attack type and response guidance |

> ⚠️ Packet capture and interface monitoring may require admin/root privileges.

---

### 🕵️ 4. OSINT Investigation Engine

Enter any IP, domain, email, phone number, or username to build an intelligence profile.

| Feature | Tool | What It Does |
|---------|------|--------------|
| Automated Recon | **SpiderFoot** | Queries broad OSINT sources automatically |
| Email & Subdomain Hunt | **theHarvester** | Finds emails, subdomains, and associated identities |
| Exposed Services | **Shodan API** | Enumerates indexed ports, banners, and exposures |
| AI Entity Extraction | **CyNER** | Extracts IPs, CVEs, domains, and hashes from text |
| WHOIS / DNS History | SecurityTrails API | DNS records, historical WHOIS, subdomains |
| Breach Check | HaveIBeenPwned API | Checks exposure in known breaches |
| Threat Correlation | Mixtral LLM | Links results to campaigns or actors |

---

### 🛡️ 5. Defense Engine & WAF

Protects servers and web applications in real time with local controls, WAF integrations, and AI-assisted hardening.

| Feature | Tool | What It Does |
|---------|------|--------------|
| ML Web Firewall | **Open-AppSec** | Blocks SQLi, XSS, RCE, path traversal, and SSRF |
| Auto-Learning Mode | Open-AppSec | Learns normal traffic and flags anomalies |
| IP Reputation Block | AbuseIPDB + custom logic | Blocks known bad IPs before they connect |
| Rate Limiting | Defense Engine | Slows brute-force and DDoS attempts |
| Geo-Blocking | GeoIP engine | Blocks traffic by region or country |
| Threat DB | PostgreSQL | Stores blocked events and context |
| Alert on Block | Telegram/Email | Sends alerts when attacks are blocked |
| Cloudflare WAF Stats | `security/cloudflare_client.py` | Pulls account zones and WAF statistics |
| Cloudflare IP Blocking | `block_ip(zone_id, ip)` | Pushes firewall block rules to Cloudflare in real time |
| CAI Defensive Mode | `security/cai_engine.py` | Runs port audit, SSL checks, and HTTP security header auditing |

#### CAI Engine

The CAI Engine is a dual-mode cybersecurity AI pipeline.

- `mode="offensive"` runs recon, CVE checks, web checks, and LLM analysis.
- `mode="defensive"` performs port audits, SSL certificate inspection, HTTP security header checks, and AI-generated hardening recommendations.
- The defensive audit checks for headers such as `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, and `Content-Security-Policy`.

---

### 🧠 6. Threat Intelligence Engine

Cross-references findings across modules against global threat databases.

| Feature | Tool | What It Does |
|---------|------|--------------|
| IOC Management | **MISP** | Stores IPs, hashes, domains, and events |
| Attack Graph | **OpenCTI** | Visualizes threat actor → TTP → IOC relationships |
| IOC Lookup | MISP API | Checks whether a finding is already known |
| Graph DB | **Neo4j** | Stores relationships and attack chains |
| Cross-module Correlation | All engines | Links network, OSINT, intel, and defense findings |
| OTX Feeds | AlienVault OTX | Pulls community threat pulses |

---

### 📊 7. SOC / SIEM Layer

A desktop SOC workflow for log review, scoring, alerting, and automated response.

| Feature | Tool | What It Does |
|---------|------|--------------|
| Log Collection | **Wazuh** agent | Collects OS, application, and security logs |
| Log Indexing | **Elasticsearch** | Searches large volumes of log data quickly |
| Anomaly Detection | ML + heuristics | Finds unusual login, file, and network behavior |
| Real-time Alerts | FastAPI WebSocket | Pushes live alerts to GUI and dashboard consumers |
| Auto IP Block | Local / remote controls | Blocks attacker IPs when thresholds are exceeded |
| Attack Pattern Library | SOC engine regex rules | Detects brute force, SQLi, XSS, path traversal, port scan, DDoS, malware, and privilege escalation |
| IP Scoring | `_score_ips` logic | Scores suspicious IPs and escalates or blocks high-risk addresses |
| Log File Drop Analysis | `analyze_log_file(path)` | Parses arbitrary log files such as auth, web, or service logs |
| Dashboard Data | `get_dashboard_data()` | Returns aggregate threat stats for the session |

---

### 🏆 8. Bug Bounty Platform

A vulnerability disclosure and reward platform is bundled with DAVID.

| Feature | What It Does |
|---------|--------------|
| Bug Submission | Researchers submit via GUI form or REST API (`POST /bounty/submit`) |
| AI Validation | LLM reads the report and estimates exploitability |
| CVSS v3.1 Auto-Score | Calculates severity automatically |
| Duplicate Detection | Rejects identical submissions |
| PoC Upload | Attaches screenshots, video, or exploit code |
| Auto Severity | CRITICAL / HIGH / MEDIUM / LOW / INFORMATIONAL |
| Admin Panel | Approve, reject, or request more info |
| Reward Tracker | Tracks payouts and researcher ranking |
| REST API | Separate API docs at `http://localhost:8001/docs` |

---

### 🐛 9. App Bug Analyzer

Drop any application file or source folder into DAVID to find security issues and suggested fixes.

| Input | What Gets Analyzed |
|-------|--------------------|
| `.apk` | AndroidManifest.xml, Java/Kotlin code, resources |
| `.exe` / `.dll` | PE headers, mitigations, strings, YARA hits |
| `.php` | SQLi, RFI, `eval`, `shell_exec`, redirects, weak hashing |
| `.py` | Hardcoded secrets, `debug=True`, `eval`, pickle misuse |
| `.js` / `.ts` | XSS sinks, token storage, `eval`, insecure URLs |
| `.java` / `.kt` | SQL concat, `ProcessBuilder`, weak randomness, debug flags |
| URL | Security headers, cookie flags, mixed content, error leaks |
| Folder / ZIP | Recursive scan across project files |

**Each bug report gives:**
- Severity: CRITICAL / HIGH / MEDIUM / LOW / INFO
- File name and exact line number
- Triggering code snippet
- Fix suggestion
- CVSS estimate
- Export to HTML or JSON report

```bash
python engines/bug_analyzer.py app-release.apk
python engines/bug_analyzer.py https://yoursite.com
python engines/bug_analyzer.py C:\projects\myapp\
```

---

### 🌍 10. Live Cyber Attack Map

The live attack map is a dedicated tracking module for real-time visualization of hostile activity.

| Feature | How It Works |
|---------|--------------|
| Live attack feed | Uses reputation and threat-intel feeds such as AbuseIPDB and OTX |
| World map canvas | Renders a Tkinter/PIL world map widget |
| Animated arrows | Draws attack source → destination movement |
| Attack labels | Shows attack types such as DDoS, SQLi, brute force, or malware |
| Local alerts | Raises a popup when monitored assets are targeted |
| Attack counter | Tracks volume per second or per hour |
| Filter by type | Filters displayed event classes |
| Heatmap mode | Colors regions by observed activity volume |

> Implemented module path: `tracking/attack_map.py` and exposed in the GUI as a dedicated tab.

---

### ✈️ 11. Live Flight Tracking

Track aircraft in real time using external flight data sources.

| Feature | Details |
|---------|---------|
| Data source | OpenSky Network API |
| Search | Callsign, ICAO24, airline, country, or area |
| Live data | Position, altitude, speed, heading, squawk |
| Flight path | Recent flight path rendering |
| Auto-refresh | Periodic updates |
| Alert mode | Alert when a flight enters a watched region |

```python
flight_tracker.track(callsign="AIC101")
```

---

### 🚢 12. Live Ship Tracking

Track vessels worldwide using AIS-backed sources.

| Feature | Details |
|---------|---------|
| Data source | MarineTraffic API and public AIS feeds |
| Search | Vessel name, MMSI, IMO number, flag state |
| Live data | Position, speed, heading, destination, ETA |
| Ship types | Cargo, tanker, passenger, fishing, naval |
| Port arrivals | Tracks arrivals and departures |
| Route history | Recent route history |

```python
ship_tracker.track(mmsi="235009998")
```

---

### 🛰️ 13. Live Satellite Tracking

Track satellites and space stations using TLE and orbit propagation data.

| Feature | Details |
|---------|---------|
| Data source | CelesTrak TLE data and N2YO API |
| Propagation | Skyfield orbital calculations |
| Search | Satellite name, NORAD ID, or category |
| Categories | ISS, weather, GPS, spy sats, Starlink, amateur |
| Live position | Latitude, longitude, altitude, velocity |
| Orbital path | Ground track rendering |
| Next pass | Calculates next visible pass for your location |

```python
satellite_tracker.track(norad_id=25544)
```

---

### 📍 14. IP Geolocation

Map any IP address to location and network metadata.

| Feature | Details |
|---------|---------|
| Data source | ip-api.com |
| Returns | Country, city, ISP, ASN, timezone, lat/lon |
| Threat check | Cross-checks with AbuseIPDB and OTX |
| Map pin | Shows the IP on a map |
| Bulk lookup | Handles multiple IPs |
| Reverse DNS | Includes hostname lookup |

---

### ⚙️ 15. Automation & Alerting

DAVID can schedule jobs, generate notifications, and automate multi-module workflows.

| Feature | What It Does |
|---------|--------------|
| Scheduled Jobs | Runs any supported module on a schedule |
| General Scheduler | `ScanScheduler.add_job()` accepts more than vuln/pentest jobs, including `osint`, `malware`, `geo`, and others routed by the task router |
| Telegram Alerts | Sends instant messages on CRITICAL/HIGH events |
| Email Alerts | SMTP mail with threat report attachments |
| Auto IP Block | Blocks attacking IPs automatically |
| Auto Patch Reports | Generates fix guidance after scans |
| Watchlist Alerts | Alerts on watched IPs, domains, or indicators |

---

## 🌐 Web Dashboard

A browser-based dashboard is served directly by the FastAPI backend.

- Default URL: `http://localhost:8000/`
- Static assets: `/static`
- OpenAPI docs: `http://localhost:8000/docs`
- Health endpoint: `http://localhost:8000/health`

If `dashboard/index.html` exists, the API root serves that page automatically.

---

## 🔑 Required API Keys

All keys go in your `.env` file. Most integrations can run on free or self-hosted services.

### 🟢 Free / Self-hosted Core

| Service | What For | `.env` Key |
|---------|----------|------------|
| Shodan | Exposed services and internet recon | `SHODAN_API_KEY` |
| OWASP ZAP | Web application scanning | `ZAP_URL`, `ZAP_API_KEY` |
| OpenVAS | Vulnerability scanning | `OPENVAS_URL`, `OPENVAS_USER`, `OPENVAS_PASS` |
| MISP | Threat intelligence IOC management | `MISP_URL`, `MISP_KEY` |
| OpenCTI | Threat graphing | `OPENCTI_URL`, `OPENCTI_KEY` |
| Wazuh | SIEM / alert collection | `WAZUH_URL`, `WAZUH_USER`, `WAZUH_PASS` |
| Telegram Bot | Alert notifications | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| OpenSky Network | Flight tracking | `OPENSKY_USER`, `OPENSKY_PASS` |

### 🟡 Freemium

| Service | What For | `.env` Key |
|---------|----------|------------|
| VirusTotal | File and IOC enrichment | `VIRUSTOTAL_API_KEY` |
| AbuseIPDB | IP reputation checks | `ABUSEIPDB_API_KEY` |
| AlienVault OTX | Threat pulses | `OTX_API_KEY` |
| HaveIBeenPwned | Breach lookup | `HIBP_API_KEY` |
| SecurityTrails | DNS and WHOIS history | `SECURITYTRAILS_KEY` |
| N2YO | Satellite data | `N2YO_API_KEY` |
| MarineTraffic | Ship tracking | `MARINETRAFFIC_KEY` |
| Cloudflare | WAF stats and automated IP blocking | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_EMAIL` |

### 🔴 Optional

| Service | What For | `.env` Key |
|---------|----------|------------|
| OpenAI | Alternative hosted LLM path | `OPENAI_API_KEY` |
| SMTP | Email alerts | `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `ALERT_EMAIL` |

> ✅ Core workflows can still run with local/self-hosted tooling and the offline LLM path.

---

## 📋 Complete `.env` Template

Copy `.env.example` to `.env` and fill in your values:

```env
# ── AI / LLM ─────────────────────────────────────────
LLM_MODEL_PATH=models/mixtral.gguf
LLM_MODEL_TYPE=mistral

# ── Offensive Tools ──────────────────────────────────
ZAP_URL=http://localhost:8080
ZAP_API_KEY=your_zap_api_key
OPENVAS_URL=https://localhost:9392
OPENVAS_USER=admin
OPENVAS_PASS=your_openvas_password

# ── SIEM / SOC ───────────────────────────────────────
WAZUH_URL=https://localhost:55000
WAZUH_USER=wazuh
WAZUH_PASS=your_wazuh_password

# ── Threat Intelligence ──────────────────────────────
SHODAN_API_KEY=your_shodan_key
VIRUSTOTAL_API_KEY=your_virustotal_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
OTX_API_KEY=your_otx_key
SECURITYTRAILS_KEY=your_securitytrails_key
HIBP_API_KEY=your_hibp_key
MISP_URL=https://your-misp-instance
MISP_KEY=your_misp_auth_key
OPENCTI_URL=http://localhost:8080
OPENCTI_KEY=your_opencti_key

# ── Live Tracking ────────────────────────────────────
OPENSKY_USER=your_opensky_username
OPENSKY_PASS=your_opensky_password
N2YO_API_KEY=your_n2yo_key
MARINETRAFFIC_KEY=your_marinetraffic_key

# ── Alerts ───────────────────────────────────────────
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASS=your_app_password
ALERT_EMAIL=alerts@yourdomain.com

# ── Optional / Defense Integrations ──────────────────
CLOUDFLARE_API_TOKEN=your_cloudflare_token
CLOUDFLARE_EMAIL=you@example.com
OPENAI_API_KEY=your_openai_key

# ── Databases ────────────────────────────────────────
POSTGRES_URL=postgresql://user:pass@localhost/david_db
ELASTICSEARCH_URL=http://localhost:9200
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=your_neo4j_password
```

---

## 📁 Project Directories

| Path | Purpose |
|------|---------|
| `models/` | Local LLM and ML model files used by DAVID. Place `mixtral.gguf` here and keep additional model weights in this directory. |
| `config/` | Configuration files for modules, routes, scans, and integration settings. |
| `data/` | Cached results, local datasets, scan outputs, and generated intelligence artifacts. |
| `dashboard/` | Browser dashboard frontend served by FastAPI. |
| `engines/` | Offensive, defensive, scanning, and analysis engines. |
| `security/` | Security-specific clients and pipelines such as OpenVAS, Cloudflare, and CAI. |
| `tracking/` | Flight, ship, satellite, geo, and cyber-attack tracking modules. |
| `automation/` | Scheduler and alert automation utilities. |

### Models
- `models/mixtral.gguf` is the default offline LLM path.
- Keep enough disk space for GGUF and other model artifacts before first run.
- Large models should not be committed to Git; download them locally into `models/`.

---

## 🧭 Roadmap / Status

Some modules are fully wired into the task router and API, while others are still lightweight or evolving. Treat the list below as the current implementation status guide.

| Area | Status | Notes |
|------|--------|-------|
| Core API / router | Available | FastAPI v2.0.0 backend and dashboard serving are implemented. |
| Vulnerability scanning | Available | Separate `vuln_scan` style workflows exist beyond pentest mode. |
| Attack simulation | Available | Scope-based simulation paths are implemented. |
| CAI defensive audit | Available | Includes SSL and security-header checks. |
| Cloudflare automation | Available | Stats retrieval and IP block actions exist. |
| Live cyber attack map | Documented / implementation target | Dedicated module path is `tracking/attack_map.py`; verify GUI tab wiring in your local build. |
| Network IDS advanced ML | In progress | Deep IDS integrations may still be skeletal depending on local setup. |
| OSINT mega-source coverage | In progress | External source breadth depends on installed tools and API keys. |
| Pentest / exploitation automation | In progress | Some exploit integrations may require extra services or remain partial. |
| Flight / ship tracking richness | In progress | Advanced tracking behavior depends on provider credentials and local UI wiring. |

---

## 🔌 REST API Endpoints

The backend FastAPI app identifies itself as **version 2.0.0** and exposes the following documented routes.

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serves `dashboard/index.html` when present |
| `/health` | GET | Returns status, version, developer, and loaded modules |
| `/analyze` | POST | Universal task-router endpoint for any supported module |
| `/score` | GET | Returns unified threat score report |
| `/score/update` | POST | Updates a module score and returns the aggregate report |
| `/api/wazuh/alerts` | GET | Fetches Wazuh alerts |
| `/api/zap/scan` | POST | Runs an OWASP ZAP scan |
| `/api/openvas/scan` | POST | Runs an OpenVAS scan |
| `/api/hydra/test` | POST | Runs a Hydra credential test |
| `/api/cloudflare/stats` | GET | Returns Cloudflare zone/WAF stats |
| `/api/deepexploit` | POST | Runs DeepExploit workflow |
| `/api/osint` | POST | Runs OSINT investigation |
| `/api/pentest` | POST | Runs pentest workflow |
| `/api/malware` | POST | Runs malware analysis |
| `/api/geo` | POST | Runs IP geolocation |
| `/api/chat` | POST | Sends a query to the AI chat route |
| `/ws/alerts` | WS | Live alert WebSocket stream |

### Module routing examples

```json
{"module":"vuln_scan","params":{"target":"192.168.1.10"}}
{"module":"attack_sim","params":{"target":"https://example.com","scope":"web"}}
{"module":"osint","params":{"target":"example.com"}}
```

---

## 📴 Running Without LLM

DAVID supports an offline fallback mode when the Mixtral GGUF model is not present.

- If `models/mixtral.gguf` is missing, the LLM layer can return a stub/offline response instead of crashing the platform.
- This lets you test routers, scanners, dashboard views, and API endpoints before downloading the full model.
- Recommended download source for Mixtral GGUF: [TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF)

---

## 🗄️ Data Layer

| Database | Purpose |
|----------|---------|
| PostgreSQL | Threat data, bug reports, users, rewards |
| Elasticsearch | Log indexing and SIEM search |
| Neo4j | Threat graphs and IOC relationships |
| SQLite | Local cache and offline data |
| JSON files | Fast local module output and config storage |

---

## 🧠 Unified Threat Scoring

```
Threat Score  =  Malware Score
              +  Network Score
              +  OSINT Score
              +  Threat Intel Match
              +  Active Exploit Score

  0 – 24   →  LOW       (green)   Safe
 25 – 49   →  MEDIUM    (yellow)  Monitor
 50 – 74   →  HIGH      (orange)  Investigate
 75 – 100  →  CRITICAL  (red)     Respond Now
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/david0154/david-cyber-intelligence-system
cd david-cyber-intelligence-system
pip install -r requirements.txt
cp .env.example .env
python launcher.py
# or: python gui_app.py
# or: python main.py
# or: uvicorn core.api:app --reload --port 8000
# or: uvicorn bounty.api:app --reload --port 8001
```

### Dashboard access
- Main dashboard: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`
- Bug bounty API docs: `http://localhost:8001/docs`

---

## 💿 Install as Normal Software

### Windows

```bat
install.bat
```

### Linux / macOS

```bash
bash install.sh
```

### Build Standalone Installer

```bash
python build_exe.py
```

Installer names and package versions should be updated to `2.0.0` wherever release artifacts are generated.

---

## 🤖 AI Natural Language Commands

Type these in the AI chat panel:

```text
"Scan server 192.168.1.1"
"Run vuln scan on 192.168.1.1"
"Simulate attack on https://mysite.com with scope web"
"Analyze malware.exe"
"Analyze app-release.apk"
"Show live cyber attacks"
"Track flight AIC101"
"Track ship MMSI 235009998"
"Track ISS satellite"
"Check IP 1.2.3.4"
"Is admin@domain.com breached?"
"Scan PHP project for bugs"
"Analyze auth.log"
"Show live attack alerts"
"Block IP 5.6.7.8"
"Generate pentest report"
```

---

## 🔄 Full Execution Flow

```
User Input  (IP / File / URL / Log / Text / Voice command)
      ↓
LLM Brain   (Mixtral GGUF — understands intent offline)
      ↓
Task Router (selects correct engine + tool)
      ↓
Engine runs (tool + AI model in background thread)
      ↓
Threat Intel (MISP / OTX / AbuseIPDB cross-check)
      ↓
LLM merges  (combines all results into one answer)
      ↓
Output:
  ✅ Threat Score 0–100
  ✅ Attack type + plain English explanation
  ✅ Fix / patch recommendation
  ✅ IOC saved to database
  ✅ Alert sent to Telegram / Email
  ✅ PDF/HTML report generated
```

---

## 📝 Version History

- `v2.0.0` — FastAPI backend version declared in `core/api.py`, expanded API surface, dashboard serving, Cloudflare/OpenVAS endpoints, and documented CAI / simulation / scanner workflows.
- `v1.0.0` — Initial public README/version branding.

A dedicated `CHANGELOG.md` is recommended for future tagged releases.

---

## 🤝 Contributing

This repository does not yet ship with a dedicated `CONTRIBUTING.md`, but external contributors should follow these baseline rules:

- Open an issue before large feature work.
- Keep modules isolated by engine/domain.
- Add or update README/API docs for every new feature.
- Avoid committing secrets, API keys, or large model weights.
- Test GUI, API, and CLI entry points for any changed feature.

---

## ⚠️ Legal Disclaimer

> **DAVID CIS is for authorized security testing ONLY.**
>
> You must have **written permission** from the system owner before running any scans.
> Unauthorized scanning is illegal under the Computer Fraud and Abuse Act (CFAA),
> IT Act 2000 (India), and equivalent laws worldwide.
>
> The developers (Devil Pvt Ltd / Nexuzy Tech Pvt Ltd) are **not responsible** for
> any misuse of this software.

---

## 👨‍💻 Developer

**David**  
Full-Stack Security Engineer  
Nexuzy Tech Pvt Ltd | Devil Pvt Ltd  
Kolkata, West Bengal, India

🌐 [hypechats.com](https://hypechats.com)  
📧 david@nexuzytech.com  
🐙 [github.com/david0154](https://github.com/david0154)

---

<div align="center">

**DAVID CYBER INTELLIGENCE SYSTEM v2.0**  
*Built with ❤️ in Kolkata, India*  
*Devil Pvt Ltd & Nexuzy Tech Pvt Ltd*

</div>
