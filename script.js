document.addEventListener('DOMContentLoaded', () => {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const messageList = document.getElementById('message-list');
    const chatWindow = document.getElementById('chat-window');

    const carlResponseText = `¡Hola! Soy Carl, tu asistente de IA universal. Aunque todavía estoy en desarrollo, mi objetivo es ayudarte a crear cosas increíbles. Podré generar música, imágenes, videos, e incluso crear videojuegos completos y sitios web con nuestro motor 'Creative Engine'. También puedo ayudarte a programar y mucho más.<br><br>Este proyecto es muy ambicioso. No estamos creando el modelo de IA desde cero, sino que usaremos los mejores modelos de código abierto. Para que yo pueda funcionar a mi máximo potencial, necesitamos tu apoyo para adquirir servidores potentes. ¡Juntos podemos construir el futuro de la creación digital!<br><br><a href="https://carleyinteractivestudio.github.io/Carley-Interactive-Studio/#carly-bot" target="_blank" class="support-button">Apoyar</a>`;

    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const messageText = messageInput.value.trim();

        if (messageText !== '') {
            appendUserMessage(messageText);
            messageInput.value = '';
            chatWindow.scrollTop = chatWindow.scrollHeight;

            setTimeout(() => {
                appendCarlMessage();
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }, 1000);
        }
    });

    function appendUserMessage(text) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'user-message');

        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.textContent = text;

        messageElement.appendChild(contentElement);
        messageList.appendChild(messageElement);
    }

    function appendCarlMessage() {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'carl-message');

        const imgElement = document.createElement('img');
        imgElement.src = 'assets/Carl IA.png';
        imgElement.alt = 'Carl IA';

        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.innerHTML = carlResponseText;

        messageElement.appendChild(imgElement);
        messageElement.appendChild(contentElement);
        messageList.appendChild(messageElement);
    }
});
