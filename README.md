# PSUR Generator System

Modular PSUR (Periodic Safety Update Report) generation system with semantic CER parsing and AI-powered section generation.

## Quick Start

Double-click `start.bat` to launch the system environment.

## Structure

```
modularpsur/
├── inputs/                     # Source documents
│   ├── cer.docx               # Clinical Evaluation Report
│   ├── External Databases.xlsx
│   ├── inca_complaints.xlsx
│   ├── inca_Sales.xlsx
│   ├── Previous_psur.docx
│   └── psur_template.docx
├── section_c/                 # Sales & Population
├── section_d/                 # Serious Incidents
├── section_f/                 # Performance/Safety
├── section_g/                 # Complaints/Trends
├── section_j/                 # Literature Review
├── section_k/                 # Marketed vs Evaluated
├── section_l/                 # Clinical Data
├── section_m/                 # Risk-Benefit
├── utils/                     # Core semantic parsing system
│   ├── cer_data_model.py
│   ├── document_parser.py
│   ├── entity_extractors.py
│   ├── semantic_cache.py
│   └── semantic_document_parser.py
└── requirements.txt

```

## Generate Sections

```bash
cd section_c & python c.py
cd section_d & python psur_section_d_generator.py
cd section_f & python psur_section_f_generator.py
cd section_g & python g.py
cd section_j & python j.py
cd section_k & python k.py
cd section_l & python l.py
cd section_m & python m.py
```

## Features

- Semantic CER parsing with Claude AI
- PDF and Word document support
- Intelligent caching system
- Automated section generation
- Structured data extraction
- Cost-optimized API usage

## Requirements

All dependencies are in `requirements.txt` and installed in the virtual environment.

