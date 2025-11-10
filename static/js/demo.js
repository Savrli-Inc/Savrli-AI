/**
 * Savrli AI Demo Page JavaScript
 * 
 * This script wires the demo page buttons to API calls and renders responses.
 * It provides a simple interface for manual testing of chat and multimodal endpoints.
 */

// API base URL - defaults to current origin
const API_BASE = window.location.origin;

/**
 * Initialize the demo page when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Savrli AI Demo initialized');
    setupEventListeners();
});

/**
 * Setup event listeners for all interactive elements
 */
function setupEventListeners() {
    // Chat API buttons
    const chatButtons = document.querySelectorAll('.chat-demo-btn');
    chatButtons.forEach(btn => {
        btn.addEventListener('click', handleChatDemo);
    });

    // Upload API button
    const uploadBtn = document.getElementById('upload-demo-btn');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', handleUploadDemo);
    }

    // Custom chat form submission
    const customChatForm = document.getElementById('custom-chat-form');
    if (customChatForm) {
        customChatForm.addEventListener('submit', handleCustomChat);
    }
}

/**
 * Handle chat demo button clicks
 */
async function handleChatDemo(event) {
    const button = event.target;
    const prompt = button.dataset.prompt;
    const sessionId = button.dataset.sessionId || null;
    
    if (!prompt) {
        displayError('No prompt found for this button');
        return;
    }

    displayLoading('chat-output');
    
    try {
        const response = await callChatAPI(prompt, sessionId);
        displayChatResponse(response);
    } catch (error) {
        displayError(`Chat API Error: ${error.message}`);
    }
}

/**
 * Handle custom chat form submission
 */
async function handleCustomChat(event) {
    event.preventDefault();
    
    const promptInput = document.getElementById('custom-prompt');
    const sessionInput = document.getElementById('custom-session-id');
    
    const prompt = promptInput.value.trim();
    const sessionId = sessionInput.value.trim() || null;
    
    if (!prompt) {
        displayError('Please enter a prompt');
        return;
    }

    displayLoading('chat-output');
    
    try {
        const response = await callChatAPI(prompt, sessionId);
        displayChatResponse(response);
    } catch (error) {
        displayError(`Chat API Error: ${error.message}`);
    }
}

/**
 * Call the /ai/chat API endpoint
 */
async function callChatAPI(prompt, sessionId = null) {
    const requestBody = {
        prompt: prompt
    };
    
    if (sessionId) {
        requestBody.session_id = sessionId;
    }

    const response = await fetch(`${API_BASE}/ai/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}`);
    }

    return await response.json();
}

/**
 * Handle upload demo button click
 */
async function handleUploadDemo() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    
    if (!file) {
        displayError('Please select a file to upload');
        return;
    }

    displayLoading('upload-output');
    
    try {
        const response = await callUploadAPI(file);
        displayUploadResponse(response);
    } catch (error) {
        displayError(`Upload API Error: ${error.message}`, 'upload-output');
    }
}

/**
 * Call the /api/resources/upload API endpoint
 */
async function callUploadAPI(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE}/api/resources/upload`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}`);
    }

    return await response.json();
}

/**
 * Display loading state
 */
function displayLoading(outputId) {
    const output = document.getElementById(outputId);
    if (output) {
        output.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Processing request...</p>
            </div>
        `;
        output.classList.remove('error');
        output.classList.add('loading-state');
    }
}

/**
 * Display chat API response
 */
function displayChatResponse(data) {
    const output = document.getElementById('chat-output');
    if (!output) return;

    output.classList.remove('loading-state', 'error');
    
    const responseText = data.response || 'No response text';
    const sessionId = data.session_id || 'None';

    output.innerHTML = `
        <div class="response-container">
            <div class="response-metadata">
                <span class="metadata-label">Session ID:</span>
                <span class="metadata-value">${escapeHtml(sessionId)}</span>
            </div>
            <div class="response-text">
                <h3>Response:</h3>
                <div class="response-content">${escapeHtml(responseText)}</div>
            </div>
            <div class="response-raw">
                <details>
                    <summary>Raw JSON Response</summary>
                    <pre><code>${escapeHtml(JSON.stringify(data, null, 2))}</code></pre>
                </details>
            </div>
        </div>
    `;
}

/**
 * Display upload API response
 */
function displayUploadResponse(data) {
    const output = document.getElementById('upload-output');
    if (!output) return;

    output.classList.remove('loading-state', 'error');
    
    output.innerHTML = `
        <div class="response-container">
            <div class="response-text">
                <h3>Upload Result:</h3>
                <div class="response-content">
                    ${data.message || 'File uploaded successfully'}
                </div>
                ${data.file_info ? `
                    <div class="file-info">
                        <p><strong>Filename:</strong> ${escapeHtml(data.file_info.filename)}</p>
                        <p><strong>Size:</strong> ${formatBytes(data.file_info.size)}</p>
                        <p><strong>Type:</strong> ${escapeHtml(data.file_info.content_type)}</p>
                    </div>
                ` : ''}
            </div>
            <div class="response-raw">
                <details>
                    <summary>Raw JSON Response</summary>
                    <pre><code>${escapeHtml(JSON.stringify(data, null, 2))}</code></pre>
                </details>
            </div>
        </div>
    `;
}

/**
 * Display error message
 */
function displayError(message, outputId = 'chat-output') {
    const output = document.getElementById(outputId);
    if (!output) return;

    output.classList.remove('loading-state');
    output.classList.add('error');
    
    output.innerHTML = `
        <div class="error-container">
            <h3>Error</h3>
            <p>${escapeHtml(message)}</p>
        </div>
    `;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Format bytes to human-readable size
 */
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
