# 🛠️ SETUP GUIDE — DAVID CYBER INTELLIGENCE SYSTEM v2.0.0

<div align="center">

**Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd**  
**Kolkata, West Bengal, India**

</div>

---

## 📋 Table of Contents

1. [System Requirements](#-system-requirements)
2. [Step 1 — Clone Repository](#-step-1--clone-repository)
3. [Step 2 — Python Dependencies](#-step-2--python-dependencies)
4. [Step 3 — Configure Environment](#️-step-3--configure-environment)
5. [Step 4 — Install External Security Tools](#-step-4--install-external-security-tools)
6. [Step 5 — Auto Tool Installer](#-step-5--auto-tool-installer)
7. [Step 6 — Download AI Model](#-step-6--download-ai-model)
8. [Step 7 — Database Setup](#️-step-7--database-setup)
9. [Step 8 — Run the System](#-step-8--run-the-system)
10. [Step 9 — Enable Auto Scans & Alerts](#-step-9--enable-auto-scans--alerts)
11. [Step 10 — Verify Everything Works](#-step-10--verify-everything-works)
12. [Project Structure](#️-project-structure)
13. [Troubleshooting](#-troubleshooting)

---

## 💻 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10 | 3.11+ |
| RAM | 4 GB | 16 GB (for LLM) |
| Disk Space | 5 GB | 20 GB (models + logs) |
| OS | Win 10 / Ubuntu 20.04 / macOS 12 | Latest stable |
| pip | 23+ | Latest |
| Git | Any | Latest |

> ⚠️ Nmap, Hydra, SQLMap, ZAP require admin/root privileges for full functionality on Linux/macOS.

---

## ⚡ Step 1 — Clone Repository

```bash
git clone https://github.com/david0154/david-cyber-intelligence-system
cd david-cyber-intelligence-system
```

---

## 📦 Step 2 — Python Dependencies

```bash
pip install -r requirements.txt
```

### Platform-specific fixes

**Windows — yara-python build error:**
```bat
pip install yara-python --no-binary yara-python
```

**Linux — Tkinter missing:**
```bash
sudo apt install python3-tk
```

**macOS — SSL cert errors:**
```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

---

## ⚙️ Step 3 — Configure Environment

```bash
# Copy the template
cp .env.example .env

# Edit with your values
nano .env          # Linux / macOS
notepad .env       # Windows
```

### Essential keys — minimum to get started

| Key | Required For | Where to get |
|-----|-------------|---------------|
| `SHODAN_API_KEY` | OSINT engine | [shodan.io](https://shodan.io) — free account |
| `ZAP_URL` / `ZAP_API_KEY` | Web scanning | Start ZAP → Tools → Options → API |
| `WAZUH_URL/USER/PASS` | SIEM alerts | Your Wazuh server |
| `CLOUDFLARE_API_TOKEN` | WAF + IP block | Cloudflare Dashboard → API Tokens |
| `TELEGRAM_BOT_TOKEN` | Instant alerts | @BotFather on Telegram |
| `SMTP_HOST` | Email alerts | e.g. `smtp.gmail.com` |
| `SMTP_PORT` | Email alerts | `587` for Gmail TLS |
| `SMTP_USER` / `SMTP_PASS` | Email alerts | Gmail App Password |
| `ABUSEIPDB_API_KEY` | IP reputation | [abuseipdb.com](https://abuseipdb.com) |
| `OTX_API_KEY` | Threat feeds | [otx.alienvault.com](https://otx.alienvault.com) |
| `N2YO_API_KEY` | Satellite tracking | [n2yo.com/api](https://n2yo.com/api/) |
| `LLM_MODEL_PATH` | AI reasoning | See Step 6 below |

> 💡 All keys are **optional** — the system degrades gracefully without them. Core scanners (Nmap, YARA) work with zero API keys.

---

## 🔧 Step 4 — Install External Security Tools

DAVID CIS uses these CLI tools as subprocess backends. Install them before running scans.

### 🐧 Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install -y nmap hydra suricata sqlmap ncat zeek

# Metasploit Framework
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall && sudo ./msfinstall

# OWASP ZAP
sudo snap install zaproxy --classic
# or download from: https://zaproxy.org/download/

# OpenVAS (GVM)
sudo apt install openvas
sudo gvm-setup
sudo gvm-start
```

### 🍎 macOS

```bash
brew install nmap sqlmap
brew install --cask owasp-zap

# Hydra
brew install thc-hydra

# Metasploit
brew install --cask metasploit
```

### 🪟 Windows

| Tool | Download Link | Notes |
|------|--------------|-------|
| **Nmap** | [nmap.org/download](https://nmap.org/download) | Add to PATH during install |
| **OWASP ZAP** | [zaproxy.org](https://zaproxy.org) | Run before scanning |
| **Hydra** | [GitHub releases](https://github.com/vanhauser-thc/thc-hydra/releases) | Or use WSL |
| **SQLMap** | [sqlmap.org](https://sqlmap.org) | Requires Python |
| **Metasploit** | [metasploit.com/download](https://metasploit.com/download) | MSI installer |
| **Suricata** | [suricata.io](https://suricata.io/download/) | IDS/IPS engine |
| **Zeek** | [zeek.org](https://zeek.org/get-zeek/) | Network traffic logger |

> ✅ After installing, verify each tool:
> ```bash
> nmap --version
> hydra -h
> sqlmap --version
> ```

---

## 🤖 Step 5 — Auto Tool Installer

DAVID CIS ships with `tools_installer.py` — a built-in auto-installer that detects your OS and installs all external dependencies automatically.

```bash
# Auto-detect OS and install all tools
python tools_installer.py

# Install only specific tools
python tools_installer.py --tools nmap,hydra,zap

# Check what's installed / missing
python tools_installer.py --check

# Verbose mode
python tools_installer.py --verbose
```

The installer handles:
- Nmap, Hydra, SQLMap, Suricata, Zeek
- OWASP ZAP download
- Metasploit package
- SpiderFoot and theHarvester
- Python YARA rules update

> 💡 Run this once after `pip install -r requirements.txt` — it saves manual setup.

---

## 🧠 Step 6 — Download AI Model

DAVID CIS uses a local **Mixtral / Mistral GGUF** model — it runs 100% offline, no API key needed.

```bash
# Create models directory
mkdir -p models
cd models
```

### Recommended models

| Model | Size | Speed | Quality | Command |
|-------|------|-------|---------|----------|
| Mistral 7B Q4 | ~4 GB | Fast | Good | `wget https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf` |
| Mixtral 8x7B Q4 | ~26 GB | Slow | Best | Download from [TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF) |
| Phi-2 Q4 | ~2 GB | Fastest | Basic | `wget https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf` |

```bash
# Recommended for most systems (4GB, good quality)
wget https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf
```

Then update `.env`:
```env
LLM_MODEL_PATH=models/mistral-7b-v0.1.Q4_K_M.gguf
LLM_MODEL_TYPE=mistral
LLM_MAX_TOKENS=512
```

### Running without a model

If `models/mixtral.gguf` is **missing**, DAVID CIS still works:
- All scanners, APIs, tracking, and alerts run normally
- LLM features return a stub message with the HuggingFace download link
- No crash — graceful offline fallback built into `core/llm_brain.py`

---

## 🗄️ Step 7 — Database Setup

All databases are **optional** — the system falls back to SQLite + local JSON files automatically.

### PostgreSQL (full threat storage)

```bash
# Install
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# Create database and user
sudo -u postgres psql << 'EOF'
CREATE DATABASE david_db;
CREATE USER cyberuser WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE david_db TO cyberuser;
EOF

# Update .env
POSTGRES_URL=postgresql://cyberuser:your_secure_password@localhost:5432/david_db
```

### Elasticsearch (SIEM log indexing)

```bash
# Install
sudo apt install elasticsearch
sudo systemctl enable --now elasticsearch

# Verify
curl http://localhost:9200/_cluster/health?pretty

# Update .env
ELASTICSEARCH_URL=http://localhost:9200
```

### Neo4j (threat graph relationships)

```bash
# Install
sudo apt install neo4j
sudo systemctl enable --now neo4j

# Default login: neo4j / neo4j — change on first login
# Update .env
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=your_neo4j_password
```

### Wazuh SIEM (log collection agent)

```bash
# Install Wazuh agent (Linux)
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --no-default-keyring \
  --keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg --import
echo 'deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main' \
  | sudo tee /etc/apt/sources.list.d/wazuh.list
sudo apt update && sudo apt install wazuh-agent

# Update .env
WAZUH_URL=https://your-wazuh-server:55000
WAZUH_USER=wazuh
WAZUH_PASS=your_wazuh_password
```

> 💡 **Without any databases:** DAVID CIS uses built-in SQLite (`data/david.db`) and JSON files in `data/` — fully functional for single-user desktop use.

---

## 🚀 Step 8 — Run the System

### Option A — Desktop GUI (Tkinter)

```bash
# Linux / macOS
python gui_app.py

# Windows — double-click
gui_launcher.bat

# macOS / Linux script
bash gui_launcher.sh
```

The GUI loads all engine tabs:
- Offensive / Pentest / Vuln Scanner
- Malware Analysis
- OSINT Investigation
- SOC / SIEM Log Analyzer
- Defense & WAF
- Bug Analyzer
- Tracking (Flights / Ships / Satellites / Geo)
- Bug Bounty Manager
- Live Cyber Attack Map
- AI Chat

### Option B — Terminal CLI

```bash
python main.py
```

### Option C — API Server + Web Dashboard

```bash
# Main API on port 8000
uvicorn core.api:app --reload --host 0.0.0.0 --port 8000

# Access:
# Dashboard:  http://localhost:8000/
# API Docs:   http://localhost:8000/docs
# Health:     http://localhost:8000/health
```

### Option D — Bug Bounty API (separate server)

```bash
# Bug bounty platform on port 8001
uvicorn bounty.api:app --reload --host 0.0.0.0 --port 8001

# Access:
# Submit bug:   POST http://localhost:8001/report/submit
# List reports: GET  http://localhost:8001/reports
# Statistics:   GET  http://localhost:8001/stats
# API Docs:     http://localhost:8001/docs
```

### Option E — Run both servers together

```bash
python launcher.py
```

`launcher.py` starts both FastAPI servers and the GUI in parallel threads.

### Option F — Build standalone installer (.exe)

```bash
# Windows .exe via PyInstaller + Inno Setup
pip install pyinstaller
python build_exe.py

# Output: dist/DavidCyberIntelligence.exe
# Installer: dist/DavidCIS_Setup.exe (if Inno Setup is installed)
```

---

## 🔄 Step 9 — Enable Auto Scans & Alerts

### Scheduler — any module, any interval

```python
from automation.scheduler import ScanScheduler

s = ScanScheduler()

# Vulnerability scan every 24 hours
s.add_job("Daily VulnScan",  "192.168.1.1",        "vuln_scan",  86400)

# Web app ZAP scan every 12 hours
s.add_job("Web App Scan",    "https://myapp.com",  "zap",        43200)

# OSINT recon on domain every day
s.add_job("Domain Recon",    "example.com",        "osint",      86400)

# Malware scan on watched folder every 6 hours
s.add_job("Malware Watch",   "/var/www/html",      "malware",    21600)

# Geo-check suspicious IP every hour
s.add_job("IP Geo Monitor",  "1.2.3.4",            "geo",         3600)

# Attack simulation (basic scope) weekly
s.add_job("Weekly AttackSim","https://myapp.com",  "attack_sim", 604800)

s.start()   # background thread — non-blocking
```

> 💡 `add_job()` accepts **any module name** the task router supports — not just vuln/pentest.

### Alerting — Telegram + Email

```python
from automation.alerting import AlertManager

alerts = AlertManager()

# Send Telegram alert
alerts.send_telegram("🚨 CRITICAL: RDP port open on 192.168.1.1")

# Send email alert
alerts.send_email(
    subject="DAVID CIS — HIGH severity finding",
    body="CVE-2024-XXXX found on target..."
)

# Auto-alert with severity filter (only CRITICAL/HIGH)
alerts.send_alert(
    level="CRITICAL",
    title="Brute force detected",
    details={"ip": "5.6.7.8", "attempts": 342}
)
```

Required `.env` values for alerts:
```env
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Email — ALL FOUR required or email silently fails
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASS=your_app_password
ALERT_EMAIL=alerts@yourdomain.com
```

---

## 🧪 Step 10 — Verify Everything Works

### Quick engine health check

```bash
python -c "
from core.task_router import TaskRouter
r = TaskRouter()
print('✅ Loaded engines:', list(r._engines.keys()))
"
```

Expected output (all 20 modules):
```
✅ Loaded engines: ['malware', 'network', 'osint', 'pentest', 'defense',
                    'intel', 'vuln_scan', 'soc', 'attack_sim', 'zap',
                    'wazuh', 'openvas', 'hydra', 'cloudflare', 'deepexploit',
                    'flight', 'ship', 'satellite', 'geo', 'chat']
```

### API health check

```bash
# Start server first
uvicorn core.api:app --port 8000 &

# Check health
curl http://localhost:8000/health
```

Expected JSON:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "loaded_modules": ["malware", "network", "osint", ...],
  "developer": "Devil Pvt Ltd & Nexuzy Tech Pvt Ltd"
}
```

### Test individual modules

```bash
# Test vuln scan
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"vuln_scan","params":{"target":"127.0.0.1"}}'

# Test geo lookup
curl -X POST http://localhost:8000/api/geo?ip=8.8.8.8

# Test AI chat
curl -X POST "http://localhost:8000/api/chat?query=Explain+SQL+injection"

# Check threat score
curl http://localhost:8000/score
```

---

## 🗂️ Project Structure

```
david-cyber-intelligence-system/
│
├── 📄 gui_app.py               ← Tkinter desktop GUI (all tabs)
├── 📄 main.py                  ← CLI entry point
├── 📄 launcher.py              ← Starts GUI + both API servers
├── 📄 build_exe.py             ← PyInstaller .exe builder
├── 📄 tools_installer.py       ← Auto-installs all external tools
├── 📄 requirements.txt         ← Python dependencies
├── 📄 .env.example             ← Full environment config template
├── 📄 gui_launcher.bat         ← Windows one-click launcher
├── 📄 gui_launcher.sh          ← Linux/macOS one-click launcher
├── 📄 install.bat              ← Windows full installer
├── 📄 install.sh               ← Linux/macOS full installer
│
├── 📁 core/
│   ├── api.py                  ← FastAPI v2.0.0 backend (17 endpoints + WebSocket)
│   ├── task_router.py          ← Dispatches to all 20 modules
│   ├── llm_brain.py            ← Mixtral GGUF AI — offline fallback built-in
│   └── threat_scorer.py        ← Unified 0–100 threat score across modules
│
├── 📁 engines/
│   ├── malware_engine.py       ← YARA + pefile + capstone + XGen-Q
│   ├── network_engine.py       ← Scapy + Suricata + LSTM IDS
│   ├── osint_engine.py         ← Shodan + SpiderFoot + CyNER + theHarvester
│   ├── pentest_engine.py       ← Nmap top-200 + SQLMap + DeepExploit
│   ├── defense_engine.py       ← Open-AppSec WAF + Cloudflare IP block
│   ├── vulnerability_scanner.py← Top-1000 ports + OS detect + CVE + NVD links
│   ├── soc_engine.py           ← 8 attack detectors + IP scoring + log drop
│   ├── attack_sim_engine.py    ← Scoped simulation: basic / web / full
│   ├── bug_analyzer.py         ← APK/EXE/PHP/PY/JS/KT static analysis
│   └── bug_analyzer_tab.py     ← Tkinter GUI tab for bug analyzer
│
├── 📁 security/
│   ├── cai_engine.py           ← Dual-mode CAI pipeline (offensive + defensive)
│   ├── zap_engine.py           ← OWASP ZAP DAST API client
│   ├── wazuh_client.py         ← Wazuh SIEM alert fetcher
│   ├── openvas_client.py       ← OpenVAS authenticated CVE scanner
│   ├── hydra_engine.py         ← Hydra brute-force test runner
│   ├── cloudflare_client.py    ← CF stats + get_zones() + block_ip()
│   ├── deepexploit_engine.py   ← RL-based exploit mapping
│   └── local_siem.py           ← Built-in SIEM (no Wazuh needed)
│
├── 📁 intelligence/
│   ├── threat_intel.py         ← Multi-source threat intel aggregator
│   ├── misp_client.py          ← MISP IOC lookup + submit
│   ├── opencti_client.py       ← OpenCTI threat graph client
│   └── threat_db.py            ← Local SQLite threat database
│
├── 📁 tracking/
│   ├── flight_tracker.py       ← OpenSky API + live position + alerts
│   ├── ship_tracker.py         ← AIS/MarineTraffic + vessel search
│   ├── satellite_tracker.py    ← CelesTrak TLE + Skyfield propagation
│   ├── attack_map.py           ← Tkinter world-map cyber attack visualizer
│   └── geo_engine.py           ← IP → country/city/ISP/ASN + map pin
│
├── 📁 bounty/
│   ├── api.py                  ← Bug bounty REST API (port 8001)
│   ├── models.py               ← SQLite schema for reports + researchers
│   ├── cvss_scorer.py          ← CVSS v3.1 automatic severity scorer
│   └── ai_validator.py         ← LLM-based bug report validator
│
├── 📁 automation/
│   ├── scheduler.py            ← Cron-style job scheduler (any module)
│   └── alerting.py             ← Telegram + SMTP email alert manager
│
├── 📁 intelligence/
│   └── threat_intel.py         ← OTX + MISP + AbuseIPDB + VirusTotal
│
├── 📁 dashboard/
│   └── index.html              ← Web dashboard served by FastAPI at /
│
├── 📁 models/                  ← Place GGUF model files here
├── 📁 data/                    ← SQLite DB, scan outputs, uploaded files
├── 📁 config/                  ← Module settings and route configuration
└── 📁 assets/                  ← Logo and static images
```

---

## ❓ Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `nmap not found` | Install from [nmap.org](https://nmap.org) or run `python tools_installer.py` |
| LLM not responding | Download model to `models/` — see Step 6 |
| ZAP scan fails | Start ZAP app first, then set `ZAP_URL` + `ZAP_API_KEY` in `.env` |
| Wazuh connection refused | Check `WAZUH_URL` in `.env`, verify Wazuh is running |
| Tkinter not found (Linux) | `sudo apt install python3-tk` |
| Port 8000 already in use | Use `--port 8080` or `kill $(lsof -t -i:8000)` |
| Email alerts not sending | Make sure **all four** SMTP vars are set: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` |
| Nmap needs root (Linux) | `sudo python gui_app.py` or `sudo python main.py` for full scan capability |
| yara-python build fails | `pip install yara-python --no-binary yara-python` |
| PostgreSQL connection error | Check `POSTGRES_URL` in `.env`, ensure the DB user has access |
| OpenVAS scan timeout | OpenVAS scans are slow — increase timeout or reduce target scope |
| `build_exe.py` fails | `pip install pyinstaller` then retry |

---

## 📞 Support

**David** — Full-Stack Security Engineer  
Nexuzy Tech Pvt Ltd | Devil Pvt Ltd  
Kolkata, West Bengal, India  

🌐 [hypechats.com](https://hypechats.com)  
📧 david@nexuzytech.com  
🐙 [github.com/david0154](https://github.com/david0154)

> See **[API_SETUP.md](API_SETUP.md)** for full REST API documentation, request/response examples, WebSocket usage, and module routing reference.
