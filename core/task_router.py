"""
Task Router v2 - Routes all modules with graceful fallbacks
FIXED: All import errors caught individually, never crashes
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

from loguru import logger


class TaskRouter:
    def __init__(self):
        self._engines = {}
        self._load_engines()

    def _safe_load(self, key, loader_fn):
        try:
            self._engines[key] = loader_fn()
            logger.success(f"[Router] Loaded: {key}")
        except Exception as e:
            logger.warning(f"[Router] {key} unavailable: {e}")

    def _load_engines(self):
        self._safe_load("malware", lambda: __import__('engines.malware_engine', fromlist=['MalwareEngine']).MalwareEngine())
        self._safe_load("network", lambda: __import__('engines.network_engine', fromlist=['NetworkEngine']).NetworkEngine())
        self._safe_load("osint", lambda: __import__('engines.osint_engine', fromlist=['OSINTEngine']).OSINTEngine())
        self._safe_load("pentest", lambda: __import__('engines.pentest_engine', fromlist=['PentestEngine']).PentestEngine())
        self._safe_load("defense", lambda: __import__('engines.defense_engine', fromlist=['DefenseEngine']).DefenseEngine())
        self._safe_load("intel", lambda: __import__('intelligence.misp_client', fromlist=['MISPClient']).MISPClient())
        self._safe_load("flight", lambda: __import__('tracking.flight_tracker', fromlist=['FlightTracker']).FlightTracker())
        self._safe_load("ship", lambda: __import__('tracking.ship_tracker', fromlist=['ShipTracker']).ShipTracker())
        self._safe_load("satellite", lambda: __import__('tracking.satellite_tracker', fromlist=['SatelliteTracker']).SatelliteTracker())
        self._safe_load("geo", lambda: __import__('tracking.geo_engine', fromlist=['GeoEngine']).GeoEngine())
        self._safe_load("zap", lambda: __import__('security.zap_engine', fromlist=['ZAPEngine']).ZAPEngine())
        self._safe_load("wazuh", lambda: __import__('security.wazuh_client', fromlist=['WazuhClient']).WazuhClient())
        self._safe_load("openvas", lambda: __import__('security.openvas_client', fromlist=['OpenVASClient']).OpenVASClient())
        self._safe_load("hydra", lambda: __import__('security.hydra_engine', fromlist=['HydraEngine']).HydraEngine())
        self._safe_load("cloudflare", lambda: __import__('security.cloudflare_client', fromlist=['CloudflareClient']).CloudflareClient())
        self._safe_load("deepexploit", lambda: __import__('security.deepexploit_engine', fromlist=['DeepExploitEngine']).DeepExploitEngine())
        self._safe_load("chat", lambda: __import__('core.llm_brain', fromlist=['LLMBrain']).LLMBrain())

    def route(self, module: str, params: dict) -> dict:
        module = module.lower().strip()
        engine = self._engines.get(module)
        if engine is None:
            return {"status": "error", "message": f"Module '{module}' not loaded. Check install."}
        logger.info(f"[Router] -> {module} | {params}")
        try:
            dispatch = {
                "malware": lambda: engine.analyze(params.get("file_path", "")),
                "network": lambda: engine.monitor(params.get("interface", "eth0")),
                "osint": lambda: engine.investigate(params.get("target", "")),
                "pentest": lambda: engine.run(params.get("target", "")),
                "defense": lambda: engine.status(),
                "intel": lambda: engine.lookup(params.get("ioc", "")),
                "flight": lambda: engine.track(params.get("callsign", "")),
                "ship": lambda: engine.track(params.get("mmsi", "")),
                "satellite": lambda: engine.track(params.get("sat_id", "")),
                "geo": lambda: engine.map_ip(params.get("ip", "")),
                "zap": lambda: engine.scan(params.get("url", "")),
                "wazuh": lambda: engine.get_alerts(params.get("limit", 20)),
                "openvas": lambda: engine.scan(params.get("target", "")),
                "hydra": lambda: engine.test(params.get("target", ""), params.get("service", "ssh")),
                "cloudflare": lambda: engine.get_stats(params.get("zone_id", "")),
                "deepexploit": lambda: engine.exploit(params.get("target", "")),
                "chat": lambda: {"status": "ok", "response": engine.think(params.get("query", ""))},
            }
            fn = dispatch.get(module)
            if fn:
                return fn()
            return {"status": "error", "message": "No dispatch handler found"}
        except Exception as e:
            logger.error(f"[Router] Engine crash in {module}: {e}")
            return {"status": "error", "message": str(e)}
