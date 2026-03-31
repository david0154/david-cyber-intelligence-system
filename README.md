# DAVID CYBER INTELLIGENCE SYSTEM v3.1

<div align="center">

![DAVID CIS Logo](assets/logo.jpg)

**Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-3.1.0-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-Proprietary-orange?style=for-the-badge)

> **A TRUE AI-Powered Cybersecurity Platform — Security Analysis · Defense · Bug Hunting · Tracking**

</div>

---

## 🗺️ Table of Contents

1. [Core Architecture](#-core-architecture)
2. [ALL Features Explained](#-all-features-explained)
3. [Required API Keys](#-required-api-keys--where-to-get-them)
4. [Free vs Paid APIs](#-free-vs-paid-api-summary)
5. [App Bug Analyzer](#-app-bug-analyzer-new)
6. [Data Layer](#-data-layer)
7. [Quick Start](#-quick-start)
8. [AI Commands](#-ai-natural-language-commands)
9. [Legal](#️-legal-disclaimer)

---

## 🏗️ Core Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                LLM BRAIN  (Mixtral GGUF)                     │
│                via ctransformers  (runs offline)             │
│        Intent · Reasoning · Explanation · Routing            │
└──────────────────────────┬───────────────────────────────────┘
                           │
                  ┌────────▼────────┐
                  │   TASK ROUTER   │
                  └────────┬────────┘
                           │
 ┌──────────┬──────────┬───┴──────┬──────────┬──────────┐
 │ Malware  │ Network  │  OSINT   │ Pentest  │ Defense  │
 │ Engine   │ IDS      │  Engine  │ Engine   │ Engine   │
 └──────────┴──────────┴──────────┴──────────┴──────────┘
                  ┌────────┬────────┐
                  │ Bug    │ SOC /  │
                  │Analyzer│ SIEM   │
                  └────────┴────────┘
                           │
              Threat Intelligence Layer
               (MISP + OpenCTI + Neo4j)
                           │
                  Unified Threat Score
               PostgreSQL · ELK · SQLite
```

---

## ✅ All Features Explained

### 🔴 1. Offensive Security Engine

Runs real penetration testing tools automatically. You give a target IP or URL — it scans, finds vulnerabilities, and the AI explains each one and suggests how to fix it.

| Feature | Tool Used | What It Does |
|---------|-----------|--------------|
| Port & Service Scan | **Nmap** | Scans all ports, detects running services and versions |
| CVE Detection | Nmap + vulners script | Matches services to known CVEs (e.g. CVE-2024-xxxx) |
| SQL Injection Test | **SQLMap** | Auto-tests web URLs for SQL injection vulnerabilities |
| Web App Vulnerability Scan | **OWASP ZAP** | Full DAST scan — XSS, CSRF, injections, misconfigs |
| Brute Force Test | **Hydra** | Tests login forms for weak/default passwords |
| Auto Exploitation | **DeepExploit + Metasploit** | AI selects best exploit for detected vulnerabilities |
| Pentest Workflow | PentestGPT logic | Structures full pentest: recon → scan → exploit → report |
| AI Fix Suggestions | Mixtral LLM | Explains each finding and gives a patch/fix recommendation |

> **Requires:** Nmap, SQLMap, Hydra, Metasploit installed. Use **Tool Installer tab** in GUI.

---

### 🦠 2. Malware Engine

Upload any file (`.exe`, `.dll`, `.bin`, `.apk`, script) — the engine analyzes it without running it.

| Feature | Tool Used | What It Does |
|---------|-----------|--------------|
| Signature Detection | **YARA** | Matches file against 1000s of known malware signatures |
| Binary Parsing | **pefile** | Extracts PE headers, imports, sections, metadata from EXE/DLL |
| Disassembly | **capstone** | Disassembles binary to readable assembly code |
| Behavior Analysis | **XGen-Q reasoning** | Identifies suspicious code patterns and behaviors |
| Risk Scoring | Custom scorer | 0–100 risk score based on all findings |
| AI Explanation | Mixtral LLM | Explains what the malware does in plain English |

**Flow:**
```
File → YARA signature match → pefile metadata → XGen-Q behavior → LLM explain + risk score
```

---

### 🌐 3. Network IDS Engine

Monitors your network live and detects attacks in real time.

| Feature | Tool Used | What It Does |
|---------|-----------|--------------|
| Live Packet Capture | **Scapy** | Captures all network packets on your interface |
| IDS/IPS Rules | **Suricata** | Detects DDoS, port scans, exploits using Snort-compatible rules |
| Traffic Logging | **Zeek** | Creates structured logs of all network connections |
| Anomaly Detection | **LSTM Autoencoder** | Deep learning model detects unusual traffic patterns |
| Phishing Detection | **DQN model** | RL model classifies phishing vs legitimate URLs |
| AI Explanation | Mixtral LLM | Identifies attack type and recommends blocking action |

**Flow:**
```
Network → Scapy capture → Suricata alerts → LSTM anomaly detect → LLM explain attack
```

> **Requires:** Suricata installed, Wireshark/tshark for packet capture. Run as Admin/sudo.

---

### 🕵️ 4. OSINT Investigation Engine

Give it an IP address, domain name, email, or username — it builds a full digital profile.

| Feature | Tool Used | What It Does |
|---------|-----------|--------------|
| IP/Domain Recon | **SpiderFoot** | Automated OSINT collection from 200+ sources |
| Email Harvesting | **theHarvester** | Finds emails, subdomains, IPs linked to a domain |
| Exposed Services | **Shodan API** | Shows open ports, services, vulns indexed by Shodan |
| Entity Extraction | **CyNER** | AI extracts IPs, CVEs, domains, hashes from raw text |
| Threat Correlation | Mixtral LLM | Links findings to known threat actors and patterns |

**Flow:**
```
IP / Email / Domain → OSINT tools collect → CyNER extracts entities → LLM correlates threats
```

> **Requires:** Shodan API key (free tier available).

---

### 🛡️ 5. Defense Engine (WAF + AppSec)

Actively protects your web application from attacks in real time.

| Feature | Tool Used | What It Does |
|---------|-----------|--------------|
| ML-based WAF | **Open-AppSec** | Machine learning firewall — blocks web attacks |
| Auto-learning | Open-AppSec | Learns normal traffic, auto-blocks anomalies |
| Attack Detection | Pattern + ML | Detects SQLi, XSS, RCE, path traversal, etc. |
| IP Blocking | Defense Engine | Automatically blocks attacker IPs |
| Threat Storage | PostgreSQL | Saves all attacks to database for analysis |

**Flow:**
```
Incoming Request → Open-AppSec ML → Attack detected → Block / Allow → Store in threat DB
```

---

### 🧠 6. Threat Intelligence Engine

Links all findings across all modules to known global threat data.

| Feature | Tool Used | What It Does |
|---------|-----------|--------------|
| IOC Database | **MISP** | Open-source threat intelligence sharing platform |
| Graph Intelligence | **OpenCTI** | Visualizes threat actor → attack → IOC relationships |
| IP/Hash/Domain Lookup | MISP API | Checks if an IP/hash/domain is a known threat |
| Relationship Mapping | **Neo4j** | Graph database of attack chains and threat actors |
| Cross-module correlation | All engines | If Network finds IP, OSINT checks it, MISP confirms threat |

**Flow:**
```
All modules → Store IOC in MISP → Build graph in OpenCTI → Cross-check new threats
```

> **Requires:** MISP self-hosted or MISP cloud. OpenCTI self-hosted (Docker).

---

### 📊 7. SOC / SIEM Layer

Security Operations Center capabilities — monitors logs, detects breaches, auto-responds.

| Feature | Tool Used | What It Does |
|---------|-----------|--------------|
| Log Collection & Alerts | **Wazuh** | SIEM agent collects system/app/security logs |
| Log Indexing & Search | **Elasticsearch** | Full-text search through millions of log lines |
| Anomaly Detection | LSTM + ML | Detects unusual login patterns, file changes |
| Real-time Alerts | FastAPI WebSocket | Pushes alerts to GUI/Telegram/email instantly |
| Auto IP Blocking | SOC Engine | Blocks attacking IPs automatically on HIGH/CRITICAL |
| Failed Login Detection | Wazuh rules | Detects brute force / credential stuffing |

> **Requires:** Wazuh manager running (self-hosted). Elasticsearch optionally via Docker.

---

### 🐞 8. Bug Bounty Platform

A complete platform to submit, validate, score, and reward vulnerability reports.

| Feature | What It Does |
|---------|-------------|
| Bug Submission Form | Researchers submit bugs via GUI or REST API |
| AI Auto-Validation | LLM checks if the report describes a real vulnerability |
| CVSS v3.1 Auto-Scoring | Automatically calculates severity score |
| Duplicate Detection | SHA256 hash prevents same bug submitted twice |
| Screenshot / PoC Upload | Attach proof-of-concept files |
| Auto Severity Classification | Critical / High / Medium / Low / Informational |
| Admin Approve/Reject Panel | Admin reviews and approves/rejects each report |
| Reward Tracking & Leaderboard | Track bounties paid and top researchers |

**Flow:**
```
Submit bug → AI validates → CVSS scored → Duplicate check → Admin approves → Reward issued
```

---

### 🐛 9. App Bug Analyzer *(NEW)*

Drag-and-drop any application — it finds all security bugs and tells you exactly how to fix them.

| Target | What It Analyzes |
|--------|-----------------|
| **Android APK** | AndroidManifest.xml + Java/Kotlin code — debuggable, allowBackup, world-readable files, SQLi, etc. |
| **EXE / DLL** | PE headers — ASLR, DEP, stack cookies, strings, YARA scan |
| **PHP files** | SQLi, RFI, eval, shell_exec, open redirect, weak hashing, session bugs |
| **Python files** | Hardcoded secrets, debug=True, eval, unsafe pickle, bare except |
| **JavaScript / TypeScript** | XSS sinks, localStorage tokens, HTTP URLs, eval, loose equality |
| **Java / Kotlin** | SQL concat, OS exec, SecureRandom, stack trace, debug logging |
| **URL / Web App** | HTTP headers (CSP, HSTS, X-Frame), error messages in body, cookies, mixed content |
| **Project Folder** | Recursively scans every file in the project |
| **ZIP Archive** | Extracts and scans all contents |

**Every bug report includes:**
- ✅ Severity: CRITICAL / HIGH / MEDIUM / LOW / INFO
- ✅ File + exact line number
- ✅ The code line that triggered the bug
- ✅ Fix suggestion — exactly what to change
- ✅ CVSS score estimate (e.g. `9.0–10.0`)
- ✅ Export as JSON or HTML report

**Run from command line:**
```bash
python engines/bug_analyzer.py myapp.apk
python engines/bug_analyzer.py mywebsite.php
python engines/bug_analyzer.py C:\projects\myapp\
python engines/bug_analyzer.py https://example.com
```

---

### ✈️ 10. Tracking & Geo Intelligence

| Feature | Data Source | What It Does |
|---------|-------------|--------------|
| Flight Tracking | **OpenSky Network API** | Tracks any aircraft by callsign or ICAO24 |
| Ship Tracking | **AIS / MarineTraffic** | Tracks vessels by MMSI number |
| Satellite Tracking | **CelesTrak + Skyfield** | Computes real-time satellite position by NORAD ID |
| IP Geolocation | **ip-api.com** | Maps IP to country, city, ISP, lat/long |

---

### ⚙️ 11. Automation & Alerting

| Feature | What It Does |
|---------|-------------|
| Scheduled Scans | Auto-scan targets at set intervals (background thread) |
| Email Alerts | SMTP alert on HIGH/CRITICAL threat detected |
| Telegram Bot Alerts | Instant message to your Telegram when attack detected |
| Auto Patch Suggestions | AI generates fix recommendation for every finding |
| Auto IP Block | Blocks attacker IP automatically on CRITICAL threat |

---

## 🔑 Required API Keys — Where to Get Them

These are ALL the API keys used by DAVID. Put them in your `.env` file.

### 🟢 Free APIs (No Payment Needed)

| API Key Name | Service | How to Get | `.env` Variable |
|-------------|---------|-----------|-----------------|
| Shodan Free | Shodan — shows open ports/services for any IP | Sign up at [shodan.io](https://account.shodan.io/register) → My Account → API Key | `SHODAN_API_KEY` |
| ip-api | IP Geolocation (city, country, ISP) | **No key needed** — free up to 1000/day | *(none)* |
| OpenSky Network | Live flight data | Sign up at [opensky-network.org](https://opensky-network.org/index.php?option=com_users&view=registration) | `OPENSKY_USER` + `OPENSKY_PASS` |
| CelesTrak | Satellite TLE data | **No key needed** — public API | *(none)* |
| theHarvester | Email/subdomain OSINT | Built-in tool — no key needed | *(none)* |
| MISP (self-hosted) | Threat intelligence | Deploy via Docker: `docker-compose up` | `MISP_URL` + `MISP_KEY` |
| OpenCTI (self-hosted) | Threat graph | Deploy via Docker | `OPENCTI_URL` + `OPENCTI_KEY` |
| Wazuh (self-hosted) | SIEM / log analysis | Deploy free: [wazuh.com/install](https://documentation.wazuh.com/current/installation-guide/) | `WAZUH_URL` + `WAZUH_USER` + `WAZUH_PASS` |
| OWASP ZAP | Web app scanner | Download free: [zaproxy.org](https://www.zaproxy.org/download/) then start daemon | `ZAP_URL` + `ZAP_API_KEY` |

---

### 🟡 Freemium APIs (Free Tier Available)

| API Key Name | Service | Free Tier | How to Get | `.env` Variable |
|-------------|---------|-----------|-----------|-----------------|
| Shodan Membership | More scan results | Free = 1 API credit/month | [shodan.io/store](https://shodan.io/store) | `SHODAN_API_KEY` |
| VirusTotal | File/URL malware scan | 500 requests/day free | [virustotal.com/gui/join-us](https://www.virustotal.com/gui/join-us) → API Key | `VIRUSTOTAL_API_KEY` |
| AbuseIPDB | Check if IP is malicious | 1000/day free | [abuseipdb.com/account/api](https://www.abuseipdb.com/account/api) | `ABUSEIPDB_API_KEY` |
| AlienVault OTX | Threat intel / IOCs | Free account | [otx.alienvault.com](https://otx.alienvault.com) → API Keys | `OTX_API_KEY` |
| SecurityTrails | DNS/WHOIS history | 50 queries/month free | [securitytrails.com](https://securitytrails.com) → Sign up | `SECURITYTRAILS_KEY` |
| HaveIBeenPwned | Check email breaches | Free read API | [haveibeenpwned.com/API/Key](https://haveibeenpwned.com/API/Key) | `HIBP_API_KEY` |
| N2YO | Satellite real-time tracking | 1000 req/hour free | [n2yo.com/login/](https://www.n2yo.com/login/?action=register) | `N2YO_API_KEY` |
| MarineTraffic | Ship tracking | Limited free | [marinetraffic.com/en/p/api-services](https://www.marinetraffic.com/en/p/api-services) | `MARINETRAFFIC_KEY` |

---

### 🔴 Paid / Optional APIs

| API Key Name | Service | Cost | Why Needed | `.env` Variable |
|-------------|---------|------|-----------|-----------------|
| Shodan Enterprise | Deep scan / historical | $69/month | More scan data | `SHODAN_API_KEY` |
| Cloudflare API | WAF stats, zone analytics | Free with CF account | If your site uses Cloudflare | `CLOUDFLARE_API_TOKEN` |
| OpenAI API | Alternative LLM (GPT-4) | Pay-per-token | Only if not using local Mixtral | `OPENAI_API_KEY` |
| Telegram Bot | Alert notifications | **Free** | Create bot via [@BotFather](https://t.me/botfather) | `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` |
| SMTP Email | Alert emails | Free (Gmail/SMTP) | For email alerts | `SMTP_USER` + `SMTP_PASS` + `ALERT_EMAIL` |

---

## 💰 Free vs Paid API Summary

| Category | Free Option | What You Miss Without Paying |
|----------|-------------|------------------------------|
| Threat Intel | AbuseIPDB + OTX + MISP (self-hosted) | Historical attack data, premium feeds |
| Port Scanning | Nmap (local) | Nothing — Nmap is 100% free |
| Web Scanning | OWASP ZAP (local) | Nothing — ZAP is 100% free |
| Malware Scan | YARA + pefile (local) | Cloud scan speed via VirusTotal |
| IP Lookup | ip-api.com | Nothing — fully free |
| LLM / AI | Mixtral GGUF (offline, local) | Nothing — runs on your machine |
| SIEM | Wazuh (self-hosted, free) | Enterprise support |
| Shodan | 1 credit/month free | Historical data, more results |
| Tracking | OpenSky (free) + CelesTrak (free) | Real-time AIS ship tracking |

> ✅ **Core system works 100% with zero paid APIs.** Paid APIs only add more data.

---

## 📋 Complete `.env` File Template

```env
# ── LLM ─────────────────────────────────────────────
LLM_MODEL_PATH=models/mixtral.gguf
LLM_MODEL_TYPE=mistral

# ── Security Tools ───────────────────────────────────
ZAP_URL=http://localhost:8080
ZAP_API_KEY=your_zap_api_key_here

WAZUH_URL=https://localhost:55000
WAZUH_USER=wazuh
WAZUH_PASS=your_wazuh_password

# ── Threat Intelligence ──────────────────────────────
SHODAN_API_KEY=your_shodan_key            # shodan.io
VIRUSTOTAL_API_KEY=your_vt_key            # virustotal.com
ABUSEIPDB_API_KEY=your_abuseipdb_key      # abuseipdb.com
OTX_API_KEY=your_otx_key                  # otx.alienvault.com
SECURITYTRAILS_KEY=your_st_key            # securitytrails.com
HIBP_API_KEY=your_hibp_key                # haveibeenpwned.com

MISP_URL=https://your-misp-instance
MISP_KEY=your_misp_auth_key

OPENCTI_URL=http://localhost:8080
OPENCTI_KEY=your_opencti_key

# ── Tracking ─────────────────────────────────────────
OPENSKY_USER=your_opensky_username        # opensky-network.org
OPENSKY_PASS=your_opensky_password
N2YO_API_KEY=your_n2yo_key               # n2yo.com
MARINETRAFFIC_KEY=your_mt_key            # marinetraffic.com

# ── Cloudflare (optional) ────────────────────────────
CLOUDFLARE_API_TOKEN=your_cf_token        # cloudflare.com → My Profile → API Tokens

# ── Alerts ───────────────────────────────────────────
TELEGRAM_BOT_TOKEN=your_bot_token         # t.me/botfather
TELEGRAM_CHAT_ID=your_chat_id
SMTP_USER=your@gmail.com
SMTP_PASS=your_app_password
ALERT_EMAIL=alert@yourdomain.com

# ── Database ─────────────────────────────────────────
POSTGRES_URL=postgresql://user:pass@localhost/david_db
ELASTICSEARCH_URL=http://localhost:9200
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=your_neo4j_password
```

---

## 🗄️ Data Layer

| Storage | Purpose |
|---------|---------|
| **PostgreSQL** | Structured threat data, bug reports, users, rewards |
| **Elasticsearch** | Log indexing, SIEM search, full-text log queries |
| **Neo4j** | Threat relationship graphs, attack chains, IOC links |
| **SQLite** | Local cache, quick bug bounty DB |
| **JSON** | Fast module output cache |

---

## 🔄 Full Execution Flow

```
User Input (IP / File / URL / Log / Text)
        ↓
LLM Brain (understands intent)
        ↓
Task Router (selects right engine)
        ↓
Engine runs tool + AI model
        ↓
Threat Intel cross-check (MISP / OTX / AbuseIPDB)
        ↓
LLM merges all results
        ↓
Final Output:
  ✅ Threat Score (0–100)
  ✅ Attack type + explanation
  ✅ Fix / patch suggestion
  ✅ IOC stored to DB
  ✅ Alert sent (Telegram / email)
```

---

## 🚀 Quick Start

See **[SETUP.md](SETUP.md)** for full installation.

```bash
# Clone
git clone https://github.com/david0154/david-cyber-intelligence-system
cd david-cyber-intelligence-system

# Install Python dependencies
pip install -r requirements.txt

# Copy and fill your API keys
cp .env.example .env

# ── Launch Options ──────────────────────────────────
# GUI Desktop App (recommended for non-tech users)
python gui_app.py

# CLI
python main.py

# REST API
uvicorn core.api:app --reload --port 8000

# Bug Bounty API
uvicorn bounty.api:app --reload --port 8001

# Bug Analyzer CLI
python engines/bug_analyzer.py /path/to/app.apk
python engines/bug_analyzer.py https://yoursite.com
```

**First-time setup (GUI):**
1. Open app → click **📦 Tool Installer** tab
2. Click **▶ INSTALL ALL** → all tools auto-install
3. Click **⚙️ Settings** → fill in API keys → click **Save**
4. Go to **🔧 Modules** → select any module → click **▶ RUN**

---

## 🤖 AI Natural Language Commands

```bash
"Scan my server 192.168.1.1"        → Nmap + CVE scan + AI report
"Test web app https://mysite.com"   → ZAP + SQLMap + AI fixes
"Analyze this file malware.exe"     → YARA + pefile + risk score
"Analyze my APK app.apk"            → Bug Analyzer → full security report
"Show live attacks"                 → Wazuh SIEM alerts
"Check IP 1.2.3.4"                  → OSINT + MISP + Shodan
"Fix vulnerability CVE-2024-1234"   → AI patch suggestion
"What ships are near Mumbai?"       → AIS ship tracking
"Is this email breached?"           → HIBP check
"Scan my PHP project for bugs"      → Bug Analyzer → finds SQLi, XSS, RFI
```

---

## ⚠️ Legal Disclaimer

> This system is for **authorized security testing only**.  
> Always obtain **written permission** before scanning any system.  
> Unauthorized use is illegal. The developer is not responsible for misuse.

---

## 👨‍💻 Developer

**David**  
Full-Stack Security Engineer  
Nexuzy Tech Pvt Ltd | Devil Pvt Ltd  
Kolkata, West Bengal, India  
https://hypechats.com
