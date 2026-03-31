"""
Ship Tracker — Full Implementation
MarineTraffic API + public AIS fallback
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import re
import requests
from datetime import datetime
from loguru import logger


class ShipTracker:
    """
    Live vessel tracking via MarineTraffic API v2 and public AIS sources.
    Supports MMSI, IMO, vessel name lookup, port arrivals, route history.
    """

    MT_BASE = "https://services.marinetraffic.com/api"
    FALLBACK_BASE = "https://www.vessel-finder.com"

    SHIP_TYPES = {
        0: "Not available", 20: "Wing In Ground", 30: "Fishing",
        31: "Towing", 36: "Sailing", 37: "Pleasure craft",
        60: "Passenger", 70: "Cargo", 80: "Tanker",
        90: "Other",
    }

    def __init__(self):
        self.api_key = os.getenv("MARINETRAFFIC_KEY", "")
        self._cache: dict = {}   # mmsi -> last position
        logger.success("ShipTracker ready.")

    # ─────────────────────────────────────────
    #  MAIN TRACK
    # ─────────────────────────────────────────
    def track(self, mmsi: str = "", imo: str = "",
              vessel_name: str = "") -> dict:
        """Track a vessel by MMSI, IMO, or name."""
        if mmsi:
            return self._get_by_mmsi(mmsi)
        if imo:
            return self._get_by_imo(imo)
        if vessel_name:
            return self._search_by_name(vessel_name)
        return {"status": "error", "message": "Provide mmsi, imo, or vessel_name"}

    # ─────────────────────────────────────────
    #  BY MMSI
    # ─────────────────────────────────────────
    def _get_by_mmsi(self, mmsi: str) -> dict:
        if not self.api_key:
            return self._public_ais_lookup(mmsi)
        try:
            r = requests.get(
                f"{self.MT_BASE}/exportvessel/v:8/{self.api_key}/",
                params={"mmsi": mmsi, "protocol": "jsono",
                        "msgtype": "extended"},
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                if data:
                    return {"status": "ok", "vessel": self._parse_mt(data[0])}
            return {"status": "not_found", "mmsi": mmsi}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────
    #  BY IMO
    # ─────────────────────────────────────────
    def _get_by_imo(self, imo: str) -> dict:
        if not self.api_key:
            return {"status": "error",
                    "message": "IMO lookup requires MARINETRAFFIC_KEY"}
        try:
            r = requests.get(
                f"{self.MT_BASE}/exportvessel/v:8/{self.api_key}/",
                params={"imo": imo, "protocol": "jsono",
                        "msgtype": "extended"},
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                if data:
                    return {"status": "ok", "vessel": self._parse_mt(data[0])}
            return {"status": "not_found", "imo": imo}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────
    #  SEARCH BY NAME
    # ─────────────────────────────────────────
    def _search_by_name(self, name: str) -> dict:
        if not self.api_key:
            return {"status": "error",
                    "message": "Name search requires MARINETRAFFIC_KEY"}
        try:
            r = requests.get(
                f"{self.MT_BASE}/getvessel/v:3/{self.api_key}/",
                params={"name": name, "protocol": "jsono"},
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                results = [self._parse_mt(v) for v in (data or [])[:10]]
                return {"status": "ok", "results": results,
                        "count": len(results)}
            return {"status": "not_found", "name": name}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────
    #  PORT ARRIVALS
    # ─────────────────────────────────────────
    def get_port_arrivals(self, port_id: str, limit: int = 20) -> dict:
        """Get recent vessel arrivals/departures at a port."""
        if not self.api_key:
            return {"status": "error", "message": "MARINETRAFFIC_KEY required"}
        try:
            r = requests.get(
                f"{self.MT_BASE}/portcalls/v:4/{self.api_key}/",
                params={"portid": port_id, "protocol": "jsono",
                        "msgtype": "simple", "limit": limit},
                timeout=10,
            )
            return {"status": "ok", "calls": r.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────
    #  ROUTE HISTORY
    # ─────────────────────────────────────────
    def get_route_history(self, mmsi: str, hours: int = 24) -> dict:
        """Get last N hours of vessel route."""
        if not self.api_key:
            return {"status": "error", "message": "MARINETRAFFIC_KEY required"}
        try:
            r = requests.get(
                f"{self.MT_BASE}/expectedarrivals/v:3/{self.api_key}/",
                params={"mmsi": mmsi, "protocol": "jsono",
                        "period": hours},
                timeout=10,
            )
            return {"status": "ok", "history": r.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────
    #  AREA SEARCH
    # ─────────────────────────────────────────
    def get_vessels_in_area(self, min_lat: float, max_lat: float,
                             min_lon: float, max_lon: float) -> dict:
        """Return all vessels in bounding box."""
        if not self.api_key:
            return {"status": "error", "message": "MARINETRAFFIC_KEY required"}
        try:
            r = requests.get(
                f"{self.MT_BASE}/getvessel/v:3/{self.api_key}/",
                params={
                    "minlat": min_lat, "maxlat": max_lat,
                    "minlon": min_lon, "maxlon": max_lon,
                    "protocol": "jsono",
                },
                timeout=10,
            )
            vessels = [self._parse_mt(v) for v in (r.json() or [])]
            return {"status": "ok", "count": len(vessels), "vessels": vessels}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────
    #  PUBLIC AIS FALLBACK (no key)
    # ─────────────────────────────────────────
    def _public_ais_lookup(self, mmsi: str) -> dict:
        """Free fallback via vessel-finder public endpoint."""
        try:
            r = requests.get(
                f"https://www.vessel-finder.com/vessels/{mmsi}",
                headers={"User-Agent": "DAVID-CIS"},
                timeout=8,
            )
            if r.status_code == 200:
                lat = re.search(r'"lat"\s*:\s*([\d.-]+)', r.text)
                lon = re.search(r'"lon"\s*:\s*([\d.-]+)', r.text)
                name = re.search(r'"name"\s*:\s*"([^"]+)"', r.text)
                speed = re.search(r'"speed"\s*:\s*([\d.]+)', r.text)
                return {
                    "status": "ok",
                    "source": "public_ais_fallback",
                    "vessel": {
                        "mmsi": mmsi,
                        "name": name.group(1) if name else "Unknown",
                        "latitude": float(lat.group(1)) if lat else None,
                        "longitude": float(lon.group(1)) if lon else None,
                        "speed_knots": float(speed.group(1)) if speed else None,
                    },
                }
        except Exception:
            pass
        return {"status": "error",
                "message": "MARINETRAFFIC_KEY not set and public fallback failed."}

    # ─────────────────────────────────────────
    #  PARSE MARINETRAFFIC RESPONSE
    # ─────────────────────────────────────────
    def _parse_mt(self, v: dict) -> dict:
        ship_type_code = int(v.get("SHIPTYPE", 0) or 0)
        ship_type_base = (ship_type_code // 10) * 10
        return {
            "mmsi":        v.get("MMSI", ""),
            "imo":         v.get("IMO", ""),
            "name":        v.get("SHIPNAME", ""),
            "flag":        v.get("FLAG", ""),
            "ship_type":   self.SHIP_TYPES.get(ship_type_base, f"Type {ship_type_code}"),
            "latitude":    v.get("LAT"),
            "longitude":   v.get("LON"),
            "speed_knots": v.get("SPEED"),
            "heading":     v.get("HEADING"),
            "course":      v.get("COURSE"),
            "status":      v.get("STATUS"),
            "destination": v.get("DESTINATION", ""),
            "eta":         v.get("ETA", ""),
            "draught":     v.get("DRAUGHT"),
            "length":      v.get("LENGTH"),
            "width":       v.get("WIDTH"),
            "last_seen":   v.get("TIMESTAMP", ""),
        }
