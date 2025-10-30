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
- ✅ Modern web UI
- ✅ File upload and management

### Phase 2 (Planned)
- 🔄 AI-assisted comparison analysis
- 🔄 Advanced conversion rules engine
- 🔄 Batch processing
- 🔄 Export reports and converted code

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Installation

1. **Backend Setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Frontend Setup**:
```bash
cd frontend
npm install
```

### Running the Application

1. **Start Backend**:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

2. **Start Frontend**:
```bash
cd frontend
npm run dev
```

3. Open browser to `http://localhost:5173`

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
│   ├── tests/
│   └── requirements.txt
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── hooks/         # Custom React hooks
│   │   └── App.tsx
│   └── package.json
├── samples/               # Sample COBOL files
│   ├── pre/              # PRE conversion examples
│   └── post/             # POST conversion examples
└── docs/                  # Documentation
```

## Contributing

This is an iterative project designed to improve over time. Contributions welcome!

## License

MIT
