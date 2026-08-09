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

    if (type === 'bot') {
        div.innerHTML = formatBotResponse(text);
    } else {
        div.textContent = text;   // user bubble: plain text
    }

    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div.id;
}

/**
 * Parse bot response text into structured HTML:
 * - Splits on " * " to get bullet points
 * - First chunk = intro paragraph
 * - Remaining chunks = <ul><li> list
 * - Grays out (Source X) citations
 */
function formatBotResponse(text) {
    // Remove trailing/leading whitespace
    text = text.trim();

    // Gray out source citations like "(Source 3 and 4)" or "(Source 5)"
    text = text.replace(/\(Source[^)]+\)/g, match =>
        `<span style="color:#94A3B8; font-size:0.78rem;">${match}</span>`
    );

    // Split on " * " to detect bullet list
    const parts = text.split(/ \* /);

    if (parts.length <= 1) {
        // No bullets — just a paragraph
        return `<p style="margin:0; line-height:1.7;">${text}</p>`;
    }

    // First part = intro sentence, rest = bullet items
    const intro = parts[0];
    const bullets = parts.slice(1).filter(b => b.trim());

    const listItems = bullets
        .map(b => `<li style="margin-bottom:0.4rem; line-height:1.6;">${b.trim()}</li>`)
        .join('');

    return `
        ${intro ? `<p style="margin:0 0 0.75rem 0; line-height:1.7;">${intro}</p>` : ''}
        <ul style="margin:0; padding-left:1.25rem; color:#334155;">
            ${listItems}
        </ul>
    `;
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