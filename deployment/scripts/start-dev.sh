#!/bin/bash
# Start BruceOps Development Server

echo "Starting BruceOps development server..."
echo ""

cd ../harriswildlands || {
    echo "[ERROR] Could not find harriswildlands directory"
    exit 1
}

echo "Running: npm run dev"
echo ""
echo "Server will be available at: http://localhost:5000"
echo ""

npm run dev
