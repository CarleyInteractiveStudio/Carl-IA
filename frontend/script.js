document.addEventListener('DOMContentLoaded', () => {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const messageList = document.getElementById('message-list');
    const chatWindow = document.getElementById('chat-window');

    // IMPORTANTE: Deberás reemplazar esto con la URL de tu Space "orquestador"
    const ORCHESTRATOR_URL = "http://localhost:8000/chat/"; // URL de ejemplo para desarrollo local

    messageForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const userText = messageInput.value.trim();

        if (userText !== '') {
            appendUserMessage(userText);
            messageInput.value = '';
            showTypingIndicator();

            try {
                const response = await fetch(ORCHESTRATOR_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompt: userText }),
                });

                removeTypingIndicator();

                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor.');
                }

                const data = await response.json();
                handleCarlResponse(data);

            } catch (error) {
                removeTypingIndicator();
                console.error("Error al contactar al cerebro de Carl:", error);
                appendCarlTextMessage("Lo siento, estoy teniendo problemas para conectar con mis sistemas. Inténtalo de nuevo más tarde.");
            }
        }
    });

    function hexToUint8Array(hexString) {
        const bytes = new Uint8Array(hexString.length / 2);
        for (let i = 0; i < hexString.length; i += 2) {
            bytes[i / 2] = parseInt(hexString.substr(i, 2), 16);
        }
        return bytes;
    }

    function handleCarlResponse(data) {
        if (data.type === 'image') {
            const imageBytes = hexToUint8Array(data.content);
            const imageBlob = new Blob([imageBytes], { type: 'image/png' });
            const imageUrl = URL.createObjectURL(imageBlob);
            appendCarlImageMessage(imageUrl);
        } else {
            appendCarlTextMessage(data.content);
        }
    }

    function appendUserMessage(text) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'user-message');

        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.textContent = text;

        messageElement.appendChild(contentElement);
        messageList.appendChild(messageElement);
        scrollToBottom();
    }

    function appendCarlTextMessage(text) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'carl-message');

        const avatar = document.createElement('img');
        avatar.src = 'assets/Carl IA.png';
        avatar.alt = 'Carl IA';

        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.innerHTML = text;

        messageElement.appendChild(avatar);
        messageElement.appendChild(contentElement);
        messageList.appendChild(messageElement);
        scrollToBottom();
    }

    function appendCarlImageMessage(imageUrl) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'carl-message');

        const avatar = document.createElement('img');
        avatar.src = 'assets/Carl IA.png';
        avatar.alt = 'Carl IA';

        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content', 'image-content');

        const image = document.createElement('img');
        image.src = imageUrl;
        image.alt = "Imagen generada por Carl IA";
        image.style.maxWidth = '100%';
        image.style.borderRadius = '12px';

        contentElement.appendChild(image);
        messageElement.appendChild(avatar);
        messageElement.appendChild(contentElement);
        messageList.appendChild(messageElement);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.id = 'typing-indicator';
        typingElement.classList.add('message', 'carl-message');

        const avatar = document.createElement('img');
        avatar.src = 'assets/Carl IA.png';

        const content = document.createElement('div');
        content.classList.add('message-content');
        content.textContent = '...';

        typingElement.appendChild(avatar);
        typingElement.appendChild(content);
        messageList.appendChild(typingElement);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const typingElement = document.getElementById('typing-indicator');
        if (typingElement) {
            typingElement.remove();
        }
    }

    function scrollToBottom() {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});
