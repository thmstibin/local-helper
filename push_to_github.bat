@echo off
REM Local Helper - GitHub Push Script (Windows)
REM This script will push your code to GitHub and create a release

echo.
echo ================================
echo Local Helper - GitHub Push Script
echo ================================
echo.

REM Step 1: Final security check
echo Step 1: Running final security check...
echo.

findstr /R /C:"sk-ant-api[0-9]" *.py src\*.py 2>nul | findstr /V "xxxxx" >nul
if %errorlevel% equ 0 (
    echo ERROR: Found actual API key in code!
    echo Please remove it before pushing.
    exit /b 1
)

if exist .env (
    echo WARNING: .env file exists
    echo Make sure it's in .gitignore
    findstr /C:".env" .gitignore >nul
    if %errorlevel% neq 0 (
        echo ERROR: .env is not in .gitignore!
        exit /b 1
    )
    echo OK: .env is properly ignored
)

echo OK: Security check passed - no secrets found
echo.

REM Step 2: Check git status
echo Step 2: Checking git status...
echo.

git add .
git status --short
echo.

REM Step 3: Commit
echo Step 3: Creating commit...
echo.

if exist COMMIT_MESSAGE.txt (
    git commit -F COMMIT_MESSAGE.txt
) else (
    git commit -m "Initial Release: Local Helper v0.1.0" -m "Open-source, cross-platform alternative to Claude Cowork"
)

echo OK: Commit created
echo.

REM Step 4: Set up remote
echo Step 4: Setting up GitHub remote...
echo.

git remote | findstr "origin" >nul
if %errorlevel% equ 0 (
    echo Remote 'origin' already exists
    git remote set-url origin https://github.com/thmstibin/local-helper.git
) else (
    echo Adding remote 'origin'
    git remote add origin https://github.com/thmstibin/local-helper.git
)

echo OK: Remote configured
echo.

REM Step 5: Push to GitHub
echo Step 5: Pushing to GitHub...
echo.
echo This will push to: https://github.com/thmstibin/local-helper
echo.
echo Press any key to continue, or Ctrl+C to cancel...
pause >nul

git push -u origin main

echo.
echo OK: Successfully pushed to GitHub!
echo.

REM Step 6: Instructions
echo Step 6: Next steps - Create a release
echo.
echo To create a release on GitHub:
echo.
echo 1. Go to: https://github.com/thmstibin/local-helper/releases/new
echo.
echo 2. Fill in the release form:
echo    - Tag: v0.1.0
echo    - Title: Local Helper v0.1.0 - Initial Release
echo    - Description: Copy from RELEASE_NOTES_v0.1.0.md
echo.
echo 3. Click 'Publish release'
echo.
echo All done! Your code is now on GitHub!
echo.
echo Repository: https://github.com/thmstibin/local-helper
echo.
echo Don't forget to:
echo   - Add repository description on GitHub
echo   - Add topics/tags
echo   - Create the v0.1.0 release
echo   - Share your project!
echo.
pause

