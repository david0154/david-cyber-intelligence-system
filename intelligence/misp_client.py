"""
MISP Threat Intelligence Client
IOC lookup and event management
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
from loguru import logger


class MISPClient:
    """
    Connects to a MISP instance for IOC lookups.
    Requires MISP_URL and MISP_KEY environment variables.
    """

    def __init__(self):
        self.url = os.getenv("MISP_URL", "")
        self.key = os.getenv("MISP_KEY", "")
        self.misp = None
        self._connect()

    def _connect(self):
        if not self.url or not self.key:
            logger.warning("MISP_URL or MISP_KEY not set. MISP integration disabled.")
            return
        try:
            from pymisp import PyMISP
            self.misp = PyMISP(self.url, self.key, ssl=False)
            logger.success("Connected to MISP.")
        except ImportError:
            logger.warning("pymisp not installed.")
        except Exception as e:
            logger.error(f"MISP connection failed: {e}")

    def lookup(self, ioc: str) -> dict:
        if self.misp is None:
            return {"status": "offline", "message": "MISP not configured.", "ioc": ioc}
        try:
            result = self.misp.search(value=ioc, pythonify=True)
            events = [{"id": e.id, "info": e.info, "date": str(e.date)} for e in result[:5]]
            return {
                "status": "ok",
                "ioc": ioc,
                "matches": len(result),
                "events": events,
                "flagged": len(result) > 0,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def submit_ioc(self, ioc: str, ioc_type: str, comment: str = "") -> dict:
        if self.misp is None:
            return {"status": "offline"}
        try:
            from pymisp import MISPEvent, MISPAttribute
            event = MISPEvent()
            event.info = f"David Cyber Intel: {ioc}"
            event.add_attribute(ioc_type, ioc, comment=comment)
            self.misp.add_event(event)
            return {"status": "ok", "submitted": ioc}
        except Exception as e:
            return {"status": "error", "message": str(e)}
