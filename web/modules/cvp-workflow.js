/**
 * Omniscope AI - CVP Workflow Module
 * Manages Customer Value Proposition input, evaluation, neighbor cards, and sidebar syncing.
 */

import { CvpApi } from './api-client.js';
import { ChartVisualizer } from './chart-visualizer.js';
import { CompanyIntelligence } from './company-intelligence.js';

export class CvpWorkflow {
    constructor(state, callbacks = {}) {
        this.state = state;
        this.callbacks = callbacks;
        this.initDom();
    }

    initDom() {
        this.formCvp = document.getElementById('form-cvp-input');
        this.inputCvp = document.getElementById('input-cvp-text');
        this.btnSubmit = document.getElementById('btn-analyze-cvp');
        this.resultsPanel = document.getElementById('step1-results-panel');
        this.matchesList = document.getElementById('cvp-matches-list');
        this.sidebarCvpText = document.getElementById('sidebar-active-cvp');
        this.sidebarNeighbors = document.getElementById('sidebar-neighbors-list');
        this.canvasPestle = document.getElementById('canvas-pestle');
        this.canvasPorter = document.getElementById('canvas-porter');
        this.sideCanvasPestle = document.getElementById('sidebar-canvas-pestle');
        this.sideCanvasPorter = document.getElementById('sidebar-canvas-porter');

        // Modal Quick Edit
        this.modalQuick = document.getElementById('modal-quick-edit-cvp');
        this.btnQuickEdit = document.getElementById('btn-quick-edit-cvp');
        this.btnCloseQuick = document.getElementById('btn-close-quick-cvp');
        this.btnCancelQuick = document.getElementById('btn-cancel-quick-cvp');
        this.btnSaveQuick = document.getElementById('btn-save-quick-cvp');
        this.inputQuickCvp = document.getElementById('input-quick-cvp-text');

        this.bindEvents();
    }

    bindEvents() {
        if (this.formCvp) {
            this.formCvp.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.evaluateCvp(this.inputCvp.value.trim());
            });
        }

        if (this.btnQuickEdit && this.modalQuick) {
            this.btnQuickEdit.addEventListener('click', () => {
                if (this.inputQuickCvp) this.inputQuickCvp.value = this.state.activeCvpText;
                this.modalQuick.classList.add('active');
                if (this.inputQuickCvp) this.inputQuickCvp.focus();
            });
        }

        if (this.btnCloseQuick) this.btnCloseQuick.addEventListener('click', () => this.modalQuick.classList.remove('active'));
        if (this.btnCancelQuick) this.btnCancelQuick.addEventListener('click', () => this.modalQuick.classList.remove('active'));

        if (this.btnSaveQuick) {
            this.btnSaveQuick.addEventListener('click', async () => {
                const text = this.inputQuickCvp.value.trim();
                if (!text) {
                    alert('Please enter a CVP statement.');
                    return;
                }
                this.btnSaveQuick.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Re-evaluating 500 Companies...`;
                this.btnSaveQuick.disabled = true;
                try {
                    await this.evaluateCvp(text);
                    this.modalQuick.classList.remove('active');
                } finally {
                    this.btnSaveQuick.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Re-evaluate & Update CVP`;
                    this.btnSaveQuick.disabled = false;
                }
            });
        }

        // Delegate Match List clicks
        [this.matchesList, this.sidebarNeighbors].forEach(container => {
            if (!container) return;
            container.addEventListener('click', (e) => {
                const radarBtn = e.target.closest('.btn-peer-radar');
                if (radarBtn) {
                    const comp = radarBtn.dataset.company;
                    if (comp) this.callbacks.onPeerRadarOverlay?.(comp);
                    return;
                }
                const profileBtn = e.target.closest('.company-profile-btn, .btn-peer-action');
                if (profileBtn) {
                    const comp = profileBtn.dataset.company;
                    if (comp) {
                        CompanyIntelligence.loadAndShowProfile(
                            comp, 
                            this.state.activePestleVector, 
                            this.state.activePorterVector, 
                            (peer) => this.callbacks.onPeerRadarOverlay?.(peer.company)
                        );
                    }
                    return;
                }
            });
        });
    }

    async evaluateCvp(cvpText) {
        if (!cvpText) {
            alert('Please enter a Customer Value Proposition (CVP).');
            return;
        }

        if (this.btnSubmit) {
            this.btnSubmit.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Projecting 384-D Vector & Searching 500 Companies...`;
            this.btnSubmit.disabled = true;
        }

        try {
            const data = await CvpApi.evaluate(cvpText, this.state.groqApiKey);
            if (data.error) throw new Error(data.error);

            this.state.activeCvpText = data.cvp_text;
            this.state.activePestleVector = data.pestle_vector || [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
            this.state.activePorterVector = data.porter_vector || [0.3, 0.3, 0.3, 0.3, 0.3];
            this.state.activeUser11DVector = data.user_11d_vector || [...this.state.activePestleVector, ...this.state.activePorterVector];
            this.state.activeNearestCvps = data.nearest_cvps || [];

            this.syncStateToUi();

            if (this.callbacks.onCvpEvaluated) {
                this.callbacks.onCvpEvaluated(data);
            }
        } catch (err) {
            alert(`CVP Evaluation Error: ${err.message}`);
        } finally {
            if (this.btnSubmit) {
                this.btnSubmit.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Analyze CVP & Generate Dual Radar Charts`;
                this.btnSubmit.disabled = false;
            }
        }
    }

    syncStateToUi() {
        if (this.sidebarCvpText) this.sidebarCvpText.textContent = `"${this.state.activeCvpText}"`;
        if (this.inputCvp) this.inputCvp.value = this.state.activeCvpText;

        // Render Radars
        const peerPestle = this.state.activeOverlayPeer ? this.state.activeOverlayPeer.pestle_vector : null;
        const peerPorter = this.state.activeOverlayPeer ? this.state.activeOverlayPeer.porter_vector : null;

        ChartVisualizer.drawPestleCanvas(this.canvasPestle, this.state.activePestleVector, peerPestle);
        ChartVisualizer.drawPestleCanvas(this.sideCanvasPestle, this.state.activePestleVector, peerPestle);
        ChartVisualizer.drawPorterCanvas(this.canvasPorter, this.state.activePorterVector, peerPorter);
        ChartVisualizer.drawPorterCanvas(this.sideCanvasPorter, this.state.activePorterVector, peerPorter);

        ChartVisualizer.updateCvpLegendValues(this.state.activePestleVector, this.state.activePorterVector);


        this.renderMatches(this.state.activeNearestCvps);

        if (this.resultsPanel) {
            this.resultsPanel.classList.remove('hidden');
            this.resultsPanel.scrollIntoView({ behavior: 'smooth' });
        }
    }

    renderMatches(matches) {
        if (!matches || matches.length === 0) return;

        const borderColors = ['#00FF66', '#00E5FF', '#10B981', '#A855F7', '#FFB300'];

        const html = matches.map((m, idx) => `
            <div class="cvp-match-card" style="border-left: 4px solid ${borderColors[idx % borderColors.length]};">
                <div class="cvp-match-header">
                    <span>
                        <button type="button" class="company-profile-btn" data-company="${CompanyIntelligence.escapeHtml(m.company)}" title="Click to view on-DB company intelligence">
                            <span>${CompanyIntelligence.escapeHtml(m.company)}</span>
                            <i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 11px; opacity: 0.8;"></i>
                        </button>
                        <span class="cvp-match-sector-tag"><i class="fa-solid fa-building"></i> ${CompanyIntelligence.escapeHtml(m.sector || 'Enterprise')}</span>
                    </span>
                    <span class="cvp-match-badge">${m.similarity_pct}% CVP Similarity</span>
                </div>
                <p class="cvp-match-cvp">"${CompanyIntelligence.escapeHtml(m.cvp)}"</p>
                <div class="neighbor-card-actions">
                    <button type="button" class="btn-peer-action" data-company="${CompanyIntelligence.escapeHtml(m.company)}">
                        <i class="fa-solid fa-id-card"></i> View DB Profile
                    </button>
                    <button type="button" class="btn-peer-action cyan btn-peer-radar" data-company="${CompanyIntelligence.escapeHtml(m.company)}">
                        <i class="fa-solid fa-chart-pie"></i> Compare Radars
                    </button>
                </div>
            </div>
        `).join('');

        if (this.matchesList) this.matchesList.innerHTML = html;
        if (this.sidebarNeighbors) this.sidebarNeighbors.innerHTML = html;
    }
}
