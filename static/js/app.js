let uploadedFiles = {};
let selectedSections = new Set();
let currentJobId = null;
let statusInterval = null;

document.addEventListener('DOMContentLoaded', function() {
    setupFileUploads();
    setupSectionSelection();
    setupGenerateButton();
    loadExistingOutputs();
});

function setupFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                uploadFile(input.id, file);
            }
        });
    });
}

function uploadFile(fileType, file) {
    const statusEl = document.getElementById(`${fileType}-status`);
    statusEl.textContent = 'Uploading...';
    statusEl.style.color = '#0066ff';
    
    const formData = new FormData();
    formData.append(fileType, file);
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            uploadedFiles[fileType] = file.name;
            statusEl.textContent = '✓ Uploaded';
            statusEl.style.color = '#00c853';
        } else {
            statusEl.textContent = '✗ Failed';
            statusEl.style.color = '#ff3d00';
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        statusEl.textContent = '✗ Error';
        statusEl.style.color = '#ff3d00';
    });
}

function setupSectionSelection() {
    const sectionCards = document.querySelectorAll('.section-card');
    
    sectionCards.forEach(card => {
        const checkbox = card.querySelector('input[type="checkbox"]');
        const section = card.dataset.section;
        
        card.addEventListener('click', function(e) {
            if (e.target.type !== 'checkbox') {
                checkbox.checked = !checkbox.checked;
            }
            
            if (checkbox.checked) {
                selectedSections.add(section);
                card.classList.add('selected');
            } else {
                selectedSections.delete(section);
                card.classList.remove('selected');
            }
        });
        
        checkbox.addEventListener('change', function() {
            if (checkbox.checked) {
                selectedSections.add(section);
                card.classList.add('selected');
            } else {
                selectedSections.delete(section);
                card.classList.remove('selected');
            }
        });
    });
}

function setupGenerateButton() {
    const btn = document.getElementById('generate-btn');
    
    btn.addEventListener('click', function() {
        if (selectedSections.size === 0) {
            alert('Please select at least one section to generate');
            return;
        }
        
        startGeneration();
    });
}

function startGeneration() {
    const btn = document.getElementById('generate-btn');
    btn.disabled = true;
    btn.textContent = 'Generating...';
    
    fetch('/api/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sections: Array.from(selectedSections)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentJobId = data.job_id;
            showStatusSection();
            startStatusPolling();
        } else {
            alert('Failed to start generation');
            btn.disabled = false;
            btn.textContent = 'Generate Reports';
        }
    })
    .catch(error => {
        console.error('Generation error:', error);
        alert('Error starting generation');
        btn.disabled = false;
        btn.textContent = 'Generate Reports';
    });
}

function showStatusSection() {
    const statusSection = document.getElementById('status-section');
    statusSection.style.display = 'block';
    statusSection.scrollIntoView({ behavior: 'smooth' });
}

function startStatusPolling() {
    if (statusInterval) {
        clearInterval(statusInterval);
    }
    
    statusInterval = setInterval(() => {
        updateStatus();
    }, 1000);
}

function updateStatus() {
    if (!currentJobId) return;
    
    fetch(`/api/status/${currentJobId}`)
    .then(response => response.json())
    .then(data => {
        const statusContent = document.getElementById('status-content');
        const progressFill = document.getElementById('progress-fill');
        
        const total = data.sections.length;
        const completed = data.completed.length;
        const progress = (completed / total) * 100;
        
        progressFill.style.width = progress + '%';
        
        let html = '';
        
        data.sections.forEach(section => {
            const isCompleted = data.completed.includes(section);
            const hasError = data.errors.some(e => e.section === section);
            const isProcessing = data.status === `generating_${section}`;
            
            let statusClass = 'processing';
            let statusText = 'Pending';
            
            if (isCompleted) {
                statusClass = 'success';
                statusText = 'Completed';
            } else if (hasError) {
                statusClass = 'error';
                statusText = 'Error';
            } else if (isProcessing) {
                statusClass = 'processing';
                statusText = 'Processing...';
            }
            
            html += `
                <div class="status-item ${statusClass}">
                    <span>Section ${section.toUpperCase()}</span>
                    <span>${statusText}</span>
                </div>
            `;
        });
        
        statusContent.innerHTML = html;
        
        if (data.status === 'completed' || data.status === 'failed') {
            clearInterval(statusInterval);
            
            const btn = document.getElementById('generate-btn');
            btn.disabled = false;
            btn.textContent = 'Generate Reports';
            
            setTimeout(() => {
                loadExistingOutputs();
            }, 1000);
        }
    })
    .catch(error => {
        console.error('Status polling error:', error);
    });
}

function loadExistingOutputs() {
    fetch('/api/outputs')
    .then(response => response.json())
    .then(data => {
        if (Object.keys(data).length > 0) {
            displayOutputs(data);
        }
    })
    .catch(error => {
        console.error('Error loading outputs:', error);
    });
}

function displayOutputs(outputs) {
    const outputsSection = document.getElementById('outputs-section');
    const outputsList = document.getElementById('outputs-list');
    
    outputsSection.style.display = 'block';
    
    let html = '';
    
    Object.keys(outputs).forEach(section => {
        const files = outputs[section];
        
        html += `
            <div class="output-item">
                <div>
                    <div class="section-name">Section ${section.toUpperCase()}</div>
                    <div style="font-size: 0.85rem; color: #666; margin-top: 4px;">
                        ${files.length} file(s) generated
                    </div>
                </div>
                <div class="files">
                    <a href="/api/download/${section}" class="download-link">
                        Download
                    </a>
                </div>
            </div>
        `;
    });
    
    outputsList.innerHTML = html;
}
