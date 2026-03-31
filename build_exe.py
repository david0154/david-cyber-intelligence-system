#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM
Cross-Platform Build Script

Builds:
  Windows  → .exe (PyInstaller) + NSIS installer (.exe setup)
  macOS    → .app bundle + .dmg disk image
  Linux    → binary + .deb package + AppImage

Run: python build_exe.py
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import subprocess
import sys
import os
import platform
import shutil
from pathlib import Path

# ── Config
APP_NAME    = "DAVID-CIS"
APP_FULL    = "DAVID Cyber Intelligence System"
APP_VER     = "3.1.0"
APP_VENDOR  = "Devil Pvt Ltd & Nexuzy Tech Pvt Ltd"
APP_URL     = "https://hypechats.com"
ICON_WIN    = "assets/icon.ico"
ICON_MAC    = "assets/icon.icns"
ICON_LINUX  = "assets/icon.png"
ENTRY       = "launcher.py"      # splash → gui_app

OS = platform.system()   # Windows / Darwin / Linux

HIDDEN = [
    "core.task_router", "core.llm_brain",
    "engines.malware_engine", "engines.network_engine",
    "engines.osint_engine",   "engines.pentest_engine",
    "engines.defense_engine", "engines.bug_analyzer",
    "security.zap_engine",    "security.wazuh_client",
    "security.hydra_engine",  "security.deepexploit_engine",
    "tracking.flight_tracker","tracking.ship_tracker",
    "tracking.satellite_tracker", "tracking.geo_engine",
    "intelligence.misp_client",
    "tools_installer",
    "tkinter", "tkinter.ttk", "tkinter.scrolledtext",
    "PIL", "PIL.Image", "PIL.ImageTk",
    "requests", "loguru", "dotenv",
]

DATA_DIRS = [
    ("dashboard",   "dashboard"),
    ("data",         "data"),
    ("assets",       "assets"),
    ("config",       "config"),
    (".env.example", "."),
]


def run(cmd, **kw):
    print(f"\n\033[36m$ {' '.join(str(c) for c in cmd)}\033[0m")
    return subprocess.run(cmd, **kw)


def build_pyinstaller():
    """Build binary with PyInstaller (all platforms)."""
    icon = None
    if OS == "Windows" and os.path.exists(ICON_WIN):
        icon = ICON_WIN
    elif OS == "Darwin" and os.path.exists(ICON_MAC):
        icon = ICON_MAC
    elif OS == "Linux" and os.path.exists(ICON_LINUX):
        icon = ICON_LINUX

    sep = os.pathsep
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "--onedir",              # folder → faster startup than --onefile
        "--windowed",            # no console
        "--name", APP_NAME,
    ]

    for src, dst in DATA_DIRS:
        if os.path.exists(src):
            cmd += ["--add-data", f"{src}{sep}{dst}"]

    for h in HIDDEN:
        cmd += ["--hidden-import", h]

    if icon:
        cmd += ["--icon", icon]

    cmd.append(ENTRY)

    r = run(cmd)
    if r.returncode != 0:
        print("\n\033[31m[Build] PyInstaller FAILED\033[0m")
        sys.exit(1)
    print(f"\n\033[32m[Build] Binary ready: dist/{APP_NAME}/\033[0m")


def build_windows_installer():
    """Create Windows NSIS installer .exe"""
    nsis = shutil.which("makensis")
    if not nsis:
        print("[NSIS] makensis not found — skipping installer.")
        print("  Install: winget install NSIS.NSIS  or  choco install nsis")
        return

    nsi_script = f""";NSIS Installer Script for {APP_FULL}
!include MUI2.nsh

Name "{APP_FULL}"
OutFile "dist\\{APP_NAME}-{APP_VER}-Setup.exe"
InstallDir "$PROGRAMFILES64\\{APP_NAME}"
InstallDirRegKey HKLM "Software\\{APP_NAME}" ""
RequestExecutionLevel admin

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Section "Main" SEC01
  SetOutPath "$INSTDIR"
  File /r "dist\\{APP_NAME}\\*.*"
  WriteUninstaller "$INSTDIR\\Uninstall.exe"

  ; Start Menu
  CreateDirectory "$SMPROGRAMS\\{APP_NAME}"
  CreateShortCut  "$SMPROGRAMS\\{APP_NAME}\\{APP_FULL}.lnk" \
                  "$INSTDIR\\{APP_NAME}.exe" "" \
                  "$INSTDIR\\{APP_NAME}.exe" 0
  CreateShortCut  "$SMPROGRAMS\\{APP_NAME}\\Uninstall.lnk" \
                  "$INSTDIR\\Uninstall.exe"

  ; Desktop Shortcut
  CreateShortCut "$DESKTOP\\{APP_FULL}.lnk" \
                 "$INSTDIR\\{APP_NAME}.exe" "" \
                 "$INSTDIR\\{APP_NAME}.exe" 0

  ; Registry
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}" \
                   "DisplayName" "{APP_FULL}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}" \
                   "UninstallString" "$INSTDIR\\Uninstall.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}" \
                   "DisplayVersion" "{APP_VER}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}" \
                   "Publisher" "{APP_VENDOR}"
SectionEnd

Section "Uninstall"
  RMDir /r "$INSTDIR"
  Delete "$SMPROGRAMS\\{APP_NAME}\\*.*"
  RMDir  "$SMPROGRAMS\\{APP_NAME}"
  Delete "$DESKTOP\\{APP_FULL}.lnk"
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}"
SectionEnd
"""
    with open("installer.nsi", "w") as f:
        f.write(nsi_script)

    r = run([nsis, "installer.nsi"])
    if r.returncode == 0:
        print(f"\033[32m[NSIS] Installer: dist/{APP_NAME}-{APP_VER}-Setup.exe\033[0m")
    else:
        print("\033[31m[NSIS] Installer build failed.\033[0m")


def build_macos_dmg():
    """Create macOS .dmg using create-dmg or hdiutil."""
    app_path = f"dist/{APP_NAME}.app"
    dmg_path = f"dist/{APP_NAME}-{APP_VER}.dmg"

    if shutil.which("create-dmg"):
        r = run([
            "create-dmg",
            "--volname", APP_FULL,
            "--volicon", ICON_MAC,
            "--window-pos", "200", "120",
            "--window-size", "800", "400",
            "--icon-size", "100",
            "--icon", f"{APP_NAME}.app", "200", "190",
            "--hide-extension", f"{APP_NAME}.app",
            "--app-drop-link", "600", "185",
            dmg_path, app_path,
        ])
        if r.returncode == 0:
            print(f"\033[32m[DMG] Ready: {dmg_path}\033[0m")
    else:
        # Fallback: plain hdiutil
        run(["hdiutil", "create", "-volname", APP_NAME,
             "-srcfolder", app_path, "-ov",
             "-format", "UDZO", dmg_path])
        print(f"\033[32m[DMG] Ready: {dmg_path}\033[0m")
        print("  Tip: brew install create-dmg  for a prettier installer")


def build_linux_deb():
    """Create .deb package for Debian/Ubuntu."""
    pkg   = APP_NAME.lower()
    build = Path(f"dist/{pkg}_deb")
    bin_src = Path(f"dist/{APP_NAME}")
    if not bin_src.exists():
        print("[DEB] Binary not found. Run PyInstaller first.")
        return

    # Structure
    (build / "DEBIAN").mkdir(parents=True, exist_ok=True)
    (build / f"usr/local/bin/{pkg}").mkdir(parents=True, exist_ok=True)
    (build / f"usr/share/applications").mkdir(parents=True, exist_ok=True)
    (build / f"usr/share/pixmaps").mkdir(parents=True, exist_ok=True)

    # Copy binary
    shutil.copytree(bin_src, build / f"opt/{pkg}", dirs_exist_ok=True)

    # Symlink wrapper
    wrapper = build / f"usr/local/bin/{pkg}/{pkg}"
    wrapper.write_text(f"#!/bin/sh\nexec /opt/{pkg}/{APP_NAME} "$@"\n")
    wrapper.chmod(0o755)

    # Desktop entry
    desktop = build / f"usr/share/applications/{pkg}.desktop"
    desktop.write_text(
        f"[Desktop Entry]\n"
        f"Name={APP_FULL}\n"
        f"Comment=AI-Powered Cybersecurity Platform\n"
        f"Exec=/opt/{pkg}/{APP_NAME}\n"
        f"Icon=/opt/{pkg}/assets/icon.png\n"
        f"Terminal=false\n"
        f"Type=Application\n"
        f"Categories=Security;Network;\n"
    )

    # Copy icon
    if os.path.exists(ICON_LINUX):
        shutil.copy(ICON_LINUX, build / f"usr/share/pixmaps/{pkg}.png")

    # Control file
    (build / "DEBIAN/control").write_text(
        f"Package: {pkg}\n"
        f"Version: {APP_VER}\n"
        f"Section: net\n"
        f"Priority: optional\n"
        f"Architecture: amd64\n"
        f"Maintainer: David <david@nexuzytech.com>\n"
        f"Description: {APP_FULL}\n"
        f" AI-powered cybersecurity platform for security analysis,\n"
        f" defense, bug hunting, and tracking.\n"
    )

    r = run(["dpkg-deb", "--build", str(build),
             f"dist/{pkg}_{APP_VER}_amd64.deb"])
    if r.returncode == 0:
        print(f"\033[32m[DEB] Package: dist/{pkg}_{APP_VER}_amd64.deb\033[0m")
    else:
        print("\033[31m[DEB] dpkg-deb failed.\033[0m")


def build_appimage():
    """Create AppImage for universal Linux."""
    if not shutil.which("appimagetool"):
        print("[AppImage] appimagetool not found.")
        print("  Download: https://github.com/AppImage/AppImageKit/releases")
        return

    pkg = APP_NAME.lower()
    ai  = Path(f"dist/{APP_NAME}.AppDir")
    (ai / "usr/bin").mkdir(parents=True, exist_ok=True)
    shutil.copytree(f"dist/{APP_NAME}", ai / f"usr/bin/{APP_NAME}",
                    dirs_exist_ok=True)

    # AppRun
    apprun = ai / "AppRun"
    apprun.write_text(
        f"#!/bin/sh\n"
        f"SELF=$(readlink -f "$0")\n"
        f"HERE=$(dirname "$SELF")\n"
        f"exec "$HERE/usr/bin/{APP_NAME}/{APP_NAME}" "$@"\n"
    )
    apprun.chmod(0o755)

    # Desktop + icon
    (ai / f"{pkg}.desktop").write_text(
        f"[Desktop Entry]\nName={APP_FULL}\nExec={APP_NAME}\n"
        f"Icon={pkg}\nType=Application\nCategories=Security;\n"
    )
    if os.path.exists(ICON_LINUX):
        shutil.copy(ICON_LINUX, ai / f"{pkg}.png")

    run(["appimagetool", str(ai),
         f"dist/{APP_NAME}-{APP_VER}-x86_64.AppImage"])
    print(f"\033[32m[AppImage] Ready: dist/{APP_NAME}-{APP_VER}-x86_64.AppImage\033[0m")


# ── Main
if __name__ == "__main__":
    print(f"\n\033[32m{'='*60}")
    print(f"  {APP_FULL} v{APP_VER} — Build System")
    print(f"  Platform: {OS}")
    print(f"{'='*60}\033[0m\n")

    # 1. Ensure PyInstaller installed
    run([sys.executable, "-m", "pip", "install", "pyinstaller", "-q"])

    # 2. Build binary
    build_pyinstaller()

    # 3. Platform-specific packaging
    if OS == "Windows":
        build_windows_installer()
    elif OS == "Darwin":
        build_macos_dmg()
    elif OS == "Linux":
        build_linux_deb()
        build_appimage()

    print(f"\n\033[32m{'='*60}")
    print(f"  Build complete! Check dist/ folder.")
    print(f"{'='*60}\033[0m")
