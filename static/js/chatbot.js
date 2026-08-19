const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const chatHistory = document.getElementById('chatHistory');
const newChatBtn = document.getElementById('newChatBtn');

async function sendMessage() {
    const message = chatInput.value.trim();

    if (!message) return;

    appendBubble(message, 'user');
    chatInput.value = '';

    document.getElementById('chatSuggestions').style.display = 'none';

    const loadingId = `loading-${Date.now()}`;
    appendBubble('...', 'bot', loadingId);

    try {
        const token = localStorage.getItem('token');

        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                user_message: message 
            })
        });
        const data = await response.json();

        console.log('Chat status:', response.status);
        console.log('Chat response:', data);

        document.getElementById(loadingId)?.remove();

        if (!response.ok) {
            throw new Error(
                data.error || 'Failed to get AI response.'
            );
        }

        appendBubble(
            data.data.ai_response,
            'bot'
        );

    } catch (error) {
        console.error('Chat error:', error);

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
    // Escape HTML terlebih dahulu agar response AI aman
    const escapeHtml = (value) => {
        return value
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    };

    text = escapeHtml(text.trim());

    // Bold Markdown: **text** -> <strong>text</strong>
    text = text.replace(
        /\*\*(.*?)\*\*/g,
        '<strong>$1</strong>'
    );

    // Source citation
    text = text.replace(
        /\(Source[^)]+\)/g,
        '<span class="chat-source">$&</span>'
    );

    // Pecah response berdasarkan baris
    const lines = text.split(/\r?\n/);

    let html = '';
    let listItems = [];

    const flushList = () => {
        if (listItems.length === 0) return;

        html += `
            <ul>
                ${listItems
                    .map(item => `<li>${item}</li>`)
                    .join('')}
            </ul>
        `;

        listItems = [];
    };

    lines.forEach(line => {
        const trimmed = line.trim();

        // Baris kosong = paragraph spacing
        if (!trimmed) {
            flushList();
            return;
        }

        // Bullet Markdown:
        // - item
        // * item
        if (/^[-*]\s+/.test(trimmed)) {
            const item = trimmed.replace(/^[-*]\s+/, '');
            listItems.push(item);
            return;
        }

        // Kalau bukan bullet, tutup list sebelumnya
        flushList();

        // Heading sederhana
        if (/^#{1,3}\s+/.test(trimmed)) {
            const heading = trimmed.replace(/^#{1,3}\s+/, '');

            html += `<h3>${heading}</h3>`;
            return;
        }

        // Paragraph
        html += `<p>${trimmed}</p>`;
    });

    // Pastikan list terakhir ikut dimasukkan
    flushList();

    return html;
}

function renderChatHistory(histories){
    chatHistory.innerHTML = '';

    if(!histories || histories.length === 0){
        return;
    }

    histories.forEach(chat => {
        const li = document.createElement('li');

        li.textContent = chat.user_message;

        li.dataset.chatId = chat.id;

        chatHistory.appendChild(li);
    });
}

async function loadChatHistory() {
    try {
        const token = localStorage.getItem('token');

        const response = await fetch('/api/chat-history/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const result = await response.json();

        console.log('Chat history status:', response.status);
        console.log('Chat history response:', result);

        if(!response.ok){
            throw new Error(
                result.error || 'Failed to load chat history.'
            );
        }

        renderChatHistory(result.data);

    } catch (error) {
        console.error('Chat history error:', error);
    }
}

function startNewChat() {
    chatMessages.innerHTML = `
        <div class="chat-bubble chat-bubble--bot">
            Hello! I'm your GlucoSense AI assistant. How can I help you understand your metabolic health or diabetes risk today?
        </div>
    `;

    chatInput.value = '';

    document.getElementById('chatSuggestions').style.display = 'flex';

    chatInput.focus();

    chatMessages.scrollTop = 0;
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

newChatBtn.addEventListener('click', startNewChat);

document.addEventListener('DOMContentLoaded', () => {
    loadChatHistory();
});