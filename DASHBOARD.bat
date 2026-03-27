@echo off
REM ============================================================
REM TY AUTOMATION - MO DASHBOARD
REM Double-click file nay de mo giao dien web
REM ============================================================
title TY AUTOMATION - Dashboard
color 0B
cls

echo ============================================================
echo   TY AUTOMATION - DASHBOARD
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if setup was done
if not exist "data\profiles" (
    echo [!] Chua setup. Dang chay SETUP.bat truoc...
    echo.
    call SETUP.bat
)

echo [*] Dang khoi dong Dashboard...
echo [*] Trinh duyet se tu dong mo tai: http://127.0.0.1:5000
echo [!] KHONG DONG CUA SO NAY khi dang su dung
echo.

REM Open browser after 2 seconds
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:5000"

REM Start dashboard
python app\dashboard.py
