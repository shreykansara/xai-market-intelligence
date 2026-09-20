/**
 * Omniscope AI - Executive Dashboard Manager Module
 * Manages the executive dashboard screen: live KPIs, recent analyses feed,
 * filter tabs, real-time search, AI thread cards, and workspace restorations.
 */

import { UserHistoryApi, ApiClient } from './api-client.js';

export class DashboardManager {
    constructor(authManager, callbacks = {}) {
        this.authManager = authManager;
        this.callbacks = callbacks;
        this.analyses = [];
        this.conversations = [];
        this.activeFilter = 'all';
        this.searchQuery = '';
        this.initDom();
    }

    initDom() {
        this.bannerAvatar = document.getElementById('dash-banner-avatar');
        this.bannerName = document.getElementById('dash-banner-name');
        this.bannerSub = document.getElementById('dash-banner-sub');

        // KPI elements
        this.kpiCvp = document.getElementById('dash-kpi-cvp-count');
        this.kpiRev = document.getElementById('dash-kpi-rev-count');
        this.kpiChat = document.getElementById('dash-kpi-chat-count');
        this.kpiRisk = document.getElementById('dash-kpi-risk-val');
        this.kpiRiskLabel = document.getElementById('dash-kpi-risk-label');

        // Tabs and counters
        this.tabCountAll = document.getElementById('dash-tab-count-all');
        this.tabCountCvp = document.getElementById('dash-tab-count-cvp');
        this.tabCountRev = document.getElementById('dash-tab-count-revenue');
        this.filterTabs = document.querySelectorAll('.dash-filter-tab');

        // Search & Feed
        this.searchInput = document.getElementById('dash-search-input');
        this.analysesFeed = document.getElementById('dash-analyses-feed');
        this.threadsList = document.getElementById('dash-threads-list');

        this.bindEvents();
    }

    bindEvents() {
        // Tab Filtering
        this.filterTabs?.forEach(tab => {
            tab.addEventListener('click', () => {
                this.filterTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                this.activeFilter = tab.dataset.filter || 'all';
                this.renderAnalysesFeed();
            });
        });

        // Search
        this.searchInput?.addEventListener('input', (e) => {
            this.searchQuery = (e.target.value || '').trim().toLowerCase();
            this.renderAnalysesFeed();
        });

        // Delegate Feed Actions (Restore & Delete)
        this.analysesFeed?.addEventListener('click', async (e) => {
            const restoreBtn = e.target.closest('.btn-dash-restore');
            if (restoreBtn) {
                const id = restoreBtn.dataset.id;
                const analysis = this.analyses.find(a => String(a.id) === String(id));
                if (analysis) {
                    if (analysis.analysis_type === 'revenue_sensitivity' || analysis.analysis_type === 'revenue') {
                        this.callbacks.onRestoreRevenue?.(analysis);
                    } else {
                        this.callbacks.onRestoreCvp?.(analysis);
                    }
                }
                return;
            }

            const deleteBtn = e.target.closest('.btn-dash-delete');
            if (deleteBtn) {
                const id = deleteBtn.dataset.id;
                if (confirm('Remove this analysis from your saved executive workspace?')) {
                    await this.deleteAnalysis(id);
                }
            }
        });

        // Delegate Chat Resume Actions
        this.threadsList?.addEventListener('click', (e) => {
            const resumeBtn = e.target.closest('.btn-dash-resume-thread');
            if (resumeBtn) {
                const sessionId = resumeBtn.dataset.sessionId;
                const conv = this.conversations.find(c => String(c.session_id) === String(sessionId));
                if (conv) {
                    this.callbacks.onRestoreConversation?.(conv);
                }
            }
        });
    }

    async refresh() {
        this.renderUserProfile();
        await this.loadData();
        this.renderKpis();
        this.renderAnalysesFeed();
        this.renderThreadsList();
    }

    renderUserProfile() {
        const user = this.authManager?.currentUser;
        if (user) {
            const initials = this.getInitials(user.full_name || user.email);
            if (this.bannerAvatar) this.bannerAvatar.textContent = initials;
            if (this.bannerName) this.bannerName.textContent = user.full_name || 'Executive Strategist';
            if (this.bannerSub) {
                const company = user.company_name ? `${user.company_name} • ` : '';
                const role = user.role ? `${user.role.toUpperCase()} • ` : '';
                this.bannerSub.textContent = `${company}${role}384-D Vector Projections • GDELT Macro Event Stream Active`;
            }
        } else {
            if (this.bannerAvatar) this.bannerAvatar.textContent = 'EX';
            if (this.bannerName) this.bannerName.textContent = 'Guest Strategist';
            if (this.bannerSub) this.bannerSub.textContent = 'Local Session Storage • Sign in to synchronize enterprise portfolio across devices';
        }
    }

    async loadData() {
        if (ApiClient.hasUserToken()) {
            try {
                const [anaRes, convRes] = await Promise.all([
                    UserHistoryApi.getAnalyses(),
                    UserHistoryApi.getConversations()
                ]);
                this.analyses = anaRes.success ? (anaRes.analyses || []) : [];
                this.conversations = convRes.success ? (convRes.conversations || []) : [];
                return;
            } catch (err) {
                console.warn('[DashboardManager] Failed to load remote data, falling back to local:', err.message);
            }
        }

        // Fallback to local guest storage
        try {
            this.analyses = JSON.parse(localStorage.getItem('omniscope_guest_analyses') || '[]');
            this.conversations = JSON.parse(localStorage.getItem('omniscope_guest_conversations') || '[]');
        } catch {
            this.analyses = [];
            this.conversations = [];
        }
    }

    renderKpis() {
        const cvpCount = this.analyses.filter(a => a.analysis_type === 'cvp').length;
        const revCount = this.analyses.filter(a => a.analysis_type === 'revenue_sensitivity' || a.analysis_type === 'revenue').length;
        const chatCount = this.conversations.length;

        if (this.kpiCvp) this.kpiCvp.textContent = cvpCount;
        if (this.kpiRev) this.kpiRev.textContent = revCount;
        if (this.kpiChat) this.kpiChat.textContent = chatCount;

        if (this.tabCountAll) this.tabCountAll.textContent = this.analyses.length;
        if (this.tabCountCvp) this.tabCountCvp.textContent = cvpCount;
        if (this.tabCountRev) this.tabCountRev.textContent = revCount;

        // Calculate average macro risk
        let totalPestleSum = 0;
        let countWithVectors = 0;
        this.analyses.forEach(a => {
            const vec = a.results_data?.pestle_vector;
            if (Array.isArray(vec) && vec.length > 0) {
                const avg = vec.reduce((s, v) => s + Number(v), 0) / vec.length;
                totalPestleSum += avg;
                countWithVectors++;
            }
        });

        const riskScore = countWithVectors > 0 ? (totalPestleSum / countWithVectors) : 0.26;
        if (this.kpiRisk) this.kpiRisk.textContent = riskScore.toFixed(2);

        if (this.kpiRiskLabel) {
            if (riskScore < 0.35) {
                this.kpiRiskLabel.textContent = 'RESILIENT';
                this.kpiRiskLabel.className = 'kpi-chip green';
            } else if (riskScore < 0.65) {
                this.kpiRiskLabel.textContent = 'MODERATE RISK';
                this.kpiRiskLabel.className = 'kpi-chip amber';
            } else {
                this.kpiRiskLabel.textContent = 'ELEVATED HEADWINDS';
                this.kpiRiskLabel.className = 'kpi-chip purple';
            }
        }
    }

    renderAnalysesFeed() {
        if (!this.analysesFeed) return;

        let filtered = this.analyses.filter(a => {
            if (this.activeFilter === 'cvp') return a.analysis_type === 'cvp';
            if (this.activeFilter === 'revenue') return a.analysis_type === 'revenue_sensitivity' || a.analysis_type === 'revenue';
            return true;
        });

        if (this.searchQuery) {
            filtered = filtered.filter(a => {
                const title = (a.title || '').toLowerCase();
                const cvp = (a.input_data?.cvp_text || a.results_data?.cvp_text || '').toLowerCase();
                const peer = (a.results_data?.nearest_cvps?.[0]?.company || '').toLowerCase();
                return title.includes(this.searchQuery) || cvp.includes(this.searchQuery) || peer.includes(this.searchQuery);
            });
        }

        if (filtered.length === 0) {
            this.analysesFeed.innerHTML = `
                <div class="dash-empty-state">
                    <div class="empty-icon"><i class="fa-solid fa-layer-group"></i></div>
                    <h4>No analyses saved yet in this view</h4>
                    <p>Execute a CVP evaluation or revenue sensitivity model to store verified vector intelligence here.</p>
                    <div class="dash-empty-actions">
                        <button type="button" class="btn-primary-sm" id="btn-dash-empty-cvp">
                            <i class="fa-solid fa-bullseye"></i> Launch CVP
                        </button>
                        <button type="button" class="btn-outline-sm" id="btn-dash-empty-rev">
                            <i class="fa-solid fa-chart-line"></i> Launch Revenue
                        </button>
                    </div>
                </div>
            `;
            document.getElementById('btn-dash-empty-cvp')?.addEventListener('click', () => {
                window.navigationManager?.switchScreen(document.getElementById('view-step1-cvp'));
            });
            document.getElementById('btn-dash-empty-rev')?.addEventListener('click', () => {
                window.navigationManager?.switchScreen(document.getElementById('view-step1-revenue'));
            });
            return;
        }

        this.analysesFeed.innerHTML = filtered.map(a => {
            const isCvp = a.analysis_type === 'cvp';
            const typeBadge = isCvp ?
                '<span class="history-type-tag cvp-tag"><i class="fa-solid fa-bullseye"></i> CVP</span>' :
                '<span class="history-type-tag rev-tag"><i class="fa-solid fa-chart-line"></i> Revenue</span>';

            const dateStr = a.created_at ? new Date(a.created_at).toLocaleDateString(undefined, {
                month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit'
            }) : 'Recent Session';

            const summary = isCvp
                ? (a.input_data?.cvp_text || a.results_data?.cvp_text || 'Customer Value Proposition Projection')
                : (a.results_data?.top_recommendation || 'Financial Sensitivity & Lagging Indicators Model');

            const peerTag = a.results_data?.nearest_cvps?.[0]
                ? `<span class="dash-item-peer"><i class="fa-solid fa-building"></i> Nearest Peer: <strong>${this.escapeHtml(a.results_data.nearest_cvps[0].company)}</strong> (${a.results_data.nearest_cvps[0].similarity_pct}%)</span>`
                : '';

            return `
                <div class="dash-item-card">
                    <div class="dash-item-header">
                        <div class="dash-item-title-row">
                            ${typeBadge}
                            <h4 class="dash-item-title">${this.escapeHtml(a.title || 'Market Intelligence Model')}</h4>
                        </div>
                        <span class="dash-item-date"><i class="fa-regular fa-clock"></i> ${dateStr}</span>
                    </div>
                    <p class="dash-item-summary">"${this.escapeHtml(summary)}"</p>
                    <div class="dash-item-footer">
                        <div class="dash-item-meta">
                            ${peerTag}
                        </div>
                        <div class="dash-item-actions">
                            <button type="button" class="btn-dash-restore btn-history-restore" data-id="${a.id}">
                                <i class="fa-solid fa-arrow-up-right-from-square"></i>
                                <span>Restore to Workspace</span>
                            </button>
                            <button type="button" class="btn-dash-delete btn-history-delete" data-id="${a.id}" title="Delete Record">
                                <i class="fa-regular fa-trash-can"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    renderThreadsList() {
        if (!this.threadsList) return;

        if (this.conversations.length === 0) {
            this.threadsList.innerHTML = `
                <div class="dash-empty-state-mini">
                    <i class="fa-solid fa-comments"></i>
                    <p>No active cognitive threads recorded.</p>
                </div>
            `;
            return;
        }

        this.threadsList.innerHTML = this.conversations.slice(0, 5).map(c => {
            const dateStr = c.updated_at ? new Date(c.updated_at).toLocaleDateString(undefined, {
                month: 'short', day: 'numeric'
            }) : 'Recent';
            const count = Array.isArray(c.messages) ? c.messages.length : (c.turn_count || 1);

            return `
                <div class="dash-thread-card">
                    <div class="thread-info">
                        <h5 class="thread-title">${this.escapeHtml(c.title || 'Market Strategy Discussion')}</h5>
                        <div class="thread-meta">
                            <span><i class="fa-solid fa-message"></i> ${count} turn(s)</span>
                            <span>•</span>
                            <span>${dateStr}</span>
                        </div>
                    </div>
                    <button type="button" class="btn-dash-resume-thread btn-outline-sm" data-session-id="${c.session_id}">
                        <span>Resume</span>
                        <i class="fa-solid fa-arrow-right"></i>
                    </button>
                </div>
            `;
        }).join('');
    }

    async deleteAnalysis(id) {
        if (ApiClient.hasUserToken()) {
            try {
                const res = await UserHistoryApi.deleteAnalysis(id);
                if (res.success) {
                    this.analyses = this.analyses.filter(a => String(a.id) !== String(id));
                    this.renderKpis();
                    this.renderAnalysesFeed();
                    return;
                }
            } catch (err) {
                console.warn('[DashboardManager] Remote delete failed:', err.message);
            }
        }

        // Local deletion
        this.analyses = this.analyses.filter(a => String(a.id) !== String(id));
        try {
            localStorage.setItem('omniscope_guest_analyses', JSON.stringify(this.analyses));
        } catch {}
        this.renderKpis();
        this.renderAnalysesFeed();
    }

    getInitials(name) {
        if (!name) return 'EX';
        const parts = name.trim().split(/\s+/);
        if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
        return parts[0].slice(0, 2).toUpperCase();
    }

    escapeHtml(str) {
        return (str || '').replace(/[&<>"']/g, (m) => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        }[m]));
    }
}
