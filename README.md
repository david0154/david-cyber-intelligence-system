# 🛡️ DAVID CYBER INTELLIGENCE SYSTEM v3.0

> **Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd**  
> **A TRUE AI-Powered Cybersecurity Platform — NOT just an AI assistant**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-3.0.0-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)

---

## 🏗️ System Architecture

```
[GUI App (Tkinter)] ←→ [FastAPI Backend]
           ↓
    [AI Brain Layer]
    Mixtral GGUF + CodeBERT
           ↓
┌──────────────────────────────────────────┐
│  OFFENSIVE ENGINE    │  DEFENSIVE ENGINE  │
│  Nmap, SQLMap, ZAP   │  Wazuh, Suricata   │
│  Metasploit, Hydra   │  ELK Stack, IDS    │
├──────────────────────┴────────────────────┤
│         BUG BOUNTY PLATFORM               │
│  Submit → AI Verify → CVSS → Reward       │
├───────────────────────────────────────────┤
│  OSINT │ Tracking │ Threat Intel │ SOC    │
└───────────────────────────────────────────┘
           ↓
[PostgreSQL + Elasticsearch + Neo4j + SQLite]
```

---

## ✅ Full Feature Matrix

### 🔴 1. OFFENSIVE SECURITY ENGINE
| Feature | Tool | Status |
|---------|------|--------|
| Port & Service Scan | Nmap | ✅ |
| CVE Detection | Nmap Vulners Script | ✅ |
| Web App Testing | OWASP ZAP | ✅ |
| SQL Injection | SQLMap | ✅ |
| Brute Force Test | Hydra | ✅ |
| Auto Exploitation | DeepExploit + MSF | ✅ |
| AI Explains Results | Mixtral LLM | ✅ |
| AI Suggests Fixes | LLM Patch Engine | ✅ |

### 🛡️ 2. DEFENSIVE AI / SOC LAYER
| Feature | Tool | Status |
|---------|------|--------|
| SIEM Log Collection | Wazuh | ✅ |
| IDS/IPS | Suricata | ✅ |
| Log Indexing | Elasticsearch (ELK) | ✅ |
| Anomaly Detection | LSTM Autoencoder | ✅ |
| Behavior Analysis | ML Pipeline | ✅ |
| Real-time Alerts | WebSocket | ✅ |
| Auto IP Blocking | Defense Engine | ✅ |
| Failed Login Detection | Wazuh Rules | ✅ |

### 🧠 3. AI CYBER BRAIN
| Feature | Model | Status |
|---------|-------|--------|
| Reasoning & Explanation | Mixtral GGUF | ✅ |
| Code Vulnerability Detection | CodeBERT | ✅ |
| Phishing Detection | DQN Model | ✅ |
| Natural Language Commands | LLM Router | ✅ |
| Auto Patch Suggestions | LLM | ✅ |
| Risk Report Generation | LLM | ✅ |

### 🐞 4. BUG BOUNTY PLATFORM
| Feature | Status |
|---------|--------|
| Bug Submission Portal | ✅ |
| AI Auto-Validation | ✅ |
| CVSS v3.1 Scoring | ✅ |
| Duplicate Detection | ✅ |
| Screenshot / PoC Upload | ✅ |
| Auto Severity Classification | ✅ |
| Admin Approval Panel | ✅ |
| Reward Tracking | ✅ |

### ⚙️ 5. AUTOMATION LAYER
| Feature | Status |
|---------|--------|
| Scheduled Scans (Cron) | ✅ |
| Email Alerts | ✅ |
| Auto Patch Suggestions | ✅ |
| Threat Auto-Block | ✅ |
| Telegram Bot Alerts | ✅ |

### 🌐 6. TRACKING & INTELLIGENCE
| Feature | Source | Status |
|---------|--------|--------|
| Flight Tracking | OpenSky Network | ✅ |
| Ship Tracking | MarineTraffic / AIS | ✅ |
| Satellite Tracking | CelesTrak + Skyfield | ✅ |
| IP Geolocation | ip-api.com | ✅ |
| Threat Heatmaps | Folium | ✅ |
| OSINT Recon | Shodan + SpiderFoot | ✅ |

### 🗄️ 7. DATA LAYER
| Store | Purpose |
|-------|---------|
| PostgreSQL | Structured threat data, bug reports |
| Elasticsearch | Log indexing & SIEM search |
| Neo4j | Threat relationship graphs |
| SQLite | Local cache & bug bounty DB |

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/david0154/david-cyber-intelligence-system
cd david-cyber-intelligence-system
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run Options

**GUI App (Tkinter Desktop):**
```bash
python gui_app.py
# Windows: double-click gui_launcher.bat
```

**CLI (Terminal):**
```bash
python main.py
```

**API + Web Dashboard:**
```bash
uvicorn core.api:app --reload --host 0.0.0.0 --port 8000
# Open: http://localhost:8000
# Docs: http://localhost:8000/docs
```

**Bug Bounty API:**
```bash
uvicorn bounty.api:app --port 8001
# Open: http://localhost:8001/docs
```

---

## 📦 Tool Installation

### Linux
```bash
sudo apt install nmap ncat hydra suricata sqlmap
```

### macOS
```bash
brew install nmap hydra sqlmap
```

### Windows
- Nmap: https://nmap.org/download
- OWASP ZAP: https://zaproxy.org
- Hydra: https://github.com/vanhauser-thc/thc-hydra
- SQLMap: https://sqlmap.org
- Metasploit: https://metasploit.com

---

## 🤖 AI Commands (Natural Language)

```
"Scan my server 192.168.1.1"       → Nmap + CVE scan
"Test web app https://mysite.com"  → ZAP scan
"Check SQL injection on /login"    → SQLMap
"Show live attacks"                → Wazuh alerts
"What CVEs are on port 22?"        → AI explains
"Fix vulnerability CVE-2024-1234" → AI patch suggestion
```

---

## 🐞 Bug Bounty Flow

```
User submits bug
      ↓
AI validates (real vulnerability?)
      ↓
CVSS v3.1 auto-scored
      ↓
Duplicate check
      ↓
Admin approves
      ↓
Reward issued
```

---

## ⚠️ Legal Disclaimer

This system is for **authorized security testing only**.  
Always obtain **written permission** before scanning any system.  
Developer is not responsible for misuse.

---

## 👨‍💻 Developer

**David** — Full-Stack Security Engineer  
Nexuzy Tech Pvt Ltd | Devil Pvt Ltd  
Kolkata, West Bengal, India  
https://hypechats.com
