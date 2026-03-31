"""
OSINT Engine
Shodan + theHarvester + SpiderFoot + CyNER
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import os
import requests
from loguru import logger


class OSINTEngine:
    """
    Open-source intelligence gathering for IPs, domains, emails.
    """

    def __init__(self):
        self.shodan_key = os.getenv("SHODAN_API_KEY", "")

    def investigate(self, target: str) -> dict:
        result = {
            "status": "ok",
            "target": target,
            "shodan": {},
            "geolocation": {},
            "entities": [],
            "risk": "UNKNOWN",
        }

        result["geolocation"] = self._geolocate(target)
        result["shodan"] = self._shodan_lookup(target)

        # NER extraction
        result["entities"] = self._extract_entities(
            str(result["shodan"]) + " " + str(result["geolocation"])
        )

        return result

    def _geolocate(self, ip: str) -> dict:
        try:
            resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.debug(f"Geolocation failed: {e}")
        return {}

    def _shodan_lookup(self, ip: str) -> dict:
        if not self.shodan_key:
            return {"message": "SHODAN_API_KEY not set in environment."}
        try:
            import shodan
            api = shodan.Shodan(self.shodan_key)
            return api.host(ip)
        except ImportError:
            return {"message": "shodan library not installed."}
        except Exception as e:
            return {"message": str(e)}

    def _extract_entities(self, text: str) -> list:
        entities = []
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text[:5000])
            entities = [(ent.text, ent.label_) for ent in doc.ents]
        except Exception as e:
            logger.debug(f"NER extraction failed: {e}")
        return entities
