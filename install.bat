@echo off
chcp 65001 >nul
SETLOCAL EnableDelayedExpansion

title DAVID CIS — Windows Installer
color 0A

echo.
echo  ================================================
echo   DAVID CYBER INTELLIGENCE SYSTEM v3.1
echo   Windows Installer
echo   Devil Pvt Ltd and Nexuzy Tech Pvt Ltd
echo  ================================================
echo.

:: ── Check Admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] Please run this script as Administrator.
    echo      Right-click install.bat and select "Run as administrator"
    pause
    exit /b 1
)

:: ── Check Python
echo  [1/8] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] Python not found. Installing via winget...
    winget install Python.Python.3.11 --silent --accept-package-agreements
    if %errorlevel% neq 0 (
        echo  [!] winget failed. Download Python from https://python.org
        pause
        exit /b 1
    )
    echo  [+] Python installed. Please restart this installer.
    pause
    exit /b 0
)
for /f "tokens=*" %%i in ('python --version') do echo  [+] Found: %%i

:: ── Upgrade pip
echo.
echo  [2/8] Upgrading pip...
python -m pip install --upgrade pip -q

:: ── Install Python packages
echo.
echo  [3/8] Installing Python dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo  [!] Some packages failed. Trying individually...
    for /f %%p in (requirements.txt) do (
        python -m pip install %%p -q 2>nul
    )
)
echo  [+] Python packages installed.

:: ── Install winget packages
echo.
echo  [4/8] Installing security tools (winget)...
winget install Insecure.Nmap          --silent --accept-package-agreements 2>nul
winget install WiresharkFoundation.Wireshark --silent --accept-package-agreements 2>nul
winget install Git.Git                --silent --accept-package-agreements 2>nul
echo  [+] Core tools installed.

:: ── Install Chocolatey (for extra tools)
echo.
echo  [5/8] Checking Chocolatey...
choco --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [*] Installing Chocolatey...
    powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command ^(Set-ExecutionPolicy Bypass -Scope Process -Force;[System.Net.ServicePointManager]::SecurityProtocol=[System.Net.SecurityProtocolType]'Tls12';iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')))
    set "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
)
choco install python-pip nmap sqlmap thc-hydra wget curl -y --no-progress 2>nul
echo  [+] Extra tools installed.

:: ── Copy .env
echo.
echo  [6/8] Setting up configuration...
if not exist .env (
    copy .env.example .env
    echo  [+] Created .env file. Edit it to add your API keys.
) else (
    echo  [+] .env already exists.
)

:: ── Create Desktop Shortcut
echo.
echo  [7/8] Creating shortcuts...
set SCRIPT_DIR=%~dp0
set SHORTCUT=%USERPROFILE%\Desktop\DAVID CIS.lnk
powershell -Command ^$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%SHORTCUT%');^$s.TargetPath='pythonw';^$s.Arguments='"%SCRIPT_DIR%launcher.py"';^$s.WorkingDirectory='%SCRIPT_DIR%';^$s.IconLocation='%SCRIPT_DIR%assets\icon.ico';^$s.Description='DAVID Cyber Intelligence System';^$s.Save()
echo  [+] Desktop shortcut created.

:: ── Create Start Menu shortcut
set STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\DAVID CIS
mkdir "%STARTMENU%" 2>nul
set SHORTCUT2=%STARTMENU%\DAVID CIS.lnk
powershell -Command ^$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%SHORTCUT2%');^$s.TargetPath='pythonw';^$s.Arguments='"%SCRIPT_DIR%launcher.py"';^$s.WorkingDirectory='%SCRIPT_DIR%';^$s.IconLocation='%SCRIPT_DIR%assets\icon.ico';^$s.Description='DAVID Cyber Intelligence System';^$s.Save()
echo  [+] Start Menu shortcut created.

echo.
echo  [8/8] Verifying installation...
python -c "import tkinter, requests, loguru; print('[+] Core modules OK')"

echo.
echo  ================================================
echo   Installation Complete!
echo.
echo   To launch: Double-click 'DAVID CIS' on Desktop
echo          or: python launcher.py
echo.
echo   First run: Open 'Tool Installer' tab to install
echo             all security tools automatically.
echo  ================================================
echo.
pause
