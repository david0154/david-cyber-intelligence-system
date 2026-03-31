"""
OpenCTI Threat Intelligence Client
Graph-based threat relationship management
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
from loguru import logger


class OpenCTIClient:
    """
    Connects to OpenCTI for threat graph intelligence.
    Requires OPENCTI_URL and OPENCTI_TOKEN environment variables.
    """

    def __init__(self):
        self.url = os.getenv("OPENCTI_URL", "")
        self.token = os.getenv("OPENCTI_TOKEN", "")
        self.client = None
        self._connect()

    def _connect(self):
        if not self.url or not self.token:
            logger.warning("OPENCTI_URL or OPENCTI_TOKEN not set.")
            return
        try:
            from pycti import OpenCTIApiClient
            self.client = OpenCTIApiClient(self.url, self.token)
            logger.success("Connected to OpenCTI.")
        except ImportError:
            logger.warning("pycti not installed.")
        except Exception as e:
            logger.error(f"OpenCTI connection failed: {e}")

    def search_indicator(self, value: str) -> dict:
        if self.client is None:
            return {"status": "offline", "message": "OpenCTI not configured."}
        try:
            indicators = self.client.indicator.list(
                filters=[{"key": "name", "values": [value]}]
            )
            return {"status": "ok", "value": value, "indicators": indicators[:5]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
