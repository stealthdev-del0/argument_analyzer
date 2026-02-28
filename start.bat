@echo off
REM 🧠 Argument Structure Analyzer - Quick Start Windows

cd /D %~dp0

echo.
echo =========================================================
echo  Argument Structure Analyzer - Lokaler Start
echo =========================================================
echo.

REM Check if venv exists
if not exist ".venv" (
    echo [1/3] Creating virtual environment...
    python -m venv .venv
    echo [OK] Virtual environment created
)

REM Activate venv
echo [2/3] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo [3/3] Installing dependencies...
pip install -q -r requirements.txt

echo.
echo =========================================================
echo  Setup complete! Starting app...
echo =========================================================
echo.
echo   Local URL: http://localhost:8501
echo.
echo   Tip: Press Ctrl+C to stop the app
echo.
echo =========================================================
echo.

REM Start Streamlit
streamlit run app.py --server.port=8501 --server.address=localhost

pause
