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

    // Company Profile Modal Controls
    const modalCompanyProfile = document.getElementById('modal-company-profile');
    const btnCloseCompModal = document.getElementById('btn-close-comp-modal');
    const modalCompName = document.getElementById('modal-comp-name');
    const modalCompSector = document.getElementById('modal-comp-sector');
    const modalCompProduct = document.getElementById('modal-comp-product');
    const modalCompCvp = document.getElementById('modal-comp-cvp');
    const modalCompTargetCustomer = document.getElementById('modal-comp-target-customer');
    const modalCompNeed = document.getElementById('modal-comp-need');
    const modalCompBenefit = document.getElementById('modal-comp-benefit');
    const comparePestleBars = document.getElementById('compare-pestle-bars');
    const comparePorterBars = document.getElementById('compare-porter-bars');
    const btnModalOverlayRadar = document.getElementById('btn-modal-overlay-radar');
    const btnModalAskAi = document.getElementById('btn-modal-ask-ai');

    // Quick Edit CVP Modal Controls
    const modalQuickEditCvp = document.getElementById('modal-quick-edit-cvp');
    const btnCloseQuickCvp = document.getElementById('btn-close-quick-cvp');
    const btnCancelQuickCvp = document.getElementById('btn-cancel-quick-cvp');
    const btnSaveQuickCvp = document.getElementById('btn-save-quick-cvp');
    const inputQuickCvpText = document.getElementById('input-quick-cvp-text');
    const btnQuickEditCvp = document.getElementById('btn-quick-edit-cvp');

    // Sidebar Action Buttons
    const btnBackStep1 = document.getElementById('btn-back-step1');
    const btnSidebarHub = document.getElementById('btn-sidebar-hub');
    const btnSidebarHome = document.getElementById('btn-sidebar-home');

    let currentModalCompany = null;
    let activeOverlayPeer = null;

    // Canvas Elements
    const canvasPestle = document.getElementById('canvas-pestle');
    const canvasPorter = document.getElementById('canvas-porter');
    const sidebarCanvasPestle = document.getElementById('sidebar-canvas-pestle');
    const sidebarCanvasPorter = document.getElementById('sidebar-canvas-porter');
    // Revenue Fluctuation & Evidence DOM Elements
    const fluctuationClustersList = document.getElementById('fluctuation-clusters-list');
    const strategicEvidenceList = document.getElementById('strategic-evidence-list');
    const auditPestleList = document.getElementById('audit-pestle-categories-list');
    const auditPorterList = document.getElementById('audit-porter-categories-list');
    const btnExpandAllAudit = document.getElementById('btn-expand-all-audit');
    const btnCollapseAllAudit = document.getElementById('btn-collapse-all-audit');
    let activeFluctuationClusters = [];
    let activeEvidenceRecords = [];
    let activeMatchedNews = [];
    let activeAuditCategories = null;

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

    // Company Profile Modal Close Handlers
    if (btnCloseCompModal && modalCompanyProfile) {
        btnCloseCompModal.addEventListener('click', () => modalCompanyProfile.classList.remove('active'));
        modalCompanyProfile.addEventListener('click', (e) => {
            if (e.target === modalCompanyProfile) modalCompanyProfile.classList.remove('active');
        });
    }

    // Quick Edit CVP Modal Handlers
    if (btnQuickEditCvp && modalQuickEditCvp) {
        btnQuickEditCvp.addEventListener('click', () => {
            if (inputQuickCvpText) {
                inputQuickCvpText.value = activeCvpText;
            }
            modalQuickEditCvp.classList.add('active');
            if (inputQuickCvpText) inputQuickCvpText.focus();
        });
    }
    if (btnCloseQuickCvp && modalQuickEditCvp) {
        btnCloseQuickCvp.addEventListener('click', () => modalQuickEditCvp.classList.remove('active'));
    }
    if (btnCancelQuickCvp && modalQuickEditCvp) {
        btnCancelQuickCvp.addEventListener('click', () => modalQuickEditCvp.classList.remove('active'));
    }
    if (modalQuickEditCvp) {
        modalQuickEditCvp.addEventListener('click', (e) => {
            if (e.target === modalQuickEditCvp) modalQuickEditCvp.classList.remove('active');
        });
    }

    // Left Panel: Return to Step 1 & Edit CVP
    if (btnChangeCvp) {
        btnChangeCvp.addEventListener('click', () => {
            showStep1View();
            if (inputCvpText) {
                inputCvpText.value = activeCvpText;
                inputCvpText.focus();
                inputCvpText.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }

    // Left Panel: Navigation buttons
    if (btnBackStep1) {
        btnBackStep1.addEventListener('click', () => showStep1View());
    }
    if (btnSidebarHub) {
        btnSidebarHub.addEventListener('click', () => switchScreen(viewModeSelection));
    }
    if (btnSidebarHome) {
        btnSidebarHome.addEventListener('click', () => switchScreen(viewLandingPage));
    }

    // Quick Edit CVP Save Action
    if (btnSaveQuickCvp) {
        btnSaveQuickCvp.addEventListener('click', async () => {
            const newCvp = inputQuickCvpText.value.trim();
            if (!newCvp) {
                alert('Please enter a CVP statement.');
                return;
            }

            btnSaveQuickCvp.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Re-evaluating 500 Companies...`;
            btnSaveQuickCvp.disabled = true;

            try {
                const res = await fetch('/api/evaluate_cvp', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cvp_text: newCvp, groq_api_key: groqApiKey })
                });
                const data = await res.json();
                btnSaveQuickCvp.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Re-evaluate & Update CVP`;
                btnSaveQuickCvp.disabled = false;

                if (data.error) {
                    alert(`Error: ${data.error}`);
                    return;
                }

                activeCvpText = data.cvp_text;
                activePestleVector = data.pestle_vector || [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
                activePorterVector = data.porter_vector || [0.3, 0.3, 0.3, 0.3, 0.3];
                activeUser11DVector = data.user_11d_vector || [...activePestleVector, ...activePorterVector];
                activeNearestCvps = data.nearest_cvps || [];

                sidebarActiveCvp.textContent = `"${activeCvpText}"`;
                if (inputCvpText) inputCvpText.value = activeCvpText;

                drawPestleRadarChart(activePestleVector, activeOverlayPeer ? activeOverlayPeer.pestle_vector : null);
                drawPorterRadarChart(activePorterVector, activeOverlayPeer ? activeOverlayPeer.porter_vector : null);
                updatePestleLegendValues(activePestleVector);
                updatePorterLegendValues(activePorterVector);

                renderSidebarNeighbors(activeNearestCvps);
                renderCvpMatchesList(activeNearestCvps);

                modalQuickEditCvp.classList.remove('active');

                const topPeer = activeNearestCvps[0] ? activeNearestCvps[0].company : 'Industry Benchmark';
                const topSimilarity = activeNearestCvps[0] ? activeNearestCvps[0].similarity_pct : 85;

                appendSystemMessage(`CVP MODIFIED & VECTOR SPACE RECALIBRATED

Updated CVP: "${escapeHtml(activeCvpText)}"
- Closest 500-Company Vector Peer: ${escapeHtml(topPeer)} (${topSimilarity}% CVP Similarity)
- Real-time TF-IDF & Cosine Alignment re-indexed against 500 benchmark companies.
- Dual PESTLE & Porter radars updated with your new strategic coordinates.`);

            } catch (err) {
                btnSaveQuickCvp.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Re-evaluate & Update CVP`;
                btnSaveQuickCvp.disabled = false;
                alert(`Update failed: ${err.message}`);
            }
        });
    }

    // Profile Modal Actions
    if (btnModalOverlayRadar) {
        btnModalOverlayRadar.addEventListener('click', () => {
            if (!currentModalCompany) return;
            activeOverlayPeer = currentModalCompany;
            drawPestleRadarChart(activePestleVector, activeOverlayPeer.pestle_vector);
            drawPorterRadarChart(activePorterVector, activeOverlayPeer.porter_vector);
            modalCompanyProfile.classList.remove('active');

            appendSystemMessage(`STRATEGIC BENCHMARK OVERLAY ACTIVE

Overlaying **${escapeHtml(currentModalCompany.company)}** (${escapeHtml(currentModalCompany.sector || 'Peer')}) onto your dual radars in electric cyan dashed lines.
Compare your internal CVP risks directly against ${escapeHtml(currentModalCompany.company)}'s verified profile.`);
        });
    }

    if (btnModalAskAi) {
        btnModalAskAi.addEventListener('click', () => {
            if (!currentModalCompany) return;
            const compName = currentModalCompany.company;
            modalCompanyProfile.classList.remove('active');
            showStep2View();
            if (userInput) {
                userInput.value = `Can you compare my CVP against ${compName}? Specifically explain our major differences across PESTLE macro risks and Porter's 5 forces, and suggest how my business model can differentiate most effectively.`;
                userInput.focus();
                userInput.style.height = 'auto';
                userInput.style.height = Math.min(userInput.scrollHeight, 150) + 'px';
                chatForm.dispatchEvent(new Event('submit'));
            }
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
    const viewLandingPage = document.getElementById('view-landing-page');
    const viewModeSelection = document.getElementById('view-mode-selection');
    const viewStep1Cvp = document.getElementById('view-step1-cvp');
    const viewStep1Revenue = document.getElementById('view-step1-revenue');

    // Navigation Buttons
    const btnNavLaunchApp = document.getElementById('btn-nav-launch-app');
    const btnHeroLaunchCvp = document.getElementById('btn-hero-launch-cvp');
    const btnHeroLaunchRevenue = document.getElementById('btn-hero-launch-revenue');
    const heroPresetTesla = document.getElementById('hero-preset-tesla');
    const heroPresetStripe = document.getElementById('hero-preset-stripe');
    const btnFounderLaunch = document.getElementById('btn-founder-launch');
    const btnInvestorLaunch = document.getElementById('btn-investor-launch');
    const btnBannerLaunchHub = document.getElementById('btn-banner-launch-hub');
    const btnBackLandingHub = document.getElementById('btn-back-landing-hub');
    const brandLogoHome = document.getElementById('brand-logo-home');

    const btnSelectCvpMode = document.getElementById('btn-select-cvp-mode');
    const btnSelectRevenueMode = document.getElementById('btn-select-revenue-mode');
    const btnBackHubCvp = document.getElementById('btn-back-hub-cvp');
    const btnBackHubRevenue = document.getElementById('btn-back-hub-revenue');

    // CVP Preset Chips
    const btnPresetCvpTesla = document.getElementById('btn-preset-cvp-tesla');
    const btnPresetCvpStripe = document.getElementById('btn-preset-cvp-stripe');

    // Footer Links
    const footLinkLanding = document.getElementById('foot-link-landing');
    const footLinkHub = document.getElementById('foot-link-hub');
    const footLinkCvp = document.getElementById('foot-link-cvp');
    const footLinkRevenue = document.getElementById('foot-link-revenue');

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
        [viewLandingPage, viewModeSelection, viewStep1Cvp, viewStep1Revenue, viewStep2].forEach(view => {
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

    // Landing Page Navigation Handlers
    if (btnNavLaunchApp) {
        btnNavLaunchApp.addEventListener('click', () => switchScreen(viewModeSelection));
    }
    if (btnBannerLaunchHub) {
        btnBannerLaunchHub.addEventListener('click', () => switchScreen(viewModeSelection));
    }
    if (btnBackLandingHub) {
        btnBackLandingHub.addEventListener('click', () => switchScreen(viewLandingPage));
    }
    if (brandLogoHome) {
        brandLogoHome.addEventListener('click', (e) => {
            e.preventDefault();
            switchScreen(viewLandingPage);
        });
    }

    if (footLinkLanding) footLinkLanding.addEventListener('click', (e) => { e.preventDefault(); switchScreen(viewLandingPage); });
    if (footLinkHub) footLinkHub.addEventListener('click', (e) => { e.preventDefault(); switchScreen(viewModeSelection); });
    if (footLinkCvp) footLinkCvp.addEventListener('click', (e) => { e.preventDefault(); activeIntelligenceMode = 'cvp'; switchScreen(viewStep1Cvp); });
    if (footLinkRevenue) footLinkRevenue.addEventListener('click', (e) => { e.preventDefault(); activeIntelligenceMode = 'revenue'; switchScreen(viewStep1Revenue); });

    // Mode Launch Actions
    if (btnHeroLaunchCvp) {
        btnHeroLaunchCvp.addEventListener('click', () => {
            activeIntelligenceMode = 'cvp';
            switchScreen(viewStep1Cvp);
        });
    }
    if (btnFounderLaunch) {
        btnFounderLaunch.addEventListener('click', () => {
            activeIntelligenceMode = 'cvp';
            switchScreen(viewStep1Cvp);
        });
    }

    if (btnHeroLaunchRevenue) {
        btnHeroLaunchRevenue.addEventListener('click', () => {
            activeIntelligenceMode = 'revenue';
            switchScreen(viewStep1Revenue);
        });
    }
    if (btnInvestorLaunch) {
        btnInvestorLaunch.addEventListener('click', () => {
            activeIntelligenceMode = 'revenue';
            switchScreen(viewStep1Revenue);
        });
    }

    if (btnSelectCvpMode) {
        btnSelectCvpMode.addEventListener('click', () => {
            activeIntelligenceMode = 'cvp';
            switchScreen(viewStep1Cvp);
        });
    }
    function loadRetailPreset() {
        const sampleCsv = `Period,Revenue_USD,Change_Pct,Notes
2026-07-W2 (Jul 08-14),118500,-16.8,Tariff Escalation Anticipation & Pre-emptive Port Ingestion
2026-07-W4 (Jul 22-28),104200,-12.1,Red Sea Maritime Shipping Disruptions & Logistics Delays
2026-08-W2 (Aug 05-11),132400,+27.1,Digital-First Neighbourhood Format Launch & Retail Store Unveiling
2026-08-W4 (Aug 19-25),134100,+1.3,Standard Consumer Energy Tax Holiday & Mid-Quarter Equilibrium`;
        parseAndSetRevenueSeries(sampleCsv, 'retail_apparel_sales_jul_aug_2026.csv');
    }

    if (btnSelectRevenueMode) {
        btnSelectRevenueMode.addEventListener('click', () => {
            activeIntelligenceMode = 'revenue';
            switchScreen(viewStep1Revenue);
            if (!parsedRevenueSeries || parsedRevenueSeries.length === 0) {
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

    // CVP Demo Preset Handlers - Loads input data beforehand, waits for user to click Generate
    const teslaCvpText = "For eco-conscious drivers and tech enthusiasts seeking sustainable high-performance mobility, Tesla is an electric automotive and energy platform that delivers long-range zero-emission vehicles with full autonomous driving software and over-the-air software updates.";
    const stripeCvpText = "For internet businesses and developer-first startups needing frictionless global commerce infrastructure, Stripe is a unified financial infrastructure platform that enables instant multi-currency card processing, subscription billing, and fraud prevention through modern REST APIs.";

    function loadCvpPresetText(text) {
        activeIntelligenceMode = 'cvp';
        switchScreen(viewStep1Cvp);
        if (inputCvpText) {
            inputCvpText.value = text;
            inputCvpText.focus();
        }
        // Ensure output data is NOT there until user clicks Generate
        const step1Results = document.getElementById('step1-results');
        if (step1Results) step1Results.classList.add('hidden');
        const btnSubmit = document.getElementById('btn-analyze-cvp');
        if (btnSubmit) {
            btnSubmit.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Analyze CVP & Generate Dual Radar Charts`;
            btnSubmit.disabled = false;
        }
    }

    if (btnPresetCvpTesla) btnPresetCvpTesla.addEventListener('click', () => loadCvpPresetText(teslaCvpText));
    if (heroPresetTesla) heroPresetTesla.addEventListener('click', () => loadCvpPresetText(teslaCvpText));

    if (btnPresetCvpStripe) btnPresetCvpStripe.addEventListener('click', () => loadCvpPresetText(stripeCvpText));
    if (heroPresetStripe) heroPresetStripe.addEventListener('click', () => loadCvpPresetText(stripeCvpText));


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
            const previewBox = document.getElementById('revenue-input-preview-box');
            if (previewBox) previewBox.classList.add('hidden');
            if (revenueResultsPanel) revenueResultsPanel.classList.add('hidden');
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
                        change_pct: floatVal(item.change_pct || item.change || 0),
                        notes: item.notes || item.description || ''
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
                    const notes = parts.length >= 4 ? parts.slice(3).join(', ') : '';
                    series.push({ period, revenue: val, change_pct: chg, notes: notes });
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

        // Render Input Preview Table beforehand so user can inspect preset inputs before generating
        const previewBox = document.getElementById('revenue-input-preview-box');
        const previewTbody = document.getElementById('revenue-preview-tbody');
        if (previewTbody) {
            previewTbody.innerHTML = '';
            series.forEach(item => {
                const tr = document.createElement('tr');
                const chgColor = item.change_pct < 0 ? '#ff4d4f' : (item.change_pct > 0 ? '#00FF66' : '#8892b0');
                const chgSign = item.change_pct > 0 ? '+' : '';
                tr.innerHTML = `
                    <td style="font-weight: 600; color: #fff; padding: 6px 10px;">${escapeHtml(item.period)}</td>
                    <td style="color: var(--text-muted); font-family: monospace; padding: 6px 10px;">$${Number(item.revenue).toLocaleString()}</td>
                    <td style="font-weight: 700; color: ${chgColor}; font-family: monospace; padding: 6px 10px;">${chgSign}${item.change_pct.toFixed(1)}%</td>
                    <td style="color: var(--text-muted); font-style: italic; padding: 6px 10px;">${escapeHtml(item.notes || 'Operational Performance')}</td>
                `;
                previewTbody.appendChild(tr);
            });
            if (previewBox) previewBox.classList.remove('hidden');
        }

        // Keep output results panel hidden until user clicks Generate / Match
        if (revenueResultsPanel) {
            revenueResultsPanel.classList.add('hidden');
        }
        if (btnAnalyzeRevenue) {
            btnAnalyzeRevenue.disabled = false;
            btnAnalyzeRevenue.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Match Revenue Fluctuation & Filter Relevant Market Clusters`;
        }
    }

    function floatVal(val) {
        if (typeof val === 'number') return val;
        const cleaned = strVal(val).replace('%', '').replace('$', '').replace(/,/g, '').trim();
        const parsed = parseFloat(cleaned);
        return isNaN(parsed) ? 0.0 : parsed;
    }

    function strVal(v) { return v === null || v === undefined ? '' : String(v); }

    // Sample Presets (July - August 2026)
    if (btnPresetCsvRetail) {
        btnPresetCsvRetail.addEventListener('click', () => {
            const sampleCsv = `Period,Revenue_USD,Change_Pct,Notes
2026-07-W2 (Jul 08-14),118500,-16.8,Tariff Escalation Anticipation & Pre-emptive Port Ingestion
2026-07-W4 (Jul 22-28),104200,-12.1,Red Sea Maritime Shipping Disruptions & Logistics Delays
2026-08-W2 (Aug 05-11),132400,+27.1,Digital-First Neighbourhood Format Launch & Retail Store Unveiling
2026-08-W4 (Aug 19-25),134100,+1.3,Standard Consumer Energy Tax Holiday & Mid-Quarter Equilibrium`;
            parseAndSetRevenueSeries(sampleCsv, 'retail_apparel_sales_jul_aug_2026.csv');
        });
    }

    if (btnPresetCsvTech) {
        btnPresetCsvTech.addEventListener('click', () => {
            const sampleCsv = `Period,MRR_USD,Change_Pct,Notes
2026-07-W3 (Jul 15-21),395000,-18.2,Cybersecurity Cross-Border Trade Probe & Procurement Freeze
2026-08-W1 (Aug 01-07),352000,-10.9,Enterprise Fixed-Fare Pricing Competition & Below-Cost Price Rivalry
2026-08-W3 (Aug 15-21),464000,+31.8,Global Demand for AI Tech Surge & Open-Source Infrastructure Expansion
2026-08-Close (Aug 26-31),465800,+0.4,Month-End Predictable Contract Renewals & Seasonal Equilibrium`;
            parseAndSetRevenueSeries(sampleCsv, 'saas_mrr_history_jul_aug_2026.csv');
        });
    }

    // Submit File & Analyze
    if (btnAnalyzeRevenue) {
        btnAnalyzeRevenue.addEventListener('click', async () => {
            if (parsedRevenueSeries.length === 0) {
                alert('Please drag & drop or select a sales CSV file first, or click a Sample Dataset.');
                return;
            }

            btnAnalyzeRevenue.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Fluctuations & Evaluating Lagging Indicator News...`;
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
                activeMatchedNews = data.matched_news || [];
                activeFluctuationClusters = data.active_clusters || [];
                activeEvidenceRecords = data.evidence_records || [];
                activeStoredClusters = data.stored_clusters || [];
                activeAuditCategories = data.audit_categories || null;

                // 1. Render Fluctuation Clusters & Collective Decisions
                renderFluctuationClusters(activeFluctuationClusters);

                // 2. Render Lagging Indicator News & Likelihood Scoring Matrix
                renderLaggingNewsMatrix(activeMatchedNews);

                // 3. Render Radar Canvases for Revenue
                drawPestleCanvas(canvasRevenuePestle, activePestleVector);
                drawPorterCanvas(canvasRevenuePorter, activePorterVector);
                updateRevenueRadarLegends(activeUser11DVector);

                // 4. Render Strategic Evidence & Rationales Audit Trail
                renderStrategicEvidence(activeAuditCategories, activeEvidenceRecords);

                // 5. Render 500-Company Benchmark Peers
                renderRevenuePeers(activeNearestCvps);

                // Show Results
                if (revenueResultsPanel) {
                    revenueResultsPanel.classList.remove('hidden');
                    revenueResultsPanel.scrollIntoView({ behavior: 'smooth' });
                }

            } catch (err) {
                btnAnalyzeRevenue.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Match Revenue Fluctuation & Filter Relevant Market Clusters`;
                btnAnalyzeRevenue.disabled = false;
                alert(`Connection error: ${err.message}`);
            }
        });
    }

    // 1. Render Fluctuation Clusters & Collective Decisions
    function renderFluctuationClusters(clusters) {
        if (!fluctuationClustersList) return;
        if (!clusters || clusters.length === 0) {
            fluctuationClustersList.innerHTML = '<p class="text-dim">No fluctuation clusters detected.</p>';
            return;
        }

        fluctuationClustersList.innerHTML = clusters.map(c => `
            <div class="fluctuation-cluster-card cluster-${escapeHtml(c.severity)}">
                <div class="cluster-card-header">
                    <div class="cluster-title-wrap">
                        <h4>${escapeHtml(c.cluster_name)}</h4>
                        <span class="cluster-band-badge badge-band-${escapeHtml(c.severity)}">${escapeHtml(c.badge)}</span>
                    </div>
                    <span style="font-weight:700; font-family:var(--font-heading); color:${c.avg_change_pct >= 0 ? 'var(--accent-green)' : '#f87171'}; font-size:14px;">
                        Average Fluctuation: ${c.avg_change_pct >= 0 ? '+' : ''}${c.avg_change_pct.toFixed(1)}%
                    </span>
                </div>
                <div class="cluster-meta-row">
                    <span><i class="fa-solid fa-calendar-days"></i> Periods (${c.period_count}): ${c.periods.map(p => `<span class="cluster-period-pill">${escapeHtml(p)}</span>`).join(' ')}</span>
                    <span class="dominant-category-tag"><i class="fa-solid fa-tag"></i> Dominant News Category: ${escapeHtml(c.dominant_category)} (${c.dominant_category_pct}% frequency)</span>
                </div>
                <div class="collective-decision-box">
                    <i class="fa-solid fa-lightbulb decision-icon"></i>
                    <div class="decision-text">
                        <strong>COLLECTIVE STRATEGIC DECISION:</strong><br>
                        ${escapeHtml(c.collective_decision)}
                    </div>
                </div>
            </div>
        `).join('');
    }

    // 2. Render Lagging Indicator News Assignment & Likelihood Scoring Matrix
    function renderLaggingNewsMatrix(newsItems) {
        if (!correlationMatrixList) return;
        if (!newsItems || newsItems.length === 0) {
            correlationMatrixList.innerHTML = '<p class="text-dim">No market events matched.</p>';
            return;
        }

        correlationMatrixList.innerHTML = newsItems.map(it => {
            const isDip = it.change_pct < -3.0;
            const isSurge = it.change_pct > 3.0;
            const cardClass = isDip ? 'dip' : (isSurge ? 'surge' : 'flat');

            let likelihoodClass = 'likelihood-mod';
            let fillColor = '#00E5FF';
            if (it.likelihood_score >= 85) {
                likelihoodClass = 'likelihood-high';
                fillColor = '#00FF66';
            } else if (it.likelihood_score < 50) {
                likelihoodClass = 'likelihood-low';
                fillColor = '#6b7280';
            }

            return `
                <div class="lagging-news-card ${cardClass}">
                    <div class="lagging-card-top">
                        <div style="flex: 1;">
                            <div class="news-headline-text">${escapeHtml(it.news_headline)}</div>
                            <span class="news-category-badge"><i class="fa-solid fa-layer-group"></i> ${escapeHtml(it.category)}</span>
                            <div style="font-size:12px; color:var(--text-muted); margin-top:5px;">
                                <i class="fa-solid fa-calendar-days"></i> Recorded Period: <strong>${escapeHtml(it.period)}</strong> | Sales Fluctuation: <span class="${isDip ? 'fluctuation-pill-dip' : 'fluctuation-pill-spike'}">${it.change_pct >= 0 ? '+' : ''}${it.change_pct.toFixed(1)}%</span>
                            </div>
                        </div>
                        <div class="likelihood-meter-box">
                            <span class="likelihood-badge ${likelihoodClass}">
                                <i class="fa-solid fa-crosshairs"></i> ${it.likelihood_score}% Likelihood
                            </span>
                            <div class="likelihood-bar-track">
                                <div class="likelihood-bar-fill" style="width: ${it.likelihood_score}%; background: ${fillColor};"></div>
                            </div>
                            <span style="font-size:10.5px; color:var(--text-dim); margin-top:3px;">${escapeHtml(it.causal_status)}</span>
                        </div>
                    </div>
                    <div class="lagging-rationale-box">
                        <strong>Lagging Indicator Relationship:</strong> ${escapeHtml(it.lag_window)}<br>
                        <strong>Filter Rationale:</strong> ${escapeHtml(it.filter_rationale)}
                    </div>
                </div>
            `;
        }).join('');
    }

    // 4. Render Strategic Evidence & Rationales Audit Trail (11 Categories, PESTLE + Porter)
    function handleAccordionClick(e) {
        if (e.target.closest('.evidence-source-link')) return;
        const accordion = e.currentTarget.closest('.audit-category-accordion');
        if (accordion) {
            accordion.classList.toggle('expanded');
        }
    }

    function renderStrategicEvidence(auditCategories, fallbackEvidenceRecords) {
        const DIMENSION_ICONS = {
            political: 'fa-landmark',
            economic: 'fa-chart-line',
            social: 'fa-users',
            technological: 'fa-microchip',
            legal: 'fa-scale-balanced',
            environmental: 'fa-leaf',
            threat_of_new_entrants: 'fa-door-open',
            bargaining_power_of_buyers: 'fa-cart-shopping',
            bargaining_power_of_suppliers: 'fa-truck-field',
            threat_of_substitutes: 'fa-repeat',
            competitive_rivalry: 'fa-hand-fist'
        };

        function renderCategoryAccordion(cat, index, isExpandedDefault) {
            const icon = DIMENSION_ICONS[cat.key] || 'fa-layer-group';
            const isGroupPestle = cat.group === 'pestle';
            const groupColor = isGroupPestle ? 'var(--accent-cyan)' : 'var(--accent-green)';

            let badgeClass = 'score-badge-mod';
            if (cat.assigned_score >= 0.65) badgeClass = 'score-badge-high';
            else if (cat.assigned_score < 0.40) badgeClass = 'score-badge-low';

            const dominantFluc = cat.dominant_fluctuation || 'Empirical Baseline (0.0%)';
            let flucClass = 'fluctuation-pill-base';
            if (dominantFluc.includes('-')) flucClass = 'fluctuation-pill-dip';
            else if (dominantFluc.includes('+')) flucClass = 'fluctuation-pill-spike';

            const hasActiveShock = dominantFluc.includes('+') || dominantFluc.includes('-');
            const isExpanded = isExpandedDefault || hasActiveShock;

            const newsCardsHtml = (cat.news_items || []).map(item => {
                const isShockItem = item.associated_fluctuation && (item.associated_fluctuation.includes('-') || item.associated_fluctuation.includes('+'));
                const flucBadge = isShockItem
                    ? `<span class="${item.associated_fluctuation.includes('-') ? 'fluctuation-pill-dip' : 'fluctuation-pill-spike'}">${escapeHtml(item.associated_fluctuation)}</span>`
                    : `<span class="fluctuation-pill-base">${escapeHtml(item.associated_fluctuation || 'Empirical Baseline')}</span>`;

                const sourceLinkBtn = item.source_link && item.source_link.startsWith('http')
                    ? `<a href="${escapeHtml(item.source_link)}" target="_blank" rel="noopener noreferrer" class="evidence-source-link" title="Open source article in new tab">
                           <i class="fa-solid fa-arrow-up-right-from-square"></i>
                           <span>Original Source</span>
                       </a>`
                    : `<span class="evidence-source-link" style="opacity:0.6; cursor:default;" title="Verified PostgreSQL database record">
                           <i class="fa-solid fa-database"></i>
                           <span>DB Record</span>
                       </span>`;

                return `
                    <div class="audit-news-card ${isShockItem ? 'primary-shock' : ''}">
                        <div class="audit-news-top">
                            <div class="audit-news-quote">
                                <i class="fa-solid fa-quote-left" style="opacity:0.5; margin-right:6px; color:${groupColor};"></i>
                                "${escapeHtml(item.headline)}"
                            </div>
                            ${sourceLinkBtn}
                        </div>
                        <div class="audit-news-meta">
                            <span><i class="fa-regular fa-calendar" style="margin-right:4px;"></i>${escapeHtml(item.published_date)}</span>
                            <span>•</span>
                            <span><i class="fa-solid fa-location-dot" style="margin-right:4px;"></i>${escapeHtml(item.location_affected || 'World')}</span>
                            <span>•</span>
                            ${flucBadge}
                            <span>•</span>
                            <span style="color:${groupColor}; font-weight:600;"><i class="fa-solid fa-bolt" style="margin-right:4px;"></i>${escapeHtml(item.likelihood_score || '75%')} Causal Likelihood</span>
                        </div>
                        <div class="audit-news-rationale">
                            <strong style="color:#e2e8f0;">Empirical Rationale:</strong> ${escapeHtml(item.item_rationale || 'Database headline validates strategic scoring bounds in July-August 2026.')}
                        </div>
                    </div>
                `;
            }).join('');

            return `
                <div class="audit-category-accordion ${isExpanded ? 'expanded' : ''} ${hasActiveShock ? 'active-shock' : ''}" data-cat-key="${escapeHtml(cat.key)}">
                    <div class="audit-category-header">
                        <div class="audit-cat-left">
                            <div class="audit-cat-title">
                                <i class="fa-solid ${icon}" style="color:${groupColor};"></i>
                                <span>${escapeHtml(cat.full_name || cat.name)}</span>
                            </div>
                            <span class="${badgeClass}">Assigned Score: ${cat.assigned_score.toFixed(2)} (${escapeHtml(cat.severity_level)})</span>
                            <span class="${flucClass}">
                                <i class="fa-solid ${dominantFluc.includes('-') ? 'fa-arrow-trend-down' : (dominantFluc.includes('+') ? 'fa-arrow-trend-up' : 'fa-minus')}"></i>
                                ${escapeHtml(dominantFluc)}
                            </span>
                            <span class="score-badge-mod" style="background:rgba(0,229,255,0.08); color:#00E5FF; border-color:rgba(0,229,255,0.25);">
                                <i class="fa-solid fa-bolt"></i> ${escapeHtml(cat.dominant_likelihood || '20%')} Causal Likelihood
                            </span>
                        </div>
                        <div class="audit-cat-right">
                            <span style="font-size:11.5px; color:var(--text-muted); font-weight:600;">
                                <i class="fa-regular fa-newspaper" style="margin-right:4px;"></i>${(cat.news_items || []).length} Articles
                            </span>
                            <i class="fa-solid fa-chevron-down accordion-chevron"></i>
                        </div>
                    </div>
                    <div class="audit-category-body">
                        <div class="category-rationale-box" style="border-left-color:${groupColor};">
                            <strong style="color:#fff; display:block; margin-bottom:5px;">
                                <i class="fa-solid fa-calculator" style="color:${groupColor}; margin-right:6px;"></i>
                                Mathematical & Strategic Scoring Rationale:
                            </strong>
                            ${escapeHtml(cat.overall_rationale)}
                        </div>

                        <div class="category-news-subheading" style="color:${groupColor};">
                            <i class="fa-solid fa-database"></i>
                            Supporting Empirical Database Articles (July – August 2026)
                        </div>

                        <div class="audit-news-list">
                            ${newsCardsHtml}
                        </div>
                    </div>
                </div>
            `;
        }

        // Render Master Categories: PESTLE and Porter
        if (auditCategories && auditCategories.pestle && auditCategories.porter) {
            if (auditPestleList) {
                auditPestleList.innerHTML = auditCategories.pestle.map((c, idx) => renderCategoryAccordion(c, idx, idx === 0 || idx === 1)).join('');
            }
            if (auditPorterList) {
                auditPorterList.innerHTML = auditCategories.porter.map((c, idx) => renderCategoryAccordion(c, idx, idx === 0 || idx === 4)).join('');
            }

            // Wire up Accordion Toggle Click handlers
            const headers = document.querySelectorAll('.audit-category-header');
            headers.forEach(h => {
                h.removeEventListener('click', handleAccordionClick);
                h.addEventListener('click', handleAccordionClick);
            });
            return;
        }

        // Legacy fallback
        if (strategicEvidenceList && fallbackEvidenceRecords) {
            if (fallbackEvidenceRecords.length === 0) {
                strategicEvidenceList.innerHTML = '<p class="text-dim">No evidence records generated.</p>';
                return;
            }
            strategicEvidenceList.innerHTML = fallbackEvidenceRecords.map(ev => {
                const isDip = ev.associated_fluctuation && ev.associated_fluctuation.includes('-');
                return `
                    <div class="evidence-card-item">
                        <div class="evidence-item-header">
                            <div class="evidence-dimension-title">
                                <i class="fa-solid fa-scale-balanced" style="color:var(--accent-cyan);"></i>
                                <span>${escapeHtml(ev.dimension)}</span>
                            </div>
                            <div class="evidence-badges-row">
                                <span class="score-badge-mod">Assigned Score: ${ev.assigned_score.toFixed(2)}</span>
                                <span class="${isDip ? 'fluctuation-pill-dip' : 'fluctuation-pill-spike'}">
                                    Associated Fluctuation: ${escapeHtml(ev.associated_fluctuation)}
                                </span>
                            </div>
                        </div>
                        <div class="evidence-news-quote">"${escapeHtml(ev.associated_news)}"</div>
                        <div class="evidence-rationale-text">${escapeHtml(ev.rationale)}</div>
                    </div>
                `;
            }).join('');
        }
    }

    // Expand All / Collapse All button listeners
    if (btnExpandAllAudit) {
        btnExpandAllAudit.addEventListener('click', () => {
            document.querySelectorAll('.audit-category-accordion').forEach(el => el.classList.add('expanded'));
        });
    }
    if (btnCollapseAllAudit) {
        btnCollapseAllAudit.addEventListener('click', () => {
            document.querySelectorAll('.audit-category-accordion').forEach(el => el.classList.remove('expanded'));
        });
    }

    function updateRevenueRadarLegends(vec) {
        for (let i = 0; i < vec.length; i++) {
            const el = document.getElementById(`val-rev-p${i}`);
            if (el) el.textContent = (vec[i] || 0.30).toFixed(2);
        }
    }

    if (btnProceedRevenueChatbot) {
        btnProceedRevenueChatbot.addEventListener('click', () => {
            const topPeer = activeNearestCvps[0] ? activeNearestCvps[0].company : 'Benchmark Leaders';
            sidebarActiveCvp.innerHTML = `<strong>Revenue Mode Active</strong><br/><span style="font-size:12px; color:var(--text-muted);">${activeFluctuationClusters.length} Fluctuation Clusters (${activeStoredClusters.length} Verified Shocks)</span>`;

            renderSidebarNeighbors(activeNearestCvps);
            drawPestleRadarChart(activePestleVector);
            drawPorterRadarChart(activePorterVector);
            updatePestleLegendValues(activePestleVector);
            updatePorterLegendValues(activePorterVector);

            chatMessages.innerHTML = '';
            conversationHistory = [];

            const clusterSummaries = activeFluctuationClusters.map(c => 
                `[${c.cluster_name} (Avg ${c.avg_change_pct >= 0 ? '+' : ''}${c.avg_change_pct}%)] Dominant Driver: ${c.dominant_category} (${c.dominant_category_pct}% frequency)\nCollective Decision: ${c.collective_decision}`
            ).join('\n\n');

            const evidenceBrief = activeEvidenceRecords.slice(0, 4).map(ev => 
                `- ${ev.dimension} (Score: ${ev.assigned_score.toFixed(2)}): Associated with ${ev.associated_fluctuation} in ${ev.associated_period} via "${ev.associated_news}" (${ev.likelihood_score} Likelihood)`
            ).join('\n');

            appendSystemMessage(`OMNISCOPE REVENUE SENSITIVITY & STRATEGIC EVIDENCE ASSISTANT ACTIVE

Evaluated Sales Time-Series against Macro Shocks & 500 Benchmark Companies:
- Fluctuation Clusters: ${activeFluctuationClusters.length} severity clusters
- Primary 500-Company Peer: ${escapeHtml(topPeer)}
- Verified Strategic Shocks: ${activeStoredClusters.length}

Cluster Consensus & Collective Strategic Decisions:
${clusterSummaries || 'No high-volatility clusters detected.'}

Strategic Evidence Audit Highlights:
${evidenceBrief || 'Baseline operational parameters.'}

I am configured to answer executive market intelligence queries strictly grounded in your empirical revenue fluctuations, causal news likelihood scores, and collective strategic decisions.

How can I help you de-risk or capitalize on your market environment?`);

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

    // Draw PESTLE Radar Chart (6 Axes) with Optional Peer Overlay
    function drawPestleRadarChart(vector, peerVector = null) {
        drawPestleCanvas(canvasPestle, vector, peerVector);
        drawPestleCanvas(sidebarCanvasPestle, vector, peerVector);
    }

    function drawPestleCanvas(canvasObj, vector, peerVector = null) {
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

        // Peer Vector Polygon (if overlayed in cyan dashed line)
        if (peerVector && peerVector.length >= numAxes) {
            ctx.beginPath();
            for (let i = 0; i < numAxes; i++) {
                const val = peerVector[i] || 0.3;
                const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
                const r = radius * val;
                const x = centerX + Math.cos(angle) * r;
                const y = centerY + Math.sin(angle) * r;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.fillStyle = 'rgba(0, 229, 255, 0.18)';
            ctx.fill();
            ctx.strokeStyle = '#00E5FF';
            ctx.setLineDash([4, 4]);
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // User Vector Polygon (Your CVP in green)
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

    // Draw Porter's 5 Forces Radar Chart (5 Axes) with Optional Peer Overlay
    function drawPorterRadarChart(vector, peerVector = null) {
        drawPorterCanvas(canvasPorter, vector, peerVector);
        drawPorterCanvas(sidebarCanvasPorter, vector, peerVector);
    }

    function drawPorterCanvas(canvasObj, vector, peerVector = null) {
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

        // Peer Vector Polygon (if overlayed in green dashed line)
        if (peerVector && peerVector.length >= numAxes) {
            ctx.beginPath();
            for (let i = 0; i < numAxes; i++) {
                const val = peerVector[i] || 0.3;
                const angle = (Math.PI * 2 / numAxes) * i - (Math.PI / 2);
                const r = radius * val;
                const x = centerX + Math.cos(angle) * r;
                const y = centerY + Math.sin(angle) * r;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.fillStyle = 'rgba(0, 255, 102, 0.18)';
            ctx.fill();
            ctx.strokeStyle = '#00FF66';
            ctx.setLineDash([4, 4]);
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // User Vector Polygon (Your CVP in cyan)
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

    // Open On-DB Company Profile Modal & Render Relative PESTLE/Porter Analysis
    async function openCompanyProfileModal(companyName) {
        if (!modalCompanyProfile) return;
        modalCompanyProfile.classList.add('active');

        if (modalCompName) modalCompName.textContent = companyName;
        if (modalCompSector) modalCompSector.textContent = 'Loading...';
        if (modalCompProduct) modalCompProduct.textContent = 'Querying benchmark database...';
        if (modalCompCvp) modalCompCvp.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Fetching verified CVP and strategic factors from database...';
        if (modalCompTargetCustomer) modalCompTargetCustomer.textContent = 'Loading...';
        if (modalCompNeed) modalCompNeed.textContent = 'Loading...';
        if (modalCompBenefit) modalCompBenefit.textContent = 'Loading...';
        if (comparePestleBars) comparePestleBars.innerHTML = '<p class="text-dim"><i class="fa-solid fa-spinner fa-spin"></i> Computing relative PESTLE scores...</p>';
        if (comparePorterBars) comparePorterBars.innerHTML = '<p class="text-dim"><i class="fa-solid fa-spinner fa-spin"></i> Computing relative Porter forces...</p>';

        try {
            const res = await fetch(`/api/company_profile?name=${encodeURIComponent(companyName)}`);
            const data = await res.json();

            if (data.error) {
                if (modalCompCvp) modalCompCvp.textContent = `Error loading profile: ${data.error}`;
                return;
            }

            currentModalCompany = (data.company && typeof data.company === 'object') ? data.company : data;
            const comp = currentModalCompany;

            if (modalCompName) modalCompName.textContent = comp.company || companyName;
            if (modalCompSector) modalCompSector.textContent = comp.sector || 'Enterprise Technology';
            if (modalCompProduct) modalCompProduct.textContent = comp.product_or_service || comp.product_name || 'Strategic Offering';
            if (modalCompCvp) modalCompCvp.textContent = `"${comp.cvp || 'No CVP statement registered.'}"`;
            if (modalCompTargetCustomer) modalCompTargetCustomer.textContent = comp.target_customer || 'Market Operators & Decision Makers';
            if (modalCompNeed) modalCompNeed.textContent = comp.statement_of_need || 'Agile digital transformation and scalability';
            if (modalCompBenefit) modalCompBenefit.textContent = comp.statement_of_key_benefit || 'Reliable market leadership and operational efficiency';

            // Relative PESTLE Analysis (6 axes)
            const pestleLabels = ['Political Risk', 'Economic Pressure', 'Sociocultural Shift', 'Tech Velocity', 'Legal Compliance', 'Environmental Impact'];
            const userPestle = activePestleVector && activePestleVector.length === 6 ? activePestleVector : [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
            const peerPestle = comp.pestle_vector && comp.pestle_vector.length === 6 ? comp.pestle_vector : [0.35, 0.35, 0.35, 0.35, 0.35, 0.35];

            if (comparePestleBars) {
                comparePestleBars.innerHTML = pestleLabels.map((lbl, i) => {
                    const u = userPestle[i] || 0.3;
                    const p = peerPestle[i] || 0.3;
                    const diff = u - p;
                    const sign = diff >= 0 ? '+' : '';
                    const diffColor = diff > 0.05 ? '#ffaa00' : (diff < -0.05 ? '#00E5FF' : '#888');
                    const diffLabel = diff > 0.05 ? 'Higher Risk' : (diff < -0.05 ? 'Lower Risk' : 'Even');
                    return `
                        <div class="compare-bar-row">
                            <div class="bar-header">
                                <span class="bar-name">${escapeHtml(lbl)}</span>
                                <div class="bar-scores">
                                    <span class="score-user" title="Your CVP score">You: ${u.toFixed(2)}</span>
                                    <span class="score-peer" title="Benchmark peer score">Peer: ${p.toFixed(2)}</span>
                                    <span class="score-delta" style="color:${diffColor};">Δ ${sign}${diff.toFixed(2)} (${diffLabel})</span>
                                </div>
                            </div>
                            <div class="bar-track">
                                <div class="bar-fill-user" style="width: ${Math.min(100, Math.max(4, Math.round(u * 100)))}%;"></div>
                                <div class="bar-fill-peer" style="width: ${Math.min(100, Math.max(4, Math.round(p * 100)))}%;"></div>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            // Relative Porter's 5 Forces Analysis (5 forces)
            const porterLabels = ['Threat of Entrants', 'Buyer Power', 'Supplier Power', 'Threat of Substitutes', 'Competitive Rivalry'];
            const userPorter = activePorterVector && activePorterVector.length === 5 ? activePorterVector : [0.3, 0.3, 0.3, 0.3, 0.3];
            const peerPorter = comp.porter_vector && comp.porter_vector.length === 5 ? comp.porter_vector : [0.35, 0.35, 0.35, 0.35, 0.35];

            if (comparePorterBars) {
                comparePorterBars.innerHTML = porterLabels.map((lbl, i) => {
                    const u = userPorter[i] || 0.3;
                    const p = peerPorter[i] || 0.3;
                    const diff = u - p;
                    const sign = diff >= 0 ? '+' : '';
                    const diffColor = diff > 0.05 ? '#ffaa00' : (diff < -0.05 ? '#00E5FF' : '#888');
                    const diffLabel = diff > 0.05 ? 'Higher Pressure' : (diff < -0.05 ? 'Lower Pressure' : 'Even');
                    return `
                        <div class="compare-bar-row">
                            <div class="bar-header">
                                <span class="bar-name">${escapeHtml(lbl)}</span>
                                <div class="bar-scores">
                                    <span class="score-user" title="Your CVP score">You: ${u.toFixed(2)}</span>
                                    <span class="score-peer" title="Benchmark peer score">Peer: ${p.toFixed(2)}</span>
                                    <span class="score-delta" style="color:${diffColor};">Δ ${sign}${diff.toFixed(2)} (${diffLabel})</span>
                                </div>
                            </div>
                            <div class="bar-track">
                                <div class="bar-fill-user" style="width: ${Math.min(100, Math.max(4, Math.round(u * 100)))}%;"></div>
                                <div class="bar-fill-peer" style="width: ${Math.min(100, Math.max(4, Math.round(p * 100)))}%;"></div>
                            </div>
                        </div>
                    `;
                }).join('');
            }

        } catch (err) {
            if (modalCompCvp) modalCompCvp.textContent = `Network error fetching company profile: ${err.message}`;
        }
    }

    // Overlay Peer on Radars by Name
    async function overlayPeerRadarByName(companyName) {
        const found = activeNearestCvps.find(m => m.company === companyName);
        if (found && found.pestle_vector && found.porter_vector) {
            activeOverlayPeer = found;
            drawPestleRadarChart(activePestleVector, activeOverlayPeer.pestle_vector);
            drawPorterRadarChart(activePorterVector, activeOverlayPeer.porter_vector);
            appendSystemMessage(`STRATEGIC BENCHMARK OVERLAY ACTIVE:
            
Overlaying **${escapeHtml(companyName)}** onto your dual radar charts in electric cyan dashed vectors.
Compare your CVP positioning directly against ${escapeHtml(companyName)}.`);
            return;
        }

        try {
            const res = await fetch(`/api/company_profile?name=${encodeURIComponent(companyName)}`);
            const data = await res.json();
            const comp = (data.company && typeof data.company === 'object') ? data.company : data;
            if (comp && comp.pestle_vector && comp.porter_vector) {
                activeOverlayPeer = comp;
                drawPestleRadarChart(activePestleVector, activeOverlayPeer.pestle_vector);
                drawPorterRadarChart(activePorterVector, activeOverlayPeer.porter_vector);
                appendSystemMessage(`STRATEGIC BENCHMARK OVERLAY ACTIVE:
                
Overlaying **${escapeHtml(companyName)}** onto your dual radar charts in electric cyan dashed vectors.`);
            }
        } catch (err) {
            console.error('Failed to load radar overlay:', err);
        }
    }

    function renderCvpMatchesList(matches) {
        if (!cvpMatchesList) return;
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

        cvpMatchesList.innerHTML = matches.map((m, idx) => {
            const simPct = (m.similarity_pct !== undefined && m.similarity_pct !== null)
                ? m.similarity_pct 
                : (m.similarity ? Math.round(m.similarity * 100) : 85);

            return `
            <div class="cvp-match-card" style="border-left: 4px solid ${borderColors[idx % 3]};">
                <div class="cvp-match-header">
                    <span>
                        <button type="button" class="company-profile-btn" data-company="${escapeHtml(m.company)}" title="Click to view verified on-DB company intelligence">
                            <span>${escapeHtml(m.company)}</span>
                            <i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 11px; opacity: 0.8;"></i>
                        </button>
                        <span class="cvp-match-sector-tag"><i class="fa-solid fa-building"></i> ${escapeHtml(m.sector || 'Enterprise')}</span>
                    </span>
                    <span class="cvp-match-badge" style="${badgeColors[idx % 3]}">${simPct}% CVP Similarity</span>
                </div>
                <p class="cvp-match-cvp">"${escapeHtml(m.cvp)}"</p>
                <div class="neighbor-card-actions">
                    <button type="button" class="btn-peer-action" data-company="${escapeHtml(m.company)}">
                        <i class="fa-solid fa-id-card"></i> View DB Profile
                    </button>
                    <button type="button" class="btn-peer-action cyan btn-peer-radar" data-company="${escapeHtml(m.company)}">
                        <i class="fa-solid fa-chart-pie"></i> Compare Dual Radars
                    </button>
                </div>
            </div>
            `;
        }).join('');
    }

    function renderSidebarNeighbors(matches) {
        if (!sidebarNeighborsList) return;
        if (!matches || matches.length === 0) return;
        const borderColors = ['#00FF66', '#00E5FF', '#10B981'];
        const badgeColors = [
            'background: rgba(0, 255, 102, 0.12); color: #00FF66; border: 1px solid rgba(0, 255, 102, 0.3);',
            'background: rgba(0, 229, 255, 0.12); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3);',
            'background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3);'
        ];

        sidebarNeighborsList.innerHTML = matches.map((m, idx) => {
            const simPct = (m.similarity_pct !== undefined && m.similarity_pct !== null)
                ? m.similarity_pct 
                : (m.similarity ? Math.round(m.similarity * 100) : 85);

            return `
            <div class="neighbor-item" style="border-left: 4px solid ${borderColors[idx % 3]};">
                <div class="neighbor-header">
                    <button type="button" class="neighbor-company-btn" data-company="${escapeHtml(m.company)}" title="View On-DB Company Profile">
                        <span>${escapeHtml(m.company)}</span>
                        <i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 10px; opacity: 0.7;"></i>
                    </button>
                    <span class="neighbor-badge" style="${badgeColors[idx % 3]}">${simPct}%</span>
                </div>
                <div class="neighbor-sector">
                    <i class="fa-solid fa-layer-group"></i> ${escapeHtml(m.sector || 'Enterprise')}
                </div>
                ${m.cvp ? `<div class="neighbor-cvp-snippet">"${escapeHtml(m.cvp)}"</div>` : ''}
                <div class="neighbor-card-actions">
                    <button type="button" class="btn-peer-action" data-company="${escapeHtml(m.company)}" title="View full profile">
                        <i class="fa-solid fa-id-card"></i> Profile
                    </button>
                    <button type="button" class="btn-peer-action cyan btn-peer-radar" data-company="${escapeHtml(m.company)}" title="Overlay on radar charts">
                        <i class="fa-solid fa-chart-pie"></i> Overlay
                    </button>
                </div>
            </div>
            `;
        }).join('');
    }

    // Delegated click listeners for Company Profile and Radar Comparison
    if (cvpMatchesList) {
        cvpMatchesList.addEventListener('click', (e) => {
            const radarBtn = e.target.closest('.btn-peer-radar');
            if (radarBtn) {
                const comp = radarBtn.dataset.company;
                if (comp) overlayPeerRadarByName(comp);
                return;
            }
            const profileBtn = e.target.closest('.company-profile-btn, .btn-peer-action');
            if (profileBtn) {
                const comp = profileBtn.dataset.company;
                if (comp) openCompanyProfileModal(comp);
                return;
            }
        });
    }

    if (sidebarNeighborsList) {
        sidebarNeighborsList.addEventListener('click', (e) => {
            const radarBtn = e.target.closest('.btn-peer-radar');
            if (radarBtn) {
                const comp = radarBtn.dataset.company;
                if (comp) overlayPeerRadarByName(comp);
                return;
            }
            const profileBtn = e.target.closest('.neighbor-company-btn, .btn-peer-action');
            if (profileBtn) {
                const comp = profileBtn.dataset.company;
                if (comp) openCompanyProfileModal(comp);
                return;
            }
        });
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
                    <span>
                        <button type="button" class="company-profile-btn" data-company="${escapeHtml(m.company)}" title="Click to view on-DB company intelligence">
                            <span>${escapeHtml(m.company)}</span>
                            <i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 11px; opacity: 0.8;"></i>
                        </button>
                        <span class="cvp-match-sector-tag"><i class="fa-solid fa-building"></i> ${escapeHtml(m.sector || 'Enterprise')}</span>
                    </span>
                    <span class="cvp-match-badge" style="background: rgba(0, 229, 255, 0.12); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3);">${m.similarity_pct}% Vector Similarity</span>
                </div>
                <p class="cvp-match-cvp">"${escapeHtml(m.cvp)}"</p>
                <div class="neighbor-card-actions">
                    <button type="button" class="btn-peer-action" data-company="${escapeHtml(m.company)}">
                        <i class="fa-solid fa-id-card"></i> View DB Profile
                    </button>
                    <button type="button" class="btn-peer-action cyan btn-peer-radar" data-company="${escapeHtml(m.company)}">
                        <i class="fa-solid fa-chart-pie"></i> Compare Radars
                    </button>
                </div>
            </div>
        `).join('');
    }

    if (revenuePeersList) {
        revenuePeersList.addEventListener('click', (e) => {
            const radarBtn = e.target.closest('.btn-peer-radar');
            if (radarBtn) {
                const comp = radarBtn.dataset.company;
                if (comp) overlayPeerRadarByName(comp);
                return;
            }
            const profileBtn = e.target.closest('.company-profile-btn, .btn-peer-action');
            if (profileBtn) {
                const comp = profileBtn.dataset.company;
                if (comp) openCompanyProfileModal(comp);
                return;
            }
        });
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
