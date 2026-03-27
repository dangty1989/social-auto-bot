@echo off
REM ============================================================
REM TY AUTOMATION - SETUP (Chay 1 lan dau tien)
REM ============================================================
setlocal enabledelayedexpansion
title TY AUTOMATION - SETUP
color 0A
cls

echo ============================================================
echo   TY AUTOMATION - CAI DAT HE THONG
echo ============================================================
echo.

REM 1. Check Python
echo [1/5] Kiem tra Python...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo.
    echo [LOI] Python chua cai dat!
    echo Tai Python tai: https://www.python.org/downloads
    echo Nho chon "Add Python to PATH" khi cai dat
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo   [OK] %%i

REM 2. Create directories
echo.
echo [2/5] Tao thu muc...
set ROOT=%~dp0
if not exist "%ROOT%data\profiles" mkdir "%ROOT%data\profiles"
if not exist "%ROOT%data\logs" mkdir "%ROOT%data\logs"
if not exist "%ROOT%data\reports" mkdir "%ROOT%data\reports"
if not exist "%ROOT%data\schedules" mkdir "%ROOT%data\schedules"
if not exist "%ROOT%data\temp" mkdir "%ROOT%data\temp"
echo   [OK] data\profiles, logs, reports, schedules

REM 3. Install packages
echo.
echo [3/5] Cai dat thu vien Python...
echo   (Cho khoang 2-5 phut)
cd /d "%ROOT%"
pip install -q -r requirements.txt >nul 2>&1
if !errorlevel! equ 0 (
    echo   [OK] Tat ca thu vien da cai
) else (
    echo   [WARN] Co loi, dang thu lai...
    pip install -r requirements.txt
)

REM 4. Install Chromium
echo.
echo [4/5] Tai trinh duyet Chromium...
echo   (Cho khoang 3-10 phut lan dau)
playwright install chromium >nul 2>&1
if !errorlevel! equ 0 (
    echo   [OK] Chromium installed
) else (
    echo   [LOI] Khong tai duoc. Kiem tra Internet.
    pause
    exit /b 1
)

REM 5. Create .env
echo.
echo [5/5] Tao file cau hinh...
if not exist "%ROOT%.env" (
    copy "%ROOT%.env.example" "%ROOT%.env" >nul 2>&1
    echo   [OK] .env da tao tu .env.example
) else (
    echo   [OK] .env da ton tai
)

echo.
echo ============================================================
echo   HOAN THANH! He thong da san sang.
echo.
echo   Buoc tiep theo:
echo     1. Double-click DASHBOARD.bat de mo giao dien
echo     2. Dang nhap Facebook lan dau
echo     3. Bat dau dang bai!
echo ============================================================
echo.
pause
