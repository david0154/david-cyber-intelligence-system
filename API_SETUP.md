# 🔌 API SETUP GUIDE — DAVID CYBER INTELLIGENCE SYSTEM v2.0.0

<div align="center">

**Full REST API + WebSocket Reference**  
**Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd**

</div>

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [API Architecture](#️-api-architecture)
3. [Starting the Servers](#-starting-the-servers)
4. [Core API Endpoints — Main Server (port 8000)](#-core-api-endpoints--main-server-port-8000)
5. [Universal Module Router — POST /analyze](#-universal-module-router--post-analyze)
6. [Security Tool Endpoints](#-security-tool-endpoints)
7. [Threat Score API](#-threat-score-api)
8. [Bug Bounty API — Separate Server (port 8001)](#-bug-bounty-api--separate-server-port-8001)
9. [WebSocket — Live Alerts](#-websocket--live-alerts)
10. [All 20 Routable Modules](#-all-20-routable-modules)
11. [Request & Response Examples](#-request--response-examples)
12. [Authentication & Security](#-authentication--security)
13. [Error Handling](#-error-handling)
14. [Python SDK Examples](#-python-sdk-examples)
15. [cURL Cheatsheet](#-curl-cheatsheet)

---

## ⚡ Quick Start

```bash
# 1. Start main API server
uvicorn core.api:app --reload --host 0.0.0.0 --port 8000

# 2. Start bug bounty server (optional, separate port)
uvicorn bounty.api:app --reload --host 0.0.0.0 --port 8001

# 3. Or start both together
python launcher.py
```

Verify:
```bash
curl http://localhost:8000/health
# → {"status":"healthy","version":"2.0.0","loaded_modules":[...]}
```

Open interactive docs:
- Main API: http://localhost:8000/docs
- Bug Bounty API: http://localhost:8001/docs

---

## 🏗️ API Architecture

```
┌─────────────────────────────────────────────────────┐
│             FastAPI — core/api.py v2.0.0             │
│                   Port 8000                          │
├──────────────┬──────────────┬────────────────────────┤
│  Dashboard   │  REST API    │   WebSocket            │
│  GET /       │  17 endpoints│   /ws/alerts           │
│  /static     │  POST /analyze (universal router)     │
└──────────────┴──────┬───────┴────────────────────────┘
                       │
              TaskRouter (core/task_router.py)
                       │
        ┌──────────────┼──────────────────────┐
        │              │                      │
   20 Modules     ThreatScorer          LLM Brain
  (engines/      (core/threat_          (core/llm_
   security/      scorer.py)             brain.py)
   tracking/)

┌─────────────────────────────────────────────────────┐
│          FastAPI — bounty/api.py                     │
│                   Port 8001                          │
│  Bug submission · Reports · CVSS · AI validation     │
└─────────────────────────────────────────────────────┘
```

---

## 🖥️ Starting the Servers

### Development mode (auto-reload on file change)

```bash
# Main API
uvicorn core.api:app --reload --host 0.0.0.0 --port 8000

# Bug Bounty API
uvicorn bounty.api:app --reload --host 0.0.0.0 --port 8001
```

### Production mode

```bash
# Main API — 4 workers
uvicorn core.api:app --host 0.0.0.0 --port 8000 --workers 4

# With gunicorn
gunicorn core.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Windows service / background

```bat
REM Windows — run in background
start /B uvicorn core.api:app --host 0.0.0.0 --port 8000
```

```bash
# Linux — background with nohup
nohup uvicorn core.api:app --host 0.0.0.0 --port 8000 &

# Or as systemd service — see bottom of this file
```

---

## 📡 Core API Endpoints — Main Server (port 8000)

### Complete endpoint table

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | Serves `dashboard/index.html` web UI | None |
| `GET` | `/health` | System health — version, loaded modules | None |
| `POST` | `/analyze` | **Universal module router** (JSON body) | None |
| `GET` | `/score` | Unified threat score report (0–100) | None |
| `POST` | `/score/update` | Update a module's threat score | None |
| `GET` | `/api/wazuh/alerts` | Fetch live Wazuh SIEM alerts | None |
| `POST` | `/api/zap/scan` | Run OWASP ZAP DAST scan | None |
| `POST` | `/api/openvas/scan` | Run OpenVAS CVE scan | None |
| `POST` | `/api/hydra/test` | Run Hydra brute-force test | None |
| `GET` | `/api/cloudflare/stats` | Get Cloudflare zone WAF stats | None |
| `POST` | `/api/deepexploit` | Run DeepExploit RL exploit | None |
| `POST` | `/api/osint` | Run OSINT investigation | None |
| `POST` | `/api/pentest` | Run pentest workflow | None |
| `POST` | `/api/malware` | Run malware analysis | None |
| `POST` | `/api/geo` | IP geolocation lookup | None |
| `POST` | `/api/chat` | Send query to AI LLM brain | None |
| `WS` | `/ws/alerts` | **WebSocket** — live alert stream | None |

---

## 🔁 Universal Module Router — POST /analyze

The single most powerful endpoint. Routes any task to any loaded module.

**Endpoint:** `POST /analyze`  
**Content-Type:** `application/json`

### Request schema

```json
{
  "module": "<module_name>",
  "params": {
    "<key>": "<value>"
  }
}
```

### All supported modules via /analyze

| `module` | Required `params` key | What it does |
|----------|-----------------------|--------------|
| `malware` | `file_path` | YARA + pefile + AI malware analysis |
| `network` | `interface` | Live packet capture + IDS |
| `osint` | `target` | OSINT investigation on IP/domain/email |
| `pentest` | `target` | Full pentest: Nmap top-200 + SQLMap + DeepExploit |
| `vuln_scan` | `target` | Top-1000 port scan + OS detect + CVE + NVD patches |
| `attack_sim` | `target`, `scope` | Scoped attack simulation: `basic`/`web`/`full` |
| `defense` | *(none)* | WAF status and defense engine state |
| `soc` | `log_text`, `source` | Analyze raw log text for 8 attack patterns |
| `intel` | `ioc` | MISP IOC lookup |
| `zap` | `url` | OWASP ZAP DAST scan |
| `wazuh` | `limit` | Fetch Wazuh alerts (default: 20) |
| `openvas` | `target` | OpenVAS CVE scan |
| `hydra` | `target`, `service` | Brute-force test (service: ssh/ftp/http) |
| `cloudflare` | `zone_id` | CF zone WAF stats |
| `deepexploit` | `target` | DeepExploit RL-based exploit mapping |
| `flight` | `callsign` | Live flight tracking |
| `ship` | `mmsi` | Live vessel tracking |
| `satellite` | `sat_id` | Live satellite tracking |
| `geo` | `ip` | IP geolocation + threat check |
| `chat` | `query` | AI chat with Mixtral LLM |

### Example requests

```bash
# Vulnerability scan
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"vuln_scan","params":{"target":"192.168.1.100"}}'

# Attack simulation — web scope
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"attack_sim","params":{"target":"https://example.com","scope":"web"}}'

# OSINT on domain
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"osint","params":{"target":"example.com"}}'

# Malware analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"malware","params":{"file_path":"/tmp/suspicious.exe"}}'

# SOC log analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"soc","params":{"log_text":"Failed password for root from 1.2.3.4 port 22","source":"auth.log"}}'

# AI chat
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"chat","params":{"query":"What is SQL injection?"}}'
```

---

## 🛡️ Security Tool Endpoints

These are dedicated endpoints that bypass `/analyze` for direct tool access.

### GET /health

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "healthy",
  "version": "2.0.0",
  "loaded_modules": ["malware", "network", "osint", "pentest", "defense",
                      "intel", "vuln_scan", "soc", "attack_sim", "zap",
                      "wazuh", "openvas", "hydra", "cloudflare", "deepexploit",
                      "flight", "ship", "satellite", "geo", "chat"],
  "developer": "Devil Pvt Ltd & Nexuzy Tech Pvt Ltd"
}
```

### GET /api/wazuh/alerts

```bash
curl "http://localhost:8000/api/wazuh/alerts?limit=10"
```

| Query Param | Type | Default | Description |
|-------------|------|---------|-------------|
| `limit` | int | 20 | Max number of alerts to return |

### POST /api/zap/scan

```bash
curl -X POST "http://localhost:8000/api/zap/scan?url=https://example.com"
```

| Query Param | Type | Required | Description |
|-------------|------|----------|-------------|
| `url` | string | ✅ | Target URL to scan |

### POST /api/openvas/scan

```bash
curl -X POST "http://localhost:8000/api/openvas/scan?target=192.168.1.50"
```

### POST /api/hydra/test

```bash
curl -X POST "http://localhost:8000/api/hydra/test?target=192.168.1.50&service=ssh"
```

| Query Param | Type | Default | Description |
|-------------|------|---------|-------------|
| `target` | string | — | Target IP/hostname |
| `service` | string | `ssh` | Protocol: `ssh`, `ftp`, `http`, `rdp` |

### GET /api/cloudflare/stats

```bash
curl "http://localhost:8000/api/cloudflare/stats?zone_id=your_zone_id"
```

> Requires `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_EMAIL` in `.env`.  
> The `get_zones()` method auto-discovers zones — omit `zone_id` to list all.

### POST /api/deepexploit

```bash
curl -X POST "http://localhost:8000/api/deepexploit?target=192.168.1.100"
```

### POST /api/osint

```bash
curl -X POST "http://localhost:8000/api/osint?target=example.com"
# Or for IP
curl -X POST "http://localhost:8000/api/osint?target=1.2.3.4"
# Or for email
curl -X POST "http://localhost:8000/api/osint?target=user@domain.com"
```

### POST /api/pentest

```bash
curl -X POST "http://localhost:8000/api/pentest?target=192.168.1.100"
```

### POST /api/malware

```bash
curl -X POST "http://localhost:8000/api/malware?file_path=/path/to/file.exe"
```

### POST /api/geo

```bash
curl -X POST "http://localhost:8000/api/geo?ip=8.8.8.8"
```

Example response:
```json
{
  "status": "ok",
  "ip": "8.8.8.8",
  "country": "United States",
  "city": "Mountain View",
  "isp": "Google LLC",
  "asn": "AS15169",
  "lat": 37.4192,
  "lon": -122.0574,
  "abuseipdb_score": 0,
  "otx_pulse_count": 0
}
```

### POST /api/chat

```bash
curl -X POST "http://localhost:8000/api/chat?query=What+is+a+CVE?"
```

Example response:
```json
{
  "status": "ok",
  "response": "A CVE (Common Vulnerabilities and Exposures) is..."
}
```

---

## 📊 Threat Score API

The `ThreatScorer` aggregates scores across all modules into a unified 0–100 risk level.

### GET /score

```bash
curl http://localhost:8000/score
```

Example response:
```json
{
  "total_score": 67,
  "level": "HIGH",
  "breakdown": {
    "malware": 20,
    "network": 15,
    "osint": 10,
    "pentest": 22
  },
  "thresholds": {
    "LOW": "0–24",
    "MEDIUM": "25–49",
    "HIGH": "50–74",
    "CRITICAL": "75–100"
  }
}
```

### POST /score/update

Update the score for a specific module after a scan:

```bash
curl -X POST http://localhost:8000/score/update \
  -H "Content-Type: application/json" \
  -d '{"module":"pentest","score":45}'
```

| Field | Type | Description |
|-------|------|-------------|
| `module` | string | Engine name (e.g. `pentest`, `malware`) |
| `score` | float | Score value 0.0–100.0 |

---

## 🏆 Bug Bounty API — Separate Server (port 8001)

The bug bounty platform runs as a **separate FastAPI server** on port 8001.

```bash
uvicorn bounty.api:app --reload --host 0.0.0.0 --port 8001
```

### Bug Bounty Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/report/submit` | Submit a new bug report |
| `GET` | `/reports` | List all submitted reports |
| `GET` | `/reports/{id}` | Get a specific report by ID |
| `POST` | `/reports/{id}/approve` | Admin: approve report |
| `POST` | `/reports/{id}/reject` | Admin: reject report |
| `GET` | `/stats` | Bug bounty statistics |
| `GET` | `/docs` | Interactive Swagger UI |

### Submit a bug report

```bash
curl -X POST http://localhost:8001/report/submit \
  -H "Content-Type: application/json" \
  -d '{
    "title": "SQL Injection in login form",
    "target": "https://example.com/login",
    "description": "The username parameter is vulnerable to SQL injection.",
    "steps_to_reproduce": "1. Open login page\n2. Enter admin\' OR 1=1-- in username",
    "severity": "HIGH",
    "researcher_email": "researcher@example.com"
  }'
```

### Response

```json
{
  "id": "RPT-2026-0042",
  "status": "submitted",
  "cvss_score": 8.6,
  "severity": "HIGH",
  "ai_validation": "Report appears credible. SQL injection pattern confirmed.",
  "duplicate": false,
  "reward_estimate": "$500–$1500"
}
```

---

## 🔴 WebSocket — Live Alerts

Connect to receive real-time security alerts pushed from all modules.

**Endpoint:** `ws://localhost:8000/ws/alerts`

### JavaScript (browser)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/alerts');

ws.onopen = () => {
  console.log('Connected to DAVID CIS live alerts');
  ws.send(JSON.stringify({ subscribe: 'all' }));
};

ws.onmessage = (event) => {
  const alert = JSON.parse(event.data);
  console.log('🚨 Alert:', alert);
};

ws.onclose = () => console.log('Disconnected');
```

### Python (websockets library)

```python
import asyncio
import websockets
import json

async def listen():
    uri = "ws://localhost:8000/ws/alerts"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"subscribe": "all"}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            print(f"Alert: {data}")

asyncio.run(listen())
```

### Alert payload format

```json
{
  "type": "alert",
  "severity": "HIGH",
  "module": "soc",
  "message": "Brute force detected from 5.6.7.8",
  "ip": "5.6.7.8",
  "timestamp": "2026-03-31T10:15:00Z",
  "auto_blocked": true
}
```

---

## 🗂️ All 20 Routable Modules

Full reference for every module registered in `core/task_router.py`:

| Module | Source File | Main Method | Key Params |
|--------|-------------|-------------|------------|
| `malware` | `engines/malware_engine.py` | `analyze(file_path)` | `file_path` |
| `network` | `engines/network_engine.py` | `monitor(interface)` | `interface` |
| `osint` | `engines/osint_engine.py` | `investigate(target)` | `target` |
| `pentest` | `engines/pentest_engine.py` | `run(target)` | `target` |
| `vuln_scan` | `engines/vulnerability_scanner.py` | `full_scan(target)` | `target` |
| `attack_sim` | `engines/attack_sim_engine.py` | `run_full_pentest(target,scope)` | `target`, `scope` |
| `defense` | `engines/defense_engine.py` | `status()` | — |
| `soc` | `engines/soc_engine.py` | `analyze_log(log_text,source)` | `log_text`, `source` |
| `intel` | `intelligence/misp_client.py` | `lookup(ioc)` | `ioc` |
| `zap` | `security/zap_engine.py` | `scan(url)` | `url` |
| `wazuh` | `security/wazuh_client.py` | `get_alerts(limit)` | `limit` |
| `openvas` | `security/openvas_client.py` | `scan(target)` | `target` |
| `hydra` | `security/hydra_engine.py` | `test(target,service)` | `target`, `service` |
| `cloudflare` | `security/cloudflare_client.py` | `get_stats(zone_id)` | `zone_id` |
| `deepexploit` | `security/deepexploit_engine.py` | `exploit(target)` | `target` |
| `flight` | `tracking/flight_tracker.py` | `track(callsign)` | `callsign` |
| `ship` | `tracking/ship_tracker.py` | `track(mmsi)` | `mmsi` |
| `satellite` | `tracking/satellite_tracker.py` | `track(sat_id)` | `sat_id` |
| `geo` | `tracking/geo_engine.py` | `map_ip(ip)` | `ip` |
| `chat` | `core/llm_brain.py` | `think(query)` | `query` |

---

## 📦 Request & Response Examples

### vuln_scan — Full response

```json
{
  "status": "ok",
  "target": "192.168.1.100",
  "timestamp": "2026-03-31T10:00:00Z",
  "open_ports": [22, 80, 443, 3306],
  "services": [
    {"port": 22,   "service": "ssh",   "info": "OpenSSH 8.9"},
    {"port": 80,   "service": "http",  "info": "Apache 2.4.41"},
    {"port": 3306, "service": "mysql", "info": "MySQL 8.0"}
  ],
  "os_detection": "Ubuntu 22.04 LTS",
  "cves": [
    {"cve": "CVE-2024-1234", "nvd": "https://nvd.nist.gov/vuln/detail/CVE-2024-1234"}
  ],
  "cve_count": 1,
  "risk_score": 45,
  "risk_level": "MEDIUM",
  "patch_suggestions": [
    {"type": "port",  "port": 3306, "advice": "Restrict MySQL to localhost only"},
    {"type": "cve",   "cve": "CVE-2024-1234", "nvd": "https://nvd.nist.gov/...", "advice": "Apply patch"}
  ],
  "raw_nmap": "Starting Nmap 7.94...",
  "ai_explanation": "Target 192.168.1.100 has 4 open ports..."
}
```

### attack_sim — Full response

```json
{
  "status": "ok",
  "target": "https://example.com",
  "scope": "web",
  "steps": [
    {"step": "nmap_scan",   "status": "complete", "ports_found": [80, 443]},
    {"step": "cve_match",   "status": "complete", "cves": []},
    {"step": "sqlmap_test", "status": "complete", "injectable": false},
    {"step": "zap_dast",    "status": "complete", "alerts": 2}
  ],
  "risk_level": "MEDIUM",
  "fix_advice": [
    "Port 23 found open — replace Telnet with SSH"
  ],
  "ai_explanation": "..."
}
```

### soc — Log analysis response

```json
{
  "status": "ok",
  "source": "auth.log",
  "attacks_detected": [
    {
      "type": "brute_force",
      "matches": 47,
      "ips": ["1.2.3.4", "5.6.7.8"]
    }
  ],
  "ip_scores": {
    "1.2.3.4": 15,
    "5.6.7.8": 8
  },
  "blocked_ips": ["1.2.3.4"],
  "threat_level": "HIGH"
}
```

### CAI engine (defensive mode) — via code

```python
from security.cai_engine import CAIEngine

cai = CAIEngine()

# Defensive audit
result = cai.run_pipeline("example.com", mode="defensive")
print(result["risk_level"])         # e.g. "MEDIUM"
print(result["recommendations"])    # list of per-header / CVE / port fixes

# Offensive pipeline
result = cai.run_pipeline("192.168.1.100", mode="offensive")
print(result["steps"])              # nmap_recon, cve_scan, web_check, ip_reputation
```

---

## 🔐 Authentication & Security

By default the API runs with **no authentication** — designed for localhost desktop use.

### Adding API key authentication (recommended for networked deployments)

Add to `core/api.py`:

```python
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
import os

API_KEY = os.getenv("DAVID_API_KEY", "")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(key: str = Security(api_key_header)):
    if API_KEY and key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
```

Then add `.env`:
```env
DAVID_API_KEY=your_very_long_random_secret_key
```

### CORS

The API ships with CORS wide open (`allow_origins=["*"]`) for local use.  
For production, restrict to your frontend domain in `core/api.py`:

```python
allow_origins=["https://yourdomain.com"]
```

### Running behind reverse proxy (nginx)

```nginx
server {
    listen 443 ssl;
    server_name your-server.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/alerts {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## ⚠️ Error Handling

All endpoints return standard error shapes:

```json
{
  "detail": "Module 'xyz' not loaded. Run: pip install -r requirements.txt"
}
```

| HTTP Status | Meaning |
|-------------|----------|
| `200` | Success |
| `400` | Module error / bad input |
| `404` | Endpoint not found |
| `422` | Validation error (missing required field) |
| `500` | Internal server error |

Module-level errors return status 400 with the engine's error message:

```json
{
  "status": "error",
  "message": "nmap not installed — https://nmap.org"
}
```

---

## 🐍 Python SDK Examples

### Basic wrapper class

```python
import requests

class DavidCISClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base = base_url

    def health(self):
        return requests.get(f"{self.base}/health").json()

    def analyze(self, module: str, **params):
        return requests.post(
            f"{self.base}/analyze",
            json={"module": module, "params": params}
        ).json()

    def score(self):
        return requests.get(f"{self.base}/score").json()

    def chat(self, query: str):
        return requests.post(
            f"{self.base}/api/chat",
            params={"query": query}
        ).json()


# Usage
client = DavidCISClient()

# Vulnerability scan
result = client.analyze("vuln_scan", target="192.168.1.1")
print(result["risk_level"])

# Attack simulation — full scope
result = client.analyze("attack_sim", target="https://myapp.com", scope="full")
print(result["steps"])

# OSINT
result = client.analyze("osint", target="evil.com")
print(result)

# Geo lookup
result = client.analyze("geo", ip="8.8.8.8")
print(result["country"], result["isp"])

# Check unified threat score
print(client.score())
```

### Async example (httpx)

```python
import asyncio
import httpx

async def run_scans():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # Run vuln scan and OSINT in parallel
        vuln, osint = await asyncio.gather(
            client.post("/analyze", json={"module":"vuln_scan","params":{"target":"192.168.1.1"}}),
            client.post("/analyze", json={"module":"osint","params":{"target":"192.168.1.1"}}),
        )
        print("Vuln:", vuln.json()["risk_level"])
        print("OSINT:", osint.json())

asyncio.run(run_scans())
```

---

## 💻 cURL Cheatsheet

```bash
# ── Health ────────────────────────────────────────────────────────
curl http://localhost:8000/health

# ── Universal /analyze ───────────────────────────────────────────
# Vuln scan
curl -sX POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"vuln_scan","params":{"target":"192.168.1.1"}}' | python -m json.tool

# Attack sim — basic
curl -sX POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"attack_sim","params":{"target":"192.168.1.1","scope":"basic"}}' | python -m json.tool

# Attack sim — web (adds SQLMap + ZAP)
curl -sX POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"attack_sim","params":{"target":"https://example.com","scope":"web"}}' | python -m json.tool

# Attack sim — full (adds Metasploit)
curl -sX POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"attack_sim","params":{"target":"192.168.1.1","scope":"full"}}' | python -m json.tool

# OSINT
curl -sX POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"osint","params":{"target":"example.com"}}' | python -m json.tool

# SOC log analysis
curl -sX POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"soc","params":{"log_text":"Failed password for root from 1.2.3.4","source":"auth.log"}}' | python -m json.tool

# Malware analysis
curl -sX POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"malware","params":{"file_path":"/tmp/sample.exe"}}' | python -m json.tool

# AI chat
curl -sX POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"module":"chat","params":{"query":"Explain CVE-2024-1234"}}' | python -m json.tool

# ── Direct endpoints ──────────────────────────────────────────────
curl -sX POST "http://localhost:8000/api/zap/scan?url=https://example.com"
curl -sX POST "http://localhost:8000/api/openvas/scan?target=192.168.1.1"
curl -sX POST "http://localhost:8000/api/hydra/test?target=192.168.1.1&service=ssh"
curl -sX POST "http://localhost:8000/api/deepexploit?target=192.168.1.1"
curl -sX POST "http://localhost:8000/api/osint?target=example.com"
curl -sX POST "http://localhost:8000/api/pentest?target=192.168.1.1"
curl -sX POST "http://localhost:8000/api/malware?file_path=/tmp/test.exe"
curl -sX POST "http://localhost:8000/api/geo?ip=8.8.8.8"
curl -sX POST "http://localhost:8000/api/chat?query=What+is+XSS"
curl http://localhost:8000/api/wazuh/alerts?limit=20
curl http://localhost:8000/api/cloudflare/stats?zone_id=your_zone

# ── Threat Score ──────────────────────────────────────────────────
curl http://localhost:8000/score
curl -sX POST http://localhost:8000/score/update \
  -H "Content-Type: application/json" \
  -d '{"module":"pentest","score":55}'

# ── Bug Bounty (port 8001) ────────────────────────────────────────
curl -sX POST http://localhost:8001/report/submit \
  -H "Content-Type: application/json" \
  -d '{"title":"XSS in search","target":"https://example.com","description":"Reflected XSS via q param","severity":"MEDIUM","researcher_email":"r@example.com"}'
curl http://localhost:8001/reports
curl http://localhost:8001/stats
```

---

## 🔧 Systemd Service (Linux production)

Create `/etc/systemd/system/david-cis.service`:

```ini
[Unit]
Description=DAVID Cyber Intelligence System API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/david-cyber-intelligence-system
EnvironmentFile=/opt/david-cyber-intelligence-system/.env
ExecStart=/usr/bin/uvicorn core.api:app --host 0.0.0.0 --port 8000 --workers 2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable david-cis
sudo systemctl start david-cis
sudo systemctl status david-cis
```

---

## 👨‍💻 Developer

**David** — Full-Stack Security Engineer  
Nexuzy Tech Pvt Ltd | Devil Pvt Ltd  
Kolkata, West Bengal, India

🌐 [hypechats.com](https://hypechats.com)  
📧 david@nexuzytech.com  
🐙 [github.com/david0154](https://github.com/david0154)

> ⚠️ **Legal:** This API is for authorized security testing only. Scanning targets without written permission is illegal under CFAA, IT Act 2000, and equivalent laws worldwide.
