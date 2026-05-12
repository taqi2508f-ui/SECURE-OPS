@echo off
title SecureOps Lab
color 0B
echo.
echo  ==========================================
echo    SECUREOPS LAB - Starting...
echo  ==========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERROR: Python not found.
    echo  Download from: https://www.python.org/downloads/
    pause & exit
)

python -m streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  Installing Streamlit...
    python -m pip install streamlit requests --quiet
)

echo  Opening dashboard at http://localhost:8501
echo  Press Ctrl+C to stop.
echo.
start "" "http://localhost:8501"
python -m streamlit run "%~dp0app.py"
pause
