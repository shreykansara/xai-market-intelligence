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

document.addEventListener('DOMContentLoaded', () => {
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

    // Initialize Assistant Subsystem
    const chatAssistant = new ChatAssistant(state);

    // Initialize CVP Subsystem
    const cvpWorkflow = new CvpWorkflow(state, {
        onCvpEvaluated: (data) => {
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

    // Helper for overlaying peer on radars
    async function overlayPeerRadar(companyName) {
        const comp = await CompanyIntelligence.loadAndShowProfile(
            companyName,
            state.activePestleVector,
            state.activePorterVector
        );
        if (!comp) return;

        state.activeOverlayPeer = comp;
        const modal = document.getElementById('modal-company-profile');
        if (modal) modal.classList.remove('active');

        // Redraw radars
        const canvasPestle = document.getElementById('canvas-pestle');
        const sideCanvasPestle = document.getElementById('sidebar-canvas-pestle');
        const canvasPorter = document.getElementById('canvas-porter');
        const sideCanvasPorter = document.getElementById('sidebar-canvas-porter');

        ChartVisualizer.drawPestleCanvas(canvasPestle, state.activePestleVector, comp.pestle_vector);
        ChartVisualizer.drawPestleCanvas(sideCanvasPestle, state.activePestleVector, comp.pestle_vector);
        ChartVisualizer.drawPorterCanvas(canvasPorter, state.activePorterVector, comp.porter_vector);
        ChartVisualizer.drawPorterCanvas(sideCanvasPorter, state.activePorterVector, comp.porter_vector);

        chatAssistant.appendSystemMessage(`STRATEGIC BENCHMARK OVERLAY ACTIVE

Overlaying **${CompanyIntelligence.escapeHtml(comp.company)}** (${CompanyIntelligence.escapeHtml(comp.sector || 'Peer')}) onto your dual radars in electric cyan dashed lines.
Compare your internal CVP risks directly against ${CompanyIntelligence.escapeHtml(comp.company)}'s verified profile.`);
    }

    // Initialize Sales Subsystem
    const salesWorkflow = new SalesWorkflow(state, {
        onSalesAnalyzed: (data) => {
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
        const sampleCsv = `Period,Revenue_USD,Change_Pct,Notes
2026-07-W2 (Jul 08-14),118500,-16.8,Tariff Escalation Anticipation & Pre-emptive Port Ingestion
2026-07-W4 (Jul 22-28),104200,-12.1,Red Sea Maritime Shipping Disruptions & Logistics Delays
2026-08-W2 (Aug 05-11),132400,+27.1,Digital-First Neighbourhood Format Launch & Retail Store Unveiling
2026-08-W4 (Aug 19-25),134100,+1.3,Standard Consumer Energy Tax Holiday & Mid-Quarter Equilibrium`;
        salesWorkflow.parseAndSetRevenueSeries(sampleCsv, 'retail_apparel_sales_jul_aug_2026.csv');
    }

    function loadTechPreset() {
        const sampleCsv = `Period,Revenue_USD,Change_Pct,Notes
2026-07-W1 (Jul 01-07),245000,+18.4,Enterprise LLM Cloud Migration Acceleration & Contract Renewals
2026-07-W3 (Jul 15-21),208000,-15.1,Global Semiconductor Supply Chain Bottleneck & Hardware Allocation Delay
2026-08-W1 (Aug 01-07),215000,+3.4,Mid-Summer Enterprise SaaS Expansion & Routine Upsells
2026-08-W3 (Aug 15-21),172000,-20.0,EU AI Act Stringent Sovereign Compliance Enforcement Pause`;
        salesWorkflow.parseAndSetRevenueSeries(sampleCsv, 'enterprise_tech_saas_jul_aug_2026.csv');
    }

    // Initialize Navigation Manager
    const nav = new NavigationManager(state, {
        onRevenueModeActivated: () => {
            if (!salesWorkflow.parsedSeries || salesWorkflow.parsedSeries.length === 0) {
                loadRetailPreset();
            }
        },
        onProceedToChatbot: () => {
            if (state.activeCvpText) {
                chatAssistant.appendSystemMessage(`OMNISCOPE AI EXPLAINABILITY SESSION READY

Current Context: "${CompanyIntelligence.escapeHtml(state.activeCvpText)}"
Nearest 500-Company Vector Peer: ${CompanyIntelligence.escapeHtml(state.activeNearestCvps[0]?.company || 'Benchmark Peer')}

You can ask about strategic risk differentiations, competitive positioning, or request actionable mitigation strategies.`);
            }
        },
        onLoadRetailPreset: () => loadRetailPreset(),
        onLoadTechPreset: () => loadTechPreset()
    });

    // Settings Modal
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

    // Company Profile Modal Close Handler
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

    console.log('[Omniscope AI] Modular frontend architecture initialized successfully.');
});
