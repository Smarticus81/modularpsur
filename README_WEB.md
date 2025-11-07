# PSUR Generator Web Application

Ultra minimalist web interface for automated PSUR (Periodic Safety Update Report) generation.

## Features

- **Sleek Minimalist UI**: Clean, modern interface with no clutter
- **File Upload**: Drag-and-drop support for all input documents
- **Smart Section Selection**: Choose exactly which sections to generate
- **Real-time Status**: Live progress tracking during generation
- **Instant Downloads**: Access all generated reports immediately
- **Mobile Responsive**: Works seamlessly on all devices

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the app
python3 app.py
```

Visit `http://localhost:5000`

### Deploy to Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Set API key
railway variables set ANTHROPIC_API_KEY=your_key

# Open app
railway open
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variable in dashboard
# Go to: Project Settings > Environment Variables
# Add: ANTHROPIC_API_KEY = your_key

# Deploy to production
vercel --prod
```

## Usage

1. **Upload Files**
   - Sales Data (Excel)
   - Complaints Data (Excel)
   - CER Document (PDF/Word)
   - External Database (Excel)
   - Previous PSUR (Word)
   - PSUR Template (Word)

2. **Select Sections**
   - Section C: Sales & Population
   - Section D: Serious Incidents
   - Section F: Complaint Types & Rates
   - Section G: Complaints & Trends
   - Section J: Literature Review
   - Section K: Marketed vs Evaluated
   - Section L: Clinical Data
   - Section M: Risk-Benefit Assessment

3. **Generate**
   - Click "Generate Reports"
   - Monitor real-time progress
   - Download completed sections

## API Reference

### Upload Files
```http
POST /api/upload
Content-Type: multipart/form-data

files: sales, complaints, cer, external_db, previous_psur, template
```

### Generate Sections
```http
POST /api/generate
Content-Type: application/json

{
  "sections": ["c", "d", "f", "g"]
}
```

### Check Status
```http
GET /api/status/{job_id}
```

### Download Section
```http
GET /api/download/{section}
```

### List Outputs
```http
GET /api/outputs
```

## Architecture

- **Frontend**: Vanilla JavaScript, CSS Grid, Flexbox
- **Backend**: Flask (Python)
- **AI Engine**: Claude AI (Anthropic)
- **Document Processing**: python-docx, pandas
- **PDF Parsing**: pdfplumber, pypdf
- **Deployment**: Railway, Vercel

## Design Philosophy

- **Minimalism**: Zero unnecessary elements
- **Speed**: Fast load times, optimized assets
- **Clarity**: Intuitive interface, clear feedback
- **Reliability**: Robust error handling
- **Accessibility**: WCAG compliant

## Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...  # Required
PORT=5000                     # Optional (default: 5000)
```

## File Structure

```
/workspace
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Main UI
├── static/
│   ├── css/
│   │   └── style.css     # Minimalist styles
│   └── js/
│       └── app.js        # Frontend logic
├── section_*/            # Section generators
├── inputs/               # Input files
└── requirements.txt      # Python dependencies
```

## Development

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run with auto-reload
export FLASK_ENV=development
python3 app.py

# Test API
curl http://localhost:5000/health
```

## Production

```bash
# Use gunicorn
gunicorn app:app --bind 0.0.0.0:5000 --workers 2 --timeout 300

# Or use the Procfile
web: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300 --workers 2
```

## Troubleshooting

**Files not uploading?**
- Check file size limits (50MB max)
- Verify file extensions (.xlsx, .pdf, .docx)

**Generation fails?**
- Verify ANTHROPIC_API_KEY is set
- Check input files are valid
- Review logs for errors

**Slow generation?**
- Normal for large documents
- CER parsing can take 2-3 minutes
- Use semantic caching for speed

## License

Proprietary - All rights reserved

## Support

For issues or questions, contact the development team.
