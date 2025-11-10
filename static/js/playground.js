/**
 * Savrli AI Playground - JavaScript Integration Module
 * 
 * This module provides fetch-based examples for calling the Savrli AI backend endpoints.
 * Use this as a reference for integrating the interactive playground with multimodal endpoints.
 * 
 * Key Endpoints:
 * - /api/ai/chat - Chat completions
 * - /api/resources/upload - File upload (future implementation)
 * - /api/playground/session - Session management
 */

/**
 * Call the chat endpoint
 * @param {string} prompt - The user's message
 * @param {Object} options - Additional options (model, temperature, etc.)
 * @returns {Promise<Object>} - The AI response
 * 
 * @example
 * const response = await callChatEndpoint("Hello, world!", {
 *   model: "gpt-3.5-turbo",
 *   temperature: 0.7,
 *   session_id: "demo-session"
 * });
 * console.log(response.response);
 */
async function callChatEndpoint(prompt, options = {}) {
    const endpoint = '/ai/chat';
    
    const requestBody = {
        prompt: prompt,
        model: options.model || 'gpt-3.5-turbo',
        temperature: options.temperature || 0.7,
        max_tokens: options.max_tokens || 1000,
        session_id: options.session_id || null,
        stream: options.stream || false
    };
    
    // Add optional parameters if provided
    if (options.system) {
        requestBody.system = options.system;
    }
    
    if (options.top_p !== undefined) {
        requestBody.top_p = options.top_p;
    }
    
    if (options.context_window !== undefined) {
        requestBody.context_window = options.context_window;
    }
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Chat API Error:', error);
        throw error;
    }
}

/**
 * Upload a file/resource (stub for future implementation)
 * @param {File} file - The file to upload
 * @param {Object} options - Upload options
 * @returns {Promise<Object>} - Upload response with file ID
 * 
 * @example
 * const fileInput = document.getElementById('fileInput');
 * const file = fileInput.files[0];
 * const response = await uploadResource(file, {
 *   session_id: "demo-session"
 * });
 * console.log(response.file_id);
 */
async function uploadResource(file, options = {}) {
    const endpoint = '/api/resources/upload';
    
    const formData = new FormData();
    formData.append('file', file);
    
    if (options.session_id) {
        formData.append('session_id', options.session_id);
    }
    
    if (options.metadata) {
        formData.append('metadata', JSON.stringify(options.metadata));
    }
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
            // Note: Don't set Content-Type header, browser will set it with boundary
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Upload API Error:', error);
        throw error;
    }
}

/**
 * Get session information
 * @param {string} sessionId - The session ID
 * @returns {Promise<Object>} - Session information
 * 
 * @example
 * const sessionInfo = await getSessionInfo("demo-session");
 * console.log(sessionInfo.created_at, sessionInfo.message_count);
 */
async function getSessionInfo(sessionId) {
    const endpoint = `/api/playground/session/${sessionId}`;
    
    try {
        const response = await fetch(endpoint, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Session Info API Error:', error);
        throw error;
    }
}

/**
 * Create a new session
 * @param {Object} options - Session creation options
 * @returns {Promise<Object>} - New session information
 * 
 * @example
 * const session = await createSession({
 *   name: "My Playground Session"
 * });
 * console.log(session.session_id);
 */
async function createSession(options = {}) {
    const endpoint = '/api/playground/session';
    
    const requestBody = {
        name: options.name || 'Playground Session',
        metadata: options.metadata || {}
    };
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Create Session API Error:', error);
        throw error;
    }
}

/**
 * Delete a session
 * @param {string} sessionId - The session ID to delete
 * @returns {Promise<Object>} - Deletion confirmation
 * 
 * @example
 * const result = await deleteSession("demo-session");
 * console.log(result.message);
 */
async function deleteSession(sessionId) {
    const endpoint = `/api/playground/session/${sessionId}`;
    
    try {
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Delete Session API Error:', error);
        throw error;
    }
}

/**
 * List all playground sessions
 * @param {Object} options - Listing options
 * @returns {Promise<Object>} - List of sessions
 * 
 * @example
 * const sessions = await listSessions({ limit: 10 });
 * console.log(sessions.sessions);
 */
async function listSessions(options = {}) {
    const params = new URLSearchParams();
    
    if (options.limit) {
        params.append('limit', options.limit);
    }
    
    if (options.offset) {
        params.append('offset', options.offset);
    }
    
    const endpoint = `/api/playground/sessions${params.toString() ? '?' + params.toString() : ''}`;
    
    try {
        const response = await fetch(endpoint, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('List Sessions API Error:', error);
        throw error;
    }
}

// Export functions for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        callChatEndpoint,
        uploadResource,
        getSessionInfo,
        createSession,
        deleteSession,
        listSessions
    };
}
