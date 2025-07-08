@echo off
echo Real-Time Network Connection Monitor for Windows 10
echo ===================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

:: Check if we're running as administrator
net session >nul 2>&1
if errorlevel 1 (
    echo WARNING: Not running as administrator.
    echo For full functionality, right-click this file and select "Run as administrator"
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "!continue!"=="y" exit /b 0
)

:: Check if dependencies are installed
echo Checking dependencies...
python -c "import psutil, matplotlib, numpy, pandas" >nul 2>&1
if errorlevel 1 (
    echo Some dependencies are missing. Installing them now...
    python install_dependencies.py
    echo.
    echo Please run this script again after installation.
    pause
    exit /b 1
)

:: Run the network monitor
echo Starting Network Monitor...
echo.
python network_monitor.py

if errorlevel 1 (
    echo.
    echo An error occurred while running the network monitor.
    echo Check the error messages above for details.
    pause
)