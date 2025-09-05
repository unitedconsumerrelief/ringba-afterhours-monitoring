# 🚀 Ringba Webhook Handler - Server PC Deployment Guide

## 📋 Prerequisites
- Windows Server PC with Python 3.8+ installed
- Internet connection for dependencies
- Admin access for Windows services

## 🔧 Step-by-Step Deployment

### Step 1: Copy Files to Server PC
1. Copy all project files to the server PC
2. Place in a dedicated folder (e.g., `C:\RingbaWebhook`)

### Step 2: Run Setup Script
```batch
setup_dependencies.bat
```
This will:
- ✅ Install Python dependencies
- ✅ Show the correct webhook URL for Ringba
- ✅ Test the application

### Step 3: Configure Environment
1. Ensure `credentials.json` is in the project folder
2. Update `.env` file with your settings:
   ```
   RINGBA_CAMPAIGN_NAME=SPANISH DEBT | 3.5 STANDARD | 01292025
   RINGBA_TARGET_NAME=-no value-
   GOOGLE_SHEET_ID=your_sheet_id
   SLACK_WEBHOOK_URL=your_slack_webhook
   ```

### Step 4: Test the Application
```batch
start_server_port80.bat
```
- Verify it starts without errors
- Test with Postman if needed
- Stop the server (Ctrl+C)

### Step 5: Install as Windows Service (24/7)
```batch
install_service.bat
```
This creates a Windows service that:
- ✅ Starts automatically on boot
- ✅ Runs in background 24/7
- ✅ Restarts automatically if it crashes
- ✅ No user login required

### Step 6: Configure Ringba
1. Log into Ringba dashboard
2. Go to Campaign Settings → Webhooks
3. Add webhook URL: `http://SERVER_IP:80/ringba-webhook`
4. Set Method: POST
5. Set Content Type: application/json
6. Set Fire Pixel On: Finalized

## 🔍 Monitoring

### Check Service Status
```batch
sc query "RingbaWebhook"
```

### View Logs
- Application logs: `ringba_webhook_port80.log`
- Windows service logs: Event Viewer

### Test Webhook
```batch
python test_webhook.py
```

## 🛠️ Troubleshooting

### Service Won't Start
1. Check Windows Event Viewer
2. Verify Python path in service
3. Check file permissions

### Webhook Not Working
1. Verify service is running
2. Check firewall settings
3. Test with Postman
4. Check Ringba webhook logs

### Port 80 Issues
- Try port 8080 as alternative
- Check if IIS is using port 80
- Verify firewall allows port 80

## 📞 Support
- Check logs in `ringba_webhook_port80.log`
- Monitor Google Sheet for entries
- Check Slack for notifications

## ✅ Success Indicators
- ✅ Service shows "Running" status
- ✅ Google Sheet receives entries
- ✅ Slack notifications arrive
- ✅ No timeout errors in Ringba

**Your system will now run 24/7 automatically!** 🚀

