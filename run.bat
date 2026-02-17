@echo off
echo ==========================================
echo   ZeroClaw Research Hub Starter 🧸
echo ==========================================
echo.
echo [1/3] Checking dependencies...
pip install flask flask-cors requests
echo.
echo [2/3] Cleaning up old data for fresh start...
if exist data\knowledge.db del /q data\knowledge.db
echo.
echo [3/3] Starting the Knowledge Engine...
echo.
echo >>> Open your browser at: http://localhost:5000
echo.
python app.py
pause
