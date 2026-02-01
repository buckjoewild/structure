#!/bin/bash
# Unix Setup Script for BruceOps

set -e

echo "========================================"
echo "BruceOps Setup Script"
echo "========================================"
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed. Please install Node.js 20+ first."
    exit 1
fi

echo "[OK] Node.js found: $(node --version)"

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "[WARNING] PostgreSQL not found. You'll need to install it or use Docker."
fi

# Navigate to app
cd ../harriswildlands || {
    echo "[ERROR] Could not find harriswildlands directory"
    exit 1
}

echo ""
echo "Installing dependencies..."
npm install

echo ""
echo "Checking configuration..."
if [ ! -f .env ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "[IMPORTANT] Please edit .env with your configuration"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your database and API keys"
echo "2. Run: npm run db:push"
echo "3. Run: npm run dev"
echo ""
echo "For help, see: ai-collaboration/MASTER_INDEX.md"
