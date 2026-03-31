#!/usr/bin/env bash
# DAVID CYBER INTELLIGENCE SYSTEM v3.1
# Universal Installer — Linux & macOS
# Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd

set -e
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OS="$(uname -s)"

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  DAVID CYBER INTELLIGENCE SYSTEM v3.1${NC}"
echo -e "${CYAN}  Installer for $OS${NC}"
echo -e "${GREEN}  Devil Pvt Ltd & Nexuzy Tech Pvt Ltd${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# ── Step 1: Python check
echo -e "${CYAN}[1/9] Checking Python 3.10+...${NC}"
if ! command -v python3 &>/dev/null; then
    echo -e "${YELLOW}Python3 not found. Installing...${NC}"
    if [ "$OS" = "Darwin" ]; then
        brew install python3
    elif command -v apt &>/dev/null; then
        sudo apt update -qq && sudo apt install -y python3 python3-pip python3-venv
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &>/dev/null; then
        sudo pacman -Sy python python-pip --noconfirm
    fi
fi
PYVER=$(python3 --version)
echo -e "${GREEN}[+] Found: $PYVER${NC}"

# ── Step 2: pip upgrade
echo -e "${CYAN}[2/9] Upgrading pip...${NC}"
python3 -m pip install --upgrade pip -q

# ── Step 3: Virtual environment
echo -e "${CYAN}[3/9] Creating virtual environment...${NC}"
cd "$SCRIPT_DIR"
python3 -m venv .venv
source .venv/bin/activate
echo -e "${GREEN}[+] venv active: $VIRTUAL_ENV${NC}"

# ── Step 4: Python packages
echo -e "${CYAN}[4/9] Installing Python packages...${NC}"
pip install -r requirements.txt -q
echo -e "${GREEN}[+] Python packages installed.${NC}"

# ── Step 5: System packages
echo -e "${CYAN}[5/9] Installing system security tools...${NC}"
if [ "$OS" = "Darwin" ]; then
    # macOS — Homebrew
    if ! command -v brew &>/dev/null; then
        echo -e "${YELLOW}Installing Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install nmap wireshark python3 git curl wget 2>/dev/null || true
    brew install sqlmap hydra 2>/dev/null || true
elif command -v apt &>/dev/null; then
    # Debian / Ubuntu
    sudo apt update -qq
    sudo apt install -y nmap wireshark tshark git curl wget python3-tk \
        libpq-dev build-essential 2>/dev/null || true
    # SQLMap via pip (works everywhere)
    pip install sqlmap -q 2>/dev/null || true
elif command -v dnf &>/dev/null; then
    # Fedora / RHEL
    sudo dnf install -y nmap wireshark git curl wget python3-tkinter \
        postgresql-devel gcc 2>/dev/null || true
elif command -v pacman &>/dev/null; then
    # Arch Linux
    sudo pacman -Sy nmap wireshark-qt git curl wget python-tkinter \
        --noconfirm 2>/dev/null || true
fi
echo -e "${GREEN}[+] System tools installed.${NC}"

# ── Step 6: .env setup
echo -e "${CYAN}[6/9] Setting up configuration...${NC}"
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
    echo -e "${GREEN}[+] Created .env file. Edit it to add your API keys.${NC}"
else
    echo -e "${GREEN}[+] .env already exists.${NC}"
fi

# ── Step 7: Launcher script
echo -e "${CYAN}[7/9] Creating launcher...${NC}"
LAUNCHER="$SCRIPT_DIR/david-cis"
cat > "$LAUNCHER" << EOF
#!/usr/bin/env bash
cd "$SCRIPT_DIR"
source "$SCRIPT_DIR/.venv/bin/activate"
exec python3 "$SCRIPT_DIR/launcher.py" "\$@"
EOF
chmod +x "$LAUNCHER"
echo -e "${GREEN}[+] Launcher: $LAUNCHER${NC}"

# ── Step 8: Desktop shortcut
echo -e "${CYAN}[8/9] Creating desktop shortcut...${NC}"
if [ "$OS" = "Linux" ]; then
    DESKTOP_FILE="$HOME/.local/share/applications/david-cis.desktop"
    mkdir -p "$(dirname $DESKTOP_FILE)"
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=DAVID Cyber Intelligence System
Comment=AI-Powered Cybersecurity Platform
Exec=$LAUNCHER
Icon=$SCRIPT_DIR/assets/icon.png
Terminal=false
Type=Application
Categories=Security;Network;
StartupWMClass=DAVID-CIS
EOF
    chmod +x "$DESKTOP_FILE"
    # Also put on desktop if it exists
    if [ -d "$HOME/Desktop" ]; then
        cp "$DESKTOP_FILE" "$HOME/Desktop/david-cis.desktop"
        chmod +x "$HOME/Desktop/david-cis.desktop"
    fi
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
    echo -e "${GREEN}[+] Desktop shortcut created.${NC}"
elif [ "$OS" = "Darwin" ]; then
    # macOS: create .command file on Desktop
    CMD="$HOME/Desktop/DAVID CIS.command"
    cat > "$CMD" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
source "$SCRIPT_DIR/.venv/bin/activate"
exec python3 "$SCRIPT_DIR/launcher.py"
EOF
    chmod +x "$CMD"
    echo -e "${GREEN}[+] Desktop launcher: $CMD${NC}"
fi

# ── Step 9: Verify
echo -e "${CYAN}[9/9] Verifying installation...${NC}"
python3 -c "import tkinter, requests, loguru; print('[+] Core modules OK')"

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  Installation Complete!${NC}"
echo ""
echo -e "  Launch options:"
echo -e "  ${CYAN}$LAUNCHER${NC}              (command line)"
if [ "$OS" = "Linux" ]; then
echo -e "  ${CYAN}Desktop → DAVID CIS icon${NC}   (GUI shortcut)"
elif [ "$OS" = "Darwin" ]; then
echo -e "  ${CYAN}Desktop → DAVID CIS.command${NC} (double-click)"
fi
echo ""
echo -e "  First run: Open '${YELLOW}Tool Installer${NC}' tab to install"
echo -e "             all security tools automatically."
echo -e "${GREEN}================================================${NC}"
echo ""
