# Getting Started - PSUR Generator Web Interface

## Your System is Ready!

A sleek, ultra-minimalist web UI has been created for your PSUR Generator.

## Quick Deploy (5 minutes)

### Railway (Recommended)

```bash
# One command deploy
./deploy.sh
```

That's it! The script will:
1. Install Railway CLI (if needed)
2. Login to Railway
3. Initialize project
4. Deploy application
5. Set API key
6. Open in browser

### Manual Deploy

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize
railway init

# 4. Deploy
railway up

# 5. Set API key
railway variables set ANTHROPIC_API_KEY=your_anthropic_key

# 6. Open
railway open
```

## Test Locally First (Optional)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
export ANTHROPIC_API_KEY=your_key
# Or create .env file:
echo "ANTHROPIC_API_KEY=your_key" > .env

# 3. Run
python3 app.py

# 4. Open browser
open http://localhost:5000
```

## What You'll See

### Landing Page
- Clean header with title
- 6 upload slots for input files
- 8 section cards (C, D, F, G, J, K, L, M)
- Generate button
- Status display
- Download manager

### Workflow
1. Upload your files (any order)
2. Select sections to generate
3. Click "Generate Reports"
4. Watch real-time progress
5. Download completed sections

## Files You Can Upload

1. **Sales Data** (.xlsx)
   - `inputs/33_sales.xlsx`
   
2. **Complaints Data** (.xlsx)
   - `inputs/33_complaints.xlsx`
   
3. **CER Document** (.pdf or .docx)
   - `inputs/cer.pdf`
   
4. **External Database** (.xlsx)
   - `inputs/external_databases.xlsx`
   
5. **Previous PSUR** (.docx)
   - `inputs/Previous_psur.docx`
   
6. **PSUR Template** (.docx)
   - `inputs/psur_template.docx`

## Sections Available

- **Section C**: Sales & Population
- **Section D**: Serious Incidents
- **Section F**: Complaint Types & Rates
- **Section G**: Complaints & Trends
- **Section J**: Literature Review
- **Section K**: Marketed vs Evaluated
- **Section L**: Clinical Data
- **Section M**: Risk-Benefit Assessment

## Features

### File Upload
- Drag and drop support
- Progress indicators
- Success/error feedback
- Multiple file types
- Size limit: 50MB per file

### Generation
- Select any combination of sections
- Background processing
- Real-time status updates
- Progress bar
- Error reporting

### Downloads
- Automatic file detection
- Section-based organization
- One-click downloads
- Multiple formats (DOCX, XLSX, JSON)

## Configuration

### Required
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Get your API key from: https://console.anthropic.com/

### Optional
```
PORT=5000  # Default port
```

## Documentation

### Quick Start
- `QUICK_DEPLOY.md` - 5-minute deployment
- `START.md` - Getting started guide
- `DEPLOYMENT_COMPLETE.md` - Summary

### Detailed Guides
- `DEPLOYMENT.md` - Full deployment guide
- `README_WEB.md` - Web app documentation
- `WEB_FEATURES.md` - Feature specifications
- `TEST_DEPLOYMENT.md` - Testing procedures

### Reference
- `FINAL_CHECKLIST.md` - Pre-launch checklist
- `DEPLOYMENT_SUMMARY.md` - What was built
- `WHATS_NEW.md` - What changed

## Troubleshooting

### Port Already in Use
```bash
PORT=8000 python3 app.py
```

### API Key Not Set
```bash
# Check if set
echo $ANTHROPIC_API_KEY

# Set temporarily
export ANTHROPIC_API_KEY=your_key

# Set permanently (create .env file)
echo "ANTHROPIC_API_KEY=your_key" > .env
```

### Module Not Found
```bash
pip install -r requirements.txt --force-reinstall
```

### Upload Fails
- Check file size (< 50MB)
- Verify file extension (.xlsx, .pdf, .docx)
- Clear browser cache
- Check network connection

### Generation Stalls
- Check API quota at console.anthropic.com
- Verify internet connection
- Review logs for errors
- Restart server

## Performance

### Expected Times
- Page load: < 2 seconds
- File upload: Instant
- Section C: ~30 seconds
- Section D: ~45 seconds
- Section F: ~60 seconds
- Section G: ~45 seconds
- Sections J,K,L,M: ~60-180 seconds

### Tips
- Upload files before generating
- Generate one section at a time for testing
- Use semantic cache (automatic)
- Ensure good internet connection

## Security

### Best Practices
- Never commit .env files
- Use environment variables
- Keep API keys secret
- Use HTTPS in production
- Regular security updates

### Implemented
- File type validation
- Size limits enforced
- Input sanitization
- Secure file handling
- API key protection

## Cost

### Hosting
- Railway Free Tier: $0/month (500 hours)
- Railway Hobby: $5/month
- Vercel Free: $0/month

### API Usage
- Claude Sonnet: ~$0.003 per 1K tokens
- Typical report: $1-5
- Monthly (20 reports): $20-100

### Total Estimate
- Development: $0-50/month
- Production: $50-150/month

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers

## Next Steps

### After Deployment

1. **Test Upload**
   - Upload sample files
   - Verify success indicators

2. **Test Generation**
   - Select Section C (fastest)
   - Monitor progress
   - Check output

3. **Share with Team**
   - Share deployment URL
   - Provide quick start guide
   - Train users

4. **Monitor**
   - Check logs regularly
   - Monitor API usage
   - Track performance

5. **Optimize**
   - Based on feedback
   - Performance tuning
   - Feature additions

## Support

### Self-Help
1. Check documentation
2. Review logs
3. Test locally
4. Check API quota

### Get Help
- Documentation: Check all .md files
- Logs: `railway logs` or check Vercel dashboard
- Health: Visit `/health` endpoint
- API: Visit `/api/outputs` to check status

## Success Indicators

You're ready when:
- ✓ Health endpoint returns 200
- ✓ UI loads without errors
- ✓ Files upload successfully
- ✓ Generation completes
- ✓ Downloads work
- ✓ Mobile displays correctly

## Commands Quick Reference

```bash
# Deploy
./deploy.sh

# Local run
python3 app.py

# Railway commands
railway login
railway init
railway up
railway logs
railway open
railway variables set KEY=value

# Vercel commands
vercel
vercel --prod
vercel logs

# Health check
curl http://localhost:5000/health
curl https://your-app.railway.app/health
```

## API Endpoints

```
GET  /                      Main UI
POST /api/upload            Upload files
POST /api/generate          Start generation
GET  /api/status/:id        Check progress
GET  /api/download/:section Download output
GET  /api/outputs           List all outputs
GET  /health                Health check
```

## File Structure

```
/workspace
├── app.py                  # Flask server
├── templates/
│   └── index.html         # Main UI
├── static/
│   ├── css/style.css      # Styles
│   └── js/app.js          # Logic
├── section_*/             # Generators
├── inputs/                # Input files
└── requirements.txt       # Dependencies
```

## You're Ready!

Everything is set up. Now:

1. **Deploy**:
   ```bash
   ./deploy.sh
   ```

2. **Or Test Locally**:
   ```bash
   python3 app.py
   ```

3. **Open Browser**:
   http://localhost:5000

4. **Start Generating**!

## Questions?

- Check `DEPLOYMENT.md` for detailed guide
- Read `README_WEB.md` for features
- Review `QUICK_DEPLOY.md` for fast deploy
- See `TEST_DEPLOYMENT.md` for testing

---

**Status**: ✓ Ready to Deploy

**Next Command**: `./deploy.sh`

---

Good luck! 🚀
