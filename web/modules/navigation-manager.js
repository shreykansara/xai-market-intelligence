/**
 * Omniscope AI - Navigation Manager Module
 * Handles multi-screen switching (Landing Page, Executive Dashboard, Hub Selection,
 * Step 1 CVP, Step 1 Revenue, Step 2 Chatbot), bidirectional HTML5 History URL bar sync,
 * popstate handling, and interactive presets.
 */

export class NavigationManager {
    constructor(state, callbacks = {}) {
        this.state = state;
        this.callbacks = callbacks;
        this.initDom();
    }

    initDom() {
        // Screens
        this.viewLandingPage = document.getElementById('view-landing-page');
        this.viewUserDashboard = document.getElementById('view-user-dashboard');
        this.viewModeSelection = document.getElementById('view-mode-selection');
        this.viewStep1Cvp = document.getElementById('view-step1-cvp');
        this.viewStep1Revenue = document.getElementById('view-step1-revenue');
        this.viewStep2 = document.getElementById('view-step2-chatbot');

        // Nav and Hero Buttons
        this.btnNavLaunchApp = document.getElementById('btn-nav-launch-app');
        this.btnNavDashboard = document.getElementById('nav-link-dashboard');
        this.footLinkDashboard = document.getElementById('foot-link-dashboard');
        this.btnHeroLaunchCvp = document.getElementById('btn-hero-launch-cvp');
        this.btnHeroLaunchRevenue = document.getElementById('btn-hero-launch-revenue');
        this.heroPresetTesla = document.getElementById('hero-preset-tesla');
        this.heroPresetStripe = document.getElementById('hero-preset-stripe');
        this.btnFounderLaunch = document.getElementById('btn-founder-launch');
        this.btnInvestorLaunch = document.getElementById('btn-investor-launch');
        this.btnBannerLaunchHub = document.getElementById('btn-banner-launch-hub');
        this.btnBackLandingHub = document.getElementById('btn-back-landing-hub');
        this.brandLogoHome = document.getElementById('brand-logo-home');
        this.brandLogoDash = document.getElementById('brand-logo-dash');

        // Hub Buttons
        this.btnSelectCvpMode = document.getElementById('btn-select-cvp-mode');
        this.btnSelectRevenueMode = document.getElementById('btn-select-revenue-mode');
        this.btnBackHubCvp = document.getElementById('btn-back-hub-cvp');
        this.btnBackHubRevenue = document.getElementById('btn-back-hub-revenue');

        // Dashboard Buttons
        this.btnDashToHub = document.getElementById('btn-dash-to-hub');
        this.btnDashNewCvp = document.getElementById('btn-dash-new-cvp');
        this.btnDashNewRevenue = document.getElementById('btn-dash-new-revenue');
        this.btnDashNewChat = document.getElementById('btn-dash-new-chat');
        this.btnLaunchCvpAct = document.getElementById('btn-launch-cvp-act');
        this.btnLaunchRevAct = document.getElementById('btn-launch-rev-act');
        this.btnLaunchChatAct = document.getElementById('btn-launch-chat-act');

        // Presets
        this.btnPresetCvpTesla = document.getElementById('btn-preset-cvp-tesla');
        this.btnPresetCvpStripe = document.getElementById('btn-preset-cvp-stripe');
        this.btnPresetRetail = document.getElementById('btn-preset-retail') || document.getElementById('btn-preset-csv-retail');
        this.btnPresetTech = document.getElementById('btn-preset-tech') || document.getElementById('btn-preset-csv-tech');

        // Sidebar Navigation
        this.btnBackStep1 = document.getElementById('btn-back-step1');
        this.btnChangeCvp = document.getElementById('btn-change-cvp');
        this.btnSidebarHub = document.getElementById('btn-sidebar-hub');
        this.btnSidebarHome = document.getElementById('btn-sidebar-home');
        this.btnProceedToChatbot = document.getElementById('btn-proceed-to-chatbot');
        this.btnProceedRevenueChatbot = document.getElementById('btn-proceed-revenue-chatbot');

        this.bindEvents();

        // Synchronize initial screen from browser URL bar on load
        this.handleRouteFromLocation(false);
    }

    getAllViews() {
        return [
            this.viewLandingPage,
            this.viewUserDashboard,
            this.viewModeSelection,
            this.viewStep1Cvp,
            this.viewStep1Revenue,
            this.viewStep2
        ].filter(Boolean);
    }

    getPathForView(view) {
        if (!view) return '/';
        if (view === this.viewUserDashboard) return '/dashboard';
        if (view === this.viewModeSelection) return '/hub';
        if (view === this.viewStep1Cvp) return '/cvp';
        if (view === this.viewStep1Revenue) return '/revenue';
        if (view === this.viewStep2) return '/chat';
        return '/';
    }

    getViewForPath(path) {
        const cleanPath = (path || '').toLowerCase().replace(/\/$/, '') || '/';
        if (cleanPath === '/dashboard') return this.viewUserDashboard;
        if (cleanPath === '/hub') return this.viewModeSelection;
        if (cleanPath === '/cvp') return this.viewStep1Cvp;
        if (cleanPath === '/revenue') return this.viewStep1Revenue;
        if (cleanPath === '/chat') return this.viewStep2;
        return this.viewLandingPage;
    }

    switchScreen(targetView, updateUrl = true) {
        if (!targetView) return;

        this.getAllViews().forEach(view => {
            view.classList.remove('active');
            view.classList.add('hidden');
        });

        targetView.classList.remove('hidden');
        targetView.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });

        const path = this.getPathForView(targetView);
        if (updateUrl && window.location.pathname !== path) {
            window.history.pushState({ screenId: targetView.id, path }, '', path);
        }

        // Trigger view-specific callbacks
        if (targetView === this.viewUserDashboard) {
            this.callbacks.onDashboardActivated?.();
        } else if (targetView === this.viewStep1Revenue) {
            this.state.activeIntelligenceMode = 'revenue';
            this.callbacks.onRevenueModeActivated?.();
        } else if (targetView === this.viewStep1Cvp) {
            this.state.activeIntelligenceMode = 'cvp';
        } else if (targetView === this.viewStep2) {
            this.callbacks.onProceedToChatbot?.();
        }
    }

    handleRouteFromLocation(updateUrl = false) {
        const path = window.location.pathname.toLowerCase().replace(/\/$/, '') || '/';
        const targetView = this.getViewForPath(path);
        this.switchScreen(targetView, updateUrl);
    }

    navigateToRoute(path) {
        const view = this.getViewForPath(path);
        if (view) {
            this.switchScreen(view, true);
        }
    }

    bindEvents() {
        // Browser Back / Forward buttons sync
        window.addEventListener('popstate', (e) => {
            if (e.state?.path) {
                const view = this.getViewForPath(e.state.path);
                this.switchScreen(view, false);
            } else {
                this.handleRouteFromLocation(false);
            }
        });

        // Brand Logos
        this.brandLogoHome?.addEventListener('click', (e) => {
            e.preventDefault();
            this.switchScreen(this.viewLandingPage);
        });

        this.brandLogoDash?.addEventListener('click', (e) => {
            e.preventDefault();
            this.switchScreen(this.viewLandingPage);
        });

        // Dashboard Links
        [this.btnNavDashboard, this.footLinkDashboard].forEach(link => {
            link?.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchScreen(this.viewUserDashboard);
            });
        });

        // Hub Launches
        [this.btnNavLaunchApp, this.btnBannerLaunchHub, this.btnDashToHub].forEach(btn => {
            btn?.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchScreen(this.viewModeSelection);
            });
        });

        this.btnBackLandingHub?.addEventListener('click', () => this.switchScreen(this.viewLandingPage));

        // CVP Mode Select
        [this.btnHeroLaunchCvp, this.btnFounderLaunch, this.btnSelectCvpMode, this.btnDashNewCvp, this.btnLaunchCvpAct].forEach(btn => {
            btn?.addEventListener('click', () => {
                this.state.activeIntelligenceMode = 'cvp';
                this.switchScreen(this.viewStep1Cvp);
            });
        });

        // Revenue Mode Select
        [this.btnHeroLaunchRevenue, this.btnInvestorLaunch, this.btnSelectRevenueMode, this.btnDashNewRevenue, this.btnLaunchRevAct].forEach(btn => {
            btn?.addEventListener('click', () => {
                this.state.activeIntelligenceMode = 'revenue';
                this.switchScreen(this.viewStep1Revenue);
            });
        });

        // Chatbot Launches from Dashboard
        [this.btnDashNewChat, this.btnLaunchChatAct].forEach(btn => {
            btn?.addEventListener('click', () => {
                this.switchScreen(this.viewStep2);
            });
        });

        this.btnBackHubCvp?.addEventListener('click', () => this.switchScreen(this.viewModeSelection));
        this.btnBackHubRevenue?.addEventListener('click', () => this.switchScreen(this.viewModeSelection));

        // Step 2 Proceed Handlers
        this.btnProceedToChatbot?.addEventListener('click', () => {
            this.switchScreen(this.viewStep2);
        });

        this.btnProceedRevenueChatbot?.addEventListener('click', () => {
            this.switchScreen(this.viewStep2);
        });

        // Left Panel Back & Edit in Step 1 Handler
        const returnToStep1 = () => {
            if (this.state.activeIntelligenceMode === 'revenue') {
                this.switchScreen(this.viewStep1Revenue);
            } else {
                this.switchScreen(this.viewStep1Cvp);
                const input = document.getElementById('input-cvp-text');
                if (input) {
                    if (this.state.activeCvpText && !input.value) {
                        input.value = this.state.activeCvpText;
                    }
                    input.focus();
                }
            }
        };

        this.btnBackStep1?.addEventListener('click', returnToStep1);
        this.btnChangeCvp?.addEventListener('click', returnToStep1);

        this.btnSidebarHub?.addEventListener('click', () => this.switchScreen(this.viewModeSelection));
        this.btnSidebarHome?.addEventListener('click', () => this.switchScreen(this.viewLandingPage));

        // Presets
        const tataMotorsText = "For safety-conscious middle-class Indian families and modern urban commuters who demand certified 5-star crash safety and reliable indigenous electric personal mobility, the Nexon EV & Bharat NCAP 5-Star SUV Range is a Electric & ICE Compact SUVs that delivers certified 5-star structural crash safety, indigenous Ziptron EV powertrains, and extensive public charging ecosystem support.";
        const zerodhaText = "For active retail stock traders, long-term equity investors, and DIY personal finance managers who demand zero-brokerage long-term investing, blazing-fast trade execution, and transparent flat ₹20 F&O pricing, the Kite Trading Platform & Console Analytics is a Discount Broking & Wealth Technology that delivers zero brokerage on equity delivery investments, ultra-reliable sub-millisecond Kite execution, and comprehensive tax P&L reporting.";

        const loadCvpPreset = (text) => {
            this.state.activeIntelligenceMode = 'cvp';
            this.switchScreen(this.viewStep1Cvp);
            const input = document.getElementById('input-cvp-text');
            if (input) {
                input.value = text;
                input.focus();
            }
            const step1Results = document.getElementById('step1-results-panel');
            if (step1Results) step1Results.classList.add('hidden');
        };

        this.btnPresetCvpTesla?.addEventListener('click', () => loadCvpPreset(tataMotorsText));
        this.heroPresetTesla?.addEventListener('click', () => loadCvpPreset(tataMotorsText));
        this.btnPresetCvpStripe?.addEventListener('click', () => loadCvpPreset(zerodhaText));
        this.heroPresetStripe?.addEventListener('click', () => loadCvpPreset(zerodhaText));

        // Revenue presets
        this.btnPresetRetail?.addEventListener('click', () => this.callbacks.onLoadRetailPreset?.());
        this.btnPresetTech?.addEventListener('click', () => this.callbacks.onLoadTechPreset?.());
    }
}
