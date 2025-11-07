# Deploy to Railway - Manual Steps

Since Railway CLI requires authentication that needs to be done on your local machine, here's how to deploy:

## Option 1: Deploy from Your Local Machine

### Step 1: Clone/Download Your Code
```bash
# If using git, push your changes first, then on your local machine:
git clone <your-repo-url>
cd <your-repo-name>

# Or download the files directly
```

### Step 2: Install Railway CLI
```bash
npm i -g @railway/cli
```

### Step 3: Login to Railway
```bash
railway login
```
This will open your browser for authentication.

### Step 4: Initialize Project
```bash
railway init
```
Choose "Create a new project" and give it a name like "psur-generator"

### Step 5: Set Environment Variable
```bash
railway variables set ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Step 6: Deploy
```bash
railway up
```

### Step 7: Open Your App
```bash
railway open
```

Your PSUR Generator will be live!

---

## Option 2: Deploy via Railway Dashboard (Easiest)

### Step 1: Push to GitHub
```bash
# Make sure your code is in a GitHub repository
git add .
git commit -m "Add web interface"
git push origin main
```

### Step 2: Go to Railway Dashboard
1. Visit https://railway.app
2. Sign up or log in
3. Click "New Project"
4. Choose "Deploy from GitHub repo"
5. Select your repository
6. Railway will auto-detect the configuration

### Step 3: Set Environment Variable
1. Go to your project in Railway
2. Click on "Variables"
3. Add: `ANTHROPIC_API_KEY` = `your_key_here`

### Step 4: Deploy
Railway will automatically deploy! 

Visit your app at the provided URL (usually `https://your-app.railway.app`)

---

## Option 3: Deploy via Railway CLI (One Command)

On your local machine where you can authenticate:

```bash
# All in one script
./deploy.sh
```

This will:
1. Install Railway CLI (if needed)
2. Login to Railway
3. Initialize project
4. Deploy application
5. Set API key
6. Open in browser

---

## Option 4: Manual Railway Setup

### 1. Create Railway Account
- Go to https://railway.app
- Sign up with GitHub

### 2. Create New Project
- Click "New Project"
- Choose "Empty Project"

### 3. Connect GitHub (Recommended)
- Click "Deploy from GitHub"
- Authorize Railway
- Select your repository

### 4. Configure
Railway will detect:
- `railway.json` - Deployment config
- `Procfile` - Start command
- `requirements.txt` - Dependencies

### 5. Add Environment Variable
Settings → Variables → Add Variable:
```
ANTHROPIC_API_KEY = sk-ant-your-key-here
```

### 6. Deploy
Railway deploys automatically on push!

---

## Verify Deployment

### Check Health
```bash
curl https://your-app.railway.app/health
```

Expected:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-07T..."
}
```

### Open in Browser
Visit: `https://your-app.railway.app`

You should see the PSUR Generator web interface!

---

## Your Project is Configured For:

✓ **Railway deployment** (`railway.json`)
✓ **Vercel deployment** (`vercel.json`)
✓ **Process configuration** (`Procfile`)
✓ **Python 3.11** (`runtime.txt`)
✓ **All dependencies** (`requirements.txt`)

---

## Files Ready for Deployment:

```
✓ app.py                    # Flask server
✓ templates/index.html      # Web UI
✓ static/css/style.css      # Styles
✓ static/js/app.js          # Frontend
✓ railway.json              # Railway config
✓ Procfile                  # Start command
✓ requirements.txt          # Dependencies
✓ runtime.txt               # Python version
```

---

## Need Help?

### Railway Support
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Status: https://railway.app/status

### Common Issues

**"Module not found"**
- Check `requirements.txt` is complete
- Railway will install automatically

**"Application error"**
- Check environment variables set
- View logs in Railway dashboard

**"Port binding error"**
- App uses `$PORT` from environment (configured)

---

## Quick Test After Deploy

1. **Health Check**
   ```bash
   curl https://your-app.railway.app/health
   ```

2. **Open UI**
   Visit: `https://your-app.railway.app`

3. **Test Upload**
   - Upload a file
   - Check for success message

4. **Generate Section**
   - Select Section C
   - Click Generate
   - Monitor progress

---

## Cost

- **Free Tier**: 500 hours/month ($0)
- **Hobby Tier**: $5/month (unlimited)
- **API Usage**: ~$50-100/month (Anthropic)

Total: $5-105/month

---

## Next Steps After Deploy

1. Share URL with team
2. Test all features
3. Monitor logs
4. Set up custom domain (optional)
5. Configure alerts

---

## Deploy Status

Your code is **READY TO DEPLOY**

Choose your method above and follow the steps!

---

## Alternative: Vercel

If you prefer Vercel:

```bash
# On your local machine
npm i -g vercel
vercel
# Set ANTHROPIC_API_KEY in dashboard
vercel --prod
```

---

**Ready to deploy from your local machine?**

Run: `./deploy.sh`

Or follow Option 2 above for GitHub + Railway dashboard deployment.
