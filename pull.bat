@echo off
title Pull from GitHub
color 0E

echo =========================================
echo   Pulling Latest from GitHub
echo =========================================
echo.

git pull origin main
if errorlevel 1 (
    echo.
    echo ERROR: Pull failed. Check internet or repo access.
    pause
    exit /b 1
)

echo.
echo =========================================
echo   Done — you have the latest version.
echo =========================================
echo.
pause
