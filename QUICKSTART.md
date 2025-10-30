# Quick Start Guide

Get The Griddler up and running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
```

## Running the Application

### Option 1: Easy Way (Recommended) ⭐

**Terminal 1 - Backend:**
```bash
cd backend
./run.sh          # Linux/Mac
# OR
run.bat           # Windows
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option 2: Both at Once (Linux/Mac only)
```bash
# From project root
./start.sh

# To stop everything
./stop.sh
```

### Option 3: Manual Way
**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open your browser to: http://localhost:5173**

## First Steps

### 1. Try the Comparison Feature

1. Navigate to the **Compare** tab
2. Upload sample files from `samples/`:
   - PRE: `samples/pre/customer_grid_pre.cbl`
   - POST: `samples/post/customer_grid_post.cbl`
3. Click **Analyze** to see the transformation patterns

### 2. Test the Converter

1. Navigate to the **Convert** tab
2. Upload a PRE conversion file: `samples/pre/customer_grid_pre.cbl`
3. Click **Convert to SCR100** to see the automatic conversion
4. Download the converted code

### 3. Enable AI Analysis (Optional)

1. Get API keys:
   - **Claude**: https://console.anthropic.com/
   - **OpenAI**: https://platform.openai.com/

2. Add to `backend/.env`:
   ```env
   ANTHROPIC_API_KEY=your_claude_key_here
   OPENAI_API_KEY=your_openai_key_here
   ```

3. Restart the backend server

4. In the Compare tab, select **AI-Based** analysis method

## Troubleshooting

### Backend won't start / "uvicorn not recognized"
- **Solution 1 (Easiest)**: Use the run script: `cd backend && ./run.sh`
- **Solution 2**: Run directly from venv: `cd backend && ./venv/bin/uvicorn app.main:app --reload`
- **Solution 3**: Reinstall: `cd backend && ./venv/bin/pip install -r requirements.txt`
- Ensure Python 3.11+ is installed: `python3 --version`

### Frontend won't start
- Ensure Node 18+ is installed: `node --version`
- Clear cache: `rm -rf node_modules package-lock.json && npm install`
- Check port 5173 is available

### API Connection Error
- Ensure backend is running on port 8000
- Check `frontend/.env` has: `VITE_API_URL=http://localhost:8000`
- Clear browser cache and reload

### AI Analysis Unavailable
- Check API keys are set in `backend/.env`
- Restart backend after adding keys
- Verify keys are valid on provider's dashboard

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore sample COBOL programs in `samples/`
- Check the Settings tab to verify system status
- Start converting your own COBOL programs!

## Need Help?

- Check the **Settings** tab for system status
- Review sample files in `samples/` directory
- See the main README.md for architecture details

## Development

To run tests:
```bash
# Backend tests
cd backend
pytest

# Frontend linting
cd frontend
npm run lint
```

To build for production:
```bash
# Backend (already Python, no build needed)

# Frontend
cd frontend
npm run build
```
