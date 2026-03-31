"""
Hydra Brute-Force Test Engine
Tests login protection against brute-force attacks
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
Supports: Windows | macOS | Linux
WARNING: Use ONLY on systems you own or have permission to test.
"""

import subprocess
import shutil
import os
from loguru import logger


class HydraEngine:
    """
    Tests whether login endpoints properly block brute-force attempts.
    Uses Hydra tool - must be installed separately.
    Install: https://github.com/vanhauser-thc/thc-hydra
    """

    def test(self, target: str, service: str = "ssh", wordlist: str = None) -> dict:
        result = {
            "status": "ok",
            "target": target,
            "service": service,
            "result": "",
            "blocked": None,
            "recommendation": "",
        }

        hydra_cmd = "hydra"
        # Windows: hydra.exe
        if os.name == "nt":
            hydra_cmd = "hydra.exe"

        if not shutil.which(hydra_cmd):
            result["status"] = "warning"
            result["message"] = (
                "Hydra not found. Install from: https://github.com/vanhauser-thc/thc-hydra\n"
                "Linux: sudo apt install hydra\n"
                "macOS: brew install hydra"
            )
            return result

        # Use small default wordlist if none provided
        default_wl = os.path.join("data", "wordlists", "top10.txt")
        wl = wordlist or default_wl
        if not os.path.exists(wl):
            os.makedirs(os.path.dirname(wl), exist_ok=True)
            with open(wl, "w") as f:
                f.write("admin\npassword\n123456\nroot\ntest\nuser\nguest\nadmin123\npass\n1234")

        try:
            cmd = [hydra_cmd, "-L", wl, "-P", wl, "-t", "4", "-f", "-o", "-", target, service]
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            result["result"] = out.stdout[:2000]
            if "login:" in out.stdout.lower():
                result["blocked"] = False
                result["recommendation"] = "CRITICAL: Login not blocking brute-force! Implement rate-limiting and account lockout."
            else:
                result["blocked"] = True
                result["recommendation"] = "GOOD: Login appears to block brute-force attempts."
        except subprocess.TimeoutExpired:
            result["blocked"] = True
            result["recommendation"] = "Timeout — login likely has rate limiting in place."
        except Exception as e:
            result["status"] = "error"
            result["message"] = str(e)
        return result
