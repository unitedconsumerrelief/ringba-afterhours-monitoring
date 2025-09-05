@echo off
echo ========================================
echo Starting Ringba Webhook Handler (Port 80)
echo ========================================
echo.
echo Server will be available at:
echo http://localhost:80
echo http://192.168.254.100:80
echo.
echo Webhook endpoint:
echo http://192.168.254.100:80/ringba-webhook
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
python main_port80.py
pause

