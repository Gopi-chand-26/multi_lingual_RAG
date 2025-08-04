// Global variables
let isUploading = false;

// DOM elements
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadProgress = document.getElementById('uploadProgress');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const uploadResults = document.getElementById('uploadResults');
const queryInput = document.getElementById('queryInput');
const targetLanguage = document.getElementById('targetLanguage');
const searchLanguage = document.getElementById('searchLanguage');
const queryResults = document.getElementById('queryResults');
const loadingOverlay = document.getElementById('loadingOverlay');
const statsModal = document.getElementById('statsModal');
const statsContent = document.getElementById('statsContent');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    setupDragAndDrop();
});

// Setup event listeners
function setupEventListeners() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Query form submission
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey && queryInput === document.activeElement) {
            askQuestion();
        }
    });
    
    // Modal close on outside click
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target.id);
        }
    });
    
    // Escape key to close modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

// Setup drag and drop functionality
function setupDragAndDrop() {
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFiles(files);
        }
    });
    
    // Click to upload
    uploadArea.addEventListener('click', function(e) {
        if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'INPUT') {
            fileInput.click();
        }
    });
}

// Handle file selection
function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFiles(files);
    }
}

// Handle files (upload or drag & drop)
async function handleFiles(files) {
    if (isUploading) return;
    
    isUploading = true;
    showUploadProgress();
    
    const results = [];
    
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        
        // Update progress
        const progress = ((i + 1) / files.length) * 100;
        updateProgress(progress, `Uploading ${file.name}...`);
        
        try {
            const result = await uploadFile(file);
            results.push(result);
        } catch (error) {
            results.push({
                success: false,
                message: `Error uploading ${file.name}: ${error.message}`,
                fileName: file.name
            });
        }
    }
    
    hideUploadProgress();
    displayUploadResults(results);
    isUploading = false;
    
    // Clear file input
    fileInput.value = '';
}

// Upload a single file
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Upload failed');
    }
    
    return await response.json();
}

// Show upload progress
function showUploadProgress() {
    uploadProgress.style.display = 'block';
    uploadArea.style.display = 'none';
    updateProgress(0, 'Preparing upload...');
}

// Hide upload progress
function hideUploadProgress() {
    uploadProgress.style.display = 'none';
    uploadArea.style.display = 'block';
}

// Update progress bar
function updateProgress(percentage, text) {
    progressFill.style.width = `${percentage}%`;
    progressText.textContent = text;
}

// Display upload results
function displayUploadResults(results) {
    uploadResults.innerHTML = '';
    
    results.forEach(result => {
        const resultElement = document.createElement('div');
        resultElement.className = `result-item ${result.success ? 'success' : 'error'}`;
        
        if (result.success) {
            resultElement.innerHTML = `
                <h4><i class="fas fa-check-circle"></i> ${result.data.file_name}</h4>
                <p><strong>Language:</strong> ${result.data.language}</p>
                <p><strong>Chunks:</strong> ${result.data.chunk_count}</p>
                <p><strong>Size:</strong> ${formatFileSize(result.data.file_size)}</p>
                <p><strong>Status:</strong> ${result.message}</p>
            `;
        } else {
            resultElement.innerHTML = `
                <h4><i class="fas fa-exclamation-circle"></i> Upload Failed</h4>
                <p><strong>File:</strong> ${result.fileName || 'Unknown'}</p>
                <p><strong>Error:</strong> ${result.message}</p>
            `;
        }
        
        uploadResults.appendChild(resultElement);
    });
}

// Ask question function
async function askQuestion() {
    const query = queryInput.value.trim();
    const targetLang = targetLanguage.value;
    const searchLang = searchLanguage.value;
    
    if (!query) {
        showNotification('Please enter a question', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('query', query);
        formData.append('target_language', targetLang);
        formData.append('search_language', searchLang);
        
        const response = await fetch('/query', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Query failed');
        }
        
        const result = await response.json();
        displayQueryResult(result);
        
    } catch (error) {
        showNotification(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Display query result
function displayQueryResult(result) {
    queryResults.innerHTML = '';
    
    if (result.success) {
        const resultElement = document.createElement('div');
        resultElement.className = 'result-item success';
        
        let sourcesHtml = '';
        if (result.sources && result.sources.length > 0) {
            sourcesHtml = `
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee;">
                    <h5><i class="fas fa-sources"></i> Sources:</h5>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        ${result.sources.map(source => `
                            <li>${source.file_name} (${source.language}) - Similarity: ${(source.similarity * 100).toFixed(1)}%</li>
                        `).join('')}
                    </ul>
                </div>
            `;
        }
        
        resultElement.innerHTML = `
            <h4><i class="fas fa-lightbulb"></i> Answer</h4>
            <div style="margin: 15px 0; line-height: 1.6;">
                ${result.response.replace(/\n/g, '<br>')}
            </div>
            <p><strong>Query Language:</strong> ${result.query_language}</p>
            <p><strong>Answer Language:</strong> ${result.target_language}</p>
            <p><strong>Context Length:</strong> ${result.context_length} characters</p>
            ${sourcesHtml}
        `;
        
        queryResults.appendChild(resultElement);
    } else {
        const errorElement = document.createElement('div');
        errorElement.className = 'result-item error';
        errorElement.innerHTML = `
            <h4><i class="fas fa-exclamation-triangle"></i> No Results Found</h4>
            <p>${result.message}</p>
        `;
        queryResults.appendChild(errorElement);
    }
}

// Show statistics
async function showStats() {
    showModal('statsModal');
    
    try {
        const response = await fetch('/stats');
        if (!response.ok) {
            throw new Error('Failed to fetch statistics');
        }
        
        const data = await response.json();
        displayStats(data.stats);
        
    } catch (error) {
        statsContent.innerHTML = `
            <div class="result-item error">
                <h4><i class="fas fa-exclamation-triangle"></i> Error</h4>
                <p>${error.message}</p>
            </div>
        `;
    }
}

// Display statistics
function displayStats(stats) {
    const vectorStats = stats.vector_store || {};
    const translationStats = stats.translation_cache || {};
    
    statsContent.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <h4>${vectorStats.total_documents || 0}</h4>
                <p>Total Documents</p>
            </div>
            <div class="stat-card">
                <h4>${vectorStats.language_count || 0}</h4>
                <p>Languages</p>
            </div>
            <div class="stat-card">
                <h4>${vectorStats.file_count || 0}</h4>
                <p>Files</p>
            </div>
            <div class="stat-card">
                <h4>${translationStats.cache_size || 0}</h4>
                <p>Cache Entries</p>
            </div>
        </div>
        
        <div style="margin-top: 30px;">
            <h4>Languages in Database:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                ${(vectorStats.unique_languages || []).map(lang => 
                    `<span style="background: #667eea; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">${lang}</span>`
                ).join('')}
            </div>
        </div>
        
        <div style="margin-top: 20px;">
            <h4>Files:</h4>
            <ul style="margin-top: 10px; padding-left: 20px;">
                ${(vectorStats.unique_files || []).map(file => 
                    `<li style="margin-bottom: 5px;">${file}</li>`
                ).join('')}
            </ul>
        </div>
    `;
}

// Clear system data
async function clearData() {
    if (!confirm('Are you sure you want to clear all system data? This action cannot be undone.')) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/clear', {
            method: 'POST'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to clear data');
        }
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('System data cleared successfully', 'success');
            // Clear results
            uploadResults.innerHTML = '';
            queryResults.innerHTML = '';
        } else {
            showNotification(result.message, 'error');
        }
        
    } catch (error) {
        showNotification(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Show modal
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

// Close modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

// Close all modals
function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => modal.classList.remove('show'));
}

// Show loading overlay
function showLoading() {
    loadingOverlay.classList.add('show');
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.classList.remove('show');
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#667eea'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        z-index: 3000;
        max-width: 300px;
        word-wrap: break-word;
        animation: slideInRight 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style); 