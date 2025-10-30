#!/bin/bash

# The Griddler Setup Script

set -e

echo "========================================="
echo "   The Griddler - COBOL SCR100 Parser   "
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "${YELLOW}Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.11+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check Node
echo -e "${YELLOW}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 18+${NC}"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node $NODE_VERSION found${NC}"

# Setup Backend
echo ""
echo -e "${YELLOW}Setting up backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env and add your API keys${NC}"
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"

cd ..

# Setup Frontend
echo ""
echo -e "${YELLOW}Setting up frontend...${NC}"
cd frontend

if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
fi

echo "Installing Node dependencies..."
npm install

echo -e "${GREEN}✓ Frontend setup complete${NC}"

cd ..

# Done
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}   Setup Complete!                     ${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend (in terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --port 8000"
echo ""
echo "2. Start the frontend (in terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open browser to: http://localhost:5173"
echo ""
echo -e "${YELLOW}Note: For AI-based analysis, configure API keys in backend/.env${NC}"
echo ""
