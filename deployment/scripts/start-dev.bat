@echo off
REM Start BruceOps Development Server

echo Starting BruceOps development server...
echo.

cd ..\harriswildlands
if errorlevel 1 (
    echo [ERROR] Could not find harriswildlands directory
    exit /b 1
)

echo Running: npm run dev
echo.
echo Server will be available at: http://localhost:5000
echo.

call npm run dev
