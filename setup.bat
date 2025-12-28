@echo off
echo ========================================
echo   Vendor Pro 2026 - Setup & Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install PySide6

REM Create desktop shortcut (optional)
echo.
echo Do you want to create a desktop shortcut? (Y/N)
set /p shortcut=

if /i "%shortcut%"=="Y" (
    echo Creating desktop shortcut...
    
    REM Create a launcher script
    echo @echo off > "VendorPro2026.bat"
    echo echo Starting Vendor Pro 2026... >> "VendorPro2026.bat"
    echo cd /d "%~dp0" >> "VendorPro2026.bat"
    echo call venv\Scripts\activate.bat >> "VendorPro2026.bat"
    echo python main.py >> "VendorPro2026.bat"
    echo pause >> "VendorPro2026.bat"
    
    REM Copy to desktop
    copy "VendorPro2026.bat" "%USERPROFILE%\Desktop\VendorPro2026.bat" >nul
    echo ✅ Desktop shortcut created!
)

echo.
echo ========================================
echo   ✅ Setup Complete!
echo ========================================
echo.
echo To run Vendor Pro 2026:
echo 1. Double-click 'VendorPro2026.bat' on your desktop
echo    OR
echo 2. Run: .\run.bat
echo.
pause
