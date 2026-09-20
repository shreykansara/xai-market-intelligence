/**
 * Omniscope AI - Main Modular Application Entry Point
 * Orchestrates navigation, CVP workflow, sales workflow, chat assistant, and company intelligence.
 */

import { CvpWorkflow } from './modules/cvp-workflow.js';
import { SalesWorkflow } from './modules/sales-workflow.js';
import { ChatAssistant } from './modules/chat-assistant.js';
import { NavigationManager } from './modules/navigation-manager.js';
import { ChartVisualizer } from './modules/chart-visualizer.js';
import { CompanyIntelligence } from './modules/company-intelligence.js';
import { CompanyApi } from './modules/api-client.js';
import { AuthManager } from './modules/auth-manager.js';
import { HistoryManager } from './modules/history-manager.js';
import { DashboardManager } from './modules/dashboard-manager.js';

document.addEventListener('DOMContentLoaded', () => {
    // Top-level subsystem references (declared at scope top to eliminate TDZ issues)
    let chatAssistant;
    let cvpWorkflow;
    let salesWorkflow;
    let authManager;
    let historyManager;
    let dashboardManager;
    let nav;

    // Centralized Application State
    const state = {
        activeIntelligenceMode: 'cvp',
        activeCvpText: '',
        activePestleVector: [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
        activePorterVector: [0.3, 0.3, 0.3, 0.3, 0.3],
        activeUser11DVector: [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
        activeNearestCvps: [],
        activeOverlayPeer: null,
        groqApiKey: localStorage.getItem('groq_api_key') || ''
    };

    // 1. Initialize Assistant Subsystem
    chatAssistant = new ChatAssistant(state);
    window.chatAssistant = chatAssistant;

    // 2. Initialize User Authentication Subsystem
    authManager = new AuthManager({
        onAuthStateChanged: (user) => {
            historyManager?.updateCountBadges();
            dashboardManager?.refresh();
        },
        onLoginSuccess: (user) => {
            dashboardManager?.refresh();
        }
    });
    window.authManager = authManager;

    // Helper to keep sidebar radars, active context, and benchmark peers in perfect sync
    function syncSidebarRadars() {
        const sideCanvasPestle = document.getElementById('sidebar-canvas-pestle');
        const sideCanvasPorter = document.getElementById('sidebar-canvas-porter');
        const sidebarCvpEl = document.getElementById('sidebar-active-cvp');
        const sidebarNeighborsList = document.getElementById('sidebar-neighbors-list');
        const activeCvpCard = document.querySelector('.active-cvp-card');

        // 0. Hide CVP Context in sidebar when running in sales/revenue mode
        if (activeCvpCard) {
            activeCvpCard.style.display = (state.activeIntelligenceMode === 'revenue') ? 'none' : '';
        }

        const btnBackStep1 = document.getElementById('btn-back-step1');
        if (btnBackStep1) {
            if (state.activeIntelligenceMode === 'revenue') {
                btnBackStep1.innerHTML = '<i class="fa-solid fa-arrow-left"></i> Step 1 Sales';
                btnBackStep1.title = 'Return to Step 1 Sales & Revenue Analysis';
            } else {
                btnBackStep1.innerHTML = '<i class="fa-solid fa-arrow-left"></i> Step 1 CVP';
                btnBackStep1.title = 'Return to Step 1 CVP Input';
            }
        }

        // 1. Sync Active Context Text
        if (sidebarCvpEl) {
            if (state.activeIntelligenceMode === 'revenue') {
                const count = salesWorkflow?.parsedSeries?.length || 4;
                const topCluster = state.activeClusters?.[0]?.cluster_name || 'Market Analysis';
                sidebarCvpEl.textContent = state.activeCvpText || `Revenue Fluctuation Model (${count} Periods • ${topCluster})`;
            } else if (state.activeCvpText) {
                sidebarCvpEl.textContent = `"${state.activeCvpText}"`;
            } else {
                sidebarCvpEl.textContent = "Omniscope Market Intelligence Session";
            }
        }

        // 2. Vectors & Radars
        const pestleVec = state.activePestleVector || [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
        const porterVec = state.activePorterVector || [0.3, 0.3, 0.3, 0.3, 0.3];
        const peerPestle = state.activeOverlayPeer ? state.activeOverlayPeer.pestle_vector : null;
        const peerPorter = state.activeOverlayPeer ? state.activeOverlayPeer.porter_vector : null;

        if (sideCanvasPestle) {
            ChartVisualizer.drawPestleCanvas(sideCanvasPestle, pestleVec, peerPestle);
        }
        if (sideCanvasPorter) {
            ChartVisualizer.drawPorterCanvas(sideCanvasPorter, porterVec, peerPorter);
        }

        // 3. Update legend values
        if (state.activeIntelligenceMode === 'revenue') {
            ChartVisualizer.updateSalesLegendValues(pestleVec, porterVec);
        } else {
            ChartVisualizer.updateCvpLegendValues(pestleVec, porterVec);
        }

        // 4. Update Sidebar Benchmark Peers if present
        if (sidebarNeighborsList && state.activeNearestCvps && state.activeNearestCvps.length > 0) {
            const borderColors = ['var(--brand-primary)', 'var(--color-growth)', 'var(--border-medium)', 'var(--color-metric)', 'var(--color-neutral)'];
            sidebarNeighborsList.innerHTML = state.activeNearestCvps.map((m, idx) => `
                <div class="cvp-match-card" style="border-left: 3px solid ${borderColors[idx % borderColors.length]};">
                    <div class="cvp-match-header">
                        <div class="cvp-match-identity">
                            <div class="cvp-match-company-row">
                                <button type="button" class="company-profile-btn" data-company="${CompanyIntelligence.escapeHtml(m.company)}" title="Click to view on-DB company intelligence">
                                    <span>${CompanyIntelligence.escapeHtml(m.company)}</span>
                                    <i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 11px; opacity: 0.8;"></i>
                                </button>
                            </div>
                            <div class="cvp-match-sector-row">
                                <span class="cvp-match-sector-tag"><i class="fa-solid fa-building"></i> ${CompanyIntelligence.escapeHtml(m.sector || 'Enterprise')}</span>
                            </div>
                        </div>
                        <span class="cvp-match-badge">${m.similarity_pct}% Match</span>
                    </div>
                    <p class="cvp-match-cvp">"${CompanyIntelligence.escapeHtml(m.cvp || '')}"</p>
                    <div class="neighbor-card-actions">
                        <button type="button" class="btn-peer-action" data-company="${CompanyIntelligence.escapeHtml(m.company)}">
                            <i class="fa-solid fa-id-card"></i> Profile
                        </button>
                        <button type="button" class="btn-peer-action cyan btn-peer-radar" data-company="${CompanyIntelligence.escapeHtml(m.company)}">
                            <i class="fa-solid fa-chart-pie"></i> Overlay
                        </button>
                    </div>
                </div>
            `).join('');

            // Bind click events on sidebar items
            sidebarNeighborsList.querySelectorAll('.company-profile-btn, .btn-peer-action:not(.btn-peer-radar)').forEach(btn => {
                btn.addEventListener('click', () => {
                    const compName = btn.getAttribute('data-company');
                    if (compName) {
                        CompanyIntelligence.loadAndShowProfile(
                            compName,
                            state.activePestleVector,
                            state.activePorterVector,
                            (peer) => overlayPeerRadar(peer.company)
                        );
                    }
                });
            });

            sidebarNeighborsList.querySelectorAll('.btn-peer-radar').forEach(btn => {
                btn.addEventListener('click', () => {
                    const compName = btn.getAttribute('data-company');
                    if (compName) overlayPeerRadar(compName);
                });
            });
        }
    }

    // Helper for overlaying peer on radars WITHOUT flashing modal
    async function overlayPeerRadar(companyName) {
        if (!companyName) return;

        const isFlatOrInvalid = (vec) => !vec || !Array.isArray(vec) || vec.length < 5 || vec.every(v => Math.abs(Number(v) - 0.3) < 0.001);

        let comp = state.activeNearestCvps?.find(c => c.company?.toLowerCase() === companyName.toLowerCase());
        if (!comp || isFlatOrInvalid(comp.pestle_vector) || isFlatOrInvalid(comp.porter_vector)) {
            try {
                const res = await CompanyApi.getProfile(companyName);
                if (res?.success && res?.company) {
                    comp = res.company;
                    const existing = state.activeNearestCvps?.find(c => c.company?.toLowerCase() === companyName.toLowerCase());
                    if (existing) {
                        existing.pestle_vector = comp.pestle_vector;
                        existing.porter_vector = comp.porter_vector;
                    }
                }
            } catch (err) {
                console.warn('Failed to load peer profile for overlay:', err);
            }
        }

        if (!comp || !comp.pestle_vector || !comp.porter_vector) {
            alert(`Unable to load benchmark radar vectors for "${companyName}".`);
            return;
        }

        state.activeOverlayPeer = comp;

        // Redraw radars on both main and sidebar canvases WITHOUT opening/closing the modal
        const canvasPestle = document.getElementById('canvas-pestle');
        const sideCanvasPestle = document.getElementById('sidebar-canvas-pestle');
        const canvasPorter = document.getElementById('canvas-porter');
        const sideCanvasPorter = document.getElementById('sidebar-canvas-porter');

        ChartVisualizer.drawPestleCanvas(canvasPestle, state.activePestleVector, comp.pestle_vector);
        ChartVisualizer.drawPestleCanvas(sideCanvasPestle, state.activePestleVector, comp.pestle_vector);
        ChartVisualizer.drawPorterCanvas(canvasPorter, state.activePorterVector, comp.porter_vector);
        ChartVisualizer.drawPorterCanvas(sideCanvasPorter, state.activePorterVector, comp.porter_vector);

        syncSidebarRadars();

        chatAssistant.appendSystemMessage(`STRATEGIC BENCHMARK OVERLAY ACTIVE

Overlaying **${CompanyIntelligence.escapeHtml(comp.company)}** (${CompanyIntelligence.escapeHtml(comp.sector || 'Peer')}) onto your dual radars in electric cyan dashed lines.
Compare your internal CVP risks directly against ${CompanyIntelligence.escapeHtml(comp.company)}'s verified profile.`);
    }

    // 3. Initialize Workspace History Subsystem
    historyManager = new HistoryManager(authManager, {
        onRestoreCvp: (analysis) => {
            const data = analysis.results_data || analysis;
            state.activeIntelligenceMode = 'cvp';
            state.activeCvpText = data.cvp_text || analysis.input_data?.cvp_text || '';
            state.activePestleVector = data.pestle_vector || [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
            state.activePorterVector = data.porter_vector || [0.3, 0.3, 0.3, 0.3, 0.3];
            state.activeUser11DVector = data.user_11d_vector || [...state.activePestleVector, ...state.activePorterVector];
            state.activeNearestCvps = data.nearest_cvps || [];
            state.activeCvpPrognosis = data.investment_prognosis || null;

            cvpWorkflow?.syncStateToUi();
            syncSidebarRadars();
            nav?.switchScreen(document.getElementById('view-step1-cvp'));
        },
        onRestoreRevenue: (analysis) => {
            const data = analysis.results_data || analysis;
            state.activeIntelligenceMode = 'revenue';
            state.activePestleVector = data.pestle_vector || [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
            state.activePorterVector = data.porter_vector || [0.3, 0.3, 0.3, 0.3, 0.3];
            state.activeUser11DVector = data.user_11d_vector || [...state.activePestleVector, ...state.activePorterVector];
            state.activeNearestCvps = data.nearest_cvps || [];
            state.activeClusters = data.active_clusters || [];

            const inputSeries = analysis.input_data?.revenue_series || [];
            if (inputSeries.length > 0 && salesWorkflow) {
                salesWorkflow.parsedSeries = inputSeries;
            }

            salesWorkflow?.renderInvestmentScore(data.investment_prognosis || null);
            salesWorkflow?.renderLaggingNewsMatrix(data.matched_news || []);
            salesWorkflow?.renderStrategicEvidence(data.audit_categories || null, data.evidence_records || []);
            salesWorkflow?.renderRevenuePeers(state.activeNearestCvps);

            const canvasPestle = document.getElementById('canvas-revenue-pestle');
            const canvasPorter = document.getElementById('canvas-revenue-porter');
            ChartVisualizer.drawPestleCanvas(canvasPestle, state.activePestleVector);
            ChartVisualizer.drawPorterCanvas(canvasPorter, state.activePorterVector);
            ChartVisualizer.updateSalesLegendValues(state.activePestleVector, state.activePorterVector);

            const resultsPanel = document.getElementById('revenue-results-panel');
            if (resultsPanel) resultsPanel.classList.remove('hidden');

            syncSidebarRadars();
            nav?.switchScreen(document.getElementById('view-step1-revenue'));
        },
        onRestoreConversation: (conv) => {
            nav?.switchScreen(document.getElementById('view-step2-chatbot'));
            chatAssistant?.restoreConversation(conv);
            syncSidebarRadars();
        }
    });
    window.historyManager = historyManager;

    // 4. Initialize Executive Dashboard Subsystem
    dashboardManager = new DashboardManager(authManager, {
        onRestoreCvp: (analysis) => historyManager.callbacks.onRestoreCvp(analysis),
        onRestoreRevenue: (analysis) => historyManager.callbacks.onRestoreRevenue(analysis),
        onRestoreConversation: (conv) => historyManager.callbacks.onRestoreConversation(conv)
    });
    window.dashboardManager = dashboardManager;

    // 5. Initialize CVP Subsystem
    cvpWorkflow = new CvpWorkflow(state, {
        onCvpEvaluated: (data) => {
            syncSidebarRadars();
            const topPeer = data.nearest_cvps?.[0]?.company || 'Industry Benchmark';
            const topSimilarity = data.nearest_cvps?.[0]?.similarity_pct || 85;

            chatAssistant.appendSystemMessage(`REAL-TIME EMBEDDINGS EVALUATED & 500-COMPANY PEERS ALIGNED

Your Customer Value Proposition: "${CompanyIntelligence.escapeHtml(data.cvp_text)}"
- Nearest Benchmark Company: **${CompanyIntelligence.escapeHtml(topPeer)}** (${topSimilarity}% Cosine Similarity)
- Real-time TF-IDF & Distance comparison executed across all 500 benchmark companies.
- Dual PESTLE and Porter radar charts updated. Click any company card to inspect their on-DB profile.`);
        },
        onPeerRadarOverlay: (companyName) => {
            overlayPeerRadar(companyName);
        }
    });

    // 6. Initialize Sales Subsystem
    salesWorkflow = new SalesWorkflow(state, {
        onSalesAnalyzed: (data) => {
            syncSidebarRadars();
            chatAssistant.appendSystemMessage(`REVENUE FLUCTUATIONS & 11-CATEGORY AUDIT TRAIL COMPUTED

- Grouped revenue series into ${data.active_clusters?.length || 0} fluctuation severity clusters.
- Formulated collective strategic decisions based on dominant market event categories.
- Mapped lagging indicator news items with causal likelihood scoring.
- Comprehensive rationale audit trail generated across all 11 PESTLE & Porter categories.`);
        },
        onPeerRadarOverlay: (companyName) => {
            overlayPeerRadar(companyName);
        }
    });

    // Preset dataset helpers
    function loadRetailPreset() {
        salesWorkflow.loadPreset('retail');
    }

    function loadTechPreset() {
        salesWorkflow.loadPreset('tech');
    }

    // 7. Initialize Navigation Manager
    nav = new NavigationManager(state, {
        onRevenueModeActivated: () => {
            if (!salesWorkflow.parsedSeries || salesWorkflow.parsedSeries.length === 0) {
                salesWorkflow.loadPreset('retail');
            }
            syncSidebarRadars();
        },
        onProceedToChatbot: () => {
            syncSidebarRadars();
            requestAnimationFrame(() => syncSidebarRadars());
            setTimeout(() => syncSidebarRadars(), 80);

            if (state.activeIntelligenceMode === 'revenue' && salesWorkflow?.parsedSeries?.length > 0) {
                const count = salesWorkflow?.parsedSeries?.length || 4;
                const topPeer = state.activeNearestCvps?.[0]?.company || 'Inditex / Zara';
                const sim = state.activeNearestCvps?.[0]?.similarity_pct || 91.2;
                chatAssistant.appendSystemMessage(`REVENUE FLUCTUATION INTELLIGENCE COGNITIVE SESSION

Analyzed ${count} revenue financial intervals against verified database market news events.
Nearest Vector Peer: **${CompanyIntelligence.escapeHtml(topPeer)}** (${sim}% Vector Similarity)

You can ask about lagging indicator causal scoring, specific fluctuation drivers, or tactical mitigation decisions.`);
            } else if (state.activeCvpText) {
                chatAssistant.appendSystemMessage(`OMNISCOPE AI EXPLAINABILITY SESSION READY

Current Context: "${CompanyIntelligence.escapeHtml(state.activeCvpText)}"
Nearest 500-Company Vector Peer: ${CompanyIntelligence.escapeHtml(state.activeNearestCvps[0]?.company || 'Benchmark Peer')}

You can ask about strategic risk differentiations, competitive positioning, or request actionable mitigation strategies.`);
            } else {
                if (!chatAssistant.conversationHistory || chatAssistant.conversationHistory.length === 0) {
                    chatAssistant.startNewConversation();
                }
            }
        },
        onLoadRetailPreset: () => loadRetailPreset(),
        onLoadTechPreset: () => loadTechPreset(),
        onDashboardActivated: () => dashboardManager?.refresh()
    });
    window.navigationManager = nav;

    // 8. Settings Modal Handlers
    const modalSettings = document.getElementById('modal-settings');
    const btnOpenSettings = document.getElementById('btn-open-settings');
    const btnCloseSettings = document.getElementById('btn-close-settings');
    const btnSaveKey = document.getElementById('btn-save-key');
    const inputGroqKey = document.getElementById('input-groq-key');

    if (inputGroqKey && state.groqApiKey) inputGroqKey.value = state.groqApiKey;
    btnOpenSettings?.addEventListener('click', () => modalSettings?.classList.add('active'));
    btnCloseSettings?.addEventListener('click', () => modalSettings?.classList.remove('active'));
    btnSaveKey?.addEventListener('click', () => {
        state.groqApiKey = inputGroqKey?.value.trim() || '';
        localStorage.setItem('groq_api_key', state.groqApiKey);
        modalSettings?.classList.remove('active');
        chatAssistant.appendSystemMessage('Settings saved! Groq API key active.');
    });

    // 9. Company Profile Modal Handlers
    const modalProfile = document.getElementById('modal-company-profile');
    const btnCloseProfile = document.getElementById('btn-close-comp-modal');
    btnCloseProfile?.addEventListener('click', () => modalProfile?.classList.remove('active'));
    modalProfile?.addEventListener('click', (e) => {
        if (e.target === modalProfile) modalProfile.classList.remove('active');
    });

    const btnModalAskAi = document.getElementById('btn-modal-ask-ai');
    btnModalAskAi?.addEventListener('click', () => {
        const compName = document.getElementById('modal-comp-name')?.textContent;
        if (!compName) return;
        modalProfile?.classList.remove('active');
        nav.switchScreen(document.getElementById('view-step2-chatbot'));
        const userInput = document.getElementById('user-input');
        if (userInput) {
            userInput.value = `Can you compare my CVP against ${compName}? Specifically explain our major differences across PESTLE macro risks and Porter's 5 forces, and suggest how my business model can differentiate most effectively.`;
            userInput.focus();
            userInput.style.height = 'auto';
            userInput.style.height = Math.min(userInput.scrollHeight, 150) + 'px';
            document.getElementById('chat-form')?.dispatchEvent(new Event('submit'));
        }
    });

    // 10. Boot User Session and sync guest data if available
    authManager.init();

    // 11. Initial sync of sidebar radar canvases and dashboard data
    syncSidebarRadars();
    dashboardManager.refresh();

    console.log('[Omniscope AI] Modular frontend architecture initialized successfully with user authentication & persistence.');
});
