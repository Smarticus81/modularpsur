# Railway Deployment Instructions

## Your Code is Ready!

Railway CLI is installed, but authentication requires browser access which isn't available in this remote environment.

## Deploy from Your Local Machine

### Quick Deploy (Recommended)

1. **Download your code** or access it on your local machine

2. **Navigate to project directory**
   ```bash
   cd /path/to/workspace
   ```

3. **Run the deploy script**
   ```bash
   ./deploy.sh
   ```

That's it! The script handles everything.

---

## Manual Deployment Steps

If you prefer manual control:

### 1. Install Railway CLI
```bash
npm i -g @railway/cli
```

### 2. Login
```bash
railway login
```
*Opens browser for authentication*

### 3. Initialize Project
```bash
cd /workspace
railway init
```
*Select "Create new project" and name it "psur-generator"*

### 4. Set Environment Variables
```bash
railway variables set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 5. Deploy
```bash
railway up
```

### 6. Open Your App
```bash
railway open
```

---

## Alternative: GitHub + Railway Dashboard

This is the easiest method if your code is on GitHub:

### 1. Push to GitHub
```bash
git add .
git commit -m "Add web interface"
git push origin main
```

### 2. Railway Dashboard
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository

### 3. Configure Environment
1. Go to project settings
2. Click "Variables"
3. Add: `ANTHROPIC_API_KEY` with your key

### 4. Deploy
Railway auto-deploys! Your app will be live at:
`https://psur-generator-production.railway.app`

---

## What's Configured

Your project includes:

✓ **railway.json**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300 --workers 2"
  }
}
```

✓ **Procfile**
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300 --workers 2
```

✓ **requirements.txt** - All Python dependencies

✓ **runtime.txt** - Python 3.11.7

---

## Environment Variables Needed

Only one required:

```
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

Get your key from: https://console.anthropic.com/

---

## After Deployment

### Test Health Endpoint
```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-07T..."
}
```

### Open Web Interface
Visit: `https://your-app.railway.app`

You should see:
- Upload section
- Section selection cards
- Generate button
- Clean, minimalist interface

---

## Deployment Checklist

- [ ] Code on local machine or GitHub
- [ ] Railway CLI installed (`npm i -g @railway/cli`)
- [ ] Logged in to Railway (`railway login`)
- [ ] Project initialized (`railway init`)
- [ ] Environment variable set
- [ ] Deployed (`railway up`)
- [ ] Health check passes
- [ ] Web UI loads

---

## Troubleshooting

### "Not logged in"
```bash
railway login
```

### "No project linked"
```bash
railway init
```

### "Environment variable missing"
```bash
railway variables set ANTHROPIC_API_KEY=your_key
```

### "Build failed"
Check logs:
```bash
railway logs
```

### "Application error"
1. Check environment variables in Railway dashboard
2. View logs for specific error
3. Verify all files are present

---

## Cost

- **Starter (Free)**: 500 hours/month, 512MB RAM
- **Hobby ($5/month)**: Unlimited, better resources
- **Pro ($20/month)**: Team features, more resources

Plus API costs: ~$50-100/month for typical usage

---

## Next Steps

1. **Choose deployment method** (CLI or GitHub)
2. **Set up on local machine**
3. **Deploy**
4. **Test**
5. **Share with team**

---

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Project Docs: See DEPLOYMENT.md

---

## Your Deployment URL

After deployment, Railway provides a URL like:
```
https://psur-generator-production.railway.app
```

Share this with your team!

---

**Ready to deploy?**

On your local machine, run:
```bash
./deploy.sh
```

Or follow the GitHub + Railway Dashboard method above.
