"""
Build standalone .exe (Windows) or binary (Linux/macOS)
Using PyInstaller
Run: python build_exe.py
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import subprocess
import sys
import os

APP_NAME = "DavidCyberIntelligence"
ICON = os.path.join("assets", "icon.ico") if os.path.exists(os.path.join("assets", "icon.ico")) else None

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",  # No console window on Windows
    "--name", APP_NAME,
    "--add-data", f"dashboard{os.pathsep}dashboard",
    "--add-data", f"data{os.pathsep}data",
    "--add-data", f".env.example{os.pathsep}.",
    "--hidden-import", "core.task_router",
    "--hidden-import", "core.llm_brain",
    "--hidden-import", "engines.malware_engine",
    "--hidden-import", "engines.network_engine",
    "--hidden-import", "engines.osint_engine",
    "--hidden-import", "engines.pentest_engine",
    "--hidden-import", "engines.defense_engine",
    "--hidden-import", "security.zap_engine",
    "--hidden-import", "security.wazuh_client",
    "--hidden-import", "security.openvas_client",
    "--hidden-import", "security.hydra_engine",
    "--hidden-import", "security.cloudflare_client",
    "--hidden-import", "security.deepexploit_engine",
    "--hidden-import", "tracking.flight_tracker",
    "--hidden-import", "tracking.ship_tracker",
    "--hidden-import", "tracking.satellite_tracker",
    "--hidden-import", "tracking.geo_engine",
    "--hidden-import", "intelligence.misp_client",
]

if ICON:
    cmd += ["--icon", ICON]

cmd.append("gui_app.py")

print(f"[Build] Running PyInstaller...")
print(f"[Build] Command: {' '.join(cmd)}")
result = subprocess.run(cmd)

if result.returncode == 0:
    print(f"\n[Build] ✔ Success! Output in: dist/{APP_NAME}")
else:
    print(f"\n[Build] ✖ Build failed. Check errors above.")
    print("Make sure PyInstaller is installed: pip install pyinstaller")
