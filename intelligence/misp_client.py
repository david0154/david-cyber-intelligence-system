#!/usr/bin/env python3
"""
DAVID CIS — Backward-compatible MISP shim
Routes all calls to ThreatIntelEngine (no server needed).
"""
from intelligence.threat_intel import get_engine

class MISPClient:
    """Drop-in MISP replacement using free public APIs + local SQLite."""
    def __init__(self):
        self._engine = get_engine()

    def search(self, value: str) -> dict:
        return self._engine.lookup(value)

    def lookup_ip(self, ip: str) -> dict:
        return self._engine.lookup(ip)

    def lookup_hash(self, hash_val: str) -> dict:
        return self._engine.lookup(hash_val)

    def lookup_domain(self, domain: str) -> dict:
        return self._engine.lookup(domain)

    def store_event(self, ioc_type, value, threat_type="",
                    confidence=50, tags=None):
        self._engine.db.store_ioc(
            ioc_type=ioc_type, value=value,
            threat_type=threat_type, confidence=confidence,
            source="local", tags=tags
        )

    def is_connected(self) -> bool:
        return True   # Always available (local DB)

    def stats(self) -> dict:
        return self._engine.db.stats()
