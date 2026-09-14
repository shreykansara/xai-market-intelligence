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
                cvp_text: this.state.activeCvpText || '',
                business_context: this.state.activeCvpText || '',
                pestle_vector: this.state.activePestleVector,
                porter_vector: this.state.activePorterVector,
                user_11d_vector: this.state.activeUser11DVector,
                nearest_cvps: this.state.activeNearestCvps,
                conversation_history: this.conversationHistory,
                chat_history: this.conversationHistory,
                groq_api_key: this.state.groqApiKey || '',
                groq_key: this.state.groqApiKey || ''
            };

            const data = await ChatApi.sendMessage(payload);
            this.removeMessage(loadingId);

            const replyText = data.response || data.text || data.reply || data.message || '';

            if (data.error && !replyText) {
                this.appendMessage('assistant', `⚠️ **Error:** ${data.error}`);
            } else if (!replyText) {
                this.appendMessage('assistant', `⚠️ **Analysis Notice:** The strategic evaluation engine could not process this prompt. Please ask a specific query regarding your CVP, PESTLE forces, or competitive market risks.`);
            } else {
                this.appendMessage('assistant', replyText);
                this.conversationHistory.push({ role: 'user', content: text });
                this.conversationHistory.push({ role: 'assistant', content: replyText });
            }
        } catch (err) {
            this.removeMessage(loadingId);
            this.appendMessage('assistant', `⚠️ **Network Error:** Could not connect to the AI Strategy server (${err.message}). Ensure the backend server is running.`);
        }
    }

    appendMessage(role, text) {
        if (!this.chatMessages) return null;
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message ${role}`;

        const isUser = role === 'user';
        const avatarIcon = isUser ? 'fa-user' : 'fa-brain';
        const badgeTag = isUser 
            ? '<span class="msg-sender-badge user-badge"><i class="fa-solid fa-circle-user"></i> You</span>'
            : '<span class="msg-sender-badge ai-badge"><i class="fa-solid fa-brain"></i> Omniscope AI Strategist</span>';
        
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const formatted = this.formatMarkdown(text);

        msgDiv.innerHTML = `
            <div class="msg-header">
                ${badgeTag}
                <span class="msg-time">${timestamp}</span>
            </div>
            <div class="msg-row">
                <div class="msg-avatar ${isUser ? 'user-avatar' : 'ai-avatar'}">
                    <i class="fa-solid ${avatarIcon}"></i>
                </div>
                <div class="msg-bubble ${isUser ? 'user-bubble' : 'ai-bubble'}">
                    ${formatted}
                </div>
            </div>
        `;

        this.chatMessages.appendChild(msgDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        return msgDiv;
    }

    appendSystemMessage(text) {
        if (!this.chatMessages) return;

        // Deduplication: prevent spamming identical system notifications consecutively
        const trimmed = (text || '').trim();
        if (this.lastSystemMessageText === trimmed) return;
        this.lastSystemMessageText = trimmed;

        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-message system';

        const lines = trimmed.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
        let title = 'System Intelligence Update';
        let bodyLines = lines;

        if (lines.length > 0 && lines[0].toUpperCase() === lines[0] && lines[0].length < 80) {
            title = lines[0];
            bodyLines = lines.slice(1);
        }

        const bodyHtml = this.formatMarkdown(bodyLines.join('\n'));

        msgDiv.innerHTML = `
            <div class="system-card">
                <div class="system-card-header">
                    <i class="fa-solid fa-circle-info system-icon"></i>
                    <span class="system-title">${CompanyIntelligence.escapeHtml(title)}</span>
                </div>
                <div class="system-card-body">
                    ${bodyHtml}
                </div>
            </div>
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
            <div class="msg-header">
                <span class="msg-sender-badge ai-badge"><i class="fa-solid fa-brain"></i> Omniscope AI Strategist</span>
                <span class="msg-time">Formulating Analysis...</span>
            </div>
            <div class="msg-row">
                <div class="msg-avatar ai-avatar"><i class="fa-solid fa-brain"></i></div>
                <div class="msg-bubble ai-bubble typing-bubble">
                    <div class="typing-indicator">
                        <span></span><span></span><span></span>
                    </div>
                    <span class="typing-label">Analyzing strategic factors & generating intelligence...</span>
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
        if (!text) return '';
        let escaped = CompanyIntelligence.escapeHtml(text);

        // Bold
        escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Italic
        escaped = escaped.replace(/\*(.*?)\*/g, '<em>$1</em>');
        // Inline code
        escaped = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');
        // Highlight strategic headers like "PESTLE Risk Factors:", "Key Business Focus Areas:"
        escaped = escaped.replace(/^([A-Z][A-Za-z0-9\s&/–—-]+:)/gm, '<strong class="chat-section-header">$1</strong>');
        // Bullet points (- ...)
        escaped = escaped.replace(/^\s*[-•]\s+(.*)$/gm, '<li class="chat-li"><span class="chat-bullet"></span><span>$1</span></li>');
        // Wrap adjacent li in ul
        escaped = escaped.replace(/(<li class="chat-li">[\s\S]*?<\/li>)+/g, '<ul class="chat-ul">$&</ul>');
        
        // Double newlines to paragraph breaks
        const paragraphs = escaped.split(/\n\s*\n/).filter(p => p.trim().length > 0);
        
        return paragraphs.map(p => {
            if (p.startsWith('<ul class="chat-ul">')) return p;
            return `<p class="chat-paragraph">${p.replace(/\n/g, '<br>')}</p>`;
        }).join('');
    }
}
