"""
Satellite Tracker
CelesTrak + N2YO + Skyfield + sgp4
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import os
import requests
from loguru import logger
from datetime import datetime, timezone

CELESTRAK_TLE_URL = "https://celestrak.org/SOCRATES/query.php"
CELESTRAK_STATIONS = "https://celestrak.org/SOCRATES/celestrak-stations.txt"


class SatelliteTracker:
    """
    Tracks satellites using TLE data from CelesTrak.
    Uses Skyfield for precise position calculation.
    """

    def __init__(self):
        self.n2yo_key = os.getenv("N2YO_API_KEY", "")

    def track(self, sat_id: str) -> dict:
        result = {
            "status": "ok",
            "sat_id": sat_id,
            "position": {},
            "tle": [],
        }
        try:
            from skyfield.api import load, EarthSatellite, wgs84
            from skyfield.api import utc

            tle_url = f"https://celestrak.org/satcat/tle.php?CATNR={sat_id}"
            resp = requests.get(tle_url, timeout=10)
            lines = resp.text.strip().splitlines()

            if len(lines) >= 3:
                name = lines[0].strip()
                line1 = lines[1].strip()
                line2 = lines[2].strip()
                result["tle"] = [name, line1, line2]

                ts = load.timescale()
                t = ts.now()
                satellite = EarthSatellite(line1, line2, name, ts)
                geocentric = satellite.at(t)
                subpoint = wgs84.subpoint(geocentric)

                result["position"] = {
                    "name": name,
                    "latitude": float(subpoint.latitude.degrees),
                    "longitude": float(subpoint.longitude.degrees),
                    "altitude_km": float(subpoint.elevation.km),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            else:
                result["status"] = "warning"
                result["message"] = f"No TLE data found for NORAD ID {sat_id}"
        except ImportError:
            logger.warning("skyfield not installed.")
            result["status"] = "warning"
            result["message"] = "Install skyfield: pip install skyfield"
        except Exception as e:
            logger.error(f"Satellite track error: {e}")
            result["status"] = "error"
            result["message"] = str(e)
        return result

    def list_stations(self) -> list:
        """Get ISS + major stations from CelesTrak."""
        try:
            from skyfield.api import load
            satellites = load.tle_file(
                "https://celestrak.org/SOCRATES/celestrak-stations.txt"
            )
            return [{"name": s.name, "epoch": str(s.epoch.utc_iso())} for s in satellites[:20]]
        except Exception as e:
            logger.error(f"Station list error: {e}")
            return []
