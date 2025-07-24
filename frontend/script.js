// Configuration
const API_URL = 'http://localhost:5000';
let sessionId = localStorage.getItem('sessionId') || generateSessionId();

// Save session ID
localStorage.setItem('sessionId', sessionId);

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const typingIndicator = document.getElementById('typingIndicator');

// Generate unique session ID
function generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9);
}

// Initialize chat with greeting
window.onload = function() {
    // Show initial greeting after a short delay
    setTimeout(() => {
        addMessage("Hey there! I've been waiting for you 💕 How's your day going?", 'ai');
    }, 1000);
};

// Send message function
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message
    addMessage(message, 'user');
    messageInput.value = '';

    // Show typing indicator
    showTyping();

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });

        const data = await response.json();
        hideTyping();

        // Simulate realistic typing delay
        const typingDelay = Math.min(data.response.length * 20, 2000);
        
        setTimeout(() => {
            addMessage(data.response, 'ai');
        }, typingDelay);

    } catch (error) {
        console.error('Error:', error);
        hideTyping();
        
        // Fallback message
        setTimeout(() => {
            addMessage("I'm having trouble connecting right now, but I'm still here for you 💕 Can you try again?", 'ai');
        }, 500);
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = text;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTyping() {
    typingIndicator.style.display = 'flex';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Hide typing indicator
function hideTyping() {
    typingIndicator.style.display = 'none';
}

// Enter key support
messageInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Toggle menu (for future features)
function toggleMenu() {
    alert('Menu features coming soon! 💕');
}

// Auto-resize input (optional)
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});