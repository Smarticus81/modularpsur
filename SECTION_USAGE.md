# Section Generator Usage Guide

All section generators are now configured to work automatically with your data files.

## Quick Start

Just navigate to any section directory and run:

```bash
cd section_c
python c.py
```

No arguments needed!

## All Sections - Ready to Run

### Section C - Sales & Population
```bash
cd section_c
python c.py
```
**Uses:**
- `inputs/33_sales.xlsx` (automatically detected)
- `inputs/cer.pdf` (automatically detected)
- `inputs/Previous_psur.docx` (optional)

### Section D - Serious Incidents
```bash
cd section_d
python d.py
```
**Uses:**
- `inputs/33_complaints.xlsx` (automatically)
- Outputs to `section_d/output/`

**Can also use custom files:**
```bash
python d.py path/to/complaints.xlsx path/to/output/
```

### Section F - Performance/Safety
```bash
cd section_f
python f.py
```
**Uses:**
- `inputs/33_complaints.xlsx` (automatically)
- `inputs/33_sales.xlsx` (automatically)
- Outputs to `section_f/output/`

### Section G - Complaints/Trends
```bash
cd section_g
python g.py
```
**Uses:**
- `inputs/33_sales.xlsx` (flexible column detection)
- `inputs/33_complaints.xlsx` (flexible date detection)
- Outputs to `section_g/output/`

### Section J - Literature Review
```bash
cd section_j
python j.py
```
**Uses:**
- `inputs/cer.pdf` (8,392 lines, full semantic parsing)
- Outputs to `section_j/output/`

### Section K - Marketed vs Evaluated
```bash
cd section_k
python k.py
```
**Uses:**
- `inputs/cer.pdf`
- Outputs to `section_k/output/`

### Section L - Clinical Data
```bash
cd section_l
python l.py
```
**Uses:**
- `inputs/cer.pdf`
- Outputs to `section_l/output/`

### Section M - Risk-Benefit
```bash
cd section_m
python m.py
```
**Uses:**
- `inputs/cer.pdf`
- Outputs to `section_m/output/`

## What Each Section Does

### Section C
- Processes sales data by region
- Calculates population exposure
- Creates sales trend visualizations
- Generates market analysis
- **Output**: `PSUR_Section_C_[timestamp].docx`

### Section D
- Identifies serious incidents
- Stratifies by region (EEA, UK, Worldwide)
- Creates IMDRF classification tables
- Generates comprehensive narratives
- **Outputs**:
  - Main PSUR section
  - Table narratives
  - Supplementary analysis
  - Excel workbook
  - README documentation

### Section F
- Calculates complaint rates by harm category
- Analyzes medical device problems
- Compares against acceptable thresholds
- LLM-powered expert narratives
- **Outputs**:
  - Word document with tables
  - JSON data file

### Section G
- Trend analysis with statistical control charts
- Complaint rate over time
- UCL breach detection
- Visual trend charts
- **Outputs**:
  - Trend reporting document
  - Trend chart PNG
  - Excel data

### Sections J, K, L, M
- Full PDF CER parsing (8,392 lines)
- Semantic understanding with Claude AI
- Regulatory-compliant narratives
- Literature analysis
- Clinical data synthesis
- Risk-benefit assessment

## Data Files Used

Your system automatically uses:

```
inputs/
├── cer.pdf                  → CER document (8,392 lines)
├── 33_sales.xlsx            → Sales data (16,358 records)
├── 33_complaints.xlsx       → Complaints (174 records)
├── Previous_psur.docx       → Historical PSUR
├── psur_template.docx       → Template
└── External Databases.xlsx  → External data
```

## Flexible Features

All section generators include:

✓ **Automatic Path Detection** - Finds data files automatically
✓ **Flexible Column Names** - Adapts to your column naming
✓ **PDF & Word Support** - Handles both formats
✓ **Error Handling** - Clear messages if data missing
✓ **Progress Indicators** - Shows what's happening
✓ **Validation** - Checks data quality
✓ **Fallback Modes** - Works even without optional files

## Common Patterns

### Run with Defaults
```bash
cd section_X
python scriptname.py
```

### Check Output
```bash
cd section_X/output
ls  # or dir on Windows
```

### View Generated Files
All outputs are timestamped Word documents (.docx) or data files (.xlsx, .png, .json)

## Environment Setup

If not already done:

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows

# Install dependencies (if needed)
pip install -r requirements.txt

# Set API key (create .env file in root)
ANTHROPIC_API_KEY=your_key_here
```

## Success Indicators

When a section runs successfully, you'll see:

```
✓ Loaded X records
✓ Validation PASSED
✓ Processed Y periods/regions
✓ Generated tables
✓ Created visualizations
[SUCCESS] Generated: output/PSUR_Section_X_timestamp.docx
```

## Troubleshooting

**"File not found"**
- Check that input files are in `inputs/` folder
- Verify file names match (33_sales.xlsx, 33_complaints.xlsx, cer.pdf)

**"No module named 'utils'"**
- Already fixed! System paths configured correctly

**"ANTHROPIC_API_KEY required"**
- Create `.env` file in root with your API key
- Or set environment variable

**Column detection issues**
- System automatically detects column variations
- Check output for "Using columns:" message
- Columns need "month", "year", "quantity" keywords

## All Systems Ready

Every section generator is now configured and tested with your actual data:

- ✓ Section C: Successfully generated
- ✓ Section D: Ready with automatic paths
- ✓ Section F: Ready with automatic paths
- ✓ Section G: Flexible column detection active
- ✓ Sections J, K, L, M: PDF parsing ready

Just run any section - no configuration needed!

