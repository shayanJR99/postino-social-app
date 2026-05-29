@echo off
TITLE Postino Project - Docker Manager
echo ========================================
echo   Welcome to Postino Project (Windows)
echo ========================================
echo.
echo [1/3] Checking Docker status...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not running!
    echo Please install Docker Desktop and try again.
    pause
    exit /b
)

echo [2/3] Building and Starting Containers...
echo This might take a minute on the first run...
docker-compose up --build -d

echo.
echo [3/3] Success!
echo Project is running at: http://localhost:8000
echo Admin panel at: http://localhost:8000/admin
echo.
echo ----------------------------------------
echo To stop the project, just close this window or 
echo run "docker-compose down" in this folder.
echo ----------------------------------------
pause
