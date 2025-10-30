#!/bin/bash
# Stop script for The Griddler

echo "Stopping The Griddler..."

# Kill processes on port 8000 (backend)
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Stopping backend (port 8000)..."
    kill $(lsof -t -i:8000) 2>/dev/null || true
    echo "✓ Backend stopped"
else
    echo "ℹ Backend not running"
fi

# Kill processes on port 5173 (frontend)
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Stopping frontend (port 5173)..."
    kill $(lsof -t -i:5173) 2>/dev/null || true
    echo "✓ Frontend stopped"
else
    echo "ℹ Frontend not running"
fi

echo "Done!"
