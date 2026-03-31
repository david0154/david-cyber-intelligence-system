"""
Task Router — Routes queries to appropriate engine modules
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

from loguru import logger


class TaskRouter:
    """
    Central router that directs user requests to the appropriate engine.
    Supports: malware, network, osint, pentest, defense, intel,
              flight, ship, satellite, geo, chat
    """

    def __init__(self):
        self._engines = {}
        self._load_engines()

    def _load_engines(self):
        # Lazy-load engines to prevent startup failures if optional deps missing
        try:
            from engines.malware_engine import MalwareEngine
            self._engines["malware"] = MalwareEngine()
        except Exception as e:
            logger.warning(f"MalwareEngine load failed: {e}")

        try:
            from engines.network_engine import NetworkEngine
            self._engines["network"] = NetworkEngine()
        except Exception as e:
            logger.warning(f"NetworkEngine load failed: {e}")

        try:
            from engines.osint_engine import OSINTEngine
            self._engines["osint"] = OSINTEngine()
        except Exception as e:
            logger.warning(f"OSINTEngine load failed: {e}")

        try:
            from engines.pentest_engine import PentestEngine
            self._engines["pentest"] = PentestEngine()
        except Exception as e:
            logger.warning(f"PentestEngine load failed: {e}")

        try:
            from engines.defense_engine import DefenseEngine
            self._engines["defense"] = DefenseEngine()
        except Exception as e:
            logger.warning(f"DefenseEngine load failed: {e}")

        try:
            from intelligence.misp_client import MISPClient
            self._engines["intel"] = MISPClient()
        except Exception as e:
            logger.warning(f"ThreatIntel load failed: {e}")

        try:
            from tracking.flight_tracker import FlightTracker
            self._engines["flight"] = FlightTracker()
        except Exception as e:
            logger.warning(f"FlightTracker load failed: {e}")

        try:
            from tracking.ship_tracker import ShipTracker
            self._engines["ship"] = ShipTracker()
        except Exception as e:
            logger.warning(f"ShipTracker load failed: {e}")

        try:
            from tracking.satellite_tracker import SatelliteTracker
            self._engines["satellite"] = SatelliteTracker()
        except Exception as e:
            logger.warning(f"SatelliteTracker load failed: {e}")

        try:
            from tracking.geo_engine import GeoEngine
            self._engines["geo"] = GeoEngine()
        except Exception as e:
            logger.warning(f"GeoEngine load failed: {e}")

        try:
            from core.llm_brain import LLMBrain
            self._engines["chat"] = LLMBrain()
        except Exception as e:
            logger.warning(f"LLMBrain load failed: {e}")

    def route(self, module: str, params: dict) -> dict:
        """
        Route a request to the correct engine.
        Returns a result dict with status, data, and optional LLM explanation.
        """
        module = module.lower().strip()
        engine = self._engines.get(module)

        if engine is None:
            return {"status": "error", "message": f"Module '{module}' not available."}

        logger.info(f"Routing to: {module} | Params: {params}")

        try:
            if module == "malware":
                return engine.analyze(params.get("file_path", ""))
            elif module == "network":
                return engine.monitor(params.get("interface", "eth0"))
            elif module == "osint":
                return engine.investigate(params.get("target", ""))
            elif module == "pentest":
                return engine.run(params.get("target", ""))
            elif module == "defense":
                return engine.status()
            elif module == "intel":
                return engine.lookup(params.get("ioc", ""))
            elif module == "flight":
                return engine.track(params.get("callsign", ""))
            elif module == "ship":
                return engine.track(params.get("mmsi", ""))
            elif module == "satellite":
                return engine.track(params.get("sat_id", ""))
            elif module == "geo":
                return engine.map_ip(params.get("ip", ""))
            elif module == "chat":
                response = engine.think(params.get("query", ""))
                return {"status": "ok", "response": response}
            else:
                return {"status": "error", "message": "Unknown module"}
        except Exception as e:
            logger.error(f"Engine error in {module}: {e}")
            return {"status": "error", "message": str(e)}
