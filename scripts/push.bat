@echo off
REM Git Push Script (Windows)
REM Usage: scripts\push.bat "Your commit message"

if "%~1"=="" (
    echo Please provide a commit message
    echo Usage: scripts\push.bat "Your commit message"
    exit /b 1
)

set COMMIT_MSG=%~1

echo Adding all changes...
git add .

echo Committing changes...
git commit -m "%COMMIT_MSG%"

echo Pushing to remote repository...
git push

echo Done!

