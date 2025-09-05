@echo off
echo Starting Ringba Webhook Handler...
echo.
echo Server will be available at: http://localhost:5000
echo Webhook endpoint: http://localhost:5000/ringba-webhook
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
python main.py

pause



