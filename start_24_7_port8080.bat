@echo off
echo ========================================
echo Starting Ringba Webhook Handler 24/7 (Port 8080)
echo ========================================
echo.
echo This will start the server and keep it running.
echo The window will stay open - DO NOT CLOSE IT.
echo.
echo To stop the server: Close this window or press Ctrl+C
echo.
echo Server starting in 3 seconds...
timeout /t 3 /nobreak >nul
echo.
cd /d "%~dp0"
:restart
echo [%DATE% %TIME%] Starting Ringba Webhook Handler on Port 8080...
python main_port8080.py
echo.
echo [%DATE% %TIME%] Server stopped. Restarting in 5 seconds...
echo Press Ctrl+C to stop completely.
timeout /t 5 /nobreak >nul
goto restart

