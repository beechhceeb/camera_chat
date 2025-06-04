let chatWindow = document.getElementById('chat-window');
let chatForm = document.getElementById('chat-form');
let userInput = document.getElementById('user-input');
let chatHistory = '';
let mode = 'recommend';
const modeRadios = document.getElementsByName('mode');

modeRadios.forEach(radio => {
    radio.addEventListener('change', function() {
        if (this.checked) mode = this.value;
    });
});

function appendMessage(text, sender, isMarkdown = false) {
    let msg = document.createElement('div');
    msg.className = 'message ' + sender;
    if (isMarkdown && sender === 'bot') {
        msg.innerHTML = marked.parse(text);
    } else {
        msg.textContent = text;
    }
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showLoading() {
    let loading = document.createElement('div');
    loading.className = 'message bot loading';
    loading.innerHTML = '<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>';
    loading.id = 'loading-msg';
    chatWindow.appendChild(loading);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function removeLoading() {
    let loading = document.getElementById('loading-msg');
    if (loading) loading.remove();
}

chatForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;
    appendMessage(message, 'user');
    userInput.value = '';
    showLoading();
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, history: chatHistory, mode })
        });
        removeLoading();
        if (res.ok) {
            const data = await res.json();
            if (data.chatbot_output) {
                appendMessage(data.chatbot_output, 'bot', true);
            } else {
                let botText = `Recommended Cameras: ${data.cameras.join(', ')}\n\nReason: ${data.reason}`;
                appendMessage(botText, 'bot', true);
            }
            // Update chatHistory with the new history from backend
            if (data.history) {
                chatHistory = data.history;
            }
        } else {
            appendMessage('Error: Could not get response.', 'bot');
        }
    } catch (err) {
        removeLoading();
        appendMessage('Error: Network problem.', 'bot');
    }
});
