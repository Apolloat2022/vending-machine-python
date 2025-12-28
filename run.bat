@echo off
echo ========================================
echo   Vendor Pro 2026 - Cinematic Edition
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Running setup first...
    call setup.bat
    exit /b
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
echo 🎬 Starting cinematic vending machine...
echo.
python main.py

echo.
echo ========================================
echo   Application closed
echo ========================================
pause
