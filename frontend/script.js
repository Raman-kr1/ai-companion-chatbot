// Configuration
const API_URL = '/api'; // Use a relative path for API calls
let sessionId = localStorage.getItem('sessionId') || `session_${Math.random().toString(36).substr(2, 9)}`;
localStorage.setItem('sessionId', sessionId);

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const typingIndicator = document.getElementById('typingIndicator');
const sideMenu = document.getElementById('sideMenu');
const chatContainer = document.getElementById('chatContainer');

// Load chat history on startup
window.onload = function() {
    loadChatHistory();
    if (chatMessages.children.length === 0) {
        setTimeout(() => {
            addMessage("Hey there! I've been waiting for you 💕 How's your day going?", 'ai');
        }, 1000);
    }
};

// Send message function
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    saveChatHistory();
    messageInput.value = '';
    showTyping();

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, session_id: sessionId })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        hideTyping();

        // Simulate realistic typing delay
        const typingDelay = Math.random() * 1000 + 500; // Random delay between 0.5s and 1.5s
        
        setTimeout(() => {
            addMessage(data.response, 'ai');
            saveChatHistory();
        }, typingDelay);

    } catch (error) {
        console.error('Error:', error);
        hideTyping();
        setTimeout(() => {
            addMessage("I'm having trouble connecting right now, but I'm still here for you 💕", 'ai');
            saveChatHistory();
        }, 500);
    }
}

// Add message to chat UI
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Typing indicator functions
function showTyping() {
    typingIndicator.style.display = 'flex';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTyping() {
    typingIndicator.style.display = 'none';
}

// Event listener for Enter key
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Menu toggle function
function toggleMenu() {
    sideMenu.classList.toggle('open');
    chatContainer.classList.toggle('menu-open');
}

// Chat history functions
function saveChatHistory() {
    localStorage.setItem(`chatHistory_${sessionId}`, chatMessages.innerHTML);
}

function loadChatHistory() {
    const history = localStorage.getItem(`chatHistory_${sessionId}`);
    if (history) {
        chatMessages.innerHTML = history;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}
