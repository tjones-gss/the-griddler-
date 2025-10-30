#!/bin/bash
# Master run script for The Griddler

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "   The Griddler - COBOL SCR100 Parser   "
echo "========================================="
echo ""

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Check if backend is already running
if check_port 8000; then
    echo "✓ Backend already running on port 8000"
else
    echo "Starting backend on port 8000..."
    cd backend
    ./venv/bin/uvicorn app.main:app --reload --port 8000 --host 0.0.0.0 > ../backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    echo "✓ Backend started (PID: $BACKEND_PID)"
    sleep 3
fi

# Check if frontend is already running
if check_port 5173; then
    echo "✓ Frontend already running on port 5173"
else
    echo "Starting frontend on port 5173..."
    cd frontend
    npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    echo "✓ Frontend started (PID: $FRONTEND_PID)"
    sleep 3
fi

echo ""
echo "========================================="
echo "   The Griddler is running!             "
echo "========================================="
echo ""
echo "🌐 Open in browser: http://localhost:5173"
echo "📚 API docs: http://localhost:8000/docs"
echo ""
echo "Logs:"
echo "  Backend:  tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo ""
echo "To stop:"
echo "  ./stop.sh"
echo ""
