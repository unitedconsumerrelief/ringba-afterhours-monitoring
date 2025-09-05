@echo off
echo Installing Ringba Webhook Handler as Windows Service...
echo.

REM Check if NSSM is available
where nssm >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: NSSM not found. Please install NSSM first.
    echo Download from: https://nssm.cc/download
    echo.
    pause
    exit /b 1
)

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "PYTHON_PATH=python.exe"
set "SCRIPT_PATH=%CURRENT_DIR%main_port80.py"

REM Install the service
echo Installing service...
nssm install "RingbaWebhookHandler" "%PYTHON_PATH%" "%SCRIPT_PATH%"
nssm set "RingbaWebhookHandler" AppDirectory "%CURRENT_DIR%"
nssm set "RingbaWebhookHandler" Description "Ringba Webhook Handler - Processes call data and logs to Google Sheets"

echo.
echo Service installed successfully!
echo.
echo Starting the service...
net start RingbaWebhookHandler
if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCCESS: Ringba Webhook Handler service is now running!
    echo.
    echo Service will automatically start on system boot.
    echo.
    echo Management commands:
    echo To stop the service: net stop RingbaWebhookHandler
    echo To restart the service: net stop RingbaWebhookHandler && net start RingbaWebhookHandler
    echo To remove the service: nssm remove RingbaWebhookHandler confirm
    echo.
    echo Check service status: sc query RingbaWebhookHandler
    echo View logs in: ringba_webhook_port80.log
) else (
    echo.
    echo ❌ Failed to start the service. Please check the configuration.
    echo Try starting manually: net start RingbaWebhookHandler
)
echo.
pause


