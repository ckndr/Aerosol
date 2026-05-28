@echo off
title Local Checkpoint
color 0B

echo =========================================
echo   Local Checkpoint — No Push to GitHub
echo =========================================
echo.
echo Use this BEFORE and AFTER every AI session.
echo Nothing goes live — local save only.
echo.
set /p msg="Checkpoint message: "
if "%msg%"=="" set msg=Local checkpoint - Aerosol Tracker

git add .
git commit -m "%msg%"
if errorlevel 1 (
    echo.
    echo Nothing new to commit — no changes detected.
    pause
    exit /b 0
)

echo.
echo =========================================
echo   Checkpoint saved locally.
echo   Run push.bat when ready to go live.
echo =========================================
echo.
pause
