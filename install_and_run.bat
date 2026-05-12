@echo off
title SecureOps Lab - Installer
color 0B

echo.
echo  ==========================================
echo    SECUREOPS LAB - Automated Installer
echo  ==========================================
echo.

:: ── Step 1: Check Python ──────────────────────────────────────
echo [1/6] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  Python not found. Downloading Python 3.12...
    curl -L -o "%TEMP%\python_installer.exe" https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe
    echo  Installing Python silently...
    "%TEMP%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del "%TEMP%\python_installer.exe"
    echo  Python installed. Refreshing PATH...
    call refreshenv >nul 2>&1
) else (
    echo  Python found.
)

:: ── Step 2: Upgrade pip ───────────────────────────────────────
echo.
echo [2/6] Upgrading pip...
python -m pip install --upgrade pip --quiet

:: ── Step 3: Install Python packages ──────────────────────────
echo.
echo [3/6] Installing Python packages (streamlit, requests)...
python -m pip install streamlit requests --quiet
echo  Done.

:: ── Step 4: Check / install nmap ─────────────────────────────
echo.
echo [4/6] Checking for Nmap...
nmap --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  Nmap not found. Downloading Nmap 7.95...
    curl -L -o "%TEMP%\nmap_installer.exe" https://nmap.org/dist/nmap-7.95-setup.exe
    echo  Installing Nmap silently...
    "%TEMP%\nmap_installer.exe" /S
    del "%TEMP%\nmap_installer.exe"
    echo  Nmap installed.
) else (
    echo  Nmap already installed.
)

:: ── Step 5: Write app.py ─────────────────────────────────────
echo.
echo [5/6] Writing SecureOps Lab app to %USERPROFILE%\secureops\...
mkdir "%USERPROFILE%\secureops" >nul 2>&1

:: Write app.py using Python heredoc trick
python -c "
import urllib.request, os
url = 'https://raw.githubusercontent.com/YOUR_USERNAME/secureops/main/app.py'
dest = os.path.join(os.path.expanduser('~'), 'secureops', 'app.py')
print('  NOTE: Replace the GitHub URL above with your actual repo, or place app.py manually.')
"

:: ── Alternatively: embed app.py inline ───────────────────────
:: If you don't have a GitHub repo, paste the full app.py content below.
:: This creates the file locally without any download.

(
echo import streamlit as st
echo st.set_page_config^(page_title="SecureOps Lab", page_icon="shield", layout="wide"^)
echo st.write^("App loaded! Replace this file with the full app.py from SecureOps Lab."^)
) > "%USERPROFILE%\secureops\app_placeholder.py"

echo  Files written.

:: ── Step 6: Launch ───────────────────────────────────────────
echo.
echo [6/6] Launching SecureOps Lab...
echo.
echo  Dashboard will open at: http://localhost:8501
echo  Press Ctrl+C in this window to stop the server.
echo.
start "" "http://localhost:8501"
cd /d "%USERPROFILE%\secureops"
python -m streamlit run app.py

pause
