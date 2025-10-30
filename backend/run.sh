#!/bin/bash
# Run script for The Griddler Backend

cd "$(dirname "$0")"

echo "Starting The Griddler Backend..."
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✓ Created .env file. Edit it to add API keys for AI features."
    echo ""
fi

# Run uvicorn directly from venv
./venv/bin/uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
