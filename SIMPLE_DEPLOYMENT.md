# 🚀 Simple Server PC Deployment Guide

## ✅ Quick Deployment Checklist

### Before You Start:
- [ ] Server PC has Python 3.8+ installed
- [ ] You have admin rights on the server PC
- [ ] Download NSSM from https://nssm.cc/download (extract nssm.exe to project folder)

### Step 1: Copy Files
- [ ] Copy entire project folder to server PC (e.g., `C:\RingbaWebhook`)

### Step 2: Configure
- [ ] Place `credentials.json` file in the project folder
- [ ] Edit `.env` file with your settings:
  ```
  RINGBA_CAMPAIGN_NAME=SPANISH DEBT | 3.5 STANDARD | 01292025
  RINGBA_TARGET_NAME=-no value-
  GOOGLE_SHEET_ID=your_sheet_id_here
  SLACK_WEBHOOK_URL=your_slack_webhook_url
  ```

### Step 3: Install Everything
**Run these files in order:**

1. **Right-click → "Run as administrator":**
   ```
   setup_dependencies.bat
   ```
   - Installs Python packages
   - Shows webhook URL for Ringba

2. **Right-click → "Run as administrator":**
   ```
   install_service.bat
   ```
   - Installs Windows service
   - Automatically starts the service
   - Shows success/failure status

### Step 4: Configure Ringba
- [ ] Copy the webhook URL from setup script
- [ ] Paste into Ringba dashboard webhook settings
- [ ] Set Method: POST, Content-Type: application/json

### Step 5: Test
- [ ] Check Google Sheet for test entries
- [ ] Check Slack for notifications
- [ ] Service should show "Running" status

## 🎯 That's It!
Your system is now running 24/7 and will:
- ✅ Start automatically on server boot
- ✅ Process Ringba "No Value" calls
- ✅ Log to Google Sheets
- ✅ Send Slack notifications
- ✅ Restart automatically if it crashes

## 📞 Quick Commands
```batch
# Check if service is running
sc query RingbaWebhookHandler

# Stop service
net stop RingbaWebhookHandler

# Start service
net start RingbaWebhookHandler

# View logs
notepad ringba_webhook_port80.log
```

