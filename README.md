# The Griddler - COBOL SCR100 Parser

An adaptable parser system for analyzing and converting COBOL programs from REPEAT GROUPS logic to SCR100 grid logic.

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

### Quick Start

The fastest way to get up and running:

```bash
# 1. Automated setup
chmod +x setup.sh
./setup.sh

# 2. Start backend (terminal 1)
cd backend
./run.sh          # Linux/Mac
# OR run.bat      # Windows

# 3. Start frontend (terminal 2)
cd frontend
npm run dev

# 4. Open browser
# http://localhost:5173
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions and [RUNNING.md](RUNNING.md) for troubleshooting.

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Manual Installation

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

### Running the Application

#### Option 1: Easy Way (Recommended) ⭐

```bash
# Terminal 1 - Backend
cd backend
./run.sh          # Linux/Mac
run.bat           # Windows

# Terminal 2 - Frontend
cd frontend
npm run dev
```

#### Option 2: Both at Once (Linux/Mac)

```bash
./start.sh        # Start everything
./stop.sh         # Stop everything
```

#### Option 3: Direct venv (No activation needed)

```bash
# Backend
cd backend
./venv/bin/uvicorn app.main:app --reload --port 8000

# Frontend (in another terminal)
cd frontend
npm run dev
```

Open browser to `http://localhost:5173`

> **Note:** If you get "uvicorn not recognized", use the run scripts or see [RUNNING.md](RUNNING.md) for troubleshooting.

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
│   ├── run.sh            # Easy run script (Linux/Mac)
│   ├── run.bat           # Easy run script (Windows)
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
├── setup.sh              # Automated setup script
├── start.sh              # Start both backend and frontend
├── stop.sh               # Stop all services
├── README.md             # This file
├── QUICKSTART.md         # Quick start guide
└── RUNNING.md            # Comprehensive running guide
```

## Documentation

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

### "uvicorn not recognized"
Use the run script: `cd backend && ./run.sh`

### Port already in use
```bash
./stop.sh  # Stop all services
# Or manually: kill $(lsof -t -i:8000)
```

### Frontend can't connect
1. Check backend is running: `curl http://localhost:8000/api/health`
2. Check `frontend/.env` has correct API URL

See [RUNNING.md](RUNNING.md) for comprehensive troubleshooting.

## Contributing

This is an iterative project designed to improve over time. Contributions welcome!

## License

MIT
