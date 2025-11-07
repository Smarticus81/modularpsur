# Test Your Deployment

## Pre-Deployment Testing

### 1. Local Test
```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY=your_key_here

# Run locally
python3 app.py
```

Open browser: http://localhost:5000

### 2. Test Checklist

#### UI Loads ✓
- [ ] Page loads without errors
- [ ] Header displays correctly
- [ ] Upload section visible
- [ ] Section cards render
- [ ] Generate button present
- [ ] Styles applied correctly

#### File Upload ✓
- [ ] Click file input opens dialog
- [ ] Select .xlsx file
- [ ] Upload status shows
- [ ] Success checkmark appears
- [ ] Try all 6 upload slots

#### Section Selection ✓
- [ ] Click section card
- [ ] Checkbox toggles
- [ ] Card highlights
- [ ] Multiple selection works
- [ ] All 8 sections functional

#### Generation ✓
- [ ] Select at least 1 section
- [ ] Click Generate button
- [ ] Button disables
- [ ] Status section appears
- [ ] Progress bar shows
- [ ] Real-time updates work

#### Download ✓
- [ ] After generation completes
- [ ] Outputs section appears
- [ ] Download buttons visible
- [ ] Click downloads file
- [ ] Correct file type

## Post-Deployment Testing

### 1. Health Check
```bash
curl https://your-app.railway.app/health
```

Expected:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-07T18:00:00"
}
```

### 2. Upload Test
```bash
curl -X POST \
  -F "sales=@inputs/33_sales.xlsx" \
  https://your-app.railway.app/api/upload
```

Expected:
```json
{
  "success": true,
  "uploaded": ["sales"]
}
```

### 3. Generate Test
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"sections": ["c"]}' \
  https://your-app.railway.app/api/generate
```

Expected:
```json
{
  "success": true,
  "job_id": "20251107_180000"
}
```

### 4. Status Test
```bash
curl https://your-app.railway.app/api/status/20251107_180000
```

Expected:
```json
{
  "status": "processing",
  "sections": ["c"],
  "completed": [],
  "errors": [],
  "started": "2025-11-07T18:00:00"
}
```

### 5. Outputs Test
```bash
curl https://your-app.railway.app/api/outputs
```

Expected:
```json
{
  "c": ["Section_C_output.docx"],
  "d": ["Section_D_output.docx"]
}
```

## Load Testing

### Simple Load Test
```bash
# Install ab (Apache Bench)
# macOS: brew install httpd
# Linux: apt-get install apache2-utils

# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 https://your-app.railway.app/
```

### Expected Performance
- Requests per second: > 100
- Time per request: < 100ms
- Failed requests: 0%

## Browser Testing

### Desktop
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### Mobile
- [ ] iOS Safari
- [ ] Android Chrome
- [ ] Responsive layout
- [ ] Touch targets

### Features to Test
- [ ] File upload works
- [ ] Sections selectable
- [ ] Button clickable
- [ ] Download works
- [ ] Scrolling smooth

## Error Testing

### 1. Invalid File Type
```bash
curl -X POST \
  -F "sales=@README.md" \
  https://your-app.railway.app/api/upload
```

Should reject non-.xlsx files

### 2. Large File
Create 100MB file and upload
Should respect 50MB limit

### 3. No API Key
Remove ANTHROPIC_API_KEY
Generation should fail gracefully

### 4. Invalid Section
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"sections": ["z"]}' \
  https://your-app.railway.app/api/generate
```

Should handle gracefully

### 5. Missing File
Try to generate without uploading
Should show appropriate error

## Performance Benchmarks

### Page Load
- Target: < 2 seconds
- Test: Chrome DevTools Network tab
- Measure: DOMContentLoaded

### Upload
- Target: Immediate feedback
- Test: Upload 1MB file
- Measure: Status update time

### Generation
- Section C: ~30 seconds
- Section D: ~45 seconds
- Section F: ~60 seconds
- Section G: ~45 seconds
- Sections J,K,L,M: ~60-180 seconds

### Download
- Target: < 1 second
- Test: Download generated file
- Measure: Time to download

## Monitoring Checklist

### Railway Dashboard
- [ ] Deployment succeeded
- [ ] Application running
- [ ] No error logs
- [ ] Environment variables set
- [ ] Custom domain (optional)

### Application Logs
```bash
railway logs
```

Look for:
- [ ] No Python errors
- [ ] Successful requests
- [ ] API calls working
- [ ] File operations OK

### Metrics
- [ ] CPU usage < 50%
- [ ] Memory usage < 512MB
- [ ] Response time < 1s
- [ ] Error rate < 1%

## Security Testing

### 1. Environment Variables
```bash
curl https://your-app.railway.app/
```

Check source - API key should NOT be visible

### 2. File Upload
Test uploading:
- Executable files (.exe)
- Script files (.sh)
- Large files (> 50MB)

All should be rejected or handled safely

### 3. API Endpoints
Test without authentication:
```bash
curl https://your-app.railway.app/api/status/fake_id
```

Should return 404, not crash

### 4. HTTPS
Check certificate:
```bash
curl -v https://your-app.railway.app/
```

Should show valid SSL certificate

## Production Readiness

### Checklist
- [ ] Health endpoint responds
- [ ] File upload tested
- [ ] Generation tested
- [ ] Download tested
- [ ] Errors handled gracefully
- [ ] Logs are clean
- [ ] Performance acceptable
- [ ] Security verified
- [ ] Mobile tested
- [ ] Documentation complete

### Go-Live Criteria
- All tests passing
- No critical errors
- Performance within targets
- Security measures active
- Monitoring configured
- Team trained

## Rollback Plan

If issues occur:

### Railway
```bash
# Rollback to previous deployment
railway rollback

# Or redeploy from git
railway up
```

### Vercel
```bash
# Rollback in dashboard
# Or redeploy
vercel --prod
```

### Quick Fix
```bash
# Pull latest working version
git checkout main
git pull

# Redeploy
railway up
```

## Support Contacts

### Railway Issues
- Dashboard: https://railway.app
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

### Vercel Issues
- Dashboard: https://vercel.com
- Docs: https://vercel.com/docs
- Support: support@vercel.com

### Application Issues
- Check logs first
- Review documentation
- Test locally
- Contact development team

## Success Indicators

Your deployment is successful when:
1. ✓ Health endpoint returns 200
2. ✓ UI loads without errors
3. ✓ Files upload successfully
4. ✓ Generation completes
5. ✓ Downloads work
6. ✓ No errors in logs
7. ✓ Performance is acceptable
8. ✓ Mobile works well

## Next Steps After Testing

1. **Share URL** with team
2. **Monitor** for 24 hours
3. **Gather feedback** from users
4. **Optimize** based on usage
5. **Document** any issues
6. **Plan** next features

## Celebration

If all tests pass:
- 🎉 Your PSUR Generator is live!
- 🚀 Share with your team
- 📈 Monitor usage
- 🔧 Iterate and improve

Deploy command: `./deploy.sh`
