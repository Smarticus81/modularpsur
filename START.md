# Getting Started

## Choose Your Path

### 1. Web Interface (Recommended)

**Fastest way to generate reports**

```bash
python3 app.py
```

Open: http://localhost:5000

### 2. Command Line

**For automation and scripts**

```bash
cd section_c && python3 c.py
cd section_d && python3 d.py
cd section_f && python3 f.py
# etc...
```

### 3. Deploy to Cloud

**For team access**

```bash
./deploy.sh
```

Or manually:
```bash
railway login
railway init
railway up
```

## First Time Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set API Key**
   ```bash
   cp .env.example .env
   # Edit .env with your Anthropic API key
   ```

3. **Verify Setup**
   ```bash
   python3 -c "import anthropic; print('✓ OK')"
   ```

## Quick Test

### Test Web Interface
```bash
# Start server
python3 app.py

# In another terminal
curl http://localhost:5000/health
```

Expected: `{"status": "healthy", ...}`

### Test Section Generation
```bash
cd section_c
python3 c.py
```

Check: `section_c/output/` for generated files

## File Locations

### Input Files
```
inputs/
├── 33_sales.xlsx           # Sales data
├── 33_complaints.xlsx      # Complaints
├── cer.pdf                 # CER document
├── external_databases.xlsx # External data
├── Previous_psur.docx      # Previous PSUR
└── psur_template.docx      # Template
```

### Output Files
```
section_*/output/
├── *.docx                  # Word documents
├── *.xlsx                  # Excel workbooks
└── *.json                  # Data files
```

## Common Tasks

### Generate All Sections
```bash
for section in c d f g j k l m; do
    cd section_$section && python3 $section.py && cd ..
done
```

### Clear Outputs
```bash
find . -path "*/output/*" -type f -delete
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

## Web UI Features

### Upload Files
- Drag and drop
- Click to browse
- Multiple files
- Progress tracking

### Select Sections
- Click cards
- Multiple selection
- Visual feedback
- Flexible generation

### Monitor Progress
- Real-time updates
- Progress bar
- Status tracking
- Error reporting

### Download Results
- One-click download
- Multiple formats
- Organized by section
- Instant access

## Keyboard Shortcuts

- `Tab` - Navigate
- `Enter` - Activate button
- `Space` - Toggle checkbox
- `Esc` - Clear selection

## Tips

1. **Upload Order**: Any order works
2. **Partial Generation**: Select only needed sections
3. **Reuse Outputs**: Download and save locally
4. **Monitor Logs**: Check for errors
5. **Update Regularly**: Keep dependencies current

## Troubleshooting

### Port Already in Use
```bash
# Change port
PORT=8000 python3 app.py
```

### API Key Issues
```bash
# Verify key is set
echo $ANTHROPIC_API_KEY

# Or check .env file
cat .env
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### File Upload Fails
- Check file size (< 50MB)
- Verify file extension (.xlsx, .pdf, .docx)
- Clear browser cache

### Generation Stalls
- Check API quota
- Verify internet connection
- Review logs for errors
- Restart server

## Performance Tips

### Speed Up Generation
1. Use semantic cache (automatic)
2. Process one section at a time
3. Ensure good internet connection
4. Use latest Python version

### Reduce API Costs
1. Generate only needed sections
2. Reuse previous outputs
3. Cache CER parsing
4. Batch similar tasks

### Optimize Memory
1. Close unused apps
2. Use 64-bit Python
3. Increase swap if needed
4. Process large files in chunks

## Best Practices

### File Management
- Keep inputs organized
- Archive old outputs
- Use version control
- Backup regularly

### Quality Assurance
- Review generated content
- Validate regulatory compliance
- Cross-check data
- Test before deploying

### Security
- Protect API keys
- Use HTTPS in production
- Validate file uploads
- Audit access logs

### Team Collaboration
- Share deployment URL
- Document custom settings
- Version control configs
- Communicate changes

## Next Steps

### After First Success
1. Explore all sections
2. Customize settings
3. Deploy to cloud
4. Share with team
5. Gather feedback

### Continuous Improvement
1. Monitor usage
2. Optimize performance
3. Update documentation
4. Add features
5. Scale as needed

## Resources

### Documentation
- `README.md` - Overview
- `DEPLOYMENT.md` - Deploy guide
- `README_WEB.md` - Web details
- `WEB_FEATURES.md` - Features

### Quick References
- `QUICK_DEPLOY.md` - 5-min deploy
- `TEST_DEPLOYMENT.md` - Testing
- `DEPLOYMENT_SUMMARY.md` - Summary

### Help
- Check documentation
- Review logs
- Test locally
- Contact support

## Support

Questions? Check the docs or reach out to the team.

Ready? Start here:
```bash
python3 app.py
```

Then open: http://localhost:5000
