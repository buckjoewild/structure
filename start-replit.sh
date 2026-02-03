#!/bin/bash
# Replit Deployment Script - Start all services

echo "╔══════════════════════════════════════════╗"
echo "║  HARRIS WILDERNESS MUD - REPLIT DEPLOY   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}[1/4] Installing BruceOps dependencies...${NC}"
cd harriswildlands
npm install 2>&1 | grep -v "npm WARN"
cd ..

echo -e "${BLUE}[2/4] Installing MUD Server dependencies...${NC}"
cd mud-server
pip install websockets asyncio-mqtt 2>&1 | grep -v "Requirement already satisfied"
cd ..

echo -e "${YELLOW}[3/4] Starting all services in parallel...${NC}"
echo ""

# Start all three services in the background
echo -e "${GREEN}🚀 Starting BruceOps on port 5000${NC}"
cd harriswildlands && npm run dev &
BRUCE_PID=$!
cd ..

echo -e "${GREEN}🎮 Starting MUD Server on port 4008${NC}"
cd mud-server && python src/server.py &
MUD_PID=$!
cd ..

echo -e "${GREEN}🖥️  Starting MUD Terminal on port 8080${NC}"
cd mud-terminal && python -m http.server 8080 &
TERM_PID=$!
cd ..

echo ""
echo -e "${GREEN}✅ All services started!${NC}"
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║           ACCESS POINTS                  ║"
echo "╠══════════════════════════════════════════╣"
echo "║ BruceOps App: https://your-replit-url    ║"
echo "║ MUD Terminal: https://your-replit-url:3000"
echo "║ WebSocket:   wss://your-replit-url:8080  ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down services...${NC}"
    kill $BRUCE_PID $MUD_PID $TERM_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for all processes
wait
