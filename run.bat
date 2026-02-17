@echo off
title ZeroClaw AI Research Hub
echo ==========================================
echo   ZeroClaw AI Research Hub Engine 🧸
echo ==========================================
echo.
echo [*] Checking Environment...
pip install flask flask-cors requests > nul
echo [*] Launching Knowledge Engine...
echo.
echo [!] SERVER IS STARTING...
echo [!] AUTO-OPENING: http://localhost:5000
echo.
:: 브라우저 자동 실행
start http://localhost:5000
:: 서버 실행
python app.py
pause
