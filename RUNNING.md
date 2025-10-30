# Running The Griddler - Complete Guide

This guide covers all the ways to run The Griddler, including troubleshooting common issues.

## ✅ Setup Confirmation

Before running, ensure setup is complete:

```bash
# Check backend
cd backend
ls venv/          # Should show bin/ (or Scripts/ on Windows)
ls venv/bin/uvicorn  # Should exist

# Check frontend
cd ../frontend
ls node_modules/  # Should have many packages
```

## 🚀 Running Methods

### Method 1: Run Scripts (RECOMMENDED)

These scripts handle everything for you - no need to activate venv!

**Backend:**
```bash
cd backend
./run.sh          # Linux/Mac
run.bat           # Windows
```

**Frontend (in another terminal):**
```bash
cd frontend
npm run dev
```

### Method 2: Start Everything at Once (Linux/Mac)

```bash
# From project root
./start.sh        # Starts both backend and frontend

# View logs
tail -f backend.log
tail -f frontend.log

# Stop everything
./stop.sh
```

### Method 3: Direct venv Usage (No activation needed)

**Backend:**
```bash
cd backend
./venv/bin/uvicorn app.main:app --reload --port 8000
# On Windows: venv\Scripts\uvicorn.exe app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### Method 4: Traditional Way (With venv activation)

**Backend:**
```bash
cd backend
source venv/bin/activate      # Linux/Mac
# OR
venv\Scripts\activate         # Windows

uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## 🔧 Common Issues & Solutions

### Issue: "uvicorn is not recognized"

**Problem:** You're trying to run `uvicorn` but the command isn't found.

**Solutions (try in order):**

1. **Use the run script (easiest):**
   ```bash
   cd backend
   ./run.sh
   ```

2. **Run directly from venv (no activation needed):**
   ```bash
   cd backend
   ./venv/bin/uvicorn app.main:app --reload --port 8000
   ```

3. **Activate venv first:**
   ```bash
   cd backend
   source venv/bin/activate    # Linux/Mac
   # OR
   venv\Scripts\activate       # Windows
   uvicorn app.main:app --reload --port 8000
   ```

4. **Reinstall if needed:**
   ```bash
   cd backend
   ./venv/bin/pip install -r requirements.txt
   ```

### Issue: "ModuleNotFoundError: No module named 'app'"

**Problem:** Running uvicorn from wrong directory.

**Solution:** Make sure you're in the `backend/` directory:
```bash
cd backend
./venv/bin/uvicorn app.main:app --reload
```

### Issue: "Address already in use" (Port 8000 or 5173)

**Problem:** A previous instance is still running.

**Solutions:**

1. **Linux/Mac:**
   ```bash
   # Kill backend (port 8000)
   kill $(lsof -t -i:8000)

   # Kill frontend (port 5173)
   kill $(lsof -t -i:5173)
   ```

2. **Windows:**
   ```powershell
   # Find and kill process on port 8000
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

3. **Use different ports:**
   ```bash
   # Backend on port 8001
   ./venv/bin/uvicorn app.main:app --reload --port 8001

   # Update frontend/.env
   VITE_API_URL=http://localhost:8001
   ```

### Issue: Frontend can't connect to backend

**Symptoms:**
- "Network Error" in browser console
- Settings page shows "Backend Unavailable"

**Solutions:**

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/api/health
   # Should return: {"status":"healthy",...}
   ```

2. **Check frontend .env:**
   ```bash
   cd frontend
   cat .env
   # Should have: VITE_API_URL=http://localhost:8000
   ```

3. **Restart both services:**
   ```bash
   # Stop everything
   ./stop.sh

   # Start backend
   cd backend && ./run.sh

   # Start frontend (in new terminal)
   cd frontend && npm run dev
   ```

### Issue: Frontend shows blank page

**Solutions:**

1. **Check console for errors:**
   - Open browser DevTools (F12)
   - Look at Console tab for errors

2. **Rebuild frontend:**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   npm run dev
   ```

3. **Clear browser cache:**
   - Ctrl+Shift+R (Windows/Linux)
   - Cmd+Shift+R (Mac)

## 🧪 Verification Steps

After starting, verify everything works:

### 1. Backend Health Check
```bash
# In browser or curl
curl http://localhost:8000/api/health

# Expected response:
{
  "status": "healthy",
  "version": "0.1.0",
  "ai_available": {
    "claude": false,
    "openai": false
  }
}
```

### 2. Frontend Access
- Open: http://localhost:5173
- Should see "The Griddler" header
- Three tabs: Compare, Convert, Settings

### 3. API Docs
- Open: http://localhost:8000/docs
- Should see FastAPI Swagger UI
- Can test endpoints directly

## 📝 Environment Variables

### Backend (.env)
```env
# Optional - only for AI analysis
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx

# Server config (defaults shown)
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Frontend (.env)
```env
# API URL
VITE_API_URL=http://localhost:8000
```

## 🎯 Quick Start Commands

**First Time Setup:**
```bash
# Clone and setup
cd the-griddler-
./setup.sh
```

**Every Time You Want to Run:**
```bash
# Terminal 1 - Backend
cd backend
./run.sh

# Terminal 2 - Frontend
cd frontend
npm run dev

# Open: http://localhost:5173
```

**When You're Done:**
```bash
# Stop everything
./stop.sh
# Or just Ctrl+C in each terminal
```

## 🐛 Still Having Issues?

1. **Check Python version:**
   ```bash
   python3 --version
   # Need 3.11 or higher
   ```

2. **Check Node version:**
   ```bash
   node --version
   # Need 18 or higher
   ```

3. **Start fresh:**
   ```bash
   # Backend
   cd backend
   rm -rf venv
   python3 -m venv venv
   ./venv/bin/pip install -r requirements.txt

   # Frontend
   cd ../frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Check logs:**
   ```bash
   # If using start.sh
   tail -f backend.log
   tail -f frontend.log
   ```

## 💡 Pro Tips

1. **Keep two terminals open** - one for backend, one for frontend
2. **Use the run scripts** - they handle venv activation automatically
3. **Check Settings tab** after starting to verify system status
4. **Try sample files first** - `samples/pre/customer_grid_pre.cbl`
5. **API keys are optional** - code-based analysis works without them

## 📚 Next Steps

Once running successfully:
- Read [QUICKSTART.md](QUICKSTART.md) for first steps
- Read [README.md](README.md) for full documentation
- Check `samples/` directory for example COBOL files
