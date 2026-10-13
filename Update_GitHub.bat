@echo off
title Expedition - Update & Push to GitHub Pages
cd /d "%~dp0"

echo ======================================================================
echo    EXPEDITION: 1-CLICK GITHUB PAGES UPDATE
echo    Account: Rindelk  ^|  Repository: canadian-rockies-expedition
echo ======================================================================
echo.

:: 1. Sync index.html with latest itinerary
copy /y index.html index.html >nul

:: 2. Stage all modifications
echo [*] Staging updated route tracks, day cards, and navigation assets...
git add .

:: 3. Prompt for custom update note or use automatic timestamp
set msg=
set /p msg="Enter description of update (or press Enter for automatic timestamp): "
if "%msg%"=="" (
    for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set dt=%%a-%%b-%%c
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set tm=%%a:%%b
    set msg=Update: %dt% %tm%
)

:: 4. Commit and push
echo.
echo [*] Recording commit: "%msg%"...
git commit -m "%msg%"

echo.
echo [*] Pushing updates to https://github.com/Rindelk/canadian-rockies-expedition...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo  [SUCCESS] UPDATE PUSHED TO GITHUB!
    echo ======================================================================
    echo.
    echo  GitHub Pages is compiling your changes now (~30 to 45 seconds).
    echo  Live Global Website:
    echo  --^> https://rindelk.github.io/canadian-rockies-expedition/
    echo.
    echo  Tip: On mobile phones or tablets, pull down to refresh if needed.
    echo ======================================================================
) else (
    echo.
    echo [!] Push encountered an issue. Check your connection or run git status.
)

echo.
pause
