/**
 * Omniscope AI - Navigation Manager Module
 * Handles multi-screen switching (Landing Page, Hub Selection, Step 1 CVP, Step 1 Revenue, Step 2 Chatbot) and preset loading.
 */

export class NavigationManager {
    constructor(state, callbacks = {}) {
        this.state = state;
        this.callbacks = callbacks;
        this.initDom();
    }

    initDom() {
        this.viewLandingPage = document.getElementById('view-landing-page');
        this.viewModeSelection = document.getElementById('view-mode-selection');
        this.viewStep1Cvp = document.getElementById('view-step1-cvp');
        this.viewStep1Revenue = document.getElementById('view-step1-revenue');
        this.viewStep2 = document.getElementById('view-step2-chatbot');

        this.btnNavLaunchApp = document.getElementById('btn-nav-launch-app');
        this.btnHeroLaunchCvp = document.getElementById('btn-hero-launch-cvp');
        this.btnHeroLaunchRevenue = document.getElementById('btn-hero-launch-revenue');
        this.heroPresetTesla = document.getElementById('hero-preset-tesla');
        this.heroPresetStripe = document.getElementById('hero-preset-stripe');
        this.btnFounderLaunch = document.getElementById('btn-founder-launch');
        this.btnInvestorLaunch = document.getElementById('btn-investor-launch');
        this.btnBannerLaunchHub = document.getElementById('btn-banner-launch-hub');
        this.btnBackLandingHub = document.getElementById('btn-back-landing-hub');
        this.brandLogoHome = document.getElementById('brand-logo-home');

        this.btnSelectCvpMode = document.getElementById('btn-select-cvp-mode');
        this.btnSelectRevenueMode = document.getElementById('btn-select-revenue-mode');
        this.btnBackHubCvp = document.getElementById('btn-back-hub-cvp');
        this.btnBackHubRevenue = document.getElementById('btn-back-hub-revenue');

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
    }

    switchScreen(targetView) {
        [this.viewLandingPage, this.viewModeSelection, this.viewStep1Cvp, this.viewStep1Revenue, this.viewStep2].forEach(view => {
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

    bindEvents() {
        // Brand logo
        this.brandLogoHome?.addEventListener('click', (e) => {
            e.preventDefault();
            this.switchScreen(this.viewLandingPage);
        });

        // Hub Launches
        [this.btnNavLaunchApp, this.btnBannerLaunchHub].forEach(btn => {
            btn?.addEventListener('click', () => this.switchScreen(this.viewModeSelection));
        });

        this.btnBackLandingHub?.addEventListener('click', () => this.switchScreen(this.viewLandingPage));

        // CVP Mode Select
        [this.btnHeroLaunchCvp, this.btnFounderLaunch, this.btnSelectCvpMode].forEach(btn => {
            btn?.addEventListener('click', () => {
                this.state.activeIntelligenceMode = 'cvp';
                this.switchScreen(this.viewStep1Cvp);
            });
        });

        // Revenue Mode Select
        [this.btnHeroLaunchRevenue, this.btnInvestorLaunch, this.btnSelectRevenueMode].forEach(btn => {
            btn?.addEventListener('click', () => {
                this.state.activeIntelligenceMode = 'revenue';
                this.switchScreen(this.viewStep1Revenue);
                this.callbacks.onRevenueModeActivated?.();
            });
        });

        this.btnBackHubCvp?.addEventListener('click', () => this.switchScreen(this.viewModeSelection));
        this.btnBackHubRevenue?.addEventListener('click', () => this.switchScreen(this.viewModeSelection));

        // Step 2 Proceed Handlers
        this.btnProceedToChatbot?.addEventListener('click', () => {
            this.switchScreen(this.viewStep2);
            this.callbacks.onProceedToChatbot?.();
        });

        this.btnProceedRevenueChatbot?.addEventListener('click', () => {
            this.switchScreen(this.viewStep2);
            this.callbacks.onProceedToChatbot?.();
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
