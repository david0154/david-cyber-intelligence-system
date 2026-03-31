"""
Bug Bounty Data Models
CVSS Scoring + Severity Classification
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import sqlite3
import json
import os
import hashlib
from datetime import datetime
from loguru import logger

DB_PATH = os.path.join("data", "bounty.db")


def get_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            target TEXT NOT NULL,
            vuln_type TEXT NOT NULL,
            severity TEXT DEFAULT 'UNKNOWN',
            cvss_score REAL DEFAULT 0.0,
            status TEXT DEFAULT 'PENDING',
            reporter TEXT DEFAULT 'anonymous',
            poc_path TEXT,
            screenshot_path TEXT,
            ai_validated INTEGER DEFAULT 0,
            ai_feedback TEXT,
            duplicate_of INTEGER,
            reward REAL DEFAULT 0.0,
            hash TEXT UNIQUE,
            created_at TEXT,
            updated_at TEXT
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            total_reward REAL DEFAULT 0.0,
            reports_submitted INTEGER DEFAULT 0,
            reports_accepted INTEGER DEFAULT 0,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS rewards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER,
            user TEXT,
            amount REAL,
            issued_at TEXT,
            FOREIGN KEY(report_id) REFERENCES reports(id)
        );
    """)
    conn.commit()
    conn.close()
    logger.success("[BountyDB] Initialized.")


def compute_hash(title: str, description: str, target: str) -> str:
    return hashlib.sha256(f"{title}{description}{target}".lower().encode()).hexdigest()
