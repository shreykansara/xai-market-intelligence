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
echo Web Application will open at http://127.0.0.1:5000
echo Admin Console available at   http://127.0.0.1:5000/admin
echo.

:: Automatically launch browser once server is listening
start "" cmd /c "powershell -Command \"while (!(Test-NetConnection -ComputerName 127.0.0.1 -Port 5000 -InformationLevel Quiet)) { Start-Sleep -Milliseconds 400 }; Start-Process 'http://127.0.0.1:5000'\""

:: Launch the main Flask server
python server.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Server encountered an error and exited.
    pause
)
