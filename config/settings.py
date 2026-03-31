"""
Global Configuration v3
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
from dotenv import load_dotenv

load_dotenv()

# LLM
LLM_MODEL_PATH = os.getenv("LLM_MODEL_PATH", "models/mixtral.gguf")
LLM_MODEL_TYPE = os.getenv("LLM_MODEL_TYPE", "mistral")
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "512"))

# API Keys
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
MARINETRAFFIC_API_KEY = os.getenv("MARINETRAFFIC_API_KEY", "")
N2YO_API_KEY = os.getenv("N2YO_API_KEY", "")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")

# Security Tools
ZAP_URL = os.getenv("ZAP_URL", "http://localhost:8080")
ZAP_API_KEY = os.getenv("ZAP_API_KEY", "")
WAZUH_URL = os.getenv("WAZUH_URL", "https://localhost:55000")
WAZUH_USER = os.getenv("WAZUH_USER", "wazuh")
WAZUH_PASS = os.getenv("WAZUH_PASS", "wazuh")
OPENVAS_URL = os.getenv("OPENVAS_URL", "https://localhost:9392")
OPENVAS_USER = os.getenv("OPENVAS_USER", "admin")
OPENVAS_PASS = os.getenv("OPENVAS_PASS", "admin")

# Threat Intel
MISP_URL = os.getenv("MISP_URL", "")
MISP_KEY = os.getenv("MISP_KEY", "")
OPENCTI_URL = os.getenv("OPENCTI_URL", "")
OPENCTI_TOKEN = os.getenv("OPENCTI_TOKEN", "")

# Database
POSTGRES_URL = os.getenv("POSTGRES_URL",
    "postgresql://user:password@localhost:5432/davidcyber")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
NEO4J_URL = os.getenv("NEO4J_URL", "bolt://localhost:7687")

# Alerts
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Paths
DATA_DIR = os.getenv("DATA_DIR", "data")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
