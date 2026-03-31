# DAVID CYBER INTELLIGENCE SYSTEM

<div align="center">

![DAVID CIS Logo](assets/logo.png)

**Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green?style=for-the-badge)](#-quick-start)
[![Version](https://img.shields.io/badge/Version-1.0.0-red?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-Proprietary-orange?style=for-the-badge)](#️-legal-disclaimer)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)](#)

```
██████╗  █████╗ ██╗   ██╗██╗██████╗
██╔══██╗██╔══██╗██║   ██║██║██╔══██╗
██║  ██║███████║██║   ██║██║██║  ██║
██║  ██║██╔══██║╚██╗ ██╔╝██║██║  ██║
██████╔╝██║  ██║ ╚████╔╝ ██║██████╔╝
╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═════╝
  CYBER INTELLIGENCE SYSTEM  v1.0
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
4. [Required API Keys](#-required-api-keys)
5. [Complete .env Template](#-complete-env-template)
6. [Data Layer](#-data-layer)
7. [Quick Start](#-quick-start)
8. [Install as Normal Software](#-install-as-normal-software)
9. [AI Commands](#-ai-natural-language-commands)
10. [Legal Disclaimer](#️-legal-disclaimer)

---

## 🧠 What Is DAVID?

DAVID (Defense & Attack Versatile Intelligence Daemon) is a complete AI-powered cybersecurity platform that runs on your desktop — **Windows, macOS, or Linux** — like any normal software. It combines:

- 🔴 **Offensive tools** — Nmap, SQLMap, Hydra, Metasploit, OWASP ZAP
- 🦠 **Malware analysis** — YARA, pefile, capstone, AI behavior analysis
- 🌐 **Network monitoring** — Scapy, Suricata IDS, LSTM anomaly detection
- 🕵️ **OSINT** — SpiderFoot, Shodan, theHarvester, CyNER AI
- 🛡️ **Defense** — Open-AppSec ML WAF, auto IP blocking
- 🧠 **AI brain** — Local Mixtral LLM (runs offline, no API cost)
- ✈️ **Live tracking** — Flights, ships, satellites, cyber attacks on world map
- 🐛 **Bug finder** — Analyzes any APK/EXE/PHP/Python/JS for security bugs
- 🏆 **Bug bounty** — Full platform with CVSS scoring and rewards

All controlled from **one GUI application** with a dark cyberpunk interface.

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
│ SQLMap   │ pefile   │Suricata  │ Shodan   │ Auto-IP  │ Ships   │
│ Hydra    │capstone  │ LSTM     │theHarves │  Block   │Satellite│
│ ZAP      │ XGen-Q   │  ML IDS  │ CyNER    │          │Cyber Map│
│ MSF      │          │          │          │          │         │
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

Run real penetration tests against any IP or web app. The AI guides each step, explains every finding, and auto-generates a fix report.

| Feature | Tool | What It Does |
|---------|------|--------------|
| Port & Service Scan | **Nmap** `-sV -sC` | Scans all 65535 ports, detects service versions |
| CVE Detection | Nmap + vulners.nse | Auto-matches services to known CVE database |
| SQL Injection | **SQLMap** | Tests every parameter for SQL injection |
| Full Web App Scan | **OWASP ZAP** API | DAST scan — XSS, CSRF, injections, misconfigs |
| Brute Force | **Hydra** | Tests SSH, FTP, HTTP login with wordlists |
| Auto Exploitation | **Metasploit + DeepExploit** | AI picks best exploit for detected vulns |
| Pentest Workflow | PentestGPT logic + LLM | Recon → scan → exploit → report, AI-guided |
| Fix Suggestions | Mixtral LLM | Patch recommendation for every finding |

**Flow:**
```
Target IP/URL → Nmap scan → CVE match → SQLMap test → ZAP DAST
      → DeepExploit → LLM explains all → Risk report
```

---

### 🦠 2. Malware Analysis Engine

Upload any file — analyze it without executing it. Finds trojans, ransomware, spyware, backdoors.

| Feature | Tool | What It Does |
|---------|------|--------------|
| Signature Scan | **YARA** (1000+ rules) | Matches against known malware families |
| Binary Parsing | **pefile** | PE headers, imports, exports, sections, entropy |
| Disassembly | **capstone** | Readable assembly code from binary |
| String Extraction | Custom extractor | Finds URLs, IPs, registry keys, passwords in binary |
| Behavior Analysis | **XGen-Q** model | Identifies ransomware, keylogger, botnet patterns |
| ASLR / DEP check | pefile flags | Checks if binary has exploit mitigations |
| Risk Score | Weighted scorer | 0–100 score: CLEAN / LOW / MEDIUM / HIGH / CRITICAL |
| AI Explanation | Mixtral LLM | "This file is a keylogger that exfiltrates to 1.2.3.4" |

**Supported:** `.exe` `.dll` `.bin` `.so` `.apk` `.py` `.js` `.php` `.docx` `.pdf`

---

### 🌐 3. Network IDS & Live Attack Map

Monitors your network in real time. Detects attacks as they happen. Shows them on a live world map.

| Feature | Tool | What It Does |
|---------|------|--------------|
| Packet Capture | **Scapy** | Sniffs all packets on selected network interface |
| IDS Rules Engine | **Suricata** | 40,000+ rules — detects DDoS, exploits, scans |
| Traffic Logging | **Zeek** | Structured logs of every connection |
| Anomaly Detection | **LSTM Autoencoder** | Deep learning finds traffic patterns that don't fit normal |
| Phishing Detection | **DQN RL model** | Classifies phishing URLs in real time |
| Live Attack Map | Custom canvas widget | Animated world map — shows attack source → target arrows |
| Auto Block | Defense Engine | Blocks attacker IP via firewall rule instantly |
| AI Explanation | Mixtral LLM | Names attack type and recommends response |

> ⚠️ Requires admin/root privileges for packet capture.

---

### 🕵️ 4. OSINT Investigation Engine

Enter any IP, domain, email, phone, or username — get a complete intelligence profile.

| Feature | Tool | What It Does |
|---------|------|--------------|
| Automated Recon | **SpiderFoot** | 200+ OSINT sources queried automatically |
| Email & Subdomain Hunt | **theHarvester** | Finds emails, subdomains, employees linked to target |
| Exposed Services | **Shodan API** | Finds open ports, vulns, banners indexed globally |
| AI Entity Extraction | **CyNER** (NER model) | Pulls IPs, CVEs, domain names, hashes from any text |
| WHOIS / DNS History | SecurityTrails API | Full DNS records, historical WHOIS, subdomain list |
| Breach Check | HaveIBeenPwned API | Checks if email/password appeared in known data breaches |
| Threat Correlation | Mixtral LLM | Links all OSINT findings to threat actors, campaigns |

---

### 🛡️ 5. Defense Engine & WAF

Protects your servers from attacks in real time with a machine learning firewall.

| Feature | Tool | What It Does |
|---------|------|--------------|
| ML Web Firewall | **Open-AppSec** | Blocks SQLi, XSS, RCE, path traversal, SSRF |
| Auto-Learning Mode | Open-AppSec | Learns what's normal traffic, auto-blocks anomalies |
| IP Reputation Block | AbuseIPDB + custom | Blocks known bad IPs before they connect |
| Rate Limiting | Defense Engine | Stops brute force and DDoS at application layer |
| Geo-Blocking | GeoIP engine | Block traffic from specific countries |
| Threat DB | PostgreSQL | Every blocked attack saved with full context |
| Alert on Block | Telegram/Email | Instantly notified when attack blocked |

---

### 🧠 6. Threat Intelligence Engine

Cross-references all findings across every module against global threat databases.

| Feature | Tool | What It Does |
|---------|------|--------------|
| IOC Management | **MISP** | Open threat intel platform — stores IPs, hashes, domains |
| Attack Graph | **OpenCTI** | Visualizes threat actor → TTP → IOC relationships |
| IOC Lookup | MISP API | Instantly checks if any finding is a known threat |
| Graph DB | **Neo4j** | Stores attack chains and actor relationships as graph |
| Cross-module | All engines | Network finds IP → OSINT checks it → MISP confirms threat |
| OTX Feeds | AlienVault OTX | Live threat intel pulses from 100,000+ security researchers |

---

### 📊 7. SOC / SIEM Layer

Full Security Operations Center in your desktop. Monitor, detect, and respond to breaches.

| Feature | Tool | What It Does |
|---------|------|--------------|
| Log Collection | **Wazuh** agent | Collects OS logs, app logs, security events |
| Log Indexing | **Elasticsearch** | Search through millions of log lines in milliseconds |
| Anomaly Detection | LSTM + scikit-learn | Finds unusual patterns in login/file/network logs |
| Real-time Alerts | FastAPI WebSocket | Pushes live alerts to GUI panel |
| Auto IP Block | Wazuh active-response | Blocks attacker IP the moment attack detected |
| Brute Force Detect | Wazuh rules | Triggers on 5+ failed logins in 30 seconds |
| Dashboard | GUI panel | Live event feed, severity counters, sparkline charts |

---

### 🏆 8. Bug Bounty Platform

A complete vulnerability disclosure and reward platform built in.

| Feature | What It Does |
|---------|--------------|
| Bug Submission | Researchers submit via GUI form or REST API (`POST /bounty/submit`) |
| AI Validation | LLM reads report and confirms it's a real, exploitable vulnerability |
| CVSS v3.1 Auto-Score | System calculates severity score automatically |
| Duplicate Detection | SHA256 hash of bug description — rejects identical submissions |
| PoC Upload | Attach screenshots, video, exploit code |
| Auto Severity | CRITICAL / HIGH / MEDIUM / LOW / INFORMATIONAL |
| Admin Panel | Approve, reject, request more info per report |
| Reward Tracker | Track how much paid, to whom, leaderboard of top researchers |
| REST API | Full CRUD API at `http://localhost:8001/docs` |

---

### 🐛 9. App Bug Analyzer

Drop any application file or folder — DAVID finds every security bug and tells you exactly how to fix it, with line numbers.

| Input | What Gets Analyzed |
|-------|--------------------|
| `.apk` | AndroidManifest.xml, Java/Kotlin code, resource files |
| `.exe` / `.dll` | PE headers, ASLR/DEP/GS flags, YARA, binary strings |
| `.php` | SQLi, RFI, eval, shell_exec, open redirect, weak hash, session bugs |
| `.py` | Hardcoded secrets, debug=True, eval, unsafe pickle, bare except |
| `.js` / `.ts` | XSS sinks (innerHTML), localStorage tokens, eval, HTTP URLs |
| `.java` / `.kt` | SQL concat, ProcessBuilder, SecureRandom, debuggable=true |
| URL | Missing security headers, error messages, cookie flags, mixed content |
| Folder / ZIP | Recursively scans every file inside |

**Each bug report gives:**
- ⚠️ Severity — CRITICAL / HIGH / MEDIUM / LOW / INFO
- 📁 File name + exact line number
- 💻 The actual code that triggered the bug
- ✅ Fix suggestion — exactly what to change
- 📊 CVSS score estimate (e.g. `9.0–10.0`)
- 📄 Export to HTML or JSON report

```bash
# CLI usage
python engines/bug_analyzer.py app-release.apk
python engines/bug_analyzer.py https://yoursite.com
python engines/bug_analyzer.py C:\projects\myapp\
```

---

### 🌍 10. Live Cyber Attack Map

A real-time animated world map showing global cyber attacks as they happen — like Norse Attack Map, built into DAVID.

| Feature | How It Works |
|---------|--------------|
| **Live attack feed** | Pulls from AbuseIPDB, OTX, MISP live feeds |
| **World map canvas** | Tkinter/PIL world map with country outlines |
| **Animated arrows** | Red lines fly from attacker country → target country |
| **Attack labels** | Shows attack type (DDoS, SQLi, Brute Force, Malware) |
| **Local alerts** | If your IP is targeted — red alert popup |
| **Attack counter** | Live count of attacks per second / per hour |
| **Filter by type** | Show only DDoS, or SQLi, or malware, etc. |
| **Heatmap mode** | Countries colored by attack volume (green → yellow → red) |

---

### ✈️ 11. Live Flight Tracking

Track any aircraft in real time anywhere in the world.

| Feature | Details |
|---------|---------|
| **Data source** | OpenSky Network API (free account) |
| **Map** | Interactive canvas map with aircraft icons |
| **Search** | By callsign, ICAO24, airline, country, or area |
| **Live data** | Position, altitude, speed, heading, squawk code |
| **Flight path** | Shows last 30 minutes of flight path |
| **Auto-refresh** | Updates every 10 seconds |
| **Alert mode** | Alert when specific flight enters your area |

```python
# Example: Track Air India 101
flight_tracker.track(callsign="AIC101")
# Returns: lat, lon, altitude, speed, heading, origin, destination
```

---

### 🚢 12. Live Ship Tracking

Track vessels worldwide using AIS data.

| Feature | Details |
|---------|---------|
| **Data source** | MarineTraffic API + public AIS feeds |
| **Search** | By vessel name, MMSI, IMO number, flag state |
| **Live data** | Position, speed, heading, destination port, ETA |
| **Ship types** | Cargo, tanker, passenger, fishing, naval, etc. |
| **Port arrivals** | Shows ships arriving/departing any port |
| **World map** | Ships shown as icons on interactive map |
| **Route history** | Last 24 hours of vessel route |

```python
# Example: Track by MMSI
ship_tracker.track(mmsi="235009998")
# Returns: vessel name, position, speed, destination, ETA
```

---

### 🛰️ 13. Live Satellite Tracking

Track any satellite or space station in real time.

| Feature | Details |
|---------|---------|
| **Data source** | CelesTrak TLE data (free, no key) + N2YO API |
| **Propagation** | Skyfield library — accurate orbital mechanics |
| **Search** | By satellite name, NORAD ID, or category |
| **Categories** | ISS, weather, GPS, spy sats, Starlink, amateur |
| **Live position** | Lat, lon, altitude, velocity, pass times |
| **Orbital path** | Shows ground track on world map |
| **Next pass** | Calculates next pass over your location |
| **Popular presets** | ISS, Hubble, NOAA-19, GPS Block III, Starlink |

```python
# Example: Track ISS
satellite_tracker.track(norad_id=25544)   # ISS
# Returns: lat=28.3, lon=77.1, altitude=408km, speed=7.66km/s
```

---

### 📍 14. IP Geolocation

Map any IP address to its physical location and network info.

| Feature | Details |
|---------|---------|
| **Data source** | ip-api.com (free, no key required) |
| **Returns** | Country, city, ISP, ASN, timezone, lat/lon |
| **Threat check** | Cross-checks with AbuseIPDB + OTX |
| **Map pin** | Shows IP location on world map |
| **Bulk lookup** | Upload a list of IPs — geolocate all at once |
| **Reverse DNS** | Hostname lookup included |

---

### ⚙️ 15. Automation & Alerting

Set it and forget it — DAVID monitors and alerts automatically.

| Feature | What It Does |
|---------|--------------|
| **Scheduled Scans** | Run any module on a schedule (every hour, daily, weekly) |
| **Telegram Alerts** | Instant message on CRITICAL/HIGH threat |
| **Email Alerts** | SMTP email with full threat report attached |
| **Auto IP Block** | Blocks attacking IPs automatically — no human needed |
| **Auto Patch Reports** | Generates fix report for every vulnerability found |
| **Watchlist Alerts** | Alert when a specific IP/domain appears in any scan |

---

## 🔑 Required API Keys

All keys go in your `.env` file. Most are **free**.

### 🟢 100% Free — No Credit Card

| Service | What For | Get It Here | `.env` Key |
|---------|---------|------------|------------|
| **Shodan** | Open ports / exposed services | [shodan.io](https://account.shodan.io/register) → My Account | `SHODAN_API_KEY` |
| **ip-api.com** | IP geolocation | ❌ No key needed | — |
| **OpenSky Network** | Live flight tracking | [opensky-network.org](https://opensky-network.org) → Register | `OPENSKY_USER` + `OPENSKY_PASS` |
| **CelesTrak** | Satellite TLE data | ❌ No key needed | — |
| **theHarvester** | OSINT email/subdomain | Built-in tool | — |
| **OWASP ZAP** | Web app scanner | [zaproxy.org](https://zaproxy.org/download/) | `ZAP_URL` + `ZAP_API_KEY` |
| **MISP** | Threat intelligence | Self-host: `docker-compose up` | `MISP_URL` + `MISP_KEY` |
| **OpenCTI** | Threat graph | Self-host: Docker | `OPENCTI_URL` + `OPENCTI_KEY` |
| **Wazuh** | SIEM / log analysis | Self-host: [wazuh.com](https://wazuh.com) | `WAZUH_URL` + `WAZUH_USER` + `WAZUH_PASS` |
| **Telegram Bot** | Attack alerts | [@BotFather](https://t.me/botfather) → /newbot | `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` |

### 🟡 Freemium — Free Tier Available

| Service | Free Limit | Get It Here | `.env` Key |
|---------|-----------|------------|------------|
| **VirusTotal** | 500 req/day | [virustotal.com](https://www.virustotal.com/gui/join-us) | `VIRUSTOTAL_API_KEY` |
| **AbuseIPDB** | 1,000 req/day | [abuseipdb.com](https://www.abuseipdb.com/account/api) | `ABUSEIPDB_API_KEY` |
| **AlienVault OTX** | Unlimited | [otx.alienvault.com](https://otx.alienvault.com) | `OTX_API_KEY` |
| **HaveIBeenPwned** | Read API free | [haveibeenpwned.com](https://haveibeenpwned.com/API/Key) | `HIBP_API_KEY` |
| **SecurityTrails** | 50 queries/month | [securitytrails.com](https://securitytrails.com) | `SECURITYTRAILS_KEY` |
| **N2YO** | 1,000 req/hour | [n2yo.com](https://www.n2yo.com/login/?action=register) | `N2YO_API_KEY` |
| **MarineTraffic** | Limited free | [marinetraffic.com](https://www.marinetraffic.com/en/p/api-services) | `MARINETRAFFIC_KEY` |

### 🔴 Optional / Paid

| Service | Cost | Why | `.env` Key |
|---------|------|-----|------------|
| **Cloudflare** | Free with account | WAF stats if site on CF | `CLOUDFLARE_API_TOKEN` |
| **Shodan Membership** | $69/month | More historical data | `SHODAN_API_KEY` |
| **OpenAI GPT-4** | Pay-per-token | Alternative to local LLM | `OPENAI_API_KEY` |
| **SMTP / Gmail** | Free | Email alerts | `SMTP_USER` + `SMTP_PASS` |

> ✅ **The entire system works with ZERO paid APIs.** All core features run on free/self-hosted tools.

---

## 📋 Complete `.env` Template

Copy `.env.example` to `.env` and fill in your keys:

```env
# ── AI / LLM (runs offline, no API cost) ────────────
LLM_MODEL_PATH=models/mixtral.gguf
LLM_MODEL_TYPE=mistral

# ── Offensive Tools ──────────────────────────────────
ZAP_URL=http://localhost:8080
ZAP_API_KEY=your_zap_api_key

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
SMTP_USER=you@gmail.com
SMTP_PASS=your_app_password
ALERT_EMAIL=alerts@yourdomain.com

# ── Optional ─────────────────────────────────────────
CLOUDFLARE_API_TOKEN=your_cloudflare_token
OPENAI_API_KEY=your_openai_key

# ── Databases ────────────────────────────────────────
POSTGRES_URL=postgresql://user:pass@localhost/david_db
ELASTICSEARCH_URL=http://localhost:9200
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=your_neo4j_password
```

---

## 🗄️ Data Layer

| Database | Purpose |
|----------|---------|
| **PostgreSQL** | Threat data, bug reports, users, reward tracking |
| **Elasticsearch** | Log indexing, SIEM search, full-text queries |
| **Neo4j** | Threat graphs, attack chains, IOC relationships |
| **SQLite** | Local cache, offline bug bounty DB |
| **JSON files** | Fast module output cache, config store |

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
# 1. Clone the repository
git clone https://github.com/david0154/david-cyber-intelligence-system
cd david-cyber-intelligence-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up config
cp .env.example .env
# Edit .env and add your API keys

# 4. Launch GUI (recommended)
python launcher.py

# OR: Launch directly
python gui_app.py

# OR: CLI mode
python main.py

# OR: REST API
uvicorn core.api:app --reload --port 8000

# OR: Bug Bounty API
uvicorn bounty.api:app --reload --port 8001
```

---

## 💿 Install as Normal Software

### 🪟 Windows (one-click install)

```bat
:: Right-click → Run as Administrator
install.bat
```

Creates Desktop shortcut + Start Menu entry. Double-click **DAVID CIS** to open.

### 🐧 Linux

```bash
bash install.sh
# Creates desktop icon in app menu and ~/Desktop
```

### 🍎 macOS

```bash
bash install.sh
# Creates DAVID CIS.command on Desktop — double-click to open
```

### 📦 Build Standalone Installer

```bash
# Builds .exe installer (Windows), .dmg (macOS), .deb + AppImage (Linux)
python build_exe.py
```

Outputs:
- `dist/DAVID-CIS-1.0.0-Setup.exe` — Windows installer
- `dist/DAVID-CIS-1.0.0.dmg` — macOS disk image
- `dist/david-cis_1.0.0_amd64.deb` — Debian/Ubuntu package
- `dist/DAVID-CIS-1.0.0-x86_64.AppImage` — Universal Linux

---

## 🤖 AI Natural Language Commands

Type these in the AI chat panel:

```
"Scan server 192.168.1.1"            → Full Nmap + CVE scan + AI report
"Test https://mysite.com for SQLi"   → SQLMap + OWASP ZAP scan
"Analyze malware.exe"                → YARA + pefile + behavior analysis
"Analyze app-release.apk"            → APK security audit
"Show live cyber attacks"            → Opens live attack world map
"Track flight AIC101"                → Live flight tracker
"Track ship MMSI 235009998"          → Live ship tracker
"Track ISS satellite"                → Live satellite tracker
"Check IP 1.2.3.4"                   → OSINT + Shodan + MISP lookup
"Is admin@domain.com breached?"      → HIBP breach check
"Scan PHP project for bugs"          → Bug Analyzer → finds all vulns
"Show live attack alerts"            → SOC / Wazuh SIEM panel
"Block IP 5.6.7.8"                   → Adds to firewall block list
"Generate pentest report"            → Full AI-written report
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

**DAVID CYBER INTELLIGENCE SYSTEM v1.0**
*Built with ❤️ in Kolkata, India*
*Devil Pvt Ltd & Nexuzy Tech Pvt Ltd*

</div>
