// --- CONFIG ---
const API_BASE_URL = 'http://127.0.0.1:5000';

// --- DOM ELEMENTS ---
const authContainer = document.getElementById('authContainer');
const appContainer = document.getElementById('appContainer');
const loginView = document.getElementById('loginView');
const registerView = document.getElementById('registerView');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const typingIndicator = document.getElementById('typingIndicator');
const personaModal = document.getElementById('personaModal');
const companionNameEl = document.getElementById('companionName');
const emailDisplay = document.getElementById('emailDisplay'); // Changed

// --- STATE ---
let token = localStorage.getItem('token');
let userEmail = localStorage.getItem('userEmail'); // Changed

// --- INITIALIZATION ---
window.onload = () => {
    if (token && userEmail) { // Changed
        showApp();
    } else {
        showAuth();
    }
};

// --- AUTH FUNCTIONS ---
function toggleAuthView() {
    loginView.style.display = loginView.style.display === 'none' ? 'block' : 'none';
    registerView.style.display = registerView.style.display === 'none' ? 'block' : 'none';
}

async function register() {
    const email = document.getElementById('registerEmail').value; // Changed
    const password = document.getElementById('registerPassword').value;
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }) // Changed
    });
    if (response.ok) {
        alert('Registration successful! Please log in.');
        toggleAuthView();
    } else {
        alert('Registration failed. Email may already be in use.');
    }
}

async function login() {
    const email = document.getElementById('loginEmail').value; // Changed
    const password = document.getElementById('loginPassword').value;
    const response = await await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }) // Changed
    });
    if (response.ok) {
        const data = await response.json();
        token = data.access_token;
        userEmail = data.email;
        localStorage.setItem('token', token);
        localStorage.setItem('userEmail', userEmail); // Changed
        showApp();
    } else {
        alert('Login failed. Check your email and password.');
    }
}

function logout() {
    token = null;
    userEmail = null;
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail'); // Changed
    chatMessages.innerHTML = '';
    showAuth();
}

// --- UI TOGGLING ---
function showApp() {
    authContainer.style.display = 'none';
    appContainer.style.display = 'block';
    emailDisplay.textContent = userEmail; // Changed
    loadChatHistory();
    loadPersona();
}

function showAuth() {
    authContainer.style.display = 'block';
    appContainer.style.display = 'none';
}

// --- API CALLS (No changes in this section) ---
async function apiFetch(endpoint, options = {}) {
    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    if (response.status === 401) { // Token expired or invalid
        logout();
        return;
    }
    return response;
}

// --- CHAT, PERSONA, and MENU FUNCTIONS (No changes in these sections) ---
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    messageInput.value = '';
    showTyping();

    const response = await apiFetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    
    hideTyping();
    if (response.ok) {
        const data = await response.json();
        addMessage(data.response, 'ai');
    } else {
        addMessage("Sorry, I couldn't send that message.", 'ai-error');
    }
}

async function loadChatHistory() {
    const response = await apiFetch('/chat/history');
    if (response.ok) {
        const history = await response.json();
        chatMessages.innerHTML = '';
        history.forEach(msg => addMessage(msg.message, msg.sender));
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
    typingIndicator.style.display = 'flex';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTyping() {
    typingIndicator.style.display = 'none';
}

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});


async function openPersonaSettings() {
    await loadPersona();
    personaModal.style.display = 'flex';
}

function closePersonaSettings() {
    personaModal.style.display = 'none';
}

async function loadPersona() {
    const response = await apiFetch('/persona');
    if (response.ok) {
        const data = await response.json();
        document.getElementById('personaName').value = data.name;
        document.getElementById('personaRelationship').value = data.relationship;
        document.getElementById('personaPersonality').value = data.personality;
        companionNameEl.textContent = data.name;
    }
}

async function savePersonaSettings() {
    const persona = {
        name: document.getElementById('personaName').value,
        relationship: document.getElementById('personaRelationship').value,
        personality: document.getElementById('personaPersonality').value
    };
    const response = await apiFetch('/persona', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(persona)
    });

    if (response.ok) {
        alert('Persona saved!');
        companionNameEl.textContent = persona.name;
        closePersonaSettings();
    } else {
        alert('Failed to save persona.');
    }
}

function toggleMenu() {
    document.getElementById('sideMenu').classList.toggle('open');
    document.getElementById('chatContainer').classList.toggle('menu-open');
}