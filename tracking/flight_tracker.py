"""
Flight Tracker Module
OpenSky Network + ADS-B Exchange
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import requests
from loguru import logger

OPENSKY_API = "https://opensky-network.org/api"


class FlightTracker:
    """
    Real-time aircraft tracking via OpenSky Network API.
    """

    def track(self, callsign: str = "") -> dict:
        result = {
            "status": "ok",
            "callsign": callsign,
            "flights": [],
        }
        try:
            url = f"{OPENSKY_API}/states/all"
            params = {}
            if callsign:
                params["callsign"] = callsign.upper().strip().ljust(8)
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                states = data.get("states", []) or []
                for s in states[:20]:
                    result["flights"].append({
                        "icao24": s[0],
                        "callsign": (s[1] or "").strip(),
                        "origin_country": s[2],
                        "longitude": s[5],
                        "latitude": s[6],
                        "altitude_m": s[7],
                        "velocity_mps": s[9],
                        "on_ground": s[8],
                    })
            else:
                result["status"] = "warning"
                result["message"] = f"OpenSky returned {resp.status_code}"
        except Exception as e:
            logger.error(f"Flight tracker error: {e}")
            result["status"] = "error"
            result["message"] = str(e)
        return result

    def get_all_flights(self, bbox: tuple = None) -> dict:
        """
        Get all flights. Optional bbox: (lamin, lomin, lamax, lomax)
        """
        params = {}
        if bbox:
            params = {"lamin": bbox[0], "lomin": bbox[1], "lamax": bbox[2], "lomax": bbox[3]}
        try:
            resp = requests.get(f"{OPENSKY_API}/states/all", params=params, timeout=15)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.error(f"Get all flights error: {e}")
        return {}
