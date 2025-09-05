# Quick Start Guide - Ringba Webhook Handler

## 🚀 Complete Setup in 5 Steps

### Step 1: Prepare Credentials

#### Google Sheets Setup
1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project → Enable Google Sheets API
   - Create Service Account → Download `credentials.json`

2. **Create Google Sheet**:
   - Create new Google Sheet
   - Share with service account email
   - Copy Sheet ID from URL

#### Slack Setup
1. **Create Slack App**:
   - Go to [Slack API](https://api.slack.com/apps)
   - Create New App → Enable Incoming Webhooks
   - Add webhook to workspace → Copy URL

### Step 2: Configure Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run setup script
python setup.py

# Edit .env file with your values
nano .env
```

### Step 3: Test Locally

```bash
# Start the application
python main.py

# In another terminal, test webhooks
python test_webhook.py
```

### Step 4: Deploy (Choose One)

#### Option A: Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up

# Set environment variables
railway variables set RINGBA_CAMPAIGN_NAME="Your Campaign"
railway variables set RINGBA_TARGET_NAME="Your Target"
railway variables set GOOGLE_SHEET_ID="your_sheet_id"
railway variables set SLACK_WEBHOOK_URL="your_webhook_url"

# Upload Google credentials
# In Railway dashboard: Variables → GOOGLE_CREDS_JSON → Paste credentials.json content
```

#### Option B: Render
1. Connect GitHub repository
2. Create Web Service
3. Set environment variables in dashboard
4. Deploy

#### Option C: Heroku
```bash
heroku create your-app-name
git push heroku main
heroku config:set RINGBA_CAMPAIGN_NAME="Your Campaign"
# ... set other variables
```

### Step 5: Configure Ringba

1. **In Ringba Dashboard**:
   - Go to Campaign Settings
   - Find Webhook Configuration
   - Add URL: `https://your-app.railway.app/ringba-webhook`
   - Set Method: `POST`

2. **Test Integration**:
   - Make test call through Ringba
   - Check Google Sheet for new entry
   - Verify Slack notification

## 📋 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `RINGBA_CAMPAIGN_NAME` | Campaign to filter | "Summer Sale 2024" |
| `RINGBA_TARGET_NAME` | Target to filter | "California Leads" |
| `GOOGLE_SHEET_ID` | Sheet ID from URL | "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms" |
| `SLACK_WEBHOOK_URL` | Slack webhook URL | "https://hooks.slack.com/services/..." |
| `GOOGLE_CREDS_JSON` | Google credentials (deployment) | `{"type": "service_account", ...}` |

## 🧪 Testing

### Health Check
```bash
curl https://your-app.railway.app/
```

### Test Webhook
```bash
curl -X POST https://your-app.railway.app/ringba-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "campaignName": "Your Campaign Name",
    "targetName": "Your Target Name",
    "callerId": "TEST_123"
  }'
```

## 📊 Google Sheet Structure

The app automatically creates this structure:

| Time of call | CallerID | Agent Name | Status | Notes |
|-------------|----------|------------|--------|-------|
| 2024-01-01 12:00:00 UTC | +1234567890 | | | |

## 🔧 Troubleshooting

### Common Issues

1. **Google Sheets Error**:
   - Check service account permissions
   - Verify credentials.json is valid

2. **Slack Not Working**:
   - Test webhook URL manually
   - Check if webhook is still active

3. **Webhook Not Receiving**:
   - Verify URL is accessible
   - Check Ringba webhook configuration

### Debug Mode
```bash
# Set in environment variables
FLASK_DEBUG=True
```

## 📈 Monitoring

### Health Monitoring
- **Railway**: Built-in monitoring
- **External**: UptimeRobot (free)

### Log Monitoring
```bash
# Railway
railway logs

# Check for errors
railway logs | grep -i error
```

## 💰 Cost Estimation

| Platform | Free Tier | Paid Plans |
|----------|-----------|------------|
| Railway | $0/month (limited) | $20/month (unlimited) |
| Render | $0/month (limited) | $7-25/month |
| Heroku | Discontinued | $7-25/month |

## 🚨 Emergency Procedures

### App Down
```bash
railway service restart
curl https://your-app.railway.app/
```

### Credential Issues
1. Regenerate Google credentials
2. Update environment variables
3. Redeploy application

## 📞 Support

- **Documentation**: README.md
- **Deployment Guide**: DEPLOYMENT_GUIDE.md
- **Test Script**: test_webhook.py
- **Setup Script**: setup.py

## ✅ Final Checklist

Before going live:
- [ ] All environment variables set
- [ ] Google credentials uploaded
- [ ] Slack webhook working
- [ ] Ringba webhook configured
- [ ] Health check passing
- [ ] Test webhook successful
- [ ] Google Sheet accessible
- [ ] Slack notifications working

**Your Ringba webhook handler is now ready for 24/7 operation! 🎉**



