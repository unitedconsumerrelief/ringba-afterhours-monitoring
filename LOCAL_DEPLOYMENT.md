# Local Server Deployment Guide

This guide helps you deploy the Ringba Webhook Handler on a local Windows server.

## 🖥️ **Server Requirements**

- **OS**: Windows Server 2016+ or Windows 10/11
- **Python**: 3.8+ installed
- **Network**: Accessible from Ringba (port 5000 open)
- **Storage**: ~100MB for application and logs

## 📋 **Installation Steps**

### **Step 1: Prepare the Server**

1. **Create Application Directory**:
   ```cmd
   mkdir C:\RingbaWebhook
   cd C:\RingbaWebhook
   ```

2. **Copy All Files** to the server directory:
   - `main.py`
   - `config.py`
   - `google_sheets.py`
   - `slack_notify.py`
   - `requirements.txt`
   - `credentials.json`
   - `.env`
   - `start_server.bat`
   - `install_service.bat`

### **Step 2: Install Dependencies**

```cmd
pip install -r requirements.txt
```

### **Step 3: Configure Environment**

1. **Edit `.env` file** with your settings:
   ```env
   RINGBA_CAMPAIGN_NAME=SPANISH DEBT | 3.5 STANDARD | 01292025
   RINGBA_TARGET_NAME=-no value-
   GOOGLE_SHEET_ID=1VDloSHG41df3T5O3E1bOetclcmsFz2te4uQKUScMPu4
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   FLASK_ENV=production
   FLASK_DEBUG=False
   HOST=0.0.0.0
   PORT=5000
   ```

### **Step 4: Test the Application**

```cmd
python main.py
```

You should see:
```
Starting Ringba Webhook Handler on 0.0.0.0:5000
 * Serving Flask app 'main'
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

### **Step 5: Configure as Windows Service (Optional)**

1. **Install NSSM** (Non-Sucking Service Manager):
   - Download from: https://nssm.cc/download
   - Extract to a folder in PATH

2. **Install the Service**:
   ```cmd
   install_service.bat
   ```

3. **Start the Service**:
   ```cmd
   net start RingbaWebhookHandler
   ```

## 🔧 **Configuration for Ringba**

### **Webhook URL Setup**

In your Ringba dashboard:
1. Go to Campaign Settings
2. Find Webhook Configuration
3. Add URL: `http://YOUR_SERVER_IP:5000/ringba-webhook`
4. Set Method: `POST`
5. Set Content Type: `application/json`

### **Server IP Address**

To find your server's IP address:
```cmd
ipconfig
```

Look for the IPv4 address (e.g., `192.168.1.100`)

## 🚀 **Running the Application**

### **Option A: Manual Start**
```cmd
start_server.bat
```

### **Option B: Windows Service**
```cmd
net start RingbaWebhookHandler
```

### **Option C: Direct Python**
```cmd
python main.py
```

## 📊 **Monitoring and Logs**

### **Log Files**
- **Application Log**: `ringba_webhook.log`
- **Windows Event Log**: Check Application logs for service issues

### **Health Check**
```cmd
curl http://localhost:5000/
```

Should return:
```json
{
  "status": "healthy",
  "service": "Ringba Webhook Handler",
  "filters": {
    "campaign_name": "SPANISH DEBT | 3.5 STANDARD | 01292025",
    "target_name": "-no value-"
  },
  "server": "local"
}
```

### **Test Webhook**
```cmd
curl -X POST http://localhost:5000/ringba-webhook -H "Content-Type: application/json" -d "{\"campaignName\": \"SPANISH DEBT | 3.5 STANDARD | 01292025\", \"targetName\": \"-no value-\", \"callerId\": \"TEST_123\"}"
```

## 🔒 **Security Considerations**

### **Firewall Configuration**
1. **Open Port 5000** for incoming connections
2. **Restrict access** to Ringba IP addresses if possible
3. **Use HTTPS** in production (consider reverse proxy)

### **Network Security**
- **Internal Network**: Recommended for security
- **VPN Access**: If external access needed
- **IP Whitelisting**: Restrict to Ringba servers

## 🛠️ **Troubleshooting**

### **Common Issues**

1. **Port Already in Use**:
   ```cmd
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

2. **Service Won't Start**:
   ```cmd
   net stop RingbaWebhookHandler
   net start RingbaWebhookHandler
   ```

3. **Permission Issues**:
   - Run as Administrator
   - Check file permissions

4. **Python Not Found**:
   ```cmd
   where python
   python --version
   ```

### **Log Analysis**
```cmd
type ringba_webhook.log
```

Look for:
- `ERROR`: Application errors
- `WARNING`: Potential issues
- `INFO`: Normal operation

## 📈 **Maintenance**

### **Daily Checks**
1. **Service Status**: `sc query RingbaWebhookHandler`
2. **Log Review**: Check `ringba_webhook.log`
3. **Health Check**: `curl http://localhost:5000/`

### **Weekly Tasks**
1. **Log Rotation**: Archive old logs
2. **Dependency Updates**: `pip install --upgrade -r requirements.txt`
3. **Backup**: Copy application directory

### **Monthly Tasks**
1. **Security Updates**: Update Python and dependencies
2. **Performance Review**: Check log sizes and response times
3. **Configuration Review**: Verify environment variables

## 🆘 **Emergency Procedures**

### **Service Down**
```cmd
net stop RingbaWebhookHandler
net start RingbaWebhookHandler
```

### **Application Crash**
```cmd
python main.py
```

### **Complete Restart**
```cmd
net stop RingbaWebhookHandler
taskkill /F /IM python.exe
net start RingbaWebhookHandler
```

## ✅ **Verification Checklist**

Before going live:
- [ ] Application starts without errors
- [ ] Health check endpoint responds
- [ ] Test webhook processes correctly
- [ ] Google Sheet gets updated
- [ ] Slack notification is sent
- [ ] Windows service starts automatically
- [ ] Firewall allows port 5000
- [ ] Ringba webhook URL is configured
- [ ] Logs are being written
- [ ] Backup strategy is in place

Your local Ringba webhook handler is now ready for 24/7 operation! 🚀



