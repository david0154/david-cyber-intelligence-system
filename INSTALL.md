# 🔧 Installation Guide
## DAVID CYBER INTELLIGENCE SYSTEM
**Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd**

---

## ✅ Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | Required |
| pip | Latest | Required |
| Git | Any | Required |
| Nmap | 7.x+ | Optional (Pentest) |
| SQLMap | Latest | Optional (Pentest) |

---

## 🪟 Windows Installation

```powershell
# Clone repository
git clone https://github.com/david0154/david-cyber-intelligence-system
cd david-cyber-intelligence-system

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment config
copy .env.example .env
# Edit .env with your API keys

# Run the system
python main.py
```

**Windows Notes:**
- For Scapy packet capture: Install [Npcap](https://npcap.com)
- For YARA: `pip install yara-python` (pre-compiled wheels available)
- Run as Administrator for network monitoring

---

## 🍎 macOS Installation

```bash
# Clone repository
git clone https://github.com/david0154/david-cyber-intelligence-system
cd david-cyber-intelligence-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install system dependencies
brew install nmap libmagic

# Install Python dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# nano .env  # Add your API keys

# Run
python main.py
```

---

## 🐧 Linux Installation

```bash
# Clone repository
git clone https://github.com/david0154/david-cyber-intelligence-system
cd david-cyber-intelligence-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install system dependencies
sudo apt-get update
sudo apt-get install -y nmap libssl-dev libffi-dev python3-dev

# Install Python dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# nano .env  # Add your API keys

# Run (some features require root for raw sockets)
sudo python main.py
```

---

## 🤖 LLM Model Setup

Download the Mixtral GGUF model:
```bash
# Create models directory
mkdir models

# Download from HuggingFace (example — pick quantization level)
# Q4_K_M recommended for balance of speed/quality
wget https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf -O models/mixtral.gguf
```

Update your `.env`:
```
LLM_MODEL_PATH=models/mixtral.gguf
```

---

## 🚀 Run API Server

```bash
uvicorn core.api:app --reload --host 0.0.0.0 --port 8000
```

API Docs: http://localhost:8000/docs

---

## 🗄️ Database Setup (Optional)

### PostgreSQL
```bash
pip install psycopg2-binary
# Set POSTGRES_URL in .env
```

### Elasticsearch
```bash
docker run -d -p 9200:9200 elasticsearch:8.13.0
# Set ELASTICSEARCH_URL=http://localhost:9200
```

### Neo4j
```bash
docker run -d -p 7687:7687 -p 7474:7474 neo4j:5
# Set NEO4J_URL, NEO4J_USER, NEO4J_PASSWORD in .env
```
