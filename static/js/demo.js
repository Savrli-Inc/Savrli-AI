/**
 * Savrli AI Demo Page - JavaScript
 * 
 * Simple demo script for testing /api/ai/chat endpoint
 * 
 * TODO: Expand functionality as per issue #36
 * - Add more sample prompts
 * - Add file upload support for /api/resources/upload (when implemented)
 * - Add error handling improvements
 * - Add response formatting options
 */

// API endpoint configuration
const API_BASE_URL = '/ai';
const CHAT_ENDPOINT = `${API_BASE_URL}/chat`;

/**
 * Initialize the demo page
 */
function initDemo() {
    console.log('Savrli AI Demo initialized');
    
    // Add event listeners
    const sendButton = document.getElementById('sendButton');
    const clearButton = document.getElementById('clearButton');
    const promptInput = document.getElementById('promptInput');
    
    if (sendButton) {
        sendButton.addEventListener('click', sendChatMessage);
    }
    
    if (clearButton) {
        clearButton.addEventListener('click', clearOutput);
    }
    
    if (promptInput) {
        // Allow Enter to send (Shift+Enter for new line)
        promptInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }
    
    // Add event listeners for sample prompts
    const sampleButtons = document.querySelectorAll('.sample-prompt');
    sampleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const prompt = button.dataset.prompt;
            if (promptInput && prompt) {
                promptInput.value = prompt;
            }
        });
    });
}

/**
 * Send a chat message to the API
 */
async function sendChatMessage() {
    const promptInput = document.getElementById('promptInput');
    const outputDiv = document.getElementById('output');
    const sendButton = document.getElementById('sendButton');
    
    if (!promptInput || !outputDiv) {
        console.error('Required elements not found');
        return;
    }
    
    const prompt = promptInput.value.trim();
    
    if (!prompt) {
        appendOutput('Error: Please enter a prompt', 'error');
        return;
    }
    
    // Disable button during request
    if (sendButton) {
        sendButton.disabled = true;
        sendButton.textContent = 'Sending...';
    }
    
    // Show user message
    appendOutput(`You: ${prompt}`, 'user');
    
    try {
        // Call the API
        const response = await fetch(CHAT_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                model: 'gpt-3.5-turbo',
                temperature: 0.7,
                max_tokens: 500,
                session_id: 'demo-session'
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Display AI response
        if (data.response) {
            appendOutput(`AI: ${data.response}`, 'assistant');
            
            // Clear input after successful send
            promptInput.value = '';
        } else {
            throw new Error('No response received from API');
        }
        
    } catch (error) {
        console.error('API Error:', error);
        appendOutput(`Error: ${error.message}`, 'error');
    } finally {
        // Re-enable button
        if (sendButton) {
            sendButton.disabled = false;
            sendButton.textContent = 'Send';
        }
    }
}

/**
 * Append output to the output div
 * @param {string} message - The message to display
 * @param {string} type - The type of message (user, assistant, error)
 */
function appendOutput(message, type = 'info') {
    const outputDiv = document.getElementById('output');
    
    if (!outputDiv) {
        console.error('Output div not found');
        return;
    }
    
    // Create message element
    const messageEl = document.createElement('div');
    messageEl.className = `message message-${type}`;
    
    const timestamp = new Date().toLocaleTimeString();
    messageEl.innerHTML = `
        <div class="message-header">
            <span class="message-type">${type.toUpperCase()}</span>
            <span class="message-time">${timestamp}</span>
        </div>
        <div class="message-content">${escapeHtml(message)}</div>
    `;
    
    outputDiv.appendChild(messageEl);
    
    // Scroll to bottom
    outputDiv.scrollTop = outputDiv.scrollHeight;
}

/**
 * Clear the output div
 */
function clearOutput() {
    const outputDiv = document.getElementById('output');
    
    if (!outputDiv) {
        console.error('Output div not found');
        return;
    }
    
    outputDiv.innerHTML = '<p class="placeholder">Messages will appear here...</p>';
}

/**
 * Escape HTML to prevent XSS
 * @param {string} text - The text to escape
 * @returns {string} - The escaped HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * TODO (issue #36): Add file upload functionality
 * This function will be implemented when /api/resources/upload is available
 */
async function uploadFile() {
    // Placeholder for file upload functionality
    console.log('File upload not yet implemented - see issue #36');
    appendOutput('File upload feature coming soon (issue #36)', 'info');
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDemo);
} else {
    initDemo();
}
