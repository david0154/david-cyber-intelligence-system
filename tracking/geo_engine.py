"""
Geo Intelligence Engine
IP → Location mapping, Threat heatmaps
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

import requests
import os
from loguru import logger


class GeoEngine:
    """
    Maps IPs to geographic locations and generates threat heatmaps.
    """

    def map_ip(self, ip: str) -> dict:
        result = {
            "status": "ok",
            "ip": ip,
            "location": {},
            "map_file": None,
        }
        try:
            resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            if resp.status_code == 200:
                geo = resp.json()
                result["location"] = geo
                result["map_file"] = self._generate_map(geo)
        except Exception as e:
            logger.error(f"GeoEngine error: {e}")
            result["status"] = "error"
            result["message"] = str(e)
        return result

    def _generate_map(self, geo: dict) -> str:
        try:
            import folium
            lat = geo.get("lat", 0)
            lon = geo.get("lon", 0)
            city = geo.get("city", "Unknown")
            country = geo.get("country", "")
            m = folium.Map(location=[lat, lon], zoom_start=10)
            folium.Marker(
                [lat, lon],
                popup=f"{city}, {country}",
                icon=folium.Icon(color="red", icon="exclamation-sign"),
            ).add_to(m)
            os.makedirs("output", exist_ok=True)
            map_path = os.path.join("output", f"geo_{geo.get('query','ip')}.html")
            m.save(map_path)
            return map_path
        except ImportError:
            logger.warning("folium not installed.")
        except Exception as e:
            logger.error(f"Map generation error: {e}")
        return None

    def generate_heatmap(self, ip_list: list) -> str:
        """Generate a threat heatmap from a list of IPs."""
        locations = []
        for ip in ip_list:
            try:
                resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
                if resp.status_code == 200:
                    geo = resp.json()
                    if geo.get("status") == "success":
                        locations.append([geo["lat"], geo["lon"]])
            except Exception:
                continue
        if not locations:
            return None
        try:
            import folium
            from folium.plugins import HeatMap
            m = folium.Map(location=[20, 0], zoom_start=2)
            HeatMap(locations).add_to(m)
            os.makedirs("output", exist_ok=True)
            path = os.path.join("output", "threat_heatmap.html")
            m.save(path)
            return path
        except Exception as e:
            logger.error(f"Heatmap error: {e}")
            return None
