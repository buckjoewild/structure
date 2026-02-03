#!/bin/bash

echo "========================================"
echo "Harris Wilderness MUD - Launcher"
echo "========================================"
echo ""

echo "[1] Starting MUD Server..."
cd mud-server
python src/server.py &
MUD_PID=$!
cd ..

sleep 3

echo "[2] Opening Retro Terminal..."
cd mud-terminal
python3 -m http.server 8080 &
TERM_PID=$!
cd ..

sleep 2

echo "[3] Starting OpenClaw Agent..."
cd integrations/mud-agent
node agent.js &
AGENT_PID=$!
cd ../..

echo ""
echo "========================================"
echo "All systems launched!"
echo ""
echo "MUD Server: ws://localhost:4008"
echo "Terminal: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================"

# Wait for interrupt
trap "kill $MUD_PID $TERM_PID $AGENT_PID; exit" SIGINT
wait
