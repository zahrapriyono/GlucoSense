const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');

async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    appendBubble(message, 'user');
    chatInput.value = '';
    document.getElementById('chatSuggestions').style.display = 'none';

    const loadingId = `loading-${Date.now()}`;
    appendBubble('...', 'bot', loadingId);

    try {
        const response = await fetch('/chatbot/api/chat/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        document.getElementById(loadingId)?.remove();
        appendBubble(data.answer, 'bot');
    } catch {
        document.getElementById(loadingId)?.remove();
        appendBubble('Sorry, something went wrong. Please try again.', 'bot');
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendBubble(text, type, id = null) {
    const div = document.createElement('div');
    div.id = id || `bubble-${Date.now()}`;
    div.className = `chat-bubble chat-bubble--${type}`;
    div.textContent = text;
    chatMessages.appendChild(div);
    return div.id;
}

function sendSuggestion(text) {
    chatInput.value = text;
    sendMessage()
}

chatInput.addEventListener(`keydown`, e => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});