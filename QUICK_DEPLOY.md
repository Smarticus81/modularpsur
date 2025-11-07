# Quick Deployment Guide

## Railway (5 minutes)

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Deploy**
   ```bash
   cd /workspace
   railway login
   railway init
   railway up
   ```

3. **Set API Key**
   ```bash
   railway variables set ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

4. **Open App**
   ```bash
   railway open
   ```

That's it! Your app is live.

## Vercel (Alternative)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   cd /workspace
   vercel
   ```

3. **Configure**
   - Go to Vercel dashboard
   - Project Settings > Environment Variables
   - Add: `ANTHROPIC_API_KEY` = your key
   - Redeploy

4. **Done**
   ```bash
   vercel --prod
   ```

## Railway vs Vercel

**Railway** (Recommended)
- Better for long-running processes
- Native Python support
- Generous free tier
- Easy environment variables
- Perfect for this use case

**Vercel**
- Optimized for static/serverless
- 10-second function timeout (may be tight)
- Great for simple APIs
- Excellent CDN

## Environment Variables Needed

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Get your API key from: https://console.anthropic.com/

## Test Locally First

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "ANTHROPIC_API_KEY=your_key" > .env

# Run
python3 app.py

# Visit
# http://localhost:5000
```

## Deployment Checklist

- [ ] ANTHROPIC_API_KEY is set
- [ ] requirements.txt is complete
- [ ] railway.json or vercel.json exists
- [ ] Procfile exists (Railway)
- [ ] .gitignore includes .env
- [ ] Test upload works
- [ ] Test generation works
- [ ] Test download works

## Post-Deployment

1. Test all sections
2. Monitor API usage
3. Set up custom domain (optional)
4. Enable HTTPS (automatic)
5. Monitor logs

## Troubleshooting

**Deployment fails?**
- Check requirements.txt syntax
- Verify Python version (3.11+)
- Check logs: `railway logs` or Vercel dashboard

**App not loading?**
- Check PORT environment variable
- Verify build succeeded
- Check health endpoint: `/health`

**Generation fails?**
- Verify ANTHROPIC_API_KEY
- Check API quota
- Review application logs

## Cost Estimates

**Railway**
- Free tier: 500 hours/month
- Perfect for development/testing
- Upgrade as needed

**Vercel**
- Free tier: Good for prototypes
- Hobby plan: $20/month
- Pro plan: $150/month

**Anthropic API**
- Claude Sonnet: ~$0.003 per 1K tokens
- Typical PSUR: ~$1-5 per generation
- Budget ~$50-100/month for regular use

## Support

Questions? Check DEPLOYMENT.md or README_WEB.md
