@echo off
echo ========================================
echo Harris Wilderness MUD - Launcher
echo ========================================
echo.

echo [1] Starting MUD Server...
start "MUD Server" cmd /k "cd mud-server && python src/server.py"

timeout /t 3 /nobreak >nul

echo [2] Opening Retro Terminal...
start "MUD Terminal" cmd /k "cd mud-terminal && python -m http.server 8080"

timeout /t 2 /nobreak >nul

echo [3] Starting OpenClaw Agent...
start "OpenClaw Agent" cmd /k "cd integrations/mud-agent && node agent.js"

echo.
echo ========================================
echo All systems launched!
echo.
echo MUD Server: ws://localhost:4008
echo Terminal: http://localhost:8080
echo.
echo Open browser to http://localhost:8080
echo ========================================
pause
