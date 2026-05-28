@echo off
title Push to GitHub — Go Live
color 0A

echo =========================================
echo   Push to GitHub — This Goes LIVE
echo   https://ckndr.github.io/Aerosol/
echo =========================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found in PATH.
    pause
    exit /b 1
)

echo Pulling latest from GitHub first...
git pull origin main
if errorlevel 1 (
    echo.
    echo WARNING: Pull had issues. Check above for merge conflicts.
    pause
    exit /b 1
)

echo.
set /p msg="Commit message (what changed): "
if "%msg%"=="" (
    echo ERROR: Message cannot be empty.
    pause
    exit /b 1
)

git add .
git commit -m "%msg%"
if errorlevel 1 (
    echo.
    echo Nothing new to push — no changes since last commit.
    pause
    exit /b 0
)

git push origin main
if errorlevel 1 (
    echo.
    echo ERROR: Push failed. Check internet or GitHub access.
    pause
    exit /b 1
)

echo.
echo =========================================
echo   LIVE — App updates in ~30 seconds
echo   https://ckndr.github.io/Aerosol/
echo =========================================
echo.
pause
