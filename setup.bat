@echo off
REM Setup script for The Griddler (Windows)

echo =========================================
echo    The Griddler - COBOL SCR100 Parser
echo =========================================
echo.

REM Check Python
echo Checking Python installations...

REM Try py launcher first (Windows Python Launcher)
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    echo [OK] Python 3.12 found via py launcher
    set PYTHON_CMD=py -3.12
    goto :check_node
)

py -3.11 --version >nul 2>&1
if not errorlevel 1 (
    echo [OK] Python 3.11 found via py launcher
    set PYTHON_CMD=py -3.11
    goto :check_node
)

REM Fall back to python command
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.11 or 3.12
    echo Download from: https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2>&1') do set PYTHON_VERSION=%%i
echo [INFO] Python %PYTHON_VERSION% found in PATH

REM Check if default Python version is 3.11 or 3.12
python -c "import sys; exit(0 if sys.version_info[:2] in [(3, 11), (3, 12)] else 1)" 2>nul
if errorlevel 1 (
    echo.
    echo [WARNING] Default Python is %PYTHON_VERSION%
    echo This project requires Python 3.11 or 3.12.
    echo.
    echo You have multiple Python versions installed.
    echo Please install Python 3.12 from: https://www.python.org/downloads/
    echo During install, make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
set PYTHON_CMD=python
echo [OK] Python version is compatible

:check_node
echo.

REM Check Node
echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18+
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('node --version') do set NODE_VERSION=%%i
echo [OK] Node %NODE_VERSION% found
echo.

REM Setup Backend
echo =========================================
echo Setting up Backend...
echo =========================================
cd backend

REM Check if venv exists and is valid
if exist "venv" (
    echo Checking existing virtual environment...
    venv\Scripts\python.exe --version >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Existing venv is broken or incompatible. Recreating...
        rmdir /s /q venv
        echo Creating virtual environment with %PYTHON_CMD%...
        %PYTHON_CMD% -m venv venv
    ) else (
        echo [OK] Using existing virtual environment
    )
) else (
    echo Creating virtual environment with %PYTHON_CMD%...
    %PYTHON_CMD% -m venv venv
)

echo Installing Python dependencies...
venv\Scripts\pip.exe install --quiet --upgrade pip
venv\Scripts\pip.exe install --quiet -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install Python dependencies!
    echo.
    echo This usually means:
    echo 1. You're using an incompatible Python version (need 3.11 or 3.12)
    echo 2. Some packages require compilation and build tools are missing
    echo.
    echo Please:
    echo 1. Uninstall Python 3.13 if you have it
    echo 2. Install Python 3.11 or 3.12 from https://www.python.org/downloads/
    echo 3. Run this setup script again
    echo.
    pause
    exit /b 1
)

if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo [WARNING] Please edit backend\.env and add your API keys
)

echo [OK] Backend setup complete
echo.
cd ..

REM Setup Frontend
echo =========================================
echo Setting up Frontend...
echo =========================================
cd frontend

if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
)

echo Installing Node dependencies (this may take a minute)...
call npm install

echo [OK] Frontend setup complete
echo.
cd ..

REM Done
echo.
echo =========================================
echo    Setup Complete!
echo =========================================
echo.
echo To start the application:
echo.
echo 1. Start the backend (in Command Prompt 1):
echo    cd backend
echo    run.bat
echo.
echo 2. Start the frontend (in Command Prompt 2):
echo    cd frontend
echo    npm run dev
echo.
echo 3. Open browser to: http://localhost:5173
echo.
echo [NOTE] For AI-based analysis, configure API keys in backend\.env
echo.
pause
