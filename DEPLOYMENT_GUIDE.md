# Deployment Guide - 24/7 Ringba Webhook Handler

This guide provides step-by-step instructions for deploying your Ringba webhook handler to run continuously 24/7.

## Quick Start - Railway (Recommended)

Railway is the easiest platform for this use case with excellent uptime and simple deployment.

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/yourusername/ringba-webhook-handler.git
   git push -u origin main
   ```

### Step 2: Deploy to Railway

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Get Your App URL**:
   ```bash
   railway domain
   ```
   Copy the URL (e.g., `https://your-app.railway.app`)

### Step 3: Configure Environment Variables

Set all required environment variables in Railway:

```bash
# Ringba Configuration
railway variables set RINGBA_CAMPAIGN_NAME="Your Actual Campaign Name"
railway variables set RINGBA_TARGET_NAME="Your Actual Target Name"

# Google Sheets Configuration
railway variables set GOOGLE_SHEET_ID="your_actual_sheet_id"
railway variables set GOOGLE_SHEET_TAB="Sheet1"

# Slack Configuration
railway variables set SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Production Settings
railway variables set FLASK_ENV="production"
railway variables set FLASK_DEBUG="False"
```

### Step 4: Upload Google Credentials

1. **Upload credentials.json**:
   ```bash
   railway variables set GOOGLE_CREDS_FILE="credentials.json"
   ```
   
2. **In Railway Dashboard**:
   - Go to your project
   - Click "Variables" tab
   - Add a new variable: `GOOGLE_CREDS_JSON`
   - Paste the entire contents of your `credentials.json` file

3. **Update google_sheets.py** to use environment variable:
   ```python
   import json
   import os
   
   # In the append_row_to_sheet function, replace:
   # creds = Credentials.from_service_account_file(GOOGLE_CREDS_FILE, scopes=SCOPES)
   # With:
   creds_json = os.getenv('GOOGLE_CREDS_JSON')
   creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
   ```

## Alternative Deployment Options

### Option B: Render

1. **Connect GitHub Repository**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" > "Web Service"
   - Connect your GitHub repository

2. **Configure Service**:
   - **Name**: `ringba-webhook-handler`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`

3. **Set Environment Variables**:
   - Add all variables from the Railway section above
   - For Google credentials, use the same JSON approach

### Option C: Heroku

1. **Install Heroku CLI**:
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy**:
   ```bash
   heroku create your-ringba-webhook-app
   git push heroku main
   ```

3. **Set Config Vars**:
   ```bash
   heroku config:set RINGBA_CAMPAIGN_NAME="Your Campaign Name"
   heroku config:set RINGBA_TARGET_NAME="Your Target Name"
   heroku config:set GOOGLE_SHEET_ID="your_sheet_id"
   heroku config:set SLACK_WEBHOOK_URL="your_webhook_url"
   heroku config:set FLASK_ENV="production"
   ```

## Testing Your Deployment

### 1. Health Check
```bash
curl https://your-app.railway.app/
```
Should return:
```json
{
  "status": "healthy",
  "service": "Ringba Webhook Handler",
  "filters": {
    "campaign_name": "Your Campaign Name",
    "target_name": "Your Target Name"
  }
}
```

### 2. Test Webhook
```bash
curl -X POST https://your-app.railway.app/ringba-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "campaignName": "Your Campaign Name",
    "targetName": "Your Target Name",
    "callerId": "TEST_123",
    "timestamp": "2024-01-01T12:00:00Z"
  }'
```

### 3. Check Logs
```bash
# Railway
railway logs

# Render
# Check dashboard logs

# Heroku
heroku logs --tail
```

## Ringba Configuration

### 1. Set Up Webhook in Ringba

1. **Log into Ringba Dashboard**
2. **Navigate to Campaign Settings**
3. **Find Webhook Configuration**
4. **Add Webhook URL**: `https://your-app.railway.app/ringba-webhook`
5. **Set Method**: `POST`
6. **Set Content Type**: `application/json`

### 2. Test Integration

1. **Make a test call** through your Ringba campaign
2. **Check your Google Sheet** for new entries
3. **Verify Slack notifications** are received
4. **Check application logs** for any errors

## Monitoring and Maintenance

### 1. Set Up Monitoring

#### Railway Monitoring
- **Built-in**: Railway provides uptime monitoring
- **Custom**: Add health check endpoints

#### External Monitoring (Optional)
- **UptimeRobot**: Free uptime monitoring
- **Pingdom**: Advanced monitoring
- **StatusCake**: Comprehensive monitoring

### 2. Log Monitoring

#### Set Up Log Alerts
```bash
# Railway - Monitor for errors
railway logs | grep -i error

# Set up log forwarding to external service
```

#### Common Issues to Monitor
- Google Sheets API errors
- Slack webhook failures
- Ringba webhook timeouts
- Application crashes

### 3. Regular Maintenance

#### Weekly Checks
1. **Verify Google Sheet permissions**
2. **Check Slack webhook is still active**
3. **Review application logs**
4. **Test webhook endpoint**

#### Monthly Tasks
1. **Update dependencies** (if needed)
2. **Review Ringba webhook configuration**
3. **Check service account credentials**
4. **Verify environment variables**

### 4. Backup Strategy

#### Code Backup
- **GitHub**: All code is version controlled
- **Multiple deployments**: Consider staging environment

#### Data Backup
- **Google Sheets**: Automatic Google backup
- **Logs**: Consider external log storage

## Troubleshooting Common Issues

### 1. App Not Responding

```bash
# Check if app is running
curl https://your-app.railway.app/

# Check logs
railway logs

# Restart if needed
railway service restart
```

### 2. Google Sheets Errors

```bash
# Check credentials
railway variables get GOOGLE_CREDS_JSON

# Verify sheet permissions
# Check if service account has access
```

### 3. Slack Notifications Not Working

```bash
# Test webhook URL
curl -X POST YOUR_SLACK_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{"text": "Test message"}'
```

### 4. Ringba Webhook Issues

```bash
# Check webhook endpoint
curl -X POST https://your-app.railway.app/ringba-webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## Scaling Considerations

### 1. Traffic Increase
- **Railway**: Automatically scales
- **Render**: Upgrade to paid plan
- **Heroku**: Add dynos as needed

### 2. Cost Optimization
- **Railway**: Free tier for low traffic
- **Render**: Free tier available
- **Heroku**: Free tier discontinued

### 3. Performance Monitoring
```bash
# Monitor response times
curl -w "@curl-format.txt" -o /dev/null -s https://your-app.railway.app/
```

## Security Best Practices

### 1. Environment Variables
- **Never commit secrets** to Git
- **Use platform secrets** management
- **Rotate credentials** regularly

### 2. Webhook Security
- **Validate incoming data**
- **Add rate limiting** (if needed)
- **Monitor for abuse**

### 3. Access Control
- **Limit Google Sheet access**
- **Use service accounts**
- **Regular permission reviews**

## Emergency Procedures

### 1. App Down
```bash
# Immediate restart
railway service restart

# Check logs
railway logs

# Verify health
curl https://your-app.railway.app/
```

### 2. Data Loss
- **Google Sheets**: Check version history
- **Logs**: Check platform logs
- **Backup**: Restore from Git

### 3. Credential Issues
- **Regenerate Google credentials**
- **Update Slack webhook**
- **Redeploy with new credentials**

## Support and Resources

### Platform Support
- **Railway**: [Discord Community](https://discord.gg/railway)
- **Render**: [Documentation](https://render.com/docs)
- **Heroku**: [Support Center](https://help.heroku.com/)

### Application Support
- **Check logs** first
- **Test individual components**
- **Verify configuration**
- **Use test scripts**

## Cost Estimation

### Railway
- **Free Tier**: $0/month (limited usage)
- **Pro Plan**: $20/month (unlimited)

### Render
- **Free Tier**: $0/month (limited)
- **Paid Plans**: $7-25/month

### Heroku
- **Basic Dyno**: $7/month
- **Standard Dyno**: $25/month

## Final Checklist

Before going live:

- [ ] All environment variables set
- [ ] Google credentials uploaded
- [ ] Slack webhook configured
- [ ] Ringba webhook URL set
- [ ] Health check endpoint working
- [ ] Test webhook successful
- [ ] Google Sheet accessible
- [ ] Slack notifications working
- [ ] Logs being generated
- [ ] Monitoring set up
- [ ] Backup strategy in place

Your Ringba webhook handler is now ready for 24/7 operation! 🚀



