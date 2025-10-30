@echo off
REM Start script for The Griddler (Windows)

echo =========================================
echo    The Griddler - COBOL SCR100 Parser
echo =========================================
echo.

REM Check if backend venv exists
if not exist "backend\venv" (
    echo [ERROR] Backend not set up. Please run setup.bat first.
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo [ERROR] Frontend not set up. Please run setup.bat first.
    pause
    exit /b 1
)

echo Starting backend on port 8000...
cd backend
start "Griddler Backend" cmd /k "run.bat"
cd ..

timeout /t 3 /nobreak >nul

echo Starting frontend on port 5173...
cd frontend
start "Griddler Frontend" cmd /k "npm run dev"
cd ..

timeout /t 3 /nobreak >nul

echo.
echo =========================================
echo    The Griddler is running!
echo =========================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Two new windows have been opened for backend and frontend.
echo Close those windows when you're done.
echo.
pause
