# The Griddler - COBOL SCR100 Parser

An adaptable parser system for analyzing and converting COBOL programs from REPEAT GROUPS logic to SCR100 grid logic.

> **🪟 Windows Users:** See [WINDOWS.md](WINDOWS.md) for a dedicated Windows quick start guide!

## Overview

The Griddler provides two main capabilities:

1. **Analysis & Comparison**: Compare PRE (REPEAT GROUPS) vs POST (SCR100) converted programs to understand transformation patterns
   - Code-based pattern detection
   - AI-assisted intelligent analysis

2. **Automatic Conversion**: Parse and convert PRE programs to use SCR100 logic
   - Pattern-based transformations
   - Configurable conversion rules
   - Preview before applying changes

## Architecture

```
┌─────────────────────────────────────────────┐
│          Modern Web UI (React)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Compare  │  │ Convert  │  │ Settings │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────────┐
│       Backend API (Python/FastAPI)          │
│  ┌────────────────┐  ┌──────────────────┐  │
│  │ Code-Based     │  │ AI-Based         │  │
│  │ Analyzer       │  │ Analyzer         │  │
│  └────────────────┘  └──────────────────┘  │
│  ┌─────────────────────────────────────┐   │
│  │   COBOL Parser & Converter Engine   │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic
- **Frontend**: React 18, Vite, Tailwind CSS, shadcn/ui
- **Parser**: Custom COBOL parser with regex and AST analysis
- **AI Integration**: Claude API / OpenAI API (configurable)

## Features

### Phase 1 (Current)
- ✅ Project structure and architecture
- ✅ COBOL parser foundation
- ✅ Code-based pattern comparison
- ✅ AI-assisted analysis (optional)
- ✅ Modern web UI with React + Vite
- ✅ File upload and management
- ✅ Automatic conversion engine
- ✅ Easy run scripts and documentation

### Phase 2 (Future)
- 🔄 Advanced conversion rules engine
- 🔄 Batch processing multiple files
- 🔄 Export analysis reports
- 🔄 Enhanced pattern detection
- 🔄 Custom rule builder UI

## Getting Started

### Quick Start (Windows)

The fastest way to get up and running:

```batch
REM 1. Automated setup (double-click or run in Command Prompt)
setup.bat

REM 2. Start backend (Command Prompt 1)
cd backend
run.bat

REM 3. Start frontend (Command Prompt 2)
cd frontend
npm run dev

REM 4. Open browser to: http://localhost:5173
```

**Or use the all-in-one starter:**
```batch
start.bat
```
This opens two Command Prompt windows automatically for backend and frontend.

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions and [RUNNING.md](RUNNING.md) for troubleshooting.

> **Linux/Mac users:** Use `setup.sh`, `./run.sh`, and `start.sh` instead.

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Manual Installation

**Backend (Windows):**
```batch
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

**Backend (Linux/Mac):**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

**Frontend (Windows):**
```batch
cd frontend
npm install
copy .env.example .env
```

**Frontend (Linux/Mac):**
```bash
cd frontend
npm install
cp .env.example .env
```

### Running the Application

#### Option 1: Easy Way (Recommended) ⭐

**Windows:**
```batch
REM Command Prompt 1 - Backend
cd backend
run.bat

REM Command Prompt 2 - Frontend
cd frontend
npm run dev
```

**Linux/Mac:**
```bash
# Terminal 1 - Backend
cd backend
./run.sh

# Terminal 2 - Frontend
cd frontend
npm run dev
```

#### Option 2: All-in-One Starter

**Windows:**
```batch
start.bat
```
Opens two Command Prompt windows automatically.

**Linux/Mac:**
```bash
./start.sh        # Start everything
./stop.sh         # Stop everything
```

#### Option 3: Direct venv Call (No activation needed)

**Windows:**
```batch
REM Backend
cd backend
venv\Scripts\uvicorn.exe app.main:app --reload --port 8000

REM Frontend (in another Command Prompt)
cd frontend
npm run dev
```

**Linux/Mac:**
```bash
# Backend
cd backend
./venv/bin/uvicorn app.main:app --reload --port 8000

# Frontend (in another terminal)
cd frontend
npm run dev
```

**Open browser to:** `http://localhost:5173`

> **Note:** If you get "uvicorn not recognized", use `run.bat` (Windows) or `./run.sh` (Linux/Mac) - see [RUNNING.md](RUNNING.md) for troubleshooting.

## Usage

### Analyzing PRE vs POST Programs

1. Navigate to the **Compare** tab
2. Upload a PRE program (uses REPEAT GROUPS)
3. Upload the corresponding POST program (uses SCR100)
4. Choose analysis method:
   - **Code-Based**: Fast pattern matching and diff analysis
   - **AI-Based**: Intelligent semantic analysis (requires API key)
5. Review the detected transformation patterns

### Converting a PRE Program

1. Navigate to the **Convert** tab
2. Upload a PRE program
3. Select conversion rules (auto-detected from previous comparisons)
4. Preview the converted code
5. Download or save the converted program

## Configuration

Create `.env` files in both backend and frontend directories:

**backend/.env**:
```env
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

**frontend/.env**:
```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
the-griddler/
├── backend/                # Python FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core configuration
│   │   ├── models/        # Pydantic models
│   │   ├── services/      # Business logic
│   │   │   ├── parser/    # COBOL parser
│   │   │   ├── analyzer/  # Code & AI analyzers
│   │   │   └── converter/ # Conversion engine
│   │   └── main.py        # FastAPI app entry
│   ├── run.bat           # Easy run script (Windows) ⭐
│   ├── run.sh            # Easy run script (Linux/Mac)
│   └── requirements.txt
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── App.tsx
│   └── package.json
├── samples/               # Sample COBOL files
│   ├── pre/              # PRE conversion examples
│   └── post/             # POST conversion examples
├── setup.bat             # Automated setup (Windows) ⭐
├── setup.sh              # Automated setup (Linux/Mac)
├── start.bat             # Start everything (Windows) ⭐
├── start.sh              # Start everything (Linux/Mac)
├── stop.sh               # Stop all services (Linux/Mac)
├── README.md             # This file
├── QUICKSTART.md         # Quick start guide
└── RUNNING.md            # Comprehensive running guide
```

## Documentation

- **[WINDOWS.md](WINDOWS.md)** - 🪟 Windows-specific quick start guide (recommended for Windows users!)
- **[README.md](README.md)** - This file, project overview
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[RUNNING.md](RUNNING.md)** - Comprehensive troubleshooting guide
- **[samples/README.md](samples/README.md)** - Sample COBOL programs and patterns

## Key Transformation Patterns

The Griddler detects and converts these common patterns:

### 1. REPEAT GROUP → GRID Structure
**PRE:**
```cobol
05  CUSTOMER-ENTRY REPEAT 15 TIMES.
    10  SP2-RX-CUST-ID    PIC X(10).
```

**POST:**
```cobol
05  CUSTOMER-ROW OCCURS 15 TIMES INDEXED BY CUST-IDX.
    10  CUST-ID-COL       PIC X(10).
```

### 2. SP2-RX- Fields → -COL Fields
**PRE:** `SP2-RX-CUST-NAME`
**POST:** `CUST-NAME-COL`

### 3. PERFORM VARYING → SCR100 Operations
**PRE:**
```cobol
PERFORM VARYING WS-INDEX FROM 1 BY 1 UNTIL WS-INDEX > 15
    MOVE SPACES TO SP2-RX-CUST-ID (WS-INDEX)
END-PERFORM
```

**POST:**
```cobol
MOVE 'INIT' TO SCR100-FUNCTION
CALL 'SCR100' USING SCR100-PARAMS
```

See `samples/` directory for complete examples.

## Troubleshooting

### "uvicorn not recognized" or "command not found"
**Windows:** Use `run.bat` instead:
```batch
cd backend
run.bat
```

**Linux/Mac:** Use `./run.sh` instead:
```bash
cd backend
./run.sh
```

### Port already in use (8000 or 5173)

**Windows:**
```batch
REM Find what's using port 8000
netstat -ano | findstr :8000

REM Kill the process (replace <PID> with the actual number)
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
./stop.sh  # Stops all services
# Or manually: kill $(lsof -t -i:8000)
```

### Frontend can't connect to backend
1. Check backend is running: Open `http://localhost:8000/api/health` in browser
2. Verify `frontend\.env` has: `VITE_API_URL=http://localhost:8000`
3. Restart both services

See [RUNNING.md](RUNNING.md) for comprehensive troubleshooting.

## Contributing

This is an iterative project designed to improve over time. Contributions welcome!

## License

MIT
