@echo off
setlocal
chcp 65001 >nul
echo ============================================================
echo   HireFlow / AI HR Platform - Frontend (React + Vite)
echo ============================================================
echo.
cd /d "%~dp0frontend"

echo [1/2] Installing frontend dependencies...
if not exist "node_modules" (
    npm install
    if errorlevel 1 ( echo [ERROR] npm install failed. & exit /b 1 )
) else (
    echo   node_modules already present, skipping install.
)

echo.
echo [2/2] Starting frontend dev server on http://localhost:5173 ...
echo   Press Ctrl+C to stop it.
echo.
npm run dev

endlocal
