@echo off
title Omniscope AI - Explainable Market Intelligence System
echo ======================================================================
echo           Omniscope AI - Explainable Market Intelligence System
echo ======================================================================
echo.

:: Check for python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in PATH!
    echo Please ensure Python is installed and added to PATH.
    pause
    exit /b 1
)

echo [1/2] Starting Omniscope AI Backend and Web Server...
echo Server running at http://localhost:5000
echo Admin Console available at http://localhost:5000/admin
echo.

:: Open default browser after 2 seconds in background
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:5000"

:: Launch the main Flask server
python server.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Server encountered an error and exited.
    pause
)
