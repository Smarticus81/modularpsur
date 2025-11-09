import os
import sys
import json
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import threading
from datetime import datetime

# Get the base directory (works both locally and on Vercel)
BASE_DIR = Path(__file__).parent.absolute()

app = Flask(__name__,
            static_folder=str(BASE_DIR / 'static'),
            template_folder=str(BASE_DIR / 'templates'))
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

ALLOWED_EXTENSIONS = {'xlsx', 'pdf', 'docx'}

generation_status = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_files():
    uploaded = {}
    
    for file_key in ['sales', 'complaints', 'cer', 'external_db', 'previous_psur', 'template']:
        if file_key in request.files:
            file = request.files[file_key]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded[file_key] = filepath
    
    return jsonify({'success': True, 'uploaded': list(uploaded.keys())})

@app.route('/api/generate', methods=['POST'])
def generate_sections():
    data = request.get_json()
    sections = data.get('sections', [])
    job_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    generation_status[job_id] = {
        'status': 'processing',
        'sections': sections,
        'completed': [],
        'errors': [],
        'started': datetime.now().isoformat()
    }
    
    thread = threading.Thread(target=run_generation, args=(job_id, sections))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'job_id': job_id})

def run_generation(job_id, sections):
    try:
        results = {}
        
        for section in sections:
            try:
                generation_status[job_id]['status'] = f'generating_{section}'
                
                if section == 'c':
                    from section_c.c import main as gen_c
                    gen_c()
                elif section == 'd':
                    from section_d.d import main as gen_d
                    gen_d()
                elif section == 'f':
                    from section_f.f import main as gen_f
                    gen_f()
                elif section == 'g':
                    from section_g.g import main as gen_g
                    gen_g()
                elif section == 'j':
                    from section_j.j import main as gen_j
                    gen_j()
                elif section == 'k':
                    from section_k.k import main as gen_k
                    gen_k()
                elif section == 'l':
                    from section_l.l import main as gen_l
                    gen_l()
                elif section == 'm':
                    from section_m.m import main as gen_m
                    gen_m()
                
                generation_status[job_id]['completed'].append(section)
                results[section] = 'success'
                
            except Exception as e:
                generation_status[job_id]['errors'].append({
                    'section': section,
                    'error': str(e)
                })
                results[section] = f'error: {str(e)}'
        
        generation_status[job_id]['status'] = 'completed'
        generation_status[job_id]['results'] = results
        generation_status[job_id]['finished'] = datetime.now().isoformat()
        
    except Exception as e:
        generation_status[job_id]['status'] = 'failed'
        generation_status[job_id]['error'] = str(e)

@app.route('/api/status/<job_id>')
def get_status(job_id):
    if job_id in generation_status:
        return jsonify(generation_status[job_id])
    return jsonify({'error': 'Job not found'}), 404

@app.route('/api/download/<section>')
def download_section(section):
    section_outputs = {
        'c': 'section_c/output',
        'd': 'section_d/output',
        'f': 'section_f/output',
        'g': 'section_g/output',
        'j': 'section_j/output',
        'k': 'section_k/output',
        'l': 'section_l/output',
        'm': 'section_m/output'
    }
    
    if section not in section_outputs:
        return jsonify({'error': 'Invalid section'}), 404
    
    output_dir = Path(section_outputs[section])
    if not output_dir.exists():
        return jsonify({'error': 'Output not found'}), 404
    
    files = list(output_dir.glob('*.docx')) + list(output_dir.glob('*.xlsx')) + list(output_dir.glob('*.json'))
    
    if not files:
        return jsonify({'error': 'No output files found'}), 404
    
    return send_file(files[0], as_attachment=True)

@app.route('/api/outputs')
def list_outputs():
    outputs = {}
    sections = ['c', 'd', 'f', 'g', 'j', 'k', 'l', 'm']
    
    for section in sections:
        output_dir = Path(f'section_{section}/output')
        if output_dir.exists():
            files = []
            for ext in ['*.docx', '*.xlsx', '*.json', '*.pdf']:
                files.extend([f.name for f in output_dir.glob(ext)])
            if files:
                outputs[section] = files
    
    return jsonify(outputs)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*60)
    print("  PSUR Generator - Web Interface")
    print("  EU MDR 2017/745 Compliant")
    print("="*60)
    print(f"\n  Server: http://0.0.0.0:{port}")
    print(f"  Local:  http://localhost:{port}")
    print(f"\n  Health: http://localhost:{port}/health")
    print(f"  API:    http://localhost:{port}/api/outputs")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
