/**
 * Omniscope AI - CVP Workflow Module
 * Manages Customer Value Proposition input, evaluation, neighbor cards, and sidebar syncing.
 */

import { CvpApi } from './api-client.js';
import { ChartVisualizer } from './chart-visualizer.js';
import { CompanyIntelligence } from './company-intelligence.js';
import { AuthManager } from './auth-manager.js';

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
                const profileBtn = e.target.closest('.company-profile-btn, .btn-peer-action:not(.btn-peer-radar)');
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
            this.state.activeCvpPrognosis = data.investment_prognosis || null;

            this.syncStateToUi();

            // Cache in guest store if unauthenticated
            if (!window.authManager?.currentUser) {
                AuthManager.saveGuestAnalysis({
                    id: data.analysis_id || `guest_cvp_${Date.now()}`,
                    analysis_type: 'cvp',
                    title: `CVP: ${data.cvp_text.slice(0, 45)}...`,
                    summary: `Dual radar analysis against 500 benchmark companies. Top Peer: ${data.nearest_cvps?.[0]?.company || 'Benchmark'}`,
                    input_data: { cvp_text: data.cvp_text },
                    results_data: data,
                    created_at: new Date().toISOString()
                });
            }
            window.authManager?.showToast('CVP evaluation saved to your Intelligence Workspace', 'success');
            window.historyManager?.updateCountBadges();

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

        if (this.state.activeCvpPrognosis) {
            this.renderInvestmentScore(this.state.activeCvpPrognosis);
        }

        if (this.resultsPanel) {
            this.resultsPanel.classList.remove('hidden');
            this.resultsPanel.scrollIntoView({ behavior: 'smooth' });
        }
    }

    renderMatches(matches) {
        if (!matches || matches.length === 0) return;

        const borderColors = ['var(--brand-primary)', 'var(--color-growth)', 'var(--border-medium)', 'var(--color-metric)', 'var(--color-neutral)'];

        const html = matches.map((m, idx) => `
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

    renderInvestmentScore(prognosis) {
        if (!prognosis) return;

        const badgeTier = document.getElementById('badge-cvp-investment-tier');
        const pillRec = document.getElementById('pill-cvp-investment-rec');
        const gaugeCircle = document.getElementById('gauge-cvp-investment-circle');
        const valScore = document.getElementById('val-cvp-investment-score');
        const valMoat = document.getElementById('val-cvp-moat-strength');
        const valMacro = document.getElementById('val-cvp-macro-alignment');
        const valPricing = document.getElementById('val-cvp-pricing-power');
        const boxVerdict = document.getElementById('box-cvp-executive-verdict');
        const textVerdict = document.getElementById('text-cvp-investment-verdict');

        const statusMoat = document.getElementById('status-cvp-factor-moat');
        const barMoat = document.getElementById('bar-cvp-factor-moat');
        const statusTech = document.getElementById('status-cvp-factor-tech');
        const barTech = document.getElementById('bar-cvp-factor-tech');
        const statusPricing = document.getElementById('status-cvp-factor-pricing');
        const barPricing = document.getElementById('bar-cvp-factor-pricing');
        const statusBenchmark = document.getElementById('status-cvp-factor-benchmark');
        const barBenchmark = document.getElementById('bar-cvp-factor-benchmark');

        const listCatalysts = document.getElementById('list-cvp-investment-catalysts');
        const listDeterrents = document.getElementById('list-cvp-investment-deterrents');

        // Tier badge & Recommendation pill
        if (badgeTier) {
            badgeTier.textContent = prognosis.tier_label || prognosis.tier;
            badgeTier.className = `investment-tier-badge ${prognosis.tier_badge || 'tier-mod'}`;
        }
        if (pillRec) {
            pillRec.textContent = prognosis.recommendation || 'MONITOR';
            pillRec.className = `investment-recommendation-pill pill-${prognosis.tier_badge || 'tier-mod'}`;
        }

        // Animated Radial Gauge
        const targetScore = prognosis.score || 0;
        let color = prognosis.color || '#10B981';
        if (color === '#00FF66') color = '#10B981';
        if (color === '#00E5FF') color = '#3B82F6';
        const circumference = 427.26; // 2 * pi * 68

        if (gaugeCircle) {
            gaugeCircle.style.stroke = color;
            const offset = circumference - (circumference * (targetScore / 100));
            requestAnimationFrame(() => {
                gaugeCircle.style.transition = 'stroke-dashoffset 1.4s cubic-bezier(0.16, 1, 0.3, 1)';
                gaugeCircle.style.strokeDashoffset = offset.toFixed(2);
            });
        }

        // Score number counter animation
        if (valScore) {
            valScore.style.color = color;
            const duration = 1200;
            const start = performance.now();
            const animateScore = (time) => {
                const elapsed = time - start;
                const progress = Math.min(elapsed / duration, 1);
                const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
                const currentVal = Math.round(ease * targetScore);
                valScore.textContent = currentVal;
                if (progress < 1) {
                    requestAnimationFrame(animateScore);
                } else {
                    valScore.textContent = targetScore;
                }
            };
            requestAnimationFrame(animateScore);
        }

        // Submetrics
        if (valMoat) {
            const m = prognosis.moat_strength_pct ?? 70;
            valMoat.textContent = `${m}%`;
            valMoat.style.color = m >= 60 ? 'var(--accent-green)' : '#f87171';
        }
        if (valMacro) {
            const a = prognosis.macro_alignment_pct ?? 65;
            valMacro.textContent = `${a}%`;
            valMacro.style.color = a >= 60 ? 'var(--accent-green)' : '#f87171';
        }
        if (valPricing) {
            valPricing.textContent = prognosis.pricing_power_label || 'Balanced';
            valPricing.style.color = color;
        }

        // Executive verdict narrative
        if (textVerdict) {
            textVerdict.textContent = prognosis.verdict || '';
        }
        if (boxVerdict) {
            boxVerdict.className = `executive-verdict-box verdict-${prognosis.tier_badge || 'tier-mod'}`;
        }

        // 4 Factors
        const f = prognosis.factors || {};
        if (f.moat) {
            if (statusMoat) statusMoat.textContent = `${f.moat.status} (${f.moat.score}/100)`;
            if (barMoat) {
                barMoat.style.width = `${Math.min(100, Math.max(0, f.moat.score))}%`;
                barMoat.style.background = f.moat.score >= 60 ? 'linear-gradient(90deg, #10B981, #059669)' : (f.moat.score < 45 ? 'linear-gradient(90deg, #F43F5E, #E11D48)' : 'linear-gradient(90deg, #F59E0B, #D97706)');
            }
        }
        if (f.tech) {
            if (statusTech) statusTech.textContent = `${f.tech.status} (${f.tech.score}/100)`;
            if (barTech) {
                barTech.style.width = `${Math.min(100, Math.max(0, f.tech.score))}%`;
                barTech.style.background = f.tech.score >= 60 ? 'linear-gradient(90deg, #10B981, #059669)' : (f.tech.score < 45 ? 'linear-gradient(90deg, #F43F5E, #E11D48)' : 'linear-gradient(90deg, #F59E0B, #D97706)');
            }
        }
        if (f.pricing) {
            if (statusPricing) statusPricing.textContent = `${f.pricing.status} (${f.pricing.score}/100)`;
            if (barPricing) {
                barPricing.style.width = `${Math.min(100, Math.max(0, f.pricing.score))}%`;
                barPricing.style.background = f.pricing.score >= 60 ? 'linear-gradient(90deg, #10B981, #059669)' : (f.pricing.score < 45 ? 'linear-gradient(90deg, #F43F5E, #E11D48)' : 'linear-gradient(90deg, #F59E0B, #D97706)');
            }
        }
        if (f.benchmark) {
            if (statusBenchmark) statusBenchmark.textContent = `${f.benchmark.status} (${f.benchmark.score}/100)`;
            if (barBenchmark) {
                barBenchmark.style.width = `${Math.min(100, Math.max(0, f.benchmark.score))}%`;
                barBenchmark.style.background = f.benchmark.score >= 60 ? 'linear-gradient(90deg, #10B981, #059669)' : (f.benchmark.score < 50 ? 'linear-gradient(90deg, #F43F5E, #E11D48)' : 'linear-gradient(90deg, #F59E0B, #D97706)');
            }
        }

        // Catalysts list
        if (listCatalysts) {
            const cats = prognosis.catalysts || [];
            if (cats.length === 0) {
                listCatalysts.innerHTML = '<li><span class="text-dim">No acute positive catalysts isolated.</span></li>';
            } else {
                listCatalysts.innerHTML = cats.map(c => `
                    <li class="insight-bullet-item catalyst-item">
                        <i class="fa-solid fa-circle-check" style="color: var(--color-growth);"></i>
                        <span>${CompanyIntelligence.escapeHtml(c)}</span>
                    </li>
                `).join('');
            }
        }

        // Deterrents list
        if (listDeterrents) {
            const dets = prognosis.deterrents || [];
            if (dets.length === 0) {
                listDeterrents.innerHTML = '<li><span class="text-dim">No acute structural deterrents isolated.</span></li>';
            } else {
                listDeterrents.innerHTML = dets.map(d => `
                    <li class="insight-bullet-item deterrent-item">
                        <i class="fa-solid fa-triangle-exclamation" style="color: #FFB300;"></i>
                        <span>${CompanyIntelligence.escapeHtml(d)}</span>
                    </li>
                `).join('');
            }
        }
    }
}
