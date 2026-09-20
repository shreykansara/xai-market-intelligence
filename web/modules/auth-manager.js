/**
 * Omniscope AI - User Authentication Manager Module
 * Coordinates end-user registration, login, session persistence, guest migration, and UI state.
 */

import { ApiClient, UserAuthApi, UserHistoryApi } from './api-client.js';

export class AuthManager {
    constructor(callbacks = {}) {
        this.callbacks = callbacks;
        this.currentUser = null;
        this.activeTab = 'login'; // 'login' | 'register'
        this.initDom();
        this.bindEvents();
    }

    initDom() {
        // Auth Modal Elements
        this.modalAuth = document.getElementById('modal-auth');
        this.btnCloseAuth = document.getElementById('btn-close-auth');
        this.tabLogin = document.getElementById('tab-auth-login');
        this.tabRegister = document.getElementById('tab-auth-register');
        this.formLogin = document.getElementById('form-auth-login');
        this.formRegister = document.getElementById('form-auth-register');
        this.authAlert = document.getElementById('auth-alert');

        // Inputs - Login
        this.inputLoginEmail = document.getElementById('auth-login-email');
        this.inputLoginPassword = document.getElementById('auth-login-password');
        this.btnLoginSubmit = document.getElementById('btn-auth-login-submit');

        // Inputs - Register
        this.inputRegName = document.getElementById('auth-reg-name');
        this.inputRegEmail = document.getElementById('auth-reg-email');
        this.inputRegPassword = document.getElementById('auth-reg-password');
        this.inputRegCompany = document.getElementById('auth-reg-company');
        this.btnRegSubmit = document.getElementById('btn-auth-reg-submit');

        // Demo Quick Actions
        this.btnDemoFounder = document.getElementById('btn-demo-founder');
        this.btnDemoInvestor = document.getElementById('btn-demo-investor');

        // Target slots for Auth badges
        this.navAuthSlots = document.querySelectorAll('.auth-nav-slot');
    }

    bindEvents() {
        // Modal close
        this.btnCloseAuth?.addEventListener('click', () => this.closeModal());
        this.modalAuth?.addEventListener('click', (e) => {
            if (e.target === this.modalAuth) this.closeModal();
        });

        // Tab Switching
        this.tabLogin?.addEventListener('click', () => this.switchTab('login'));
        this.tabRegister?.addEventListener('click', () => this.switchTab('register'));

        // Form Submit - Login
        this.formLogin?.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleLogin();
        });

        // Form Submit - Register
        this.formRegister?.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleRegister();
        });

        // Demo shortcuts
        this.btnDemoFounder?.addEventListener('click', () => {
            this.switchTab('login');
            if (this.inputLoginEmail) this.inputLoginEmail.value = 'founder@omniscope.ai';
            if (this.inputLoginPassword) this.inputLoginPassword.value = 'Omniscope2026!';
            this.handleLogin();
        });

        this.btnDemoInvestor?.addEventListener('click', () => {
            this.switchTab('register');
            if (this.inputRegName) this.inputRegName.value = 'Elena Rostova';
            if (this.inputRegEmail) this.inputRegEmail.value = `investor_${Date.now().toString().slice(-4)}@capital.ai`;
            if (this.inputRegPassword) this.inputRegPassword.value = 'CapitalVentures2026!';
            if (this.inputRegCompany) this.inputRegCompany.value = 'Apex Horizon Ventures';
        });

        // Global delegate for open auth buttons
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('.btn-trigger-auth');
            if (btn) {
                const mode = btn.dataset.authMode || 'login';
                this.openModal(mode);
            }

            const btnDash = e.target.closest('.btn-menu-dashboard');
            if (btnDash) {
                e.preventDefault();
                document.querySelectorAll('.user-profile-badge.open').forEach(b => b.classList.remove('open'));
                window.navigationManager?.switchScreen(document.getElementById('view-user-dashboard'));
            }

            const btnLogout = e.target.closest('.btn-trigger-logout');
            if (btnLogout) {
                e.preventDefault();
                this.handleLogout();
            }

            const dropdownToggle = e.target.closest('.user-profile-toggle');
            if (dropdownToggle) {
                const parent = dropdownToggle.closest('.user-profile-badge');
                if (parent) parent.classList.toggle('open');
            } else if (!e.target.closest('.user-profile-badge')) {
                document.querySelectorAll('.user-profile-badge.open').forEach(b => b.classList.remove('open'));
            }
        });
    }

    async init() {
        const token = ApiClient.getUserToken();
        if (token) {
            try {
                const res = await UserAuthApi.getMe();
                if (res.success && res.user) {
                    this.currentUser = res.user;
                    this.renderAuthState();
                    await this.checkAndMigrateGuestData();
                    this.callbacks.onAuthStateChanged?.(this.currentUser);
                    return;
                }
            } catch (err) {
                console.warn('[AuthManager] Session token expired or invalid:', err.message);
                ApiClient.clearUserToken();
            }
        }
        this.currentUser = null;
        this.renderAuthState();
        this.callbacks.onAuthStateChanged?.(null);
    }

    openModal(tab = 'login') {
        this.switchTab(tab);
        this.hideAlert();
        this.modalAuth?.classList.add('active');
        if (tab === 'login') {
            this.inputLoginEmail?.focus();
        } else {
            this.inputRegName?.focus();
        }
    }

    closeModal() {
        this.modalAuth?.classList.remove('active');
        this.hideAlert();
    }

    switchTab(tab) {
        this.activeTab = tab;
        if (tab === 'login') {
            this.tabLogin?.classList.add('active');
            this.tabRegister?.classList.remove('active');
            this.formLogin?.classList.remove('hidden');
            this.formRegister?.classList.add('hidden');
        } else {
            this.tabRegister?.classList.add('active');
            this.tabLogin?.classList.remove('active');
            this.formRegister?.classList.remove('hidden');
            this.formLogin?.classList.add('hidden');
        }
        this.hideAlert();
    }

    showAlert(message, type = 'error') {
        if (!this.authAlert) return;
        this.authAlert.className = `auth-alert ${type}`;
        this.authAlert.innerHTML = `<i class="fa-solid ${type === 'error' ? 'fa-triangle-exclamation' : 'fa-circle-check'}"></i> <span>${message}</span>`;
        this.authAlert.classList.remove('hidden');
    }

    hideAlert() {
        if (this.authAlert) {
            this.authAlert.classList.add('hidden');
            this.authAlert.textContent = '';
        }
    }

    async handleLogin() {
        const email = this.inputLoginEmail?.value.trim();
        const password = this.inputLoginPassword?.value;

        if (!email || !password) {
            this.showAlert('Please enter both your email address and password.');
            return;
        }

        if (this.btnLoginSubmit) {
            this.btnLoginSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Authenticating...';
            this.btnLoginSubmit.disabled = true;
        }

        try {
            const res = await UserAuthApi.login(email, password);
            if (res.success && res.token) {
                ApiClient.setUserToken(res.token, true);
                this.currentUser = res.user;
                this.renderAuthState();
                this.closeModal();
                this.showToast(`Welcome back, ${res.user.full_name}!`, 'success');
                await this.checkAndMigrateGuestData();
                this.callbacks.onAuthStateChanged?.(this.currentUser);
                this.callbacks.onLoginSuccess?.(this.currentUser);
                window.navigationManager?.switchScreen(document.getElementById('view-user-dashboard'));
            } else {
                this.showAlert(res.error || 'Authentication failed. Please verify credentials.');
            }
        } catch (err) {
            this.showAlert(err.message || 'Login failed. Please check your credentials.');
        } finally {
            if (this.btnLoginSubmit) {
                this.btnLoginSubmit.innerHTML = 'Sign In to Omniscope <i class="fa-solid fa-arrow-right"></i>';
                this.btnLoginSubmit.disabled = false;
            }
        }
    }

    async handleRegister() {
        const name = this.inputRegName?.value.trim();
        const email = this.inputRegEmail?.value.trim();
        const password = this.inputRegPassword?.value;
        const company = this.inputRegCompany?.value.trim();

        if (!name || !email || !password) {
            this.showAlert('Please fill in all required fields (Name, Email, and Password).');
            return;
        }
        if (password.length < 6) {
            this.showAlert('Password must be at least 6 characters long.');
            return;
        }

        if (this.btnRegSubmit) {
            this.btnRegSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Creating Workspace...';
            this.btnRegSubmit.disabled = true;
        }

        try {
            const res = await UserAuthApi.register({
                email,
                password,
                full_name: name,
                company_name: company,
                role: 'founder'
            });
            if (res.success && res.token) {
                ApiClient.setUserToken(res.token, true);
                this.currentUser = res.user;
                this.renderAuthState();
                this.closeModal();
                this.showToast(`Account created! Welcome to Omniscope, ${res.user.full_name}.`, 'success');
                await this.checkAndMigrateGuestData();
                this.callbacks.onAuthStateChanged?.(this.currentUser);
                this.callbacks.onLoginSuccess?.(this.currentUser);
                window.navigationManager?.switchScreen(document.getElementById('view-user-dashboard'));
            } else {
                this.showAlert(res.error || 'Registration failed.');
            }
        } catch (err) {
            this.showAlert(err.message || 'Registration failed.');
        } finally {
            if (this.btnRegSubmit) {
                this.btnRegSubmit.innerHTML = 'Create Free Account <i class="fa-solid fa-sparkles"></i>';
                this.btnRegSubmit.disabled = false;
            }
        }
    }

    async handleLogout() {
        try {
            await UserAuthApi.logout();
        } catch (e) {
            // Ignore network errors on logout
        }
        ApiClient.clearUserToken();
        this.currentUser = null;
        this.renderAuthState();
        this.showToast('You have signed out of your Omniscope account.', 'info');
        this.callbacks.onAuthStateChanged?.(null);
    }

    // ==========================================
    // GUEST DATA MIGRATION
    // ==========================================

    static getGuestAnalyses() {
        try {
            return JSON.parse(localStorage.getItem('omniscope_guest_analyses') || '[]');
        } catch {
            return [];
        }
    }

    static saveGuestAnalysis(analysis) {
        try {
            const items = AuthManager.getGuestAnalyses();
            items.unshift(analysis);
            localStorage.setItem('omniscope_guest_analyses', JSON.stringify(items.slice(0, 20)));
        } catch (e) {
            console.warn('Could not cache guest analysis:', e);
        }
    }

    static getGuestConversations() {
        try {
            return JSON.parse(localStorage.getItem('omniscope_guest_conversations') || '[]');
        } catch {
            return [];
        }
    }

    static saveGuestConversation(conv) {
        try {
            const items = AuthManager.getGuestConversations();
            const existingIdx = items.findIndex(c => c.id === conv.id);
            if (existingIdx >= 0) {
                items[existingIdx] = conv;
            } else {
                items.unshift(conv);
            }
            localStorage.setItem('omniscope_guest_conversations', JSON.stringify(items.slice(0, 20)));
        } catch (e) {
            console.warn('Could not cache guest conversation:', e);
        }
    }

    async checkAndMigrateGuestData() {
        if (!this.currentUser) return;
        const guestAnalyses = AuthManager.getGuestAnalyses();
        const guestConversations = AuthManager.getGuestConversations();

        if (guestAnalyses.length === 0 && guestConversations.length === 0) return;

        try {
            const res = await UserHistoryApi.syncGuestData({
                analyses: guestAnalyses,
                conversations: guestConversations
            });
            if (res.success && (res.saved_analyses > 0 || res.saved_conversations > 0)) {
                localStorage.removeItem('omniscope_guest_analyses');
                localStorage.removeItem('omniscope_guest_conversations');
                this.showToast(`Migrated ${res.saved_analyses} previous analysis and ${res.saved_conversations} conversation into your account!`, 'success');
            }
        } catch (err) {
            console.warn('[AuthManager] Guest data migration warning:', err);
        }
    }

    // ==========================================
    // UI RENDERING & NOTIFICATIONS
    // ==========================================

    renderAuthState() {
        const slots = document.querySelectorAll('.auth-nav-slot');
        slots.forEach(slot => {
            if (!this.currentUser) {
                // Guest mode
                slot.innerHTML = `
                    <div class="auth-guest-group">
                        <button type="button" class="btn-outline-sm btn-trigger-auth" data-auth-mode="login">
                            <i class="fa-regular fa-user"></i>
                            <span>Sign In</span>
                        </button>
                        <button type="button" class="btn-primary-sm btn-trigger-auth" data-auth-mode="register">
                            <i class="fa-solid fa-sparkles"></i>
                            <span>Join Free</span>
                        </button>
                    </div>
                `;
            } else {
                // Authenticated user mode
                const initials = this.getInitials(this.currentUser.full_name || this.currentUser.email);
                const companyTag = this.currentUser.company_name ? ` • ${this.escapeHtml(this.currentUser.company_name)}` : '';
                slot.innerHTML = `
                    <div class="user-profile-badge">
                        <button type="button" class="user-profile-toggle" title="Account Menu">
                            <div class="user-avatar-circle">${initials}</div>
                            <div class="user-details-mini">
                                <span class="user-name-text">${this.escapeHtml(this.currentUser.full_name)}</span>
                                <span class="user-role-text">${this.escapeHtml(this.currentUser.role || 'Member')}${companyTag}</span>
                            </div>
                            <i class="fa-solid fa-chevron-down toggle-chevron"></i>
                        </button>
                        <div class="user-profile-menu glass-panel">
                            <div class="menu-header">
                                <strong>${this.escapeHtml(this.currentUser.full_name)}</strong>
                                <span>${this.escapeHtml(this.currentUser.email)}</span>
                            </div>
                            <div class="menu-divider"></div>
                            <button type="button" class="menu-item btn-menu-dashboard">
                                <i class="fa-solid fa-chart-pie"></i>
                                <span>Executive Dashboard</span>
                            </button>
                            <button type="button" class="menu-item btn-open-history">
                                <i class="fa-solid fa-clock-rotate-left"></i>
                                <span>Saved Intelligence Workspace</span>
                            </button>
                            <button type="button" class="menu-item btn-trigger-logout">
                                <i class="fa-solid fa-arrow-right-from-bracket"></i>
                                <span>Sign Out</span>
                            </button>
                        </div>
                    </div>
                `;
            }
        });
    }

    getInitials(name) {
        if (!name) return 'U';
        const parts = name.trim().split(/\s+/);
        if (parts.length >= 2) {
            return (parts[0][0] + parts[1][0]).toUpperCase();
        }
        return parts[0].slice(0, 2).toUpperCase();
    }

    escapeHtml(str) {
        return (str || '').replace(/[&<>"']/g, (m) => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        }[m]));
    }

    showToast(message, type = 'info') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `omniscope-toast ${type}`;
        const icon = type === 'success' ? 'fa-circle-check' : (type === 'error' ? 'fa-circle-exclamation' : 'fa-bell');
        toast.innerHTML = `
            <i class="fa-solid ${icon}"></i>
            <span>${this.escapeHtml(message)}</span>
        `;
        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 400);
        }, 4000);
    }
}
