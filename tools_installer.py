#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM - Auto Tool Installer
One-click install for ALL required tools on Windows / macOS / Linux
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd

Supports:
  - Python packages (pip)
  - Windows: winget / Chocolatey / direct .exe download
  - Linux: apt / yum / dnf
  - macOS: brew
"""

import subprocess
import shutil
import sys
import os
import platform
import threading
import urllib.request
import zipfile
import tempfile
from loguru import logger

OS_TYPE = platform.system()  # 'Windows', 'Linux', 'Darwin'


# ─────────────────────────────────────────────────────────────────────────────
#  TOOL REGISTRY
#  Each tool: name, check_cmd, category, description, install instructions
# ─────────────────────────────────────────────────────────────────────────────
TOOLS = [
    # ── Python Packages ───────────────────────────────────────────────────
    {"id": "pip_core",
     "name": "Core Python Packages",
     "category": "Python",
     "desc": "fastapi, uvicorn, loguru, requests, python-dotenv, pydantic",
     "check": lambda: _pip_check(["fastapi", "uvicorn", "loguru", "requests", "dotenv", "pydantic"]),
     "install": lambda cb: _pip_install(
         ["fastapi", "uvicorn[standard]", "loguru", "requests",
          "python-dotenv", "pydantic"], cb)},

    {"id": "pip_security",
     "name": "Security Python Packages",
     "category": "Python",
     "desc": "yara-python, pefile, capstone, scapy, pyshark",
     "check": lambda: _pip_check(["yara", "pefile", "capstone"]),
     "install": lambda cb: _pip_install(
         ["pefile", "capstone", "pyshark", "scapy",
          "cryptography", "paramiko"], cb)},

    {"id": "pip_yara",
     "name": "YARA (Malware Scanner)",
     "category": "Python",
     "desc": "YARA signature-based malware detection",
     "check": lambda: _pip_check(["yara"]),
     "install": lambda cb: _install_yara(cb)},

    {"id": "pip_ml",
     "name": "ML / AI Packages",
     "category": "Python",
     "desc": "torch (CPU), scikit-learn, numpy, pandas, transformers",
     "check": lambda: _pip_check(["torch", "sklearn", "numpy"]),
     "install": lambda cb: _pip_install(
         ["torch", "scikit-learn", "numpy", "pandas",
          "transformers", "ctransformers"], cb)},

    {"id": "pip_tracking",
     "name": "Tracking Packages",
     "category": "Python",
     "desc": "folium, skyfield, opensky-api, requests",
     "check": lambda: _pip_check(["folium", "skyfield"]),
     "install": lambda cb: _pip_install(
         ["folium", "skyfield", "opensky-api"], cb)},

    {"id": "pip_db",
     "name": "Database Packages",
     "category": "Python",
     "desc": "sqlalchemy, psycopg2-binary, elasticsearch",
     "check": lambda: _pip_check(["sqlalchemy", "elasticsearch"]),
     "install": lambda cb: _pip_install(
         ["sqlalchemy", "psycopg2-binary", "elasticsearch",
          "aiofiles", "python-multipart"], cb)},

    {"id": "pip_bounty",
     "name": "Bug Bounty Packages",
     "category": "Python",
     "desc": "httpx, pillow, python-jose, passlib",
     "check": lambda: _pip_check(["httpx", "PIL", "jose"]),
     "install": lambda cb: _pip_install(
         ["httpx", "pillow", "python-jose[cryptography]", "passlib",
          "bcrypt", "python-telegram-bot"], cb)},

    # ── External Security Tools ───────────────────────────────────────────
    {"id": "nmap",
     "name": "Nmap",
     "category": "Security Tools",
     "desc": "Port scanner + CVE detection (REQUIRED for vuln scan)",
     "check": lambda: shutil.which("nmap") is not None,
     "install": lambda cb: _install_tool("nmap", cb)},

    {"id": "sqlmap",
     "name": "SQLMap",
     "category": "Security Tools",
     "desc": "SQL injection testing tool",
     "check": lambda: shutil.which("sqlmap") is not None,
     "install": lambda cb: _install_tool("sqlmap", cb)},

    {"id": "hydra",
     "name": "Hydra",
     "category": "Security Tools",
     "desc": "Brute-force login protection tester",
     "check": lambda: shutil.which("hydra") is not None,
     "install": lambda cb: _install_tool("hydra", cb)},

    {"id": "metasploit",
     "name": "Metasploit Framework",
     "category": "Security Tools",
     "desc": "Exploitation framework (auto-exploit engine)",
     "check": lambda: shutil.which("msfconsole") is not None,
     "install": lambda cb: _install_tool("metasploit", cb)},

    {"id": "suricata",
     "name": "Suricata IDS",
     "category": "Security Tools",
     "desc": "Network intrusion detection / prevention system",
     "check": lambda: shutil.which("suricata") is not None,
     "install": lambda cb: _install_tool("suricata", cb)},

    {"id": "wireshark",
     "name": "Wireshark / tshark",
     "category": "Security Tools",
     "desc": "Network packet capture and analysis",
     "check": lambda: (shutil.which("tshark") is not None or
                       shutil.which("wireshark") is not None),
     "install": lambda cb: _install_tool("wireshark", cb)},

    {"id": "git",
     "name": "Git",
     "category": "System",
     "desc": "Version control (required for some tool installs)",
     "check": lambda: shutil.which("git") is not None,
     "install": lambda cb: _install_tool("git", cb)},

    {"id": "curl",
     "name": "curl",
     "category": "System",
     "desc": "HTTP client (required for API testing)",
     "check": lambda: shutil.which("curl") is not None,
     "install": lambda cb: _install_tool("curl", cb)},
]


# ─────────────────────────────────────────────────────────────────────────────
#  STATUS CHECK
# ─────────────────────────────────────────────────────────────────────────────
def check_all() -> dict:
    """Returns {tool_id: True/False} for all tools."""
    results = {}
    for tool in TOOLS:
        try:
            results[tool["id"]] = bool(tool["check"]())
        except Exception:
            results[tool["id"]] = False
    return results


def check_tool(tool_id: str) -> bool:
    for t in TOOLS:
        if t["id"] == tool_id:
            try:
                return bool(t["check"]())
            except Exception:
                return False
    return False


# ─────────────────────────────────────────────────────────────────────────────
#  PIP HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _pip_check(modules: list) -> bool:
    for m in modules:
        try:
            __import__(m)
        except ImportError:
            return False
    return True


def _pip_install(packages: list, callback=None) -> bool:
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + packages
    return _run_cmd(cmd, callback)


def _install_yara(callback=None) -> bool:
    """YARA needs special handling on Windows."""
    if OS_TYPE == "Windows":
        # Try pre-built wheel first
        r = _pip_install(["yara-python"], callback)
        if not r:
            if callback:
                callback("⚠ YARA: Try: pip install yara-python --no-binary yara-python\n")
        return r
    else:
        return _pip_install(["yara-python"], callback)


# ─────────────────────────────────────────────────────────────────────────────
#  EXTERNAL TOOL INSTALLER
# ─────────────────────────────────────────────────────────────────────────────
def _install_tool(tool_id: str, callback=None) -> bool:
    if OS_TYPE == "Windows":
        return _install_windows(tool_id, callback)
    elif OS_TYPE == "Darwin":
        return _install_macos(tool_id, callback)
    else:
        return _install_linux(tool_id, callback)


def _install_windows(tool_id: str, callback=None) -> bool:
    # Try winget first, then choco, then show download link
    winget_names = {
        "nmap":       "Insecure.Nmap",
        "git":        "Git.Git",
        "wireshark":  "WiresharkFoundation.Wireshark",
        "curl":       "cURL.cURL",
        "sqlmap":     None,   # Python-based, use pip/git
        "hydra":      None,   # Use choco or manual
        "metasploit": "Rapid7.Metasploit",
        "suricata":   None,
    }
    choco_names = {
        "nmap":       "nmap",
        "git":        "git",
        "wireshark":  "wireshark",
        "curl":       "curl",
        "sqlmap":     "sqlmap",
        "hydra":      "thc-hydra",
        "metasploit": "metasploit",
        "suricata":   "suricata",
    }
    manual_urls = {
        "nmap":       "https://nmap.org/download.html",
        "wireshark":  "https://www.wireshark.org/download.html",
        "sqlmap":     "https://sqlmap.org",
        "hydra":      "https://github.com/vanhauser-thc/thc-hydra/releases",
        "metasploit": "https://metasploit.com/download",
        "suricata":   "https://suricata.io/download/",
        "git":        "https://git-scm.com/download/win",
        "curl":       "https://curl.se/windows/",
    }

    # Special: sqlmap is Python-based
    if tool_id == "sqlmap":
        if callback: callback("[sqlmap] Installing via pip...\n")
        return _pip_install(["sqlmap"], callback)

    # Try winget
    winget_name = winget_names.get(tool_id)
    if winget_name and shutil.which("winget"):
        if callback: callback(f"[{tool_id}] Installing via winget: {winget_name}\n")
        ok = _run_cmd(["winget", "install", "-e", "--id", winget_name,
                       "--accept-source-agreements", "--accept-package-agreements"], callback)
        if ok: return True

    # Try chocolatey
    choco_name = choco_names.get(tool_id)
    if choco_name and shutil.which("choco"):
        if callback: callback(f"[{tool_id}] Installing via choco: {choco_name}\n")
        ok = _run_cmd(["choco", "install", choco_name, "-y"], callback)
        if ok: return True

    # Fallback: show download link
    url = manual_urls.get(tool_id, "")
    if callback:
        callback(f"\n⚠ Auto-install not available for {tool_id} on Windows.\n")
        callback(f"🔗 Download here: {url}\n")
        callback(f"   After install, restart this app.\n")
    return False


def _install_linux(tool_id: str, callback=None) -> bool:
    apt_names = {
        "nmap":      "nmap",
        "sqlmap":    "sqlmap",
        "hydra":     "hydra",
        "suricata":  "suricata",
        "wireshark": "tshark",
        "git":       "git",
        "curl":      "curl",
        "metasploit": None,
    }
    name = apt_names.get(tool_id)
    if not name:
        if tool_id == "metasploit":
            if callback:
                callback("[metasploit] Download: https://metasploit.com/download\n")
                callback("   Or run: curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall\n")
            return False
        return False
    # Detect package manager
    mgr = "apt"
    if shutil.which("dnf"): mgr = "dnf"
    elif shutil.which("yum"): mgr = "yum"
    elif shutil.which("pacman"): mgr = "pacman"
    cmds = {
        "apt":    ["sudo", "apt", "install", "-y", name],
        "dnf":    ["sudo", "dnf", "install", "-y", name],
        "yum":    ["sudo", "yum", "install", "-y", name],
        "pacman": ["sudo", "pacman", "-S", "--noconfirm", name],
    }
    return _run_cmd(cmds[mgr], callback)


def _install_macos(tool_id: str, callback=None) -> bool:
    brew_names = {
        "nmap":      "nmap",
        "sqlmap":    "sqlmap",
        "hydra":     "hydra",
        "suricata":  "suricata",
        "wireshark": "wireshark",
        "git":       "git",
        "curl":      "curl",
        "metasploit": "metasploit",
    }
    name = brew_names.get(tool_id)
    if not name:
        if callback: callback(f"No brew formula found for {tool_id}\n")
        return False
    if not shutil.which("brew"):
        if callback:
            callback("Homebrew not found. Install: https://brew.sh\n")
        return False
    return _run_cmd(["brew", "install", name], callback)


# ─────────────────────────────────────────────────────────────────────────────
#  SUBPROCESS RUNNER
# ─────────────────────────────────────────────────────────────────────────────
def _run_cmd(cmd: list, callback=None) -> bool:
    try:
        if callback: callback(f"$ {' '.join(cmd)}\n")
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        for line in proc.stdout:
            if callback: callback(line)
        proc.wait()
        ok = proc.returncode == 0
        if callback:
            callback(f"{'\u2714 Done' if ok else '\u2716 Failed (code ' + str(proc.returncode) + ')'}\n")
        return ok
    except FileNotFoundError as e:
        if callback: callback(f"\u2716 Command not found: {e}\n")
        return False
    except Exception as e:
        if callback: callback(f"\u2716 Error: {e}\n")
        return False


# ─────────────────────────────────────────────────────────────────────────────
#  INSTALL ALL
# ─────────────────────────────────────────────────────────────────────────────
def install_all(callback=None) -> dict:
    """Install all tools. Returns {tool_id: success}."""
    results = {}
    for tool in TOOLS:
        if callback: callback(f"\n{'='*50}\nInstalling: {tool['name']}\n{'='*50}\n")
        try:
            already = tool["check"]()
            if already:
                if callback: callback(f"\u2714 Already installed: {tool['name']}\n")
                results[tool["id"]] = True
                continue
            ok = tool["install"](callback)
            results[tool["id"]] = ok
        except Exception as e:
            if callback: callback(f"\u2716 Exception: {e}\n")
            results[tool["id"]] = False
    return results


if __name__ == "__main__":
    print(f"[Installer] OS: {OS_TYPE}")
    status = check_all()
    print("\nTool Status:")
    for tid, ok in status.items():
        icon = "\u2714" if ok else "\u2716"
        print(f"  {icon} {tid}")
