@echo off
title Expedition - Initial Deploy to GitHub Pages
cd /d "%~dp0"

echo ======================================================================
echo    EXPEDITION: INITIAL DEPLOY TO GITHUB PAGES
echo    Account: Rindelk  ^|  Repository: canadian-rockies-expedition
echo ======================================================================
echo.

:: 1. Sync index.html
copy /y index.html index.html >nul

:: 2. Check if git is initialized
if not exist ".git" (
    echo [*] Initializing local Git repository (main branch)...
    git init -b main
    echo [*] Adding remote origin: https://github.com/Rindelk/canadian-rockies-expedition.git...
    git remote add origin https://github.com/Rindelk/canadian-rockies-expedition.git
) else (
    echo [OK] Git repository already initialized.
    git remote remove origin >nul 2>&1
    git remote add origin https://github.com/Rindelk/canadian-rockies-expedition.git
)

:: 3. Stage all assets
echo [*] Staging all project files and navigation assets...
git add .

:: 4. Commit
echo [*] Creating initial release commit...
git commit -m "Initial Release: Expedition Master Package"

:: 5. Push to GitHub
echo.
echo ======================================================================
echo [*] Pushing files to https://github.com/Rindelk/canadian-rockies-expedition...
echo     (If prompted, sign in via the GitHub Credential Manager popup)
echo ======================================================================
echo.
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo  [SUCCESS] INITIAL PUSH COMPLETE!
    echo ======================================================================
    echo.
    echo  Final Step: Enable GitHub Pages in your repository settings:
    echo  1. Open: https://github.com/Rindelk/canadian-rockies-expedition/settings/pages
    echo  2. Under 'Build and deployment' -^> 'Source', select: 'Deploy from a branch'
    echo  3. Under 'Branch', select 'main' and '/(root)'
    echo  4. Click 'Save'
    echo.
    echo  Within ~45 seconds, your live interactive tour will be online at:
    echo  --^> https://rindelk.github.io/canadian-rockies-expedition/
    echo ======================================================================
) else (
    echo.
    echo [!] Push failed or was cancelled. Check your network or GitHub login.
)

echo.
pause
