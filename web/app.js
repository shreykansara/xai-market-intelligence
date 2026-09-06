/* -------------------------------------------------------------------
   AI Explainable Market Intelligence - 2-Step Application Logic
   ------------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    // Persistent State
    let activeCvpText = '';
    let activePestleVector = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
    let activePorterVector = [0.3, 0.3, 0.3, 0.3, 0.3];
    let activeUser11DVector = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
    let activeNearestCvps = [];
    let conversationHistory = [];
    let groqApiKey = localStorage.getItem('groq_api_key') || '';

    // Step 1 Views & Controls
    const viewStep1 = document.getElementById('view-step1-cvp');
    const viewStep2 = document.getElementById('view-step2-chatbot');
    const formCvpInput = document.getElementById('form-cvp-input');
    const inputCvpText = document.getElementById('input-cvp-text');
    const step1ResultsPanel = document.getElementById('step1-results-panel');
    const cvpMatchesList = document.getElementById('cvp-matches-list');
    const btnProceedToChatbot = document.getElementById('btn-proceed-to-chatbot');

    // Step 2 Controls
    const sidebarActiveCvp = document.getElementById('sidebar-active-cvp');
    const sidebarNeighborsList = document.getElementById('sidebar-neighbors-list');
    const btnChangeCvp = document.getElementById('btn-change-cvp');
    const btnBackToStep1 = document.getElementById('btn-back-to-step1');

    // Chat Controls
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const promptsContainer = document.getElementById('prompts-container');

    // Settings Modal Controls
    const modalSettings = document.getElementById('modal-settings');
    const btnOpenSettings = document.getElementById('btn-open-settings');
    const btnCloseSettings = document.getElementById('btn-close-settings');
    const btnSaveKey = document.getElementById('btn-save-key');
    const inputGroqKey = document.getElementById('input-groq-key');

    // Canvas Elements
    const canvasPestle = document.getElementById('canvas-pestle');
    const canvasPorter = document.getElementById('canvas-porter');
    const sidebarCanvasPestle = document.getElementById('sidebar-canvas-pestle');
    const sidebarCanvasPorter = document.getElementById('sidebar-canvas-porter');

    // Init Settings
    if (groqApiKey && inputGroqKey) {
        inputGroqKey.value = groqApiKey;
    }

    // Modal Control
    if (btnOpenSettings && modalSettings) {
        btnOpenSettings.addEventListener('click', () => modalSettings.classList.add('active'));
    }
    if (btnCloseSettings && modalSettings) {
        btnCloseSettings.addEventListener('click', () => modalSettings.classList.remove('active'));
    }
    if (btnSaveKey && modalSettings && inputGroqKey) {
        btnSaveKey.addEventListener('click', () => {
            groqApiKey = inputGroqKey.value.trim();
            localStorage.setItem('groq_api_key', groqApiKey);
            modalSettings.classList.remove('active');
            appendSystemMessage('Settings saved! Groq API key active.');
        });
    }

    // Auto-resize textarea & handle Enter vs Shift+Enter
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 150) + 'px';
    });

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
        }
    });

    // Handle Quick Prompts
    promptsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('prompt-chip')) {
            userInput.value = e.target.textContent;
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Navigation: Change CVP / Back to Step 1
    if (btnChangeCvp) btnChangeCvp.addEventListener('click', showStep1View);
    if (btnBackToStep1) btnBackToStep1.addEventListener('click', showStep1View);

    function showStep1View() {
        conversationHistory = [];
        viewStep2.classList.add('hidden');
        viewStep1.classList.remove('hidden');
        step1ResultsPanel.classList.add('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function showStep2View() {
        viewStep1.classList.add('hidden');
        viewStep2.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // ===================================================================
    // STEP 1: CVP SUBMISSION & VECTOR ANALYSIS
    // ===================================================================
    formCvpInput.addEventListener('submit', async (e) => {
        e.preventDefault();
        const cvpText = inputCvpText.value.trim();
        if (!cvpText) return;

        conversationHistory = [];
        const btnSubmit = document.getElementById('btn-analyze-cvp');
        btnSubmit.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing CVP & Vector Space...`;
        btnSubmit.disabled = true;

        try {
            const response = await fetch('/api/evaluate_cvp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cvp_text: cvpText, groq_api_key: groqApiKey })
            });

            const data = await response.json();
            btnSubmit.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Analyze CVP & Generate Dual Radar Charts`;
            btnSubmit.disabled = false;

            if (data.error) {
                alert(`Error: ${data.error}`);
                return;
            }

            // Save active state
            activeCvpText = data.cvp_text;
            activePestleVector = data.pestle_vector || [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
            activePorterVector = data.porter_vector || [0.3, 0.3, 0.3, 0.3, 0.3];
            activeUser11DVector = data.user_11d_vector || [...activePestleVector, ...activePorterVector];
            activeNearestCvps = data.nearest_cvps || [];

            // Render Radar Charts
            drawPestleRadarChart(activePestleVector);
            drawPorterRadarChart(activePorterVector);
            updatePestleLegendValues(activePestleVector);
            updatePorterLegendValues(activePorterVector);

            // Render Nearest Benchmark Companies
            renderCvpMatchesList(activeNearestCvps);

            // Show Results Panel
            step1ResultsPanel.classList.remove('hidden');
            step1ResultsPanel.scrollIntoView({ behavior: 'smooth' });

        } catch (err) {
            btnSubmit.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Analyze CVP & Generate Dual Radar Charts`;
            btnSubmit.disabled = false;
            alert(`Connection failed: ${err.message}`);
        }
    });

    // Step 1 CTA: Proceed to Chatbot
    btnProceedToChatbot.addEventListener('click', () => {
        // Initialize Chatbot Sidebar Context
        sidebarActiveCvp.textContent = `"${activeCvpText}"`;
        renderSidebarNeighbors(activeNearestCvps);
        drawPestleRadarChart(activePestleVector);
        drawPorterRadarChart(activePorterVector);
        updatePestleLegendValues(activePestleVector);
        updatePorterLegendValues(activePorterVector);

        // Pre-seed Welcome Message in Chat if empty
        if (chatMessages.children.length === 0) {
            initializePersonalizedChat();
        }

        showStep2View();
    });

    function initializePersonalizedChat() {
        chatMessages.innerHTML = '';
        conversationHistory = [];

        const topPeer = activeNearestCvps[0] ? activeNearestCvps[0].company : 'Industry Leaders';
        const topSimilarity = activeNearestCvps[0] ? activeNearestCvps[0].similarity_pct : 85;

        appendSystemMessage(`PERSONALIZED INTELLIGENCE CHATBOT ACTIVE

Your Customer Value Proposition has been mapped into our 384-Dimensional Vector Space:
- Active CVP: "${escapeHtml(activeCvpText)}"
- Closest 384-D Vector Peer: ${escapeHtml(topPeer)} (${topSimilarity}% CVP Embedding Similarity)

I am strictly configured to answer personalized questions based on your specific CVP, your PESTLE macro-environment risks, and your Porter's 5 Forces industry dynamics.

How can I help you navigate your market environment today?`);
    }

    // ===================================================================
    // STEP 2: CHATBOT INTERACTION HANDLER
    // ===================================================================
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        appendUserMessage(message);
        userInput.value = '';
        userInput.style.height = 'auto';

        appendTypingIndicator();

        try {
            const payloadHistory = conversationHistory.map(item => ({
                role: item.role,
                content: item.content
            }));

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    business_context: {
                        cvp_statement: activeCvpText,
                        pestle_vector: activePestleVector,
                        porter_vector: activePorterVector
                    },
                    groq_api_key: groqApiKey,
                    chat_history: payloadHistory
                })
            });
            const data = await response.json();
            removeTypingIndicator();

            if (data.error) {
                appendSystemMessage(`Error: ${data.error}`);
            } else {
                appendSystemMessage(data.text);
                // Maintain conversation context history
                conversationHistory.push({ role: 'user', content: message });
                conversationHistory.push({ role: 'assistant', content: data.text });
                if (conversationHistory.length > 16) {
                    conversationHistory = conversationHistory.slice(-16);
                }
            }
        } catch (err) {
            removeTypingIndicator();
            appendSystemMessage(`Connection error: ${err.message}`);
        }
    });

    // ===================================================================
    // RENDER FUNCTIONS (DUAL RADARS & BENCHMARKS)
    // ===================================================================

    // Draw PESTLE Radar Chart (6 Axes)
    // Draw PESTLE Radar Chart (6 Axes)
    function drawPestleRadarChart(vector) {
        drawPestleCanvas(canvasPestle, vector);
        drawPestleCanvas(sidebarCanvasPestle, vector);
    }

    function drawPestleCanvas(canvasObj, vector) {
        if (!canvasObj) return;
        const ctx = canvasObj.getContext('2d');
        const width = canvasObj.width;
        const height = canvasObj.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(centerX, centerY) - 35;
        const labels = ['Political', 'Economic', 'Social', 'Tech', 'Legal', 'Enviro'];
        const numAxes = labels.length;

        ctx.clearRect(0, 0, width, height);

        // Grid circles
        for (let level = 1; level <= 4; level++) {
            const r = (radius / 4) * level;
            ctx.beginPath();
            ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
            ctx.stroke();
        }

        // Axes & Labels
        for (let i = 0; i < numAxes; i++) {
            const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
            const x = centerX + Math.cos(angle) * radius;
            const y = centerY + Math.sin(angle) * radius;

            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(x, y);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
            ctx.stroke();

            const lx = centerX + Math.cos(angle) * (radius + 18);
            const ly = centerY + Math.sin(angle) * (radius + 18);
            ctx.font = '10px Inter';
            ctx.fillStyle = '#06B6D4';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(labels[i], lx, ly);
        }

        // Vector Polygon
        ctx.beginPath();
        for (let i = 0; i < numAxes; i++) {
            const val = vector[i] || 0.3;
            const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
            const r = radius * val;
            const x = centerX + Math.cos(angle) * r;
            const y = centerY + Math.sin(angle) * r;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fillStyle = 'rgba(6, 182, 212, 0.35)';
        ctx.fill();
        ctx.strokeStyle = '#06B6D4';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    // Draw Porter's 5 Forces Radar Chart (5 Axes)
    function drawPorterRadarChart(vector) {
        drawPorterCanvas(canvasPorter, vector);
        drawPorterCanvas(sidebarCanvasPorter, vector);
    }

    function drawPorterCanvas(canvasObj, vector) {
        if (!canvasObj) return;
        const ctx = canvasObj.getContext('2d');
        const width = canvasObj.width;
        const height = canvasObj.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(centerX, centerY) - 35;
        const labels = ['New Entrants', 'Buyer Power', 'Supplier Power', 'Substitutes', 'Rivalry'];
        const numAxes = labels.length;

        ctx.clearRect(0, 0, width, height);

        // Grid circles
        for (let level = 1; level <= 4; level++) {
            const r = (radius / 4) * level;
            ctx.beginPath();
            ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
            ctx.stroke();
        }

        // Axes & Labels
        for (let i = 0; i < numAxes; i++) {
            const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
            const x = centerX + Math.cos(angle) * radius;
            const y = centerY + Math.sin(angle) * radius;

            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(x, y);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
            ctx.stroke();

            const lx = centerX + Math.cos(angle) * (radius + 18);
            const ly = centerY + Math.sin(angle) * (radius + 18);
            ctx.font = '10px Inter';
            ctx.fillStyle = '#8B5CF6';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(labels[i], lx, ly);
        }

        // Vector Polygon
        ctx.beginPath();
        for (let i = 0; i < numAxes; i++) {
            const val = vector[i] || 0.3;
            const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
            const r = radius * val;
            const x = centerX + Math.cos(angle) * r;
            const y = centerY + Math.sin(angle) * r;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fillStyle = 'rgba(139, 92, 246, 0.35)';
        ctx.fill();
        ctx.strokeStyle = '#8B5CF6';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    function updatePestleLegendValues(vec) {
        for (let i = 0; i < 6; i++) {
            const el = document.getElementById(`val-p${i}`);
            if (el) el.textContent = (vec[i] || 0.3).toFixed(2);
            const sEl = document.getElementById(`sidebar-val-p${i}`);
            if (sEl) sEl.textContent = (vec[i] || 0.3).toFixed(2);
        }
    }

    function updatePorterLegendValues(vec) {
        for (let i = 0; i < 5; i++) {
            const el = document.getElementById(`val-p${i+6}`);
            if (el) el.textContent = (vec[i] || 0.3).toFixed(2);
            const sEl = document.getElementById(`sidebar-val-p${i+6}`);
            if (sEl) sEl.textContent = (vec[i] || 0.3).toFixed(2);
        }
    }

    function renderCvpMatchesList(matches) {
        if (!matches || matches.length === 0) {
            cvpMatchesList.innerHTML = '<p class="text-dim">No benchmark matches found.</p>';
            return;
        }

        const borderColors = ['#00f2fe', '#10b981', '#a855f7'];
        const badgeColors = [
            'background: rgba(0, 242, 254, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3);',
            'background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3);',
            'background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(192, 132, 252, 0.3);'
        ];

        cvpMatchesList.innerHTML = matches.map((m, idx) => `
            <div class="cvp-match-card" style="border-left: 4px solid ${borderColors[idx % 3]};">
                <div class="cvp-match-header">
                    <span><strong style="color: #fff; font-size: 15px;">${escapeHtml(m.company)}</strong> <span class="cvp-match-sector-tag"><i class="fa-solid fa-building"></i> ${escapeHtml(m.sector)}</span></span>
                    <span class="cvp-match-badge" style="${badgeColors[idx % 3]}">${m.similarity_pct}% CVP Similarity</span>
                </div>
                <p class="cvp-match-cvp">"${escapeHtml(m.cvp)}"</p>
            </div>
        `).join('');
    }

    function renderSidebarNeighbors(matches) {
        if (!matches || matches.length === 0) return;
        const borderColors = ['#00f2fe', '#10b981', '#a855f7'];
        const badgeColors = [
            'background: rgba(0, 242, 254, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3);',
            'background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3);',
            'background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(192, 132, 252, 0.3);'
        ];

        sidebarNeighborsList.innerHTML = matches.map((m, idx) => `
            <div class="neighbor-item" style="border-left: 4px solid ${borderColors[idx % 3]};">
                <div class="neighbor-header">
                    <span class="neighbor-company-name">${escapeHtml(m.company)}</span>
                    <span class="neighbor-badge" style="${badgeColors[idx % 3]}">${m.similarity_pct}%</span>
                </div>
                <div class="neighbor-sector">
                    <i class="fa-solid fa-layer-group"></i> ${escapeHtml(m.sector)}
                </div>
                ${m.cvp ? `<div class="neighbor-cvp-snippet">"${escapeHtml(m.cvp)}"</div>` : ''}
            </div>
        `).join('');
    }

    // Messaging UI Helpers
    function appendUserMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message user-msg';
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-user"></i></div>
            <div class="msg-body"><p>${escapeHtml(text)}</p></div>
        `;
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendSystemMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message system-msg';
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="msg-body">${formatMarkdown(text)}</div>
        `;
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendTypingIndicator() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message system-msg typing-msg';
        msgDiv.id = 'typing-indicator';
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="msg-body"><p><i class="fa-solid fa-spinner fa-spin"></i> Analyzing personalized market risk...</p></div>
        `;
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function formatMarkdown(text) {
        if (!text) return '';
        let cleaned = text
            .replace(/#+\s*/g, '')
            .replace(/\*/g, '');

        let formatted = cleaned
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/^\s*-\s+(.*)$/gm, '<li>$1</li>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');

        return `<p>${formatted}</p>`;
    }

    function escapeHtml(str) {
        return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
});
