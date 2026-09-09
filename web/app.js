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

    // Dual-Mode State
    let activeIntelligenceMode = 'cvp'; // 'cvp' or 'revenue'
    let activeRevenueEvents = [];
    let activeRevenueEventImpacts = [];

    // Screen Views
    const viewModeSelection = document.getElementById('view-mode-selection');
    const viewStep1Cvp = document.getElementById('view-step1-cvp');
    const viewStep1Revenue = document.getElementById('view-step1-revenue');

    // Navigation Buttons
    const btnSelectCvpMode = document.getElementById('btn-select-cvp-mode');
    const btnSelectRevenueMode = document.getElementById('btn-select-revenue-mode');
    const btnBackHubCvp = document.getElementById('btn-back-hub-cvp');
    const btnBackHubRevenue = document.getElementById('btn-back-hub-revenue');

    // Revenue Controls
    const formRevenueInput = document.getElementById('form-revenue-input');
    const revenueTableBody = document.getElementById('revenue-table-body');
    const btnAddEventRow = document.getElementById('btn-add-event-row');
    const btnPresetRetail = document.getElementById('btn-preset-retail');
    const btnPresetTech = document.getElementById('btn-preset-tech');
    const revenueResultsPanel = document.getElementById('revenue-results-panel');
    const canvasRevenuePestle = document.getElementById('canvas-revenue-pestle');
    const canvasRevenuePorter = document.getElementById('canvas-revenue-porter');
    const revenueImpactsList = document.getElementById('revenue-impacts-list');
    const revenuePeersList = document.getElementById('revenue-peers-list');
    const btnProceedRevenueChatbot = document.getElementById('btn-proceed-revenue-chatbot');

    // Screen Switching Handler
    function switchScreen(targetView) {
        [viewModeSelection, viewStep1Cvp, viewStep1Revenue, viewStep2].forEach(view => {
            if (view) {
                view.classList.remove('active');
                view.classList.add('hidden');
            }
        });
        if (targetView) {
            targetView.classList.remove('hidden');
            targetView.classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    if (btnSelectCvpMode) {
        btnSelectCvpMode.addEventListener('click', () => {
            activeIntelligenceMode = 'cvp';
            switchScreen(viewStep1Cvp);
        });
    }
    if (btnSelectRevenueMode) {
        btnSelectRevenueMode.addEventListener('click', () => {
            activeIntelligenceMode = 'revenue';
            switchScreen(viewStep1Revenue);
            if (revenueTableBody && revenueTableBody.children.length === 0) {
                loadRetailPreset();
            }
        });
    }
    if (btnBackHubCvp) {
        btnBackHubCvp.addEventListener('click', () => switchScreen(viewModeSelection));
    }
    if (btnBackHubRevenue) {
        btnBackHubRevenue.addEventListener('click', () => switchScreen(viewModeSelection));
    }

    function showStep1View() {
        conversationHistory = [];
        if (activeIntelligenceMode === 'revenue') {
            switchScreen(viewStep1Revenue);
        } else {
            switchScreen(viewStep1Cvp);
        }
    }

    function showStep2View() {
        switchScreen(viewStep2);
    }

    // Drag & Drop Controls
    const revenueDropzone = document.getElementById('revenue-dropzone');
    const inputFileRevenue = document.getElementById('input-file-revenue');
    const fileStatusBar = document.getElementById('file-status-bar');
    const fileNameLabel = document.getElementById('file-name-label');
    const fileCountTag = document.getElementById('file-count-tag');
    const btnClearFile = document.getElementById('btn-clear-file');
    const btnAnalyzeRevenue = document.getElementById('btn-analyze-revenue');
    const correlationMatrixList = document.getElementById('correlation-matrix-list');

    const btnPresetCsvRetail = document.getElementById('btn-preset-csv-retail');
    const btnPresetCsvTech = document.getElementById('btn-preset-csv-tech');

    let parsedRevenueSeries = [];

    // Drag & Drop Event Listeners
    if (revenueDropzone && inputFileRevenue) {
        revenueDropzone.addEventListener('click', () => inputFileRevenue.click());

        ['dragenter', 'dragover'].forEach(eventName => {
            revenueDropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                revenueDropzone.classList.add('drag-over');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            revenueDropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                revenueDropzone.classList.remove('drag-over');
            });
        });

        revenueDropzone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleUploadedFile(files[0]);
            }
        });

        inputFileRevenue.addEventListener('change', (e) => {
            if (inputFileRevenue.files.length > 0) {
                handleUploadedFile(inputFileRevenue.files[0]);
            }
        });
    }

    if (btnClearFile) {
        btnClearFile.addEventListener('click', () => {
            parsedRevenueSeries = [];
            if (inputFileRevenue) inputFileRevenue.value = '';
            if (fileStatusBar) fileStatusBar.classList.add('hidden');
        });
    }

    function handleUploadedFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            parseAndSetRevenueSeries(content, file.name);
        };
        reader.readAsText(file);
    }

    function parseAndSetRevenueSeries(content, filename = 'sales_data.csv') {
        const lines = content.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
        const series = [];

        if (filename.endsWith('.json')) {
            try {
                const jsonObj = JSON.parse(content);
                const arr = Array.isArray(jsonObj) ? jsonObj : (jsonObj.data || jsonObj.revenue_series || []);
                arr.forEach(item => {
                    series.push({
                        period: item.period || item.date || item.quarter || 'Q1',
                        revenue: floatVal(item.revenue || item.sales || item.value || 0),
                        change_pct: floatVal(item.change_pct || item.change || 0)
                    });
                });
            } catch (err) {
                alert('Invalid JSON file format.');
                return;
            }
        } else {
            let headerFound = false;
            lines.forEach(line => {
                const parts = line.split(',').map(p => p.trim().replace(/^["']|["']$/g, ''));
                if (parts.length >= 2) {
                    const first = parts[0].toLowerCase();
                    if (!headerFound && (first.includes('date') || first.includes('period') || first.includes('quarter'))) {
                        headerFound = true;
                        return;
                    }
                    const period = parts[0];
                    const val = floatVal(parts[1]);
                    const chg = parts.length >= 3 ? floatVal(parts[2]) : 0.0;
                    series.push({ period, revenue: val, change_pct: chg });
                }
            });
        }

        if (series.length === 0) {
            alert('No valid revenue rows detected in file.');
            return;
        }

        parsedRevenueSeries = series;
        if (fileNameLabel) fileNameLabel.textContent = filename;
        if (fileCountTag) fileCountTag.textContent = `${series.length} periods loaded`;
        if (fileStatusBar) fileStatusBar.classList.remove('hidden');
    }

    function floatVal(val) {
        if (typeof val === 'number') return val;
        const cleaned = strVal(val).replace('%', '').replace('$', '').replace(/,/g, '').trim();
        const parsed = parseFloat(cleaned);
        return isNaN(parsed) ? 0.0 : parsed;
    }

    function strVal(v) { return v === null || v === undefined ? '' : String(v); }

    // Sample Presets
    if (btnPresetCsvRetail) {
        btnPresetCsvRetail.addEventListener('click', () => {
            const sampleCsv = `Period,Revenue_USD,Change_Pct,Notes
2025-Q1,120000,-18.5,Import Duty Increase & Customs Congestion
2025-Q2,105000,-12.5,Port Freight Bottleneck & Logistics Delay
2025-Q3,128000,+21.9,DTC Mobile App Launch & Checkout Optimization
2025-Q4,130000,+1.5,Standard Holiday Season Sales`;
            parseAndSetRevenueSeries(sampleCsv, 'retail_apparel_sales_2025.csv');
        });
    }

    if (btnPresetCsvTech) {
        btnPresetCsvTech.addEventListener('click', () => {
            const sampleCsv = `Period,MRR_USD,Change_Pct,Notes
2025-Q1,450000,-25.0,Competitor Freemium & Enterprise Price Cut
2025-Q2,382500,-15.0,Corporate IT Spending Freeze
2025-Q3,497250,+30.0,AI Automation Launch & SOC2 Compliance Certification
2025-Q4,499000,+0.3,Standard Mid-Market Renewals`;
            parseAndSetRevenueSeries(sampleCsv, 'saas_mrr_history_2025.csv');
        });
    }

    // Submit File & Analyze
    if (btnAnalyzeRevenue) {
        btnAnalyzeRevenue.addEventListener('click', async () => {
            if (parsedRevenueSeries.length === 0) {
                alert('Please drag & drop or select a sales CSV file first, or click a Sample Dataset.');
                return;
            }

            btnAnalyzeRevenue.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Matching Revenue Timestamps & Filtering Clusters...`;
            btnAnalyzeRevenue.disabled = true;

            try {
                const response = await fetch('/api/match_revenue_clusters', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ revenue_series: parsedRevenueSeries, groq_api_key: groqApiKey })
                });

                const data = await response.json();
                btnAnalyzeRevenue.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Match Revenue Fluctuation & Filter Relevant Market Clusters`;
                btnAnalyzeRevenue.disabled = false;

                if (data.error) {
                    alert(`Error: ${data.error}`);
                    return;
                }

                activePestleVector = data.pestle_vector || [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
                activePorterVector = data.porter_vector || [0.3, 0.3, 0.3, 0.3, 0.3];
                activeUser11DVector = data.user_11d_vector || [...activePestleVector, ...activePorterVector];
                activeNearestCvps = data.nearest_cvps || [];
                activeMatchedClusters = data.matched_clusters || [];
                activeStoredClusters = data.stored_clusters || [];

                // Render Correlation Matrix
                renderCorrelationMatrix(activeMatchedClusters);

                // Render Radar Canvases
                drawPestleCanvas(canvasRevenuePestle, activePestleVector);
                drawPorterCanvas(canvasRevenuePorter, activePorterVector);
                updateLegendValues('val-rev-p', activeUser11DVector);

                // Render Benchmark Peers
                renderRevenuePeers(activeNearestCvps);

                // Show Results
                revenueResultsPanel.classList.remove('hidden');
                revenueResultsPanel.scrollIntoView({ behavior: 'smooth' });

            } catch (err) {
                btnAnalyzeRevenue.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Match Revenue Fluctuation & Filter Relevant Market Clusters`;
                btnAnalyzeRevenue.disabled = false;
                alert(`Connection error: ${err.message}`);
            }
        });
    }

    function renderCorrelationMatrix(clusters) {
        if (!correlationMatrixList) return;
        if (!clusters || clusters.length === 0) {
            correlationMatrixList.innerHTML = '<p class="text-dim">No market clusters matched.</p>';
            return;
        }

        correlationMatrixList.innerHTML = clusters.map(c => {
            const isVerified = c.stored;
            const cardClass = isVerified ? 'status-verified' : 'status-discarded';
            const badgeHtml = isVerified 
                ? `<span class="badge-verified"><i class="fa-solid fa-circle-check"></i> VERIFIED RELEVANT (STORED)</span>`
                : `<span class="badge-discarded"><i class="fa-solid fa-circle-xmark"></i> UNCORRELATED NOISE (DISCARDED)</span>`;

            return `
                <div class="cluster-card ${cardClass}">
                    <div class="cluster-header">
                        <div class="cluster-title-group">
                            <h4>${escapeHtml(c.title)}</h4>
                            <div class="cluster-meta">
                                <span><i class="fa-solid fa-calendar-days"></i> Timeframe: ${escapeHtml(c.period)}</span>
                                <span><i class="fa-solid fa-tag"></i> Category: ${escapeHtml(c.category)}</span>
                                <span><i class="fa-solid fa-chart-line"></i> Sales Impact: ${escapeHtml(c.sales_impact)}</span>
                            </div>
                        </div>
                        ${badgeHtml}
                    </div>
                    <div class="cluster-desc">${escapeHtml(c.description)}</div>
                    <div class="cluster-rationale"><strong>Filter Rationale:</strong> ${escapeHtml(c.rationale)}</div>
                </div>
            `;
        }).join('');
    }

    if (btnProceedRevenueChatbot) {
        btnProceedRevenueChatbot.addEventListener('click', () => {
            const topPeer = activeNearestCvps[0] ? activeNearestCvps[0].company : 'Benchmark Leaders';
            sidebarActiveCvp.innerHTML = `<strong>Revenue Mode Active</strong><br/><span style="font-size:12px; color:var(--text-muted);">${activeStoredClusters.length} Verified Stored Clusters</span>`;

            renderSidebarNeighbors(activeNearestCvps);
            drawPestleRadarChart(activePestleVector);
            drawPorterRadarChart(activePorterVector);
            updatePestleLegendValues(activePestleVector);
            updatePorterLegendValues(activePorterVector);

            chatMessages.innerHTML = '';
            conversationHistory = [];

            const clusterSummaries = activeStoredClusters.map(c => `[${c.period}] ${c.title} (${c.category}): ${c.sales_impact}`).join('\n');

            appendSystemMessage(`OMNISCOPE REVENUE & TEMPORAL CLUSTER CHATBOT ACTIVE

Evaluated sales time series against macro market clusters:
- Verified & Stored Clusters: ${activeStoredClusters.length}
- Primary Benchmark Peer: ${escapeHtml(topPeer)}

Verified Market Shocks:
${escapeHtml(clusterSummaries || 'None (no sales dips/spikes co-occurred)')}

I am configured to answer market intelligence queries strictly informed by your verified sales dips/rises and co-occurring market event clusters.

How can I help you analyze your verified market shocks today?`);

            switchScreen(viewStep2);
        });
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

        appendSystemMessage(`OMNISCOPE AI MARKET INTELLIGENCE ACTIVE

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
            ctx.fillStyle = '#00FF66';
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
        ctx.fillStyle = 'rgba(0, 255, 102, 0.28)';
        ctx.fill();
        ctx.strokeStyle = '#00FF66';
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
            ctx.fillStyle = '#00E5FF';
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
        ctx.fillStyle = 'rgba(0, 229, 255, 0.28)';
        ctx.fill();
        ctx.strokeStyle = '#00E5FF';
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

        const borderColors = ['#00FF66', '#00E5FF', '#10B981'];
        const badgeColors = [
            'background: rgba(0, 255, 102, 0.12); color: #00FF66; border: 1px solid rgba(0, 255, 102, 0.3);',
            'background: rgba(0, 229, 255, 0.12); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3);',
            'background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3);'
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
        const borderColors = ['#00FF66', '#00E5FF', '#10B981'];
        const badgeColors = [
            'background: rgba(0, 255, 102, 0.12); color: #00FF66; border: 1px solid rgba(0, 255, 102, 0.3);',
            'background: rgba(0, 229, 255, 0.12); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3);',
            'background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3);'
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

    function renderRevenueImpacts(impacts) {
        if (!revenueImpactsList) return;
        if (!impacts || impacts.length === 0) {
            revenueImpactsList.innerHTML = '<p class="text-dim">No event impacts available.</p>';
            return;
        }

        revenueImpactsList.innerHTML = impacts.map(item => {
            const isDip = item.impact.includes('-');
            const pillClass = isDip ? 'pill-dip' : 'pill-spike';
            return `
                <div class="impact-card-item">
                    <div>
                        <div class="ev-title">${escapeHtml(item.event)}</div>
                        <div class="ev-factor"><i class="fa-solid fa-tag"></i> Strategic Factor: ${escapeHtml(item.primary_factor)}</div>
                    </div>
                    <span class="${pillClass}">${escapeHtml(item.impact)}</span>
                </div>
            `;
        }).join('');
    }

    function renderRevenuePeers(matches) {
        if (!revenuePeersList) return;
        if (!matches || matches.length === 0) {
            revenuePeersList.innerHTML = '<p class="text-dim">No benchmark matches found.</p>';
            return;
        }

        const borderColors = ['#00E5FF', '#00FF66', '#10B981'];
        revenuePeersList.innerHTML = matches.map((m, idx) => `
            <div class="cvp-match-card" style="border-left: 4px solid ${borderColors[idx % 3]};">
                <div class="cvp-match-header">
                    <span><strong style="color: #fff; font-size: 14px;">${escapeHtml(m.company)}</strong> <span class="cvp-match-sector-tag"><i class="fa-solid fa-building"></i> ${escapeHtml(m.sector)}</span></span>
                    <span class="cvp-match-badge" style="background: rgba(0, 229, 255, 0.12); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3);">${m.similarity_pct}% Vector Similarity</span>
                </div>
                <p class="cvp-match-cvp">"${escapeHtml(m.cvp)}"</p>
            </div>
        `).join('');
    }

    function updateLegendValues(prefix, vec) {
        for (let i = 0; i < vec.length; i++) {
            const el = document.getElementById(`${prefix}${i}`);
            if (el) el.textContent = (vec[i] || 0.35).toFixed(2);
        }
    }

    function escapeHtml(str) {
        return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
});
