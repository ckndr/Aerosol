@echo off
title Pull from GitHub
color 0E

echo =========================================
echo   Pulling Latest from GitHub
echo =========================================
echo.

:: If there are uncommitted local changes, stash them first
:: so the pull never gets blocked
git stash

git pull origin main
if errorlevel 1 (
    echo.
    echo ERROR: Pull failed. Check internet or repo access.
    :: Restore stashed changes if pull failed
    git stash pop
    pause
    exit /b 1
)

:: Restore any stashed local changes on top of the pull
git stash pop
if errorlevel 1 (
    echo.
    echo =======================================================
    echo   CONFLICTS DETECTED when restoring local changes!
    echo =======================================================
    git grep -n "^<<<<<<< "
    echo.
    echo   Please resolve these conflicts before committing or pushing.
    echo.
    pause
    exit /b 1
)

echo.
echo =========================================
echo   Done — you have the latest version.
echo =========================================
echo.
pause
