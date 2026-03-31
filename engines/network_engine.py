"""
Network IDS Engine
LSTM/Autoencoder + Scapy + Suricata
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
"""

from loguru import logger


class NetworkEngine:
    """
    Live packet capture and anomaly detection.
    Uses Scapy for capture, ML model for classification.
    """

    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            from models.ids_model import IDSModel
            self.model = IDSModel()
            logger.success("IDS Model loaded.")
        except Exception as e:
            logger.warning(f"IDS Model unavailable: {e}")

    def monitor(self, interface: str = "eth0", packet_count: int = 100) -> dict:
        result = {
            "status": "ok",
            "interface": interface,
            "packets_captured": 0,
            "anomalies": [],
            "alerts": [],
        }
        try:
            from scapy.all import sniff, IP, TCP, UDP
            packets = sniff(iface=interface, count=packet_count, timeout=10)
            result["packets_captured"] = len(packets)
            for pkt in packets:
                if IP in pkt:
                    src = pkt[IP].src
                    dst = pkt[IP].dst
                    proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "OTHER"
                    # Basic anomaly detection
                    if self._is_suspicious(pkt):
                        result["anomalies"].append({
                            "src": src, "dst": dst,
                            "proto": proto, "reason": "Suspicious pattern"
                        })
        except ImportError:
            logger.warning("scapy not installed.")
            result["status"] = "warning"
            result["message"] = "Install scapy: pip install scapy"
        except Exception as e:
            logger.error(f"Network monitor error: {e}")
            result["status"] = "error"
            result["message"] = str(e)
        return result

    def _is_suspicious(self, pkt) -> bool:
        """Basic heuristics — expand with ML model."""
        try:
            from scapy.all import TCP
            if TCP in pkt:
                flags = pkt["TCP"].flags
                # SYN flood heuristic
                if flags == 0x002:
                    return True
        except Exception:
            pass
        return False
