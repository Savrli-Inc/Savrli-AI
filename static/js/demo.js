/**
 * Savrli AI Demo Page JavaScript
 * Handles API interactions for chat and resource upload endpoints
 */

// API Configuration
const API_BASE = window.location.origin;
const CHAT_ENDPOINT = `${API_BASE}/ai/chat`;
const UPLOAD_ENDPOINT = `${API_BASE}/resources/upload`;

/**
 * Initialize demo page event listeners
 */
document.addEventListener('DOMContentLoaded', function() {
    // Chat demo buttons
    const chatButtons = document.querySelectorAll('.chat-demo-btn');
    chatButtons.forEach(btn => {
        btn.addEventListener('click', handleChatDemo);
    });

    // Upload demo button
    const uploadBtn = document.getElementById('upload-demo-btn');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', handleUploadDemo);
    }

    // File input change handler
    const fileInput = document.getElementById('file-upload');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
});

/**
 * Handle chat demo button clicks
 */
async function handleChatDemo(event) {
    const button = event.target;
    const prompt = button.dataset.prompt;
    const responseContainer = document.getElementById('chat-response');
    const loadingIndicator = document.getElementById('loading-indicator');

    if (!prompt) {
        showError('No prompt defined for this button');
        return;
    }

    // Show loading state
    button.disabled = true;
    if (loadingIndicator) loadingIndicator.style.display = 'block';
    if (responseContainer) {
        responseContainer.textContent = 'Generating response...';
        responseContainer.className = 'response-container loading';
    }

    try {
        const response = await fetch(CHAT_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                max_tokens: 500,
                temperature: 0.7
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Chat request failed');
        }

        const data = await response.json();
        displayChatResponse(data.response);

    } catch (error) {
        console.error('Chat error:', error);
        showError(`Chat failed: ${error.message}`);
    } finally {
        button.disabled = false;
        if (loadingIndicator) loadingIndicator.style.display = 'none';
    }
}

/**
 * TODO: Implement streaming response rendering
 * 
 * To support streaming responses:
 * 1. Add stream: true to the request body
 * 2. Use EventSource or fetch with ReadableStream
 * 3. Parse Server-Sent Events (SSE) format
 * 4. Progressively update the response container
 * 
 * Example implementation:
 * 
 * const response = await fetch(CHAT_ENDPOINT, {
 *     method: 'POST',
 *     headers: { 'Content-Type': 'application/json' },
 *     body: JSON.stringify({ prompt: prompt, stream: true })
 * });
 * 
 * const reader = response.body.getReader();
 * const decoder = new TextDecoder();
 * 
 * while (true) {
 *     const { done, value } = await reader.read();
 *     if (done) break;
 *     
 *     const chunk = decoder.decode(value);
 *     const lines = chunk.split('\n\n');
 *     
 *     for (const line of lines) {
 *         if (line.startsWith('data: ')) {
 *             const data = JSON.parse(line.slice(6));
 *             if (data.content) {
 *                 appendToResponse(data.content);
 *             }
 *         }
 *     }
 * }
 */

/**
 * Display chat response in the UI
 */
function displayChatResponse(text) {
    const responseContainer = document.getElementById('chat-response');
    if (responseContainer) {
        responseContainer.textContent = text;
        responseContainer.className = 'response-container success';
    }
}

/**
 * Handle file upload demo
 */
async function handleUploadDemo() {
    const fileInput = document.getElementById('file-upload');
    const uploadResponse = document.getElementById('upload-response');
    const loadingIndicator = document.getElementById('upload-loading');
    const uploadBtn = document.getElementById('upload-demo-btn');

    if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
        showError('Please select a file to upload');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    // Show loading state
    if (uploadBtn) uploadBtn.disabled = true;
    if (loadingIndicator) loadingIndicator.style.display = 'block';
    if (uploadResponse) {
        uploadResponse.textContent = 'Uploading file...';
        uploadResponse.className = 'response-container loading';
    }

    try {
        const response = await fetch(UPLOAD_ENDPOINT, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        const data = await response.json();
        displayUploadResponse(data);

    } catch (error) {
        console.error('Upload error:', error);
        showError(`Upload failed: ${error.message}`);
    } finally {
        if (uploadBtn) uploadBtn.disabled = false;
        if (loadingIndicator) loadingIndicator.style.display = 'none';
    }
}

/**
 * Display upload response in the UI
 */
function displayUploadResponse(data) {
    const uploadResponse = document.getElementById('upload-response');
    if (uploadResponse) {
        uploadResponse.textContent = JSON.stringify(data, null, 2);
        uploadResponse.className = 'response-container success';
    }
}

/**
 * Handle file selection
 */
function handleFileSelect(event) {
    const fileInput = event.target;
    const fileInfo = document.getElementById('file-info');
    
    if (fileInput.files && fileInput.files.length > 0) {
        const file = fileInput.files[0];
        if (fileInfo) {
            fileInfo.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
        }
    }
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Show error message
 */
function showError(message) {
    const chatResponse = document.getElementById('chat-response');
    const uploadResponse = document.getElementById('upload-response');
    
    const errorMessage = `Error: ${message}`;
    
    if (chatResponse && chatResponse.textContent.includes('Generating')) {
        chatResponse.textContent = errorMessage;
        chatResponse.className = 'response-container error';
    } else if (uploadResponse && uploadResponse.textContent.includes('Uploading')) {
        uploadResponse.textContent = errorMessage;
        uploadResponse.className = 'response-container error';
    } else {
        console.error(errorMessage);
        alert(errorMessage);
    }
}
