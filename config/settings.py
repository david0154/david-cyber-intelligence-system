"""
Global Configuration
DAVID CYBER INTELLIGENCE SYSTEM
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- LLM ---
LLM_MODEL_PATH = os.getenv("LLM_MODEL_PATH", "models/mixtral.gguf")
LLM_MODEL_TYPE = os.getenv("LLM_MODEL_TYPE", "mistral")
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "512"))

# --- API Keys ---
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
MARINETRAFFIC_API_KEY = os.getenv("MARINETRAFFIC_API_KEY", "")
N2YO_API_KEY = os.getenv("N2YO_API_KEY", "")

# --- Threat Intel ---
MISP_URL = os.getenv("MISP_URL", "")
MISP_KEY = os.getenv("MISP_KEY", "")
OPENCTI_URL = os.getenv("OPENCTI_URL", "")
OPENCTI_TOKEN = os.getenv("OPENCTI_TOKEN", "")

# --- Database ---
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost:5432/davidcyber")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
NEO4J_URL = os.getenv("NEO4J_URL", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# --- Server ---
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# --- Paths ---
DATA_DIR = os.getenv("DATA_DIR", "data")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
YARA_RULES_DIR = os.path.join(DATA_DIR, "yara_rules")
THREAT_FEEDS_DIR = os.path.join(DATA_DIR, "threat_feeds")
