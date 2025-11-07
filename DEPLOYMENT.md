# PSUR Generator - Deployment Guide

Ultra minimalist web UI for PSUR generation system with AI-powered document processing.

## Quick Deploy

### Railway (Recommended)

1. Install Railway CLI:
```bash
npm i -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway init
railway up
```

3. Set environment variable:
```bash
railway variables set ANTHROPIC_API_KEY=your_api_key
```

4. Open your app:
```bash
railway open
```

### Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variable in Vercel dashboard:
- Go to Project Settings > Environment Variables
- Add `ANTHROPIC_API_KEY` with your API key

4. Redeploy:
```bash
vercel --prod
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```
ANTHROPIC_API_KEY=your_api_key_here
```

3. Run the app:
```bash
python app.py
```

4. Open browser:
```
http://localhost:5000
```

## Features

- Ultra minimalist UI design
- File upload for all input documents
- Select specific sections to generate
- Real-time generation status
- Download generated reports
- Mobile responsive

## Architecture

- **Backend**: Flask web framework
- **Frontend**: Vanilla JavaScript (no frameworks)
- **AI**: Claude AI via Anthropic API
- **Document Processing**: python-docx, pandas, openpyxl
- **PDF Parsing**: pdfplumber, pypdf

## API Endpoints

- `POST /api/upload` - Upload input files
- `POST /api/generate` - Start report generation
- `GET /api/status/<job_id>` - Check generation status
- `GET /api/download/<section>` - Download section output
- `GET /api/outputs` - List all generated files
- `GET /health` - Health check

## Environment Variables

- `ANTHROPIC_API_KEY` - Required for AI-powered generation
- `PORT` - Port to run on (default: 5000)

## Sections

- **Section C**: Sales & Population
- **Section D**: Serious Incidents
- **Section F**: Complaint Types & Rates
- **Section G**: Complaints & Trends
- **Section J**: Literature Review
- **Section K**: Marketed vs Evaluated
- **Section L**: Clinical Data
- **Section M**: Risk-Benefit Assessment

## Production Considerations

1. Set up proper CORS if needed
2. Configure SSL/TLS certificates
3. Set up file cleanup cron jobs
4. Monitor API usage and costs
5. Implement rate limiting
6. Add authentication if needed

## Support

For issues or questions, refer to the main README.md
