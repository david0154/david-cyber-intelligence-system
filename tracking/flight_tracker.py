"""
Flight Tracker — Full Implementation
OpenSky Network API + Tkinter map rendering
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import math
import time
import requests
from datetime import datetime
from loguru import logger


class FlightTracker:
    """
    Live flight tracking using the free OpenSky Network API.
    Supports callsign search, area bounding-box, country filter,
    flight path history, and alert mode.
    """

    OPENSKY_BASE = "https://opensky-network.org/api"

    def __init__(self):
        self.user = os.getenv("OPENSKY_USER", "")
        self.pw   = os.getenv("OPENSKY_PASS", "")
        self._auth = (self.user, self.pw) if self.user else None
        self._cache: dict = {}       # icao24 -> last state
        self._history: dict = {}     # icao24 -> [(lat,lon,ts), ...]
        self._watchlist: list = []   # callsigns to alert on
        logger.success("FlightTracker ready.")

    # ─────────────────────────────────────────
    #  MAIN TRACK
    # ─────────────────────────────────────────
    def track(self, callsign: str = "", icao24: str = "") -> dict:
        """Track a specific flight by callsign or ICAO24 hex."""
        all_states = self._fetch_all_states()
        if not all_states:
            return {"status": "error", "message": "OpenSky API unavailable"}

        for state in all_states:
            s = self._parse_state(state)
            if callsign and callsign.upper().strip() == s["callsign"].upper().strip():
                return {"status": "ok", "flight": s}
            if icao24 and icao24.lower() == s["icao24"].lower():
                return {"status": "ok", "flight": s}

        return {"status": "not_found",
                "message": f"Flight '{callsign or icao24}' not found in live data"}

    # ─────────────────────────────────────────
    #  AREA SEARCH
    # ─────────────────────────────────────────
    def get_flights_in_area(self, lat_min: float, lat_max: float,
                             lon_min: float, lon_max: float) -> dict:
        """Return all flights in a bounding box."""
        try:
            r = requests.get(
                f"{self.OPENSKY_BASE}/states/all",
                auth=self._auth,
                params={"lamin": lat_min, "lamax": lat_max,
                        "lomin": lon_min, "lomax": lon_max},
                timeout=12,
            )
            if r.status_code != 200:
                return {"status": "error", "code": r.status_code}
            states = r.json().get("states", []) or []
            flights = [self._parse_state(s) for s in states]
            return {"status": "ok", "count": len(flights), "flights": flights}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────
    #  ALL LIVE FLIGHTS
    # ─────────────────────────────────────────
    def get_all_live(self, country: str = "") -> dict:
        """Fetch all live flights, optionally filtered by origin country."""
        states = self._fetch_all_states()
        if states is None:
            return {"status": "error", "message": "OpenSky API unavailable"}
        flights = [self._parse_state(s) for s in states]
        if country:
            flights = [f for f in flights
                       if f.get("origin_country", "").lower() == country.lower()]
        return {"status": "ok", "count": len(flights), "flights": flights[:200]}

    # ─────────────────────────────────────────
    #  FLIGHT PATH HISTORY
    # ─────────────────────────────────────────
    def get_flight_path(self, icao24: str) -> dict:
        """Fetch the last 30 min trajectory from OpenSky."""
        end = int(time.time())
        begin = end - 1800  # 30 minutes
        try:
            r = requests.get(
                f"{self.OPENSKY_BASE}/tracks/all",
                auth=self._auth,
                params={"icao24": icao24.lower(), "time": begin},
                timeout=12,
            )
            if r.status_code != 200:
                return {"status": "error", "code": r.status_code}
            data = r.json()
            waypoints = [
                {"lat": w[1], "lon": w[2], "altitude": w[3],
                 "heading": w[4], "ts": w[0]}
                for w in (data.get("path") or [])
                if w[1] and w[2]
            ]
            return {
                "status": "ok",
                "icao24": icao24,
                "callsign": data.get("callsign", ""),
                "waypoints": waypoints,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────
    #  WATCHLIST ALERT
    # ─────────────────────────────────────────
    def add_watchlist(self, callsign: str):
        self._watchlist.append(callsign.upper().strip())

    def check_watchlist_alerts(self) -> list:
        """Return any live flights that match the watchlist."""
        alerts = []
        states = self._fetch_all_states()
        if not states:
            return alerts
        for state in states:
            s = self._parse_state(state)
            if s["callsign"].upper().strip() in self._watchlist:
                alerts.append(s)
        return alerts

    # ─────────────────────────────────────────
    #  HELPERS
    # ─────────────────────────────────────────
    def _fetch_all_states(self):
        try:
            r = requests.get(f"{self.OPENSKY_BASE}/states/all",
                             auth=self._auth, timeout=12)
            if r.status_code == 200:
                return r.json().get("states", []) or []
        except Exception as e:
            logger.debug(f"OpenSky fetch failed: {e}")
        return None

    def _parse_state(self, s: list) -> dict:
        """
        OpenSky state vector columns:
        0:icao24 1:callsign 2:origin_country 3:time_position
        4:last_contact 5:longitude 6:latitude 7:baro_altitude
        8:on_ground 9:velocity 10:true_track 11:vertical_rate
        12:sensors 13:geo_altitude 14:squawk 15:spi 16:position_source
        """
        return {
            "icao24":         str(s[0] or ""),
            "callsign":       str(s[1] or "").strip(),
            "origin_country": str(s[2] or ""),
            "latitude":       s[6],
            "longitude":      s[5],
            "altitude_m":     s[7],
            "on_ground":      bool(s[8]),
            "speed_ms":       s[9],
            "heading":        s[10],
            "vertical_rate":  s[11],
            "squawk":         s[14],
            "last_seen":      datetime.utcfromtimestamp(s[4]).isoformat() if s[4] else "",
        }

    @staticmethod
    def speed_ms_to_kmh(ms: float) -> float:
        return round((ms or 0) * 3.6, 1)

    @staticmethod
    def altitude_m_to_ft(m: float) -> float:
        return round((m or 0) * 3.28084, 0)
