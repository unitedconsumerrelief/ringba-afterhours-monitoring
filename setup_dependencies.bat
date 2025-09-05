@echo off
echo ========================================
echo Ringba Webhook Handler - Setup Script
echo ========================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt
echo.

echo Getting IP address for Ringba webhook...
for /f "tokens=2 delims=:" %%a in ("ipconfig | findstr IPv4") do (
    set "IP=%%a"
    goto :found_ip
)
:found_ip
set "IP=%IP: =%"
echo.
echo ========================================
echo RINGBA WEBHOOK CONFIGURATION
echo ========================================
echo.
echo IMPORTANT: Configure Ringba with this webhook URL:
echo.
echo http://%IP%:80/ringba-webhook
echo.
echo Steps to configure Ringba:
echo 1. Log into your Ringba dashboard
echo 2. Go to Campaign Settings
echo 3. Find Webhook Configuration
echo 4. Add the URL above
echo 5. Set Method: POST
echo 6. Set Content Type: application/json
echo.
pause
