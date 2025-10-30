@echo off
REM Run script for The Griddler Backend (Windows)

cd /d "%~dp0"

echo Starting The Griddler Backend...
echo API will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.

REM Check if venv exists
if not exist "venv\Scripts\uvicorn.exe" (
    echo [ERROR] Virtual environment not found.
    echo.
    echo Please run setup.bat first:
    echo   1. Navigate to the project root directory
    echo   2. Run: setup.bat
    echo.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo No .env file found. Creating from template...
    copy .env.example .env
    echo Created .env file. Edit it to add API keys for AI features.
    echo.
)

REM Run uvicorn directly from venv
venv\Scripts\uvicorn.exe app.main:app --reload --port 8000 --host 0.0.0.0
