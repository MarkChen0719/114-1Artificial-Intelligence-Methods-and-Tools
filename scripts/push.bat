@echo off
REM Git Push 腳本 (Windows)
REM 使用方法: scripts\push.bat "您的提交訊息"

if "%~1"=="" (
    echo 請提供提交訊息
    echo 使用方法: scripts\push.bat "您的提交訊息"
    exit /b 1
)

set COMMIT_MSG=%~1

echo 正在添加所有更改...
git add .

echo 正在提交更改...
git commit -m "%COMMIT_MSG%"

echo 正在推送到遠程倉庫...
git push

echo 完成！

