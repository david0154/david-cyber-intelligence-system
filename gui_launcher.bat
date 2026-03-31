@echo off
chcp 65001 >nul
title DAVID CIS
cd /d "%~dp0"
pythonw launcher.py
if %errorlevel% neq 0 (
    echo [!] pythonw failed, trying python...
    python launcher.py
    pause
)
