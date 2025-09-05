@echo off
echo ========================================
echo Downloading NSSM for Windows Service
echo ========================================
echo.

echo Checking if NSSM already exists...
if exist "nssm.exe" (
    echo NSSM already found in current directory.
    echo.
    goto :end
)

echo Downloading NSSM...
echo.
echo Please download NSSM manually from: https://nssm.cc/download
echo.
echo Instructions:
echo 1. Go to https://nssm.cc/download
echo 2. Download the latest version
echo 3. Extract the zip file
echo 4. Copy nssm.exe from win64 folder (or win32 for 32-bit)
echo 5. Paste nssm.exe into this project folder
echo 6. Run install_service.bat again
echo.

:end
pause

