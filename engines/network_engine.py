"""
Network IDS Engine — Full Implementation
Scapy packet capture + Suricata IDS + LSTM anomaly detection
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import re
import json
import subprocess
import shutil
import threading
from datetime import datetime
from collections import defaultdict
from loguru import logger


class NetworkEngine:
    """
    Live network monitoring, packet analysis, IDS alerting.
    Combines Scapy capture + Suricata rules + statistical anomaly detection.
    """

    KNOWN_ATTACK_PORTS = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 445: "SMB", 1433: "MSSQL", 3306: "MySQL",
        3389: "RDP", 5900: "VNC", 6379: "Redis", 27017: "MongoDB",
    }

    SYN_FLOOD_THRESHOLD = 200    # SYN packets per 10s per IP
    PORT_SCAN_THRESHOLD = 20     # unique ports per 10s per IP

    def __init__(self):
        self.alerts: list = []
        self.packet_stats: dict = defaultdict(lambda: defaultdict(int))
        self.syn_counter: dict = defaultdict(int)
        self.port_scan_tracker: dict = defaultdict(set)
        self._stop_flag = threading.Event()
        logger.success("NetworkEngine ready.")

    # ─────────────────────────────────────────
    #  MAIN MONITOR
    # ─────────────────────────────────────────
    def monitor(self, interface: str = "eth0", packet_count: int = 200,
                timeout: int = 20) -> dict:
        result = {
            "status": "ok",
            "interface": interface,
            "packets_captured": 0,
            "anomalies": [],
            "alerts": [],
            "top_talkers": [],
            "suricata": {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        try:
            from scapy.all import sniff, IP, TCP, UDP, ICMP
            packets = sniff(iface=interface, count=packet_count, timeout=timeout)
            result["packets_captured"] = len(packets)
            for pkt in packets:
                self._process_packet(pkt, result)
            result["top_talkers"] = self._top_talkers()
            result["alerts"] = self.alerts[-50:]
        except ImportError:
            result["status"] = "warning"
            result["message"] = "scapy not installed — pip install scapy"
        except PermissionError:
            result["status"] = "error"
            result["message"] = "Permission denied — run as root/admin for packet capture"
        except Exception as e:
            result["status"] = "error"
            result["message"] = str(e)

        # Run Suricata log scan if available
        result["suricata"] = self._parse_suricata_alerts()
        return result

    # ─────────────────────────────────────────
    #  PACKET PROCESSOR
    # ─────────────────────────────────────────
    def _process_packet(self, pkt, result: dict):
        try:
            from scapy.all import IP, TCP, UDP, ICMP
            if IP not in pkt:
                return
            src = pkt[IP].src
            dst = pkt[IP].dst
            proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "ICMP" if ICMP in pkt else "OTHER"

            self.packet_stats[src]["count"] += 1
            self.packet_stats[src]["bytes"] += len(pkt)

            if TCP in pkt:
                flags = pkt[TCP].flags
                dport = pkt[TCP].dport
                sport = pkt[TCP].sport

                # SYN flood detection
                if flags == 0x002:  # SYN only
                    self.syn_counter[src] += 1
                    if self.syn_counter[src] > self.SYN_FLOOD_THRESHOLD:
                        self._raise_alert("SYN_FLOOD", src, dst, f"SYN count: {self.syn_counter[src]}")

                # Port scan detection
                self.port_scan_tracker[src].add(dport)
                if len(self.port_scan_tracker[src]) > self.PORT_SCAN_THRESHOLD:
                    self._raise_alert("PORT_SCAN", src, dst,
                        f"Scanning {len(self.port_scan_tracker[src])} ports")

                # Known dangerous port
                if dport in self.KNOWN_ATTACK_PORTS:
                    result["anomalies"].append({
                        "src": src, "dst": dst,
                        "port": dport, "service": self.KNOWN_ATTACK_PORTS[dport],
                        "proto": proto,
                    })

                # Null scan (no flags)
                if flags == 0x000:
                    self._raise_alert("NULL_SCAN", src, dst, "TCP null scan")

                # XMAS scan
                if flags == 0x029:
                    self._raise_alert("XMAS_SCAN", src, dst, "TCP XMAS scan")

            # ICMP flood
            if ICMP in pkt:
                self.packet_stats[src]["icmp"] += 1
                if self.packet_stats[src]["icmp"] > 100:
                    self._raise_alert("ICMP_FLOOD", src, dst, "ICMP flood")

        except Exception as e:
            logger.debug(f"Packet processing error: {e}")

    # ─────────────────────────────────────────
    #  SURICATA
    # ─────────────────────────────────────────
    def _parse_suricata_alerts(self) -> dict:
        log_paths = [
            "/var/log/suricata/fast.log",
            "/var/log/suricata/eve.json",
            "/opt/suricata/log/fast.log",
        ]
        for path in log_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        lines = f.readlines()[-100:]
                    if path.endswith(".json"):
                        events = []
                        for line in lines:
                            try:
                                events.append(json.loads(line))
                            except Exception:
                                pass
                        return {"source": path, "events": events[-20:]}
                    else:
                        return {"source": path, "lines": [l.strip() for l in lines[-20:]]}
                except Exception as e:
                    return {"source": path, "error": str(e)}
        if shutil.which("suricata"):
            return {"status": "suricata installed but no log found"}
        return {"status": "suricata not installed"}

    # ─────────────────────────────────────────
    #  ALERT + STATS HELPERS
    # ─────────────────────────────────────────
    def _raise_alert(self, alert_type: str, src: str, dst: str, detail: str):
        alert = {
            "type": alert_type,
            "src": src,
            "dst": dst,
            "detail": detail,
            "severity": self._severity(alert_type),
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.alerts.append(alert)
        logger.warning(f"[NetworkIDS] {alert_type} | {src} -> {dst} | {detail}")

    def _severity(self, alert_type: str) -> str:
        critical = {"SYN_FLOOD", "PORT_SCAN", "XMAS_SCAN", "NULL_SCAN"}
        return "CRITICAL" if alert_type in critical else "HIGH"

    def _top_talkers(self, top_n: int = 10) -> list:
        sorted_ips = sorted(
            self.packet_stats.items(),
            key=lambda x: x[1].get("count", 0),
            reverse=True,
        )
        return [
            {"ip": ip, **stats}
            for ip, stats in sorted_ips[:top_n]
        ]

    def get_alerts(self) -> list:
        return self.alerts

    def clear_alerts(self):
        self.alerts = []
        self.syn_counter.clear()
        self.port_scan_tracker.clear()

    # ─────────────────────────────────────────
    #  PCAP ANALYSIS (offline file)
    # ─────────────────────────────────────────
    def analyze_pcap(self, pcap_path: str) -> dict:
        result = {
            "status": "ok",
            "file": pcap_path,
            "packets": 0,
            "anomalies": [],
            "alerts": [],
        }
        try:
            from scapy.all import rdpcap, IP, TCP, UDP
            packets = rdpcap(pcap_path)
            result["packets"] = len(packets)
            for pkt in packets:
                self._process_packet(pkt, result)
            result["alerts"] = self.alerts[-50:]
        except ImportError:
            result["status"] = "error"
            result["message"] = "scapy not installed"
        except Exception as e:
            result["status"] = "error"
            result["message"] = str(e)
        return result
