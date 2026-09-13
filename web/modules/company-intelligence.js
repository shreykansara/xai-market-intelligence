/**
 * Omniscope AI - Company Intelligence Module
 * Manages company profile modals, benchmark peer cards, and relative PESTLE/Porter bar comparisons.
 */

import { CompanyApi } from './api-client.js';

export class CompanyIntelligence {
    static escapeHtml(str) {
        return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    static async loadAndShowProfile(companyName, userPestleVector = null, userPorterVector = null, onOverlayRequested = null) {
        const modal = document.getElementById('modal-company-profile');
        if (!modal) return;

        const elName = document.getElementById('modal-comp-name');
        const elSector = document.getElementById('modal-comp-sector');
        const elProduct = document.getElementById('modal-comp-product');
        const elCvp = document.getElementById('modal-comp-cvp');
        const elCustomer = document.getElementById('modal-comp-target-customer');
        const elNeed = document.getElementById('modal-comp-need');
        const elBenefit = document.getElementById('modal-comp-benefit');
        const pestleBars = document.getElementById('compare-pestle-bars');
        const porterBars = document.getElementById('compare-porter-bars');

        if (elName) elName.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Loading ${this.escapeHtml(companyName)}...`;
        if (elSector) elSector.textContent = 'Querying Database...';
        modal.classList.add('active');

        try {
            const data = await CompanyApi.getProfile(companyName);
            if (!data.success || !data.company) {
                alert(`Company profile for "${companyName}" not found.`);
                modal.classList.remove('active');
                return;
            }

            const comp = data.company;
            if (elName) elName.textContent = comp.company;
            if (elSector) elSector.textContent = comp.sector || 'Enterprise Technology';
            if (elProduct) elProduct.textContent = comp.product_name ? `${comp.product_name} (${comp.product_category || 'Core Product'})` : (comp.product_category || 'Enterprise Solution');
            if (elCvp) elCvp.textContent = `"${comp.cvp}"`;
            if (elCustomer) elCustomer.textContent = comp.target_customer || 'Enterprise Customers & Growth Teams';
            if (elNeed) elNeed.textContent = comp.statement_of_need || 'Operational efficiency, growth acceleration, and market risk hedging';
            if (elBenefit) elBenefit.textContent = comp.statement_of_key_benefit || 'Proprietary platform capability and strategic scalability';

            // Populate Relative Bar Comparisons
            const userP = userPestleVector || [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
            const compP = comp.pestle_vector || [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
            const pestleNames = ['Political Risk', 'Economic Pressure', 'Sociocultural Shift', 'Technological Velocity', 'Legal Compliance', 'Environmental Impact'];

            if (pestleBars) {
                pestleBars.innerHTML = pestleNames.map((name, i) => {
                    const uVal = Math.round((userP[i] || 0.3) * 100);
                    const cVal = Math.round((compP[i] || 0.3) * 100);
                    return `
                        <div class="compare-row">
                            <div class="compare-label-row">
                                <span class="compare-factor-title">${name}</span>
                                <span class="compare-scores">
                                    <span style="color:var(--accent-green);">${uVal}%</span> vs 
                                    <span style="color:var(--accent-cyan);">${cVal}%</span>
                                </span>
                            </div>
                            <div class="compare-bar-track">
                                <div class="bar-user-val" style="width: ${uVal}%;"></div>
                                <div class="bar-peer-val" style="width: ${cVal}%;"></div>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            const userF = userPorterVector || [0.3, 0.3, 0.3, 0.3, 0.3];
            const compF = comp.porter_vector || [0.3, 0.3, 0.3, 0.3, 0.3];
            const porterNames = ['Threat of New Entrants', 'Bargaining Power of Buyers', 'Bargaining Power of Suppliers', 'Threat of Substitutes', 'Competitive Rivalry'];

            if (porterBars) {
                porterBars.innerHTML = porterNames.map((name, i) => {
                    const uVal = Math.round((userF[i] || 0.3) * 100);
                    const cVal = Math.round((compF[i] || 0.3) * 100);
                    return `
                        <div class="compare-row">
                            <div class="compare-label-row">
                                <span class="compare-factor-title">${name}</span>
                                <span class="compare-scores">
                                    <span style="color:var(--accent-green);">${uVal}%</span> vs 
                                    <span style="color:var(--accent-cyan);">${cVal}%</span>
                                </span>
                            </div>
                            <div class="compare-bar-track">
                                <div class="bar-user-val" style="width: ${uVal}%;"></div>
                                <div class="bar-peer-val" style="width: ${cVal}%;"></div>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            // Wire Overlay button
            const btnOverlay = document.getElementById('btn-modal-overlay-radar');
            if (btnOverlay && onOverlayRequested) {
                btnOverlay.onclick = () => {
                    onOverlayRequested(comp);
                    modal.classList.remove('active');
                };
            }

            return comp;
        } catch (err) {
            alert(`Failed to load company profile: ${err.message}`);
            modal.classList.remove('active');
            return null;
        }
    }
}
