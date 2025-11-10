/**
 * Savrli AI Demo Page JavaScript
 * Handles API interactions for chat and resource upload endpoints
 * Provides a clean, responsive test harness with loading states and raw JSON
 */

// API base URL - defaults to current origin
const API_BASE = window.location.origin;
const CHAT_ENDPOINT = `${API_BASE}/ai/chat`;
const UPLOAD_ENDPOINT = `${API_BASE}/api/resources/upload`;

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
    // Chat API buttons (quick test)
    document.querySelectorAll('.chat-demo-btn').forEach(btn => {
        btn.addEventListener('click', handleChatDemo);
    });

    // Custom chat form
    const customChatForm = document.getElementById('custom-chat-form');
    if (customChatForm) {
        customChatForm.addEventListener('submit', handleCustomChat);
    }

    // Upload API button
    const uploadBtn = document.getElementById('upload-demo-btn');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', handleUploadDemo);
    }

    // File input change (for metadata preview)
    const fileInput = document.getElementById('file-input') || document.getElementById('file-upload');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
}

/**
 * Handle quick test button clicks
 */
async function handleChatDemo(event) {
    const button = event.target.closest('button');
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
        promptInput.value = ''; // Clear input
    } catch (error) {
        displayError(`Chat API Error: ${error.message}`);
    }
}

/**
 * Call the /ai/chat API endpoint
 */
async function callChatAPI(prompt, sessionId = null) {
    const requestBody = { prompt };
    if (sessionId) requestBody.session_id = sessionId;

    const response = await fetch(CHAT_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
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
    const fileInput = document.getElementById('file-input') || document.getElementById('file-upload');
    const file = fileInput?.files[0];

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

    const response = await fetch(UPLOAD_ENDPOINT, {
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
    if (!output) return;

    output.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Processing request...</p>
        </div>
    `;
    output.classList.remove('error');
    output.classList.add('loading-state');
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
                        <p><strong>Type:</strong> ${escapeHtml(data.file_info.content_type || 'N/A')}</p>
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
 * Handle file selection (preview)
 */
function handleFileSelect(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];
    const fileInfo = document.getElementById('file-info');

    if (file && fileInfo) {
        fileInfo.textContent = `Selected: ${file.name} (${formatBytes(file.size)})`;
    } else if (fileInfo) {
        fileInfo.textContent = 'No file selected';
    }
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

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}