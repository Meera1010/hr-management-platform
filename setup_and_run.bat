@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ============================================================
echo   HireFlow / AI HR Platform - Backend Setup & Run (Windows)
echo ============================================================
echo.

cd /d "%~dp0backend"
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] No venv found. Creating one...
    python -m venv venv
    if errorlevel 1 ( echo [ERROR] Failed to create venv. Install Python first. & exit /b 1 )
)

echo [1/5] Activating virtual environment...
call "venv\Scripts\activate.bat"

echo [2/5] Installing dependencies (this may take a moment)...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install requirements. Check network access.
    exit /b 1
)

echo.
echo [3/5] Verifying PostgreSQL driver installed...
python -c "import psycopg2; print('   psycopg2 version:', psycopg2.__version__)"
if errorlevel 1 (
    echo [ERROR] psycopg2 not installed. Run:  pip install psycopg2-binary
    exit /b 1
)

echo.
echo [4/5] Testing connection to Neon PostgreSQL and seeding database...
echo   (This creates the tables and demo users. Please wait...)
python seed.py
if errorlevel 1 (
    echo.
    echo [WARNING] seed.py failed. Copy the error above and send it to the developer.
    echo   If it is a connection error, the Neon DB URL may be wrong or the DB unreachable.
    echo.
    echo   Proceeding to try starting the backend anyway...
)

echo.
echo [5/5] Starting backend server on port 5001...
echo   Press Ctrl+C to stop it.
echo.
python run.py

endlocal
