"""
Ship / Maritime Tracker
MarineTraffic API + AIS Stream
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import os
import requests
from loguru import logger


class ShipTracker:
    """
    Real-time vessel tracking via MarineTraffic and AIS.
    Requires MARINETRAFFIC_API_KEY environment variable.
    """

    def __init__(self):
        self.api_key = os.getenv("MARINETRAFFIC_API_KEY", "")

    def track(self, mmsi: str) -> dict:
        result = {
            "status": "ok",
            "mmsi": mmsi,
            "vessel": {},
        }
        if not self.api_key:
            result["status"] = "warning"
            result["message"] = "MARINETRAFFIC_API_KEY not set. Using public AIS fallback."
            result["vessel"] = self._public_ais_lookup(mmsi)
            return result

        try:
            url = f"https://services.marinetraffic.com/api/exportvessel/v:8/{self.api_key}/mmsi:{mmsi}/protocol:jsono"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                result["vessel"] = data
            else:
                result["status"] = "warning"
                result["message"] = f"MarineTraffic returned {resp.status_code}"
        except Exception as e:
            logger.error(f"Ship tracker error: {e}")
            result["status"] = "error"
            result["message"] = str(e)
        return result

    def _public_ais_lookup(self, mmsi: str) -> dict:
        """Fallback: public AIS data from aisstream.io or similar."""
        try:
            resp = requests.get(
                f"https://api.aisstream.io/v0/vessel/{mmsi}",
                timeout=5
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.debug(f"AIS fallback failed: {e}")
        return {"message": "Vessel data unavailable without API key."}
