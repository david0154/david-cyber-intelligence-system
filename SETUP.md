# 🛠️ SETUP GUIDE — DAVID CYBER INTELLIGENCE SYSTEM v3.0

**Developer: Devil Pvt Ltd & Nexuzy Tech Pvt Ltd**

---

## 📋 Requirements

- Python 3.10 or higher
- pip 23+
- Git
- 4 GB RAM minimum (8 GB recommended for LLM)
- OS: Windows 10+ / Ubuntu 20.04+ / macOS 12+

---

## ⚡ Step 1: Clone Repository

```bash
git clone https://github.com/david0154/david-cyber-intelligence-system
cd david-cyber-intelligence-system
```

---

## 📦 Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ If you get errors on Windows with `yara-python`:
> ```
> pip install yara-python --no-binary yara-python
> ```

---

## ⚙️ Step 3: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

| Key | Where to get |
|-----|--------------|
| `SHODAN_API_KEY` | https://shodan.io (free account) |
| `ZAP_API_KEY` | Start ZAP → Tools → API Key |
| `WAZUH_URL/USER/PASS` | Your Wazuh server |
| `CLOUDFLARE_API_TOKEN` | Cloudflare Dashboard → API Tokens |
| `TELEGRAM_BOT_TOKEN` | @BotFather on Telegram |
| `SMTP_USER/PASS` | Gmail App Password |
| `N2YO_API_KEY` | https://n2yo.com/api/ |

---

## 🔧 Step 4: Install External Security Tools

### 🐧 Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y nmap hydra suricata sqlmap ncat

# Metasploit
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall && ./msfinstall

# OWASP ZAP
sudo snap install zaproxy --classic
```

### 🍎 macOS
```bash
brew install nmap hydra sqlmap

# ZAP: https://zaproxy.org/download/
# Metasploit: https://metasploit.com/download
```

### 🪟 Windows
| Tool | Download |
|------|----------|
| Nmap | https://nmap.org/download |
| OWASP ZAP | https://zaproxy.org |
| Hydra | https://github.com/vanhauser-thc/thc-hydra/releases |
| SQLMap | https://sqlmap.org (needs Python) |
| Metasploit | https://metasploit.com/download |

---

## 🤖 Step 5: Download AI Model (Optional but Recommended)

For full AI reasoning, download a Mixtral GGUF model:

```bash
# Create models/ directory
mkdir models
cd models

# Option A: Mixtral 7B Q4 (recommended, ~4GB)
wget https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf

# Option B: Smaller model (~2GB)
wget https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf
```

Then update `.env`:
```
LLM_MODEL_PATH=models/mistral-7b-v0.1.Q4_K_M.gguf
LLM_MODEL_TYPE=mistral
```

> 💡 If no model is downloaded, the system still works — AI features show stubs with download links.

---

## 🗄️ Step 6: Database Setup (Optional)

### PostgreSQL (for full threat storage)
```bash
# Install
sudo apt install postgresql
sudo -u postgres psql -c "CREATE DATABASE davidcyber;"
sudo -u postgres psql -c "CREATE USER cyberuser WITH PASSWORD 'yourpass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE davidcyber TO cyberuser;"

# Update .env
POSTGRES_URL=postgresql://cyberuser:yourpass@localhost:5432/davidcyber
```

### Elasticsearch (for SIEM logs)
```bash
sudo apt install elasticsearch
sudo systemctl start elasticsearch
```

> 💡 Without these, the system uses SQLite and local JSON — fully functional.

---

## 🚀 Step 7: Run the System

### Option A: Desktop GUI (Tkinter)
```bash
python gui_app.py

# Windows: double-click gui_launcher.bat
# macOS/Linux: ./gui_launcher.sh
```

### Option B: Terminal CLI
```bash
python main.py
```

### Option C: API Server + Web Dashboard
```bash
# Main API (port 8000)
uvicorn core.api:app --reload --host 0.0.0.0 --port 8000

# Open: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option D: Bug Bounty Platform
```bash
# Bug Bounty API (port 8001)
uvicorn bounty.api:app --reload --host 0.0.0.0 --port 8001

# Submit bug: POST http://localhost:8001/report/submit
# View all:   GET  http://localhost:8001/reports
# Stats:      GET  http://localhost:8001/stats
# API Docs:   http://localhost:8001/docs
```

### Option E: Build Standalone .exe (Windows)
```bash
pip install pyinstaller
python build_exe.py
# Output: dist/DavidCyberIntelligence.exe
```

---

## 🔄 Step 8: Enable Auto Scans & Alerts

Add to your Python script or `main.py`:

```python
from automation.scheduler import ScanScheduler

s = ScanScheduler()

# Scan server every 24 hours
s.add_job("Daily Server Scan", "192.168.1.1", "vuln_scan", 86400)

# Scan web app every 12 hours
s.add_job("Web App Scan", "https://myapp.com", "zap", 43200)

# Start background scheduler
s.start()
```

Configure alerts in `.env`:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
SMTP_USER=your@gmail.com
SMTP_PASS=your_app_password
ALERT_EMAIL=alerts@yourdomain.com
```

---

## 🧪 Step 9: Verify Everything Works

```bash
# Quick health check
python -c "
from core.task_router import TaskRouter
r = TaskRouter()
print('Loaded engines:', list(r._engines.keys()))
"
```

Expected output:
```
Loaded engines: ['malware', 'network', 'osint', 'pentest', 'defense',
                 'intel', 'vuln_scan', 'soc', 'attack_sim', 'zap',
                 'wazuh', 'openvas', 'hydra', 'cloudflare', 'deepexploit',
                 'flight', 'ship', 'satellite', 'geo', 'chat']
```

---

## 🗂️ Project Structure

```
david-cyber-intelligence-system/
├── gui_app.py              ← Tkinter Desktop GUI
├── main.py                 ← CLI Entry point
├── build_exe.py            ← PyInstaller build script
├── requirements.txt        ← All Python deps
├── .env.example            ← Config template
├── SETUP.md                ← This file
├── README.md               ← Full documentation
│
├── core/
│   ├── api.py              ← FastAPI backend + WebSocket
│   ├── task_router.py      ← Module dispatcher
│   └── llm_brain.py        ← Mixtral GGUF AI brain
│
├── engines/
│   ├── malware_engine.py   ← YARA + pefile + XGen-Q
│   ├── network_engine.py   ← Scapy + Suricata + LSTM
│   ├── osint_engine.py     ← Shodan + SpiderFoot + CyNER
│   ├── pentest_engine.py   ← Nmap + SQLMap + DeepExploit
│   ├── defense_engine.py   ← Open-AppSec WAF
│   ├── vulnerability_scanner.py ← CVE + Port scan
│   ├── soc_engine.py       ← Log analysis + anomaly detect
│   └── attack_sim_engine.py ← Full pentest pipeline
│
├── security/
│   ├── zap_engine.py       ← OWASP ZAP API
│   ├── wazuh_client.py     ← Wazuh SIEM
│   ├── openvas_client.py   ← OpenVAS CVE scanner
│   ├── hydra_engine.py     ← Brute force test
│   ├── cloudflare_client.py ← CF WAF + stats
│   └── deepexploit_engine.py ← RL-based exploit
│
├── intelligence/
│   └── misp_client.py      ← MISP + OpenCTI IOC
│
├── tracking/
│   ├── flight_tracker.py   ← OpenSky API
│   ├── ship_tracker.py     ← AIS tracking
│   ├── satellite_tracker.py ← CelesTrak
│   └── geo_engine.py       ← IP geolocation
│
├── bounty/
│   ├── api.py              ← Bug bounty REST API
│   ├── models.py           ← SQLite schema
│   ├── cvss_scorer.py      ← CVSS v3.1 auto-scorer
│   └── ai_validator.py     ← AI bug validation
│
├── automation/
│   └── scheduler.py        ← Cron scans + Email/Telegram
│
├── dashboard/
│   └── index.html          ← Web dashboard UI
│
├── assets/
│   └── logo.jpg            ← DAVID CIS Logo
│
├── models/                 ← AI models (GGUF, YARA rules)
├── data/                   ← SQLite DB, uploads
└── config/
    └── settings.py         ← All configuration
```

---

## ❓ Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `nmap not found` | Install nmap from https://nmap.org |
| LLM not responding | Download model to `models/` folder |
| ZAP scan fails | Start ZAP app first, then scan |
| Wazuh connection refused | Check `WAZUH_URL` in `.env` |
| Tkinter not found (Linux) | `sudo apt install python3-tk` |
| Port 8000 in use | Use `--port 8080` or kill the process |

---

## 📞 Support

**David** — Nexuzy Tech Pvt Ltd | Devil Pvt Ltd  
Kolkata, West Bengal, India  
https://hypechats.com
