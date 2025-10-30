# Windows Quick Start Guide

**The Griddler is optimized for Windows!** This guide gets Windows users up and running fast.

## Prerequisites

Before you start, ensure you have:

- ✅ **Python 3.11 or 3.12** - [Download from python.org](https://www.python.org/downloads/)
  - ⚠️ **NOT Python 3.13** - Some dependencies don't support it yet
  - **Recommended**: Python 3.12.x
  - During install, check "Add Python to PATH"
- ✅ **Node.js 18+** - [Download from nodejs.org](https://nodejs.org/)
  - LTS version recommended

Verify installation in Command Prompt:
```batch
python --version
node --version
npm --version
```

## 🚀 Super Quick Start (2 Steps!)

### Step 1: Setup
Double-click `setup.bat` or run in Command Prompt:
```batch
setup.bat
```

This will:
- Create Python virtual environment
- Install all Python dependencies
- Install all Node.js dependencies
- Create .env configuration files

### Step 2: Run
Double-click `start.bat` or run in Command Prompt:
```batch
start.bat
```

This will:
- Open two Command Prompt windows automatically
- Start the backend API (port 8000)
- Start the frontend UI (port 5173)

**Open your browser to: http://localhost:5173**

That's it! 🎉

## Alternative: Manual Control

If you prefer more control, open two Command Prompts:

**Command Prompt 1 - Backend:**
```batch
cd backend
run.bat
```

**Command Prompt 2 - Frontend:**
```batch
cd frontend
npm run dev
```

## 📁 Sample Files

Try the sample COBOL files included:

- `samples\pre\customer_grid_pre.cbl` - Uses REPEAT GROUPS
- `samples\post\customer_grid_post.cbl` - Uses SCR100

### Quick Test:

1. Open http://localhost:5173
2. Click the **Compare** tab
3. Upload `samples\pre\customer_grid_pre.cbl` as PRE
4. Upload `samples\post\customer_grid_post.cbl` as POST
5. Click **Analyze** to see transformation patterns!

## 🔧 Common Windows Issues

### "python not recognized" or wrong version
**Problem:** Python not in PATH or using Python 3.13

**Solution:**
1. Check your Python version: `python --version`
2. If you have Python 3.13, uninstall it
3. Install Python 3.11 or 3.12 from python.org
4. During install, check "Add Python to PATH"
5. Restart Command Prompt and try again

### "node not recognized"
**Problem:** Node.js not in PATH

**Solution:**
1. Reinstall Node.js from nodejs.org
2. Restart Command Prompt after install

### Port 8000 or 5173 already in use
**Problem:** Previous instance still running

**Solution:**
```batch
REM Find what's using the port
netstat -ano | findstr :8000

REM Kill it (replace <PID> with actual number from above)
taskkill /PID <PID> /F
```

Or just close the Command Prompt windows that are running the app.

### "Access Denied" errors
**Problem:** Antivirus or permissions blocking

**Solution:**
- Run Command Prompt as Administrator (right-click > Run as administrator)
- Add project folder to antivirus exceptions
- Ensure you have write permissions in the project folder

### Frontend shows "Network Error"
**Problem:** Backend not running or wrong URL

**Solution:**
1. Check backend is running: Open http://localhost:8000/api/health
2. Check `frontend\.env` has: `VITE_API_URL=http://localhost:8000`
3. Restart both backend and frontend

## 🎯 Development Workflow

### Daily Usage:
```batch
REM Just run this each time:
start.bat

REM When done, close the Command Prompt windows
```

### Updating Dependencies:
```batch
REM Backend
cd backend
venv\Scripts\pip.exe install -r requirements.txt

REM Frontend
cd frontend
npm install
```

### Fresh Start:
```batch
REM If things get weird, start fresh:
setup.bat
```

## 🤖 AI Analysis (Optional)

To use AI-assisted analysis:

1. Get API keys:
   - **Claude**: https://console.anthropic.com/
   - **OpenAI**: https://platform.openai.com/

2. Edit `backend\.env`:
   ```env
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   OPENAI_API_KEY=sk-your-key-here
   ```

3. Restart backend (close and run `backend\run.bat` again)

4. In the Compare tab, select **AI-Based** analysis

## 📚 Next Steps

- **[README.md](README.md)** - Full project documentation and setup guide
- **[samples\README.md](samples\README.md)** - Sample COBOL programs

## 💡 Tips for Windows Users

1. **Use the .bat scripts** - They handle everything automatically
2. **Keep Command Prompts open** - Don't close them while using the app
3. **Check Windows Firewall** - Allow Python and Node through firewall if prompted
4. **Use latest Python/Node** - Keeps things compatible and secure
5. **Try samples first** - Good way to learn how it works

## 🆘 Still Stuck?

See [RUNNING.md](RUNNING.md) for comprehensive troubleshooting, or check:
- Backend logs in the Command Prompt window
- Frontend logs in the Command Prompt window
- Browser console (F12 > Console tab)

## System Requirements

**Minimum:**
- Windows 10 or 11
- 4 GB RAM
- 1 GB free disk space

**Recommended:**
- Windows 10 or 11 (latest updates)
- 8 GB RAM
- 2 GB free disk space
- SSD for better performance

---

**Enjoy using The Griddler!** 🎉

For the COBOL modernization team ⚡
