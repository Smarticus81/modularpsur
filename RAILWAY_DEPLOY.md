# Deploy to Railway - Quick Guide

Your app is fully configured and ready to deploy on Railway!

## ✅ Already Configured

- `railway.json` - Build and deploy settings
- `Procfile` - Web server configuration
- `requirements.txt` - All dependencies
- `runtime.txt` - Python 3.11.7
- App cleared of sample data

## 🚀 Deploy from GitHub (Easiest Method)

### Step 1: Push Your Code

Your changes are already pushed to: `claude/clear-input-fix-deployment-011CUy377vn9kmntVxqT2acU`

Merge this to your main branch or deploy directly from this branch.

### Step 2: Railway Dashboard

1. Go to **https://railway.app**
2. Click **"Login"** → Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose **`Smarticus81/modularpsur`**
6. Select the branch you want to deploy

### Step 3: Set Environment Variable

Railway will start deploying immediately. While it builds:

1. Click on your new project
2. Click **"Variables"** tab
3. Click **"Add Variable"**
4. Add:
   - **Name**: `ANTHROPIC_API_KEY`
   - **Value**: Your API key from https://console.anthropic.com/

5. Click **"Add"**

Railway will automatically redeploy with the API key.

### Step 4: Get Your URL

1. Go to **"Settings"** tab
2. Click **"Generate Domain"** under "Networking"
3. Your app will be live at: `https://your-app-name.railway.app`

### Step 5: Test

Visit your Railway URL and test:
- Homepage: `https://your-app-name.railway.app/`
- Health check: `https://your-app-name.railway.app/health`

## 📊 What Railway Will Do

1. **Detect** Python app automatically
2. **Install** dependencies from requirements.txt
3. **Build** using Python 3.11.7
4. **Start** with: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300 --workers 2`
5. **Deploy** and provide a public URL

## ⚙️ Railway Configuration Details

From `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300 --workers 2",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## 💰 Pricing

- **Trial**: $5 free credit (no credit card)
- **Hobby**: $5/month for 500 hours
- **Pro**: $20/month unlimited

Plus Anthropic API costs (pay-as-you-go)

## 🔧 After Deployment

### View Logs
In Railway dashboard → "Deployments" → Click latest deployment → View logs

### Update App
Just push to your GitHub branch - Railway auto-deploys!

### Monitor
Railway dashboard shows:
- Deployment status
- Resource usage
- Logs
- Metrics

## 🆘 Troubleshooting

### Build Fails
- Check logs in Railway dashboard
- Verify all files are pushed to GitHub
- Ensure requirements.txt is valid

### App Crashes
- Verify `ANTHROPIC_API_KEY` is set correctly
- Check logs for error messages
- Ensure PORT is not hardcoded (Railway sets it)

### 502 Bad Gateway
- App is still starting (wait 30-60 seconds)
- Check logs for startup errors

## 📝 Next Steps

1. Deploy to Railway using steps above
2. Test all endpoints
3. Share URL with your team
4. Monitor usage in Railway dashboard

## 🔗 Useful Links

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app
- Anthropic Console: https://console.anthropic.com/

---

**Ready to deploy?** Follow Step 1 above and let's get your app live!
