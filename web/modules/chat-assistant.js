/**
 * Omniscope AI - Chat Assistant Module
 * Manages Step 2 interactive explainability chat, quick prompts, and system messages.
 */

import { ChatApi } from './api-client.js';
import { CompanyIntelligence } from './company-intelligence.js';

export class ChatAssistant {
    constructor(state) {
        this.state = state;
        this.conversationHistory = [];
        this.initDom();
    }

    initDom() {
        this.chatForm = document.getElementById('chat-form');
        this.userInput = document.getElementById('user-input');
        this.chatMessages = document.getElementById('chat-messages');
        this.promptsContainer = document.getElementById('prompts-container');

        this.bindEvents();
    }

    bindEvents() {
        if (this.chatForm) {
            this.chatForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleUserSubmit();
            });
        }

        if (this.userInput) {
            this.userInput.addEventListener('input', () => {
                this.userInput.style.height = 'auto';
                this.userInput.style.height = Math.min(this.userInput.scrollHeight, 150) + 'px';
            });

            this.userInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.chatForm?.dispatchEvent(new Event('submit', { cancelable: true }));
                }
            });
        }

        if (this.promptsContainer) {
            this.promptsContainer.addEventListener('click', (e) => {
                if (e.target.classList.contains('prompt-chip')) {
                    if (this.userInput) {
                        this.userInput.value = e.target.textContent;
                        this.chatForm?.dispatchEvent(new Event('submit'));
                    }
                }
            });
        }
    }

    async handleUserSubmit() {
        const text = this.userInput?.value.trim();
        if (!text) return;

        this.appendMessage('user', text);
        this.userInput.value = '';
        this.userInput.style.height = 'auto';

        const loadingId = this.appendLoadingIndicator();

        try {
            const payload = {
                message: text,
                cvp_text: this.state.activeCvpText,
                pestle_vector: this.state.activePestleVector,
                porter_vector: this.state.activePorterVector,
                user_11d_vector: this.state.activeUser11DVector,
                nearest_cvps: this.state.activeNearestCvps,
                conversation_history: this.conversationHistory,
                groq_api_key: this.state.groqApiKey
            };

            const data = await ChatApi.sendMessage(payload);
            this.removeMessage(loadingId);

            if (data.error) {
                this.appendMessage('assistant', `⚠️ **Error:** ${data.error}`);
            } else {
                this.appendMessage('assistant', data.response);
                this.conversationHistory.push({ role: 'user', content: text });
                this.conversationHistory.push({ role: 'assistant', content: data.response });
            }
        } catch (err) {
            this.removeMessage(loadingId);
            this.appendMessage('assistant', `⚠️ **Network Error:** ${err.message}`);
        }
    }

    appendMessage(role, text) {
        if (!this.chatMessages) return null;
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message ${role}`;

        const avatarIcon = role === 'user' ? 'fa-user' : 'fa-brain';
        const formatted = this.formatMarkdown(text);

        msgDiv.innerHTML = `
            <div class="msg-avatar"><i class="fa-solid ${avatarIcon}"></i></div>
            <div class="msg-bubble">${formatted}</div>
        `;

        this.chatMessages.appendChild(msgDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        return msgDiv;
    }

    appendSystemMessage(text) {
        if (!this.chatMessages) return;
        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-message system';
        msgDiv.innerHTML = `
            <div class="msg-avatar"><i class="fa-solid fa-circle-info"></i></div>
            <div class="msg-bubble system-bubble">${this.formatMarkdown(text)}</div>
        `;
        this.chatMessages.appendChild(msgDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    appendLoadingIndicator() {
        const id = 'msg-loading-' + Date.now();
        if (!this.chatMessages) return id;
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = 'chat-message assistant';
        msgDiv.innerHTML = `
            <div class="msg-avatar"><i class="fa-solid fa-brain"></i></div>
            <div class="msg-bubble">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        this.chatMessages.appendChild(msgDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        return id;
    }

    removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    formatMarkdown(text) {
        let formatted = CompanyIntelligence.escapeHtml(text)
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/^\s*-\s+(.*)$/gm, '<li>$1</li>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');

        return `<p>${formatted}</p>`;
    }
}
