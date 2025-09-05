# 🚀 SUPER SIMPLE Deployment (No Windows Service)

## ✅ Dead Simple Steps:

### Step 1: Setup
```batch
setup_dependencies.bat
```
- Installs everything needed
- Shows you the webhook URL for Ringba

### Step 2: Start 24/7
```batch
start_24_7.bat
```
- Starts the server
- Keeps it running 24/7
- Auto-restarts if it crashes
- **KEEP THIS WINDOW OPEN**

### Step 3: Configure Ringba
- Use the webhook URL from Step 1
- Set Method: POST
- Set Content-Type: application/json

## 🎯 That's It!

**The server will run 24/7 as long as the window stays open.**

## 📝 Important Notes:
- ✅ Keep the command window open
- ✅ Don't close the black window
- ✅ If you need to restart the PC, just run `start_24_7.bat` again
- ✅ Server will auto-restart if it crashes

## 🛑 To Stop:
- Close the command window
- Or press Ctrl+C in the window

**No Windows Services, no NSSM, no complexity!** 🚀

