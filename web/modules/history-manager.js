/**
 * Omniscope AI - Saved Intelligence History Manager Module
 * Manages the slide-in workspace history drawer, displaying and restoring past CVP runs,
 * revenue fluctuation models, and AI conversation sessions.
 */

import { UserHistoryApi } from './api-client.js';
import { AuthManager } from './auth-manager.js';

export class HistoryManager {
    constructor(authManager, callbacks = {}) {
        this.authManager = authManager;
        this.callbacks = callbacks;
        this.activeFilter = 'all'; // 'all' | 'cvp' | 'revenue' | 'chat'
        this.analyses = [];
        this.conversations = [];
        this.searchQuery = '';
        this.initDom();
        this.bindEvents();
    }

    initDom() {
        this.drawer = document.getElementById('drawer-history');
        this.drawerBackdrop = document.getElementById('drawer-history-backdrop');
        this.btnCloseDrawer = document.getElementById('btn-close-drawer-history');
        this.listContainer = document.getElementById('history-items-list');
        this.inputSearch = document.getElementById('history-search-input');
        this.tabsContainer = document.getElementById('history-filter-tabs');
        this.countBadgeAll = document.getElementById('history-count-all');
        this.btnOpenDrawerTriggers = document.querySelectorAll('.btn-open-history');
    }

    bindEvents() {
        // Open drawer delegates
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-open-history')) {
                e.preventDefault();
                this.openDrawer();
            }
        });

        // Close drawer
        this.btnCloseDrawer?.addEventListener('click', () => this.closeDrawer());
        this.drawerBackdrop?.addEventListener('click', () => this.closeDrawer());

        // Search Input
        this.inputSearch?.addEventListener('input', (e) => {
            this.searchQuery = (e.target.value || '').toLowerCase().trim();
            this.renderFilteredItems();
        });

        // Tabs
        if (this.tabsContainer) {
            this.tabsContainer.addEventListener('click', (e) => {
                const btn = e.target.closest('.history-tab-btn');
                if (btn) {
                    this.tabsContainer.querySelectorAll('.history-tab-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    this.activeFilter = btn.dataset.filter || 'all';
                    this.renderFilteredItems();
                }
            });
        }

        // Delegate item actions (Restore & Delete)
        if (this.listContainer) {
            this.listContainer.addEventListener('click', async (e) => {
                const restoreBtn = e.target.closest('.btn-history-restore');
                if (restoreBtn) {
                    const id = restoreBtn.dataset.id;
                    const type = restoreBtn.dataset.type;
                    this.handleRestore(type, id);
                    return;
                }

                const deleteBtn = e.target.closest('.btn-history-delete');
                if (deleteBtn) {
                    const id = deleteBtn.dataset.id;
                    const type = deleteBtn.dataset.type;
                    await this.handleDelete(type, id);
                    return;
                }
            });
        }
    }

    async openDrawer() {
        this.drawer?.classList.add('active');
        this.drawerBackdrop?.classList.add('active');
        await this.loadData();
    }

    closeDrawer() {
        this.drawer?.classList.remove('active');
        this.drawerBackdrop?.classList.remove('active');
    }

    async loadData() {
        if (!this.listContainer) return;
        this.listContainer.innerHTML = `
            <div class="history-loading-state">
                <i class="fa-solid fa-spinner fa-spin"></i>
                <span>Retrieving saved market intelligence...</span>
            </div>
        `;

        try {
            if (this.authManager.currentUser) {
                // Fetch from authenticated backend
                const [analysesRes, convsRes] = await Promise.all([
                    UserHistoryApi.getAnalyses(),
                    UserHistoryApi.getConversations()
                ]);
                this.analyses = analysesRes.analyses || [];
                this.conversations = convsRes.conversations || [];
            } else {
                // Load from guest local storage
                this.analyses = AuthManager.getGuestAnalyses();
                this.conversations = AuthManager.getGuestConversations();
            }
        } catch (err) {
            console.warn('[HistoryManager] Data fetch error:', err.message);
            // Fallback to guest storage
            this.analyses = AuthManager.getGuestAnalyses();
            this.conversations = AuthManager.getGuestConversations();
        }

        this.updateCountBadges();
        this.renderFilteredItems();
    }

    updateCountBadges() {
        const total = (this.analyses?.length || 0) + (this.conversations?.length || 0);
        document.querySelectorAll('.history-count-badge').forEach(badge => {
            badge.textContent = total;
            badge.style.display = total > 0 ? 'inline-flex' : 'none';
        });
    }

    getCombinedItems() {
        const items = [];

        // Format analyses
        (this.analyses || []).forEach(a => {
            const isCvp = a.analysis_type === 'cvp';
            items.push({
                id: a.id,
                kind: 'analysis',
                type: a.analysis_type,
                title: a.title || (isCvp ? 'CVP Evaluation' : 'Revenue Fluctuation Model'),
                summary: a.summary || '',
                date: a.created_at || a.updated_at,
                data: a
            });
        });

        // Format conversations
        (this.conversations || []).forEach(c => {
            items.push({
                id: c.id,
                kind: 'conversation',
                type: 'chat',
                title: c.title || 'Market Intelligence Chat',
                summary: `${c.message_count || c.messages?.length || 0} messages • ${c.mode?.toUpperCase() || 'CVP'} mode`,
                date: c.updated_at || c.created_at,
                data: c
            });
        });

        // Sort descending by date
        items.sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0));
        return items;
    }

    renderFilteredItems() {
        if (!this.listContainer) return;

        let items = this.getCombinedItems();

        // Apply Tab Filter
        if (this.activeFilter === 'cvp') {
            items = items.filter(i => i.type === 'cvp');
        } else if (this.activeFilter === 'revenue') {
            items = items.filter(i => i.type === 'revenue');
        } else if (this.activeFilter === 'chat') {
            items = items.filter(i => i.kind === 'conversation');
        }

        // Apply Search
        if (this.searchQuery) {
            items = items.filter(i => 
                i.title.toLowerCase().includes(this.searchQuery) ||
                i.summary.toLowerCase().includes(this.searchQuery)
            );
        }

        if (items.length === 0) {
            this.listContainer.innerHTML = `
                <div class="history-empty-state">
                    <div class="empty-icon"><i class="fa-solid fa-folder-open"></i></div>
                    <h4>No Saved Intelligence Found</h4>
                    <p>${this.searchQuery ? 'No reports matched your search term.' : 'Run a CVP evaluation, upload revenue data, or ask the AI Strategist to build your workspace history.'}</p>
                    ${!this.authManager.currentUser ? `
                        <div class="empty-auth-hint">
                            <i class="fa-solid fa-shield-halved"></i>
                            <span>You are currently in Guest Mode. Sign in or register to sync your intelligence across sessions.</span>
                            <button type="button" class="btn-primary-sm btn-trigger-auth" data-auth-mode="register">Sign In / Join</button>
                        </div>
                    ` : ''}
                </div>
            `;
            return;
        }

        this.listContainer.innerHTML = items.map(item => this.renderItemCard(item)).join('');
    }

    renderItemCard(item) {
        const isCvp = item.type === 'cvp';
        const isRev = item.type === 'revenue';
        const isChat = item.kind === 'conversation';

        let badgeTag = '';
        let icon = '';
        if (isCvp) {
            icon = '<i class="fa-solid fa-bullseye" style="color: var(--accent-green);"></i>';
            badgeTag = '<span class="history-type-tag cvp-tag">CVP Value Prop</span>';
        } else if (isRev) {
            icon = '<i class="fa-solid fa-chart-line" style="color: var(--accent-cyan);"></i>';
            badgeTag = '<span class="history-type-tag rev-tag">Revenue Sensitivity</span>';
        } else {
            icon = '<i class="fa-solid fa-brain" style="color: var(--color-metric);"></i>';
            badgeTag = '<span class="history-type-tag chat-tag">AI Strategy Session</span>';
        }

        const dateStr = this.formatDate(item.date);

        return `
            <div class="history-item-card" data-id="${this.escapeHtml(item.id)}" data-type="${this.escapeHtml(item.type)}">
                <div class="item-card-header">
                    <div class="item-icon-title">
                        ${icon}
                        <h4 class="item-title" title="${this.escapeHtml(item.title)}">${this.escapeHtml(item.title)}</h4>
                    </div>
                    ${badgeTag}
                </div>
                <p class="item-summary">${this.escapeHtml(item.summary)}</p>
                <div class="item-card-footer">
                    <span class="item-timestamp"><i class="fa-regular fa-clock"></i> ${dateStr}</span>
                    <div class="item-actions">
                        <button type="button" class="btn-history-restore" data-id="${this.escapeHtml(item.id)}" data-type="${this.escapeHtml(item.type)}" title="Load report into workspace">
                            <i class="fa-solid fa-arrow-up-right-from-square"></i> Restore
                        </button>
                        <button type="button" class="btn-history-delete" data-id="${this.escapeHtml(item.id)}" data-type="${this.escapeHtml(item.type)}" title="Delete saved report">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    async handleRestore(type, id) {
        const item = this.getCombinedItems().find(i => i.id === id);
        if (!item) return;

        this.closeDrawer();

        if (item.kind === 'conversation') {
            let fullConv = item.data;
            if (this.authManager.currentUser && (!fullConv.messages || fullConv.messages.length === 0)) {
                try {
                    const res = await UserHistoryApi.getConversation(id);
                    if (res.success && res.conversation) fullConv = res.conversation;
                } catch (e) {
                    console.warn('Could not fetch full conversation detail:', e);
                }
            }
            this.callbacks.onRestoreConversation?.(fullConv);
            this.authManager.showToast(`Restored chat: "${item.title}"`, 'success');
        } else if (type === 'cvp') {
            let fullAnl = item.data;
            if (this.authManager.currentUser && !fullAnl.results_data) {
                try {
                    const res = await UserHistoryApi.getAnalysis(id);
                    if (res.success && res.analysis) fullAnl = res.analysis;
                } catch (e) {
                    console.warn('Could not fetch analysis detail:', e);
                }
            }
            this.callbacks.onRestoreCvp?.(fullAnl);
            this.authManager.showToast(`Loaded CVP: "${item.title}" into active workspace`, 'success');
        } else if (type === 'revenue') {
            let fullAnl = item.data;
            if (this.authManager.currentUser && !fullAnl.results_data) {
                try {
                    const res = await UserHistoryApi.getAnalysis(id);
                    if (res.success && res.analysis) fullAnl = res.analysis;
                } catch (e) {
                    console.warn('Could not fetch analysis detail:', e);
                }
            }
            this.callbacks.onRestoreRevenue?.(fullAnl);
            this.authManager.showToast(`Loaded Revenue Fluctuation model into active workspace`, 'success');
        }
    }

    async handleDelete(type, id) {
        if (!confirm('Are you sure you want to delete this saved intelligence item?')) return;

        try {
            if (this.authManager.currentUser) {
                if (type === 'chat') {
                    await UserHistoryApi.deleteConversation(id);
                } else {
                    await UserHistoryApi.deleteAnalysis(id);
                }
            } else {
                // Delete from local guest store
                if (type === 'chat') {
                    const convs = AuthManager.getGuestConversations().filter(c => c.id !== id);
                    localStorage.setItem('omniscope_guest_conversations', JSON.stringify(convs));
                } else {
                    const anls = AuthManager.getGuestAnalyses().filter(a => a.id !== id);
                    localStorage.setItem('omniscope_guest_analyses', JSON.stringify(anls));
                }
            }
            await this.loadData();
            this.authManager.showToast('Item deleted successfully.', 'info');
        } catch (err) {
            alert(`Delete failed: ${err.message}`);
        }
    }

    formatDate(isoStr) {
        if (!isoStr) return 'Just now';
        try {
            const dt = new Date(isoStr);
            const now = new Date();
            const diffMs = now - dt;
            const diffMins = Math.floor(diffMs / 60000);
            if (diffMins < 1) return 'Just now';
            if (diffMins < 60) return `${diffMins}m ago`;
            const diffHours = Math.floor(diffMins / 60);
            if (diffHours < 24) return `${diffHours}h ago`;
            return dt.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' });
        } catch {
            return 'Recently';
        }
    }

    escapeHtml(str) {
        return (str || '').replace(/[&<>"']/g, (m) => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        }[m]));
    }
}
