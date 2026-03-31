"""
Local Threat Database (SQLite-based cache)
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import sqlite3
import os
import json
from datetime import datetime
from loguru import logger

DB_PATH = os.path.join("data", "threat_cache.db")


class ThreatDB:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._init_tables()

    def _init_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ioc TEXT NOT NULL,
                ioc_type TEXT,
                source TEXT,
                score REAL,
                level TEXT,
                metadata TEXT,
                created_at TEXT
            )
        """)
        self.conn.commit()

    def store(self, ioc: str, ioc_type: str, source: str, score: float, metadata: dict = None):
        from core.threat_scorer import ThreatScorer
        scorer = ThreatScorer()
        scorer.update("intel", score)
        level = scorer.level()
        self.conn.execute(
            "INSERT INTO threats (ioc, ioc_type, source, score, level, metadata, created_at) VALUES (?,?,?,?,?,?,?)",
            (ioc, ioc_type, source, score, level, json.dumps(metadata or {}), datetime.utcnow().isoformat())
        )
        self.conn.commit()
        logger.info(f"Stored IOC: {ioc} [{level}]")

    def lookup(self, ioc: str) -> list:
        cur = self.conn.execute("SELECT * FROM threats WHERE ioc = ?", (ioc,))
        rows = cur.fetchall()
        return [{"id": r[0], "ioc": r[1], "type": r[2], "source": r[3],
                 "score": r[4], "level": r[5], "metadata": json.loads(r[6]), "created_at": r[7]}
                for r in rows]
