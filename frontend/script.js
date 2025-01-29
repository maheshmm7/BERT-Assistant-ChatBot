class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.getElementById('send-button'),
            endChatButton: document.getElementById('end-chat-button'),
            themeToggle: document.getElementById('theme-toggle')
        };

        this.state = false;
        this.messages = [];
        // In the Chatbox constructor
        this.predefinedPrompts = [
            "Welcome to UptoSkills Chat! How can I help you today?",
            "Free Internships",
            "Where is UptoSkills located?",
            "What is Learn To Earn?",
            "What courses are available?"
        ];


        this.darkMode = false; // Initialize dark mode
    }

    display() {
        const { openButton, chatBox, sendButton, endChatButton, themeToggle } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));
        endChatButton.addEventListener('click', () => this.endChat(chatBox));
        themeToggle.addEventListener('click', () => this.toggleTheme());

        chatBox.querySelector('#user-input').addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });

        this.populateQuickReplies(chatBox);
    }

    toggleState(chatbox) {
        this.state = !this.state;

        if (this.state) {
            chatbox.classList.add('chatbox--active');
            if (this.messages.length === 0) {
                this.displayInitialPrompts(chatbox);
            }
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    displayInitialPrompts(chatbox) {
        this.predefinedPrompts.forEach(prompt => {
            this.messages.push({ name: "CUTM BOT", message: prompt, timestamp: this.getCurrentTime() });
        });
        this.updateChatText(chatbox);
    }

    populateQuickReplies(chatbox) {
        const quickReplies = [
            "What courses are available?",
            "How to contact support?",
            "Tell me about internships",
            "What is Learn To Earn?"
        ];

        const repliesContainer = chatbox.querySelector('#quick-replies');
        repliesContainer.innerHTML = quickReplies.map(reply => 
            `<button class="quick-reply-button">${reply}</button>`
        ).join('');

        repliesContainer.querySelectorAll('.quick-reply-button').forEach(button => {
            button.addEventListener('click', () => {
                this.handleQuickReply(button.innerText, chatbox);
                button.classList.add('active');
            });
        });
    }

    handleQuickReply(reply, chatbox) {
        this.messages.push({ name: "Visitor", message: reply, timestamp: this.getCurrentTime() });
        this.updateChatText(chatbox);
        this.sendMessageToBackend(reply, chatbox);
    }

    onSendButton(chatbox) {
        const input = chatbox.querySelector('#user-input');
        const message = input.value.trim();

        if (message) {
            this.messages.push({ name: "Visitor", message: message, timestamp: this.getCurrentTime() });
            this.updateChatText(chatbox);
            input.value = '';
            this.sendMessageToBackend(message, chatbox);
        }
    }

    endChat(chatbox) {
        // Clear the chat messages and show the feedback section
        this.messages = []; // Clear messages array
        chatbox.querySelector('.chatbox__messages').innerHTML = ''; // Clear chat display
        chatbox.querySelector('#feedback').style.display = 'block'; // Show feedback section
        chatbox.querySelector('#end-chat-button').style.display = 'none'; // Hide end chat button

        // Feedback buttons event listeners
        document.getElementById('thumbs-up').onclick = () => {
            this.messages.push({ name: "CUTM BOT", message: "Thank you for your response!", timestamp: this.getCurrentTime() });
            this.updateChatText(chatbox);
            this.resetChat(chatbox);
        };

        document.getElementById('thumbs-down').onclick = () => {
            this.messages.push({ name: "CUTM BOT", message: "Sorry for your inconvenience.", timestamp: this.getCurrentTime() });
            this.updateChatText(chatbox);
            this.resetChat(chatbox);
        };
    }

    resetChat(chatbox) {
        chatbox.querySelector('#feedback').style.display = 'none'; // Hide feedback section
        chatbox.querySelector('#end-chat-button').style.display = 'block'; // Show end chat button
        // Optionally, you can show a final message if needed
        this.messages.push({ name: "CUTM BOT", message: "Chat ended. Feel free to ask anything else.", timestamp: this.getCurrentTime() });
        this.updateChatText(chatbox);
    }

    typingEffect(message, chatbox) {
        const msg2 = { name: "CUTM BOT", message: "", timestamp: this.getCurrentTime() };

        if (this.messages[this.messages.length - 1]?.name === "CUTM BOT") {
            this.messages.pop();
        }

        this.messages.push(msg2);
        this.updateChatText(chatbox);

        let index = 0;
        const interval = setInterval(() => {
            if (index < message.length) {
                msg2.message += message.charAt(index);
                index++;
                this.updateChatText(chatbox);
            } else {
                clearInterval(interval);
            }
        }, 50);
    }

    async sendMessageToBackend(userInput, chatbox) {
        const loadingIndicator = chatbox.querySelector('.loading');
        const typingIndicator = chatbox.querySelector('.typing-indicator');

        loadingIndicator.style.display = 'block';
        typingIndicator.style.display = 'block';

        try {
            const response = await fetch('http://127.0.0.1:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userInput }),
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            typingIndicator.style.display = 'none';
            this.typingEffect(data.response, chatbox);
        } catch (error) {
            this.messages.push({ name: "CUTM BOT", message: "Sorry, I can't connect to the server at the moment.", timestamp: this.getCurrentTime() });
            this.updateChatText(chatbox);
            console.error('Error:', error);
        } finally {
            loadingIndicator.style.display = 'none';
        }
    }

    updateChatText(chatbox) {
        const chatMessages = chatbox.querySelector('.chatbox__messages');
        chatMessages.innerHTML = this.messages.map(msg => 
            `<div class="messages__item messages__item--${msg.name === "CUTM BOT" ? "operator" : "visitor"}">
                <div>${msg.message}</div>
                <div class="timestamp">${msg.timestamp}</div>
            </div>`
        ).join('');
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom
    }

    getCurrentTime() {
        const now = new Date();
        return `${now.getHours()}:${now.getMinutes() < 10 ? '0' + now.getMinutes() : now.getMinutes()}`;
    }

    toggleTheme() {
        const body = document.body;
        const chatbox = document.querySelector('.chatbox');
        this.darkMode = !this.darkMode;

        if (this.darkMode) {
            body.classList.add('dark-mode');
            chatbox.classList.add('dark-theme');
            this.args.themeToggle.innerHTML = "☀️"; // Sun icon for light mode
        } else {
            body.classList.remove('dark-mode');
            chatbox.classList.remove('dark-theme');
            this.args.themeToggle.innerHTML = "🌙"; // Moon icon for dark mode
        }
    }
}

const chatbox = new Chatbox();
chatbox.display();
