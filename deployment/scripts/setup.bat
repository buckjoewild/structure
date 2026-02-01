@echo off
REM Windows Setup Script for BruceOps

echo ========================================
echo BruceOps Setup Script
echo ========================================
echo.

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 20+ first.
    exit /b 1
)
echo [OK] Node.js found

REM Check PostgreSQL
psql --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PostgreSQL not found. You'll need to install it or use Docker.
)

REM Navigate to app
cd ..\harriswildlands
if errorlevel 1 (
    echo [ERROR] Could not find harriswildlands directory
    exit /b 1
)

echo.
echo Installing dependencies...
call npm install
if errorlevel 1 (
    echo [ERROR] npm install failed
    exit /b 1
)

echo.
echo Checking configuration...
if not exist .env (
    echo Creating .env from template...
    copy .env.example .env
    echo [IMPORTANT] Please edit .env with your configuration
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env with your database and API keys
echo 2. Run: npm run db:push
echo 3. Run: npm run dev
echo.
echo For help, see: ai-collaboration\MASTER_INDEX.md
