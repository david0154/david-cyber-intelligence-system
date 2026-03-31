@echo off
title DAVID CYBER INTELLIGENCE SYSTEM
echo.
echo  ============================================
echo   DAVID CYBER INTELLIGENCE SYSTEM v2.0
echo   Devil Pvt Ltd ^& Nexuzy Tech Pvt Ltd
echo  ============================================
echo.
echo  Starting Tkinter GUI...
echo.
python gui_app.py
if errorlevel 1 (
    echo.
    echo  ERROR: Failed to start. Make sure Python is installed.
    echo  Run: pip install -r requirements.txt
    pause
)
