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

:: Check for unresolved conflict markers before doing anything
git grep -q "^<<<<<<< "
if %errorlevel% equ 0 (
    echo.
    echo =======================================================
    echo   ERROR: Unresolved git conflict markers detected!
    echo =======================================================
    git grep -n "^<<<<<<< "
    echo.
    echo   Please open these files and resolve the conflicts.
    echo   Search for "<<<<<<<", "=======", and ">>>>>>>"
    echo.
    pause
    exit /b 1
)

set /p msg="Commit message (what changed): "
if "%msg%"=="" (
    echo ERROR: Message cannot be empty.
    pause
    exit /b 1
)

echo.
echo Staging all changes...
git add .

echo Committing...
git commit -m "%msg%"
:: commit may return error if nothing new — that is fine, keep going

echo.
echo Syncing with GitHub...
git pull origin main --rebase
if errorlevel 1 (
    echo.
    echo Rebase conflict detected. Falling back to merge...
    git rebase --abort
    git pull origin main --no-rebase
    if errorlevel 1 (
        echo.
        echo MERGE CONFLICT — resolve manually before pushing.
        pause
        exit /b 1
    )
    git push origin main
    goto done
)

echo Pushing...
git push origin main
if errorlevel 1 (
    echo.
    echo ERROR: Push failed. Check your internet connection.
    pause
    exit /b 1
)

:done
echo.
echo =========================================
echo   LIVE — App updates in ~60 seconds
echo   https://ckndr.github.io/Aerosol/
echo =========================================
echo.
pause
