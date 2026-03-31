# 🛡️ DAVID CYBER INTELLIGENCE SYSTEM

> **Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active%20Development-yellow?style=for-the-badge)

---

## 🧠 System Overview

DAVID CYBER INTELLIGENCE SYSTEM is an advanced AI-powered cybersecurity platform that integrates:

- 🦠 **Malware Analysis Engine** — YARA + pefile + XGen-Q + LLM
- 🌐 **Network IDS Engine** — LSTM/Autoencoder + Scapy + Suricata + Zeek
- 🕵️ **OSINT Engine** — CyNER + SpiderFoot + Shodan
- 🧪 **Pentest Engine** — PentestGPT + DeepExploit + Nmap + Metasploit
- 🛡️ **Defense Engine** — Open-AppSec ML WAF
- 🧠 **Threat Intelligence** — MISP + OpenCTI
- ✈️ **Flight Tracking** — OpenSky Network + ADS-B
- 🚢 **Ship Tracking** — MarineTraffic + AIS
- 🛰️ **Satellite Tracking** — CelesTrak + N2YO + Skyfield
- 🗺️ **Geo Intelligence** — IP Mapping + Threat Heatmaps

---

## 🏗️ Architecture

```
┌────────────────────────────┐
│   LLM BRAIN (Mixtral GGUF) │
│   via ctransformers        │
└────────────┬───────────────┘
             │
     Intent + Reasoning
             │
    ┌────────▼────────┐
    │   TASK ROUTER   │
    └────────┬────────┘
             │
┌────────────┼──────────────┬─────────────┬──────────────┐
│ Malware    │ Network      │ OSINT       │ Pentest      │ Defense
│ Engine     │ Engine       │ Engine      │ Engine       │ Engine
└────────────┴──────────────┴─────────────┴──────────────┘
             │
     Threat Intelligence Layer
      (MISP + OpenCTI + DB)
             │
        Final Response
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip
- Git

### Installation

```bash
git clone https://github.com/david0154/david-cyber-intelligence-system
cd david-cyber-intelligence-system
pip install -r requirements.txt
```

### Run API Server
```bash
uvicorn core.api:app --reload --host 0.0.0.0 --port 8000
```

### Run CLI
```bash
python main.py
```

---

## 📁 Project Structure

```
david-cyber-intelligence-system/
├── core/
│   ├── llm_brain.py          # Mixtral GGUF LLM Brain
│   ├── task_router.py        # Task routing logic
│   ├── api.py                # FastAPI server
│   └── threat_scorer.py      # Unified threat scoring
├── engines/
│   ├── malware_engine.py     # YARA + pefile + analysis
│   ├── network_engine.py     # IDS + packet analysis
│   ├── osint_engine.py       # OSINT gathering
│   ├── pentest_engine.py     # Automated pentest
│   └── defense_engine.py     # WAF + blocking
├── intelligence/
│   ├── misp_client.py        # MISP IOC integration
│   ├── opencti_client.py     # OpenCTI graph intel
│   └── threat_db.py          # Local threat database
├── tracking/
│   ├── flight_tracker.py     # OpenSky + ADS-B
│   ├── ship_tracker.py       # MarineTraffic + AIS
│   ├── satellite_tracker.py  # CelesTrak + Skyfield
│   └── geo_engine.py         # IP → Location mapping
├── models/
│   ├── ids_model.py          # LSTM/Autoencoder IDS
│   └── phishing_dqn.py       # DQN phishing detector
├── config/
│   └── settings.py           # All configuration
├── data/
│   ├── yara_rules/           # YARA signature files
│   └── threat_feeds/         # Threat intelligence feeds
├── requirements.txt
├── main.py
└── README.md
```

---

## ⚙️ Platform Support

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Malware Engine | ✅ | ✅ | ✅ |
| Network Engine | ✅ | ✅ | ✅ |
| OSINT Engine | ✅ | ✅ | ✅ |
| Pentest Engine | ✅ | ✅ | ✅ |
| Defense Engine | ✅ | ✅ | ✅ |
| Flight Tracking | ✅ | ✅ | ✅ |
| Ship Tracking | ✅ | ✅ | ✅ |
| Satellite Tracking | ✅ | ✅ | ✅ |
| Geo Intelligence | ✅ | ✅ | ✅ |

---

## 🧩 Module Details

### 🦠 Malware Engine
- YARA signature detection
- pefile binary parsing
- Capstone disassembly
- XGen-Q behavioral reasoning
- LLM explanation + risk score

### 🌐 Network Engine (IDS)
- Live packet capture with Scapy
- Suricata alert integration
- Zeek traffic log analysis
- LSTM/Autoencoder anomaly detection
- DQN phishing detection

### 🕵️ OSINT Engine
- SpiderFoot automated recon
- theHarvester email/domain intel
- Shodan device fingerprinting
- CyNER named entity extraction (IPs, CVEs, domains)

### 🧪 Pentest Engine
- Nmap port/service scanning
- SQLMap injection testing
- DeepExploit auto-exploitation
- PentestGPT workflow structuring

### 🛡️ Defense Engine
- Open-AppSec ML-based WAF
- Auto-learning firewall rules
- Real-time IP blocking
- Threat DB storage

### ✈️ Flight Tracking
- OpenSky Network API
- ADS-B Exchange
- Real-time lat/lon/altitude

### 🚢 Ship Tracking
- MarineTraffic API
- AIS stream parsing
- Vessel metadata + routes

### 🛰️ Satellite Tracking
- CelesTrak TLE data
- N2YO orbital predictions
- Skyfield + sgp4 calculations

### 🗺️ Geo Intelligence
- IP → geolocation mapping
- Attack origin visualization
- Threat heatmap generation
- Leaflet.js frontend maps

---

## 🧠 Threat Scoring System

```
Threat Score = Malware Score + Network Score + OSINT Score + Intel Match

LOW      (0-25)
MEDIUM   (26-50)
HIGH     (51-75)
CRITICAL (76-100)
```

---

## 🗄️ Data Layer

| Store | Purpose |
|-------|---------|
| PostgreSQL | Structured threat data |
| Elasticsearch | Log indexing & search |
| Neo4j | Threat relationship graphs |
| JSON Cache | Fast local caching |

---

## 📜 License

Proprietary — © 2026 Devil Pvt Ltd & Nexuzy Tech Pvt Ltd. All rights reserved.

---

## 👨‍💻 Developer

**David** — Full-Stack Security Engineer
Nexuzy Tech Pvt Ltd | Devil Pvt Ltd
Kolkata, West Bengal, India
