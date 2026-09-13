/**
 * Omniscope AI - Sales Workflow Module
 * Manages sales time-series parsing, fluctuation cluster generation, lagging indicator news assignment, and 11-category audit trail.
 */

import { SalesApi } from './api-client.js';
import { ChartVisualizer } from './chart-visualizer.js';
import { CompanyIntelligence } from './company-intelligence.js';

export class SalesWorkflow {
    constructor(state, callbacks = {}) {
        this.state = state;
        this.callbacks = callbacks;
        this.parsedSeries = [];
        this.initDom();
    }

    initDom() {
        this.dropzone = document.getElementById('revenue-dropzone');
        this.inputFile = document.getElementById('input-file-revenue');
        this.btnBrowse = document.getElementById('btn-browse-file');
        this.btnClearFile = document.getElementById('btn-clear-file');
        this.fileStatusBar = document.getElementById('file-status-bar');
        this.fileNameLabel = document.getElementById('file-name-label');
        this.fileCountTag = document.getElementById('file-count-tag');

        this.btnAnalyze = document.getElementById('btn-analyze-revenue');
        this.resultsPanel = document.getElementById('revenue-results-panel');
        this.canvasPestle = document.getElementById('canvas-revenue-pestle');
        this.canvasPorter = document.getElementById('canvas-revenue-porter');

        this.clustersList = document.getElementById('fluctuation-clusters-list');
        this.correlationMatrixList = document.getElementById('correlation-matrix-list');
        this.strategicEvidenceList = document.getElementById('strategic-evidence-list');
        this.auditPestleList = document.getElementById('audit-pestle-categories-list');
        this.auditPorterList = document.getElementById('audit-porter-categories-list');
        this.revenuePeersList = document.getElementById('revenue-peers-list');

        this.btnExpandAllAudit = document.getElementById('btn-expand-all-audit');
        this.btnCollapseAllAudit = document.getElementById('btn-collapse-all-audit');

        this.bindEvents();
    }

    bindEvents() {
        if (this.btnBrowse && this.inputFile) {
            this.btnBrowse.addEventListener('click', () => this.inputFile.click());
        }

        if (this.dropzone) {
            ['dragenter', 'dragover'].forEach(ev => {
                this.dropzone.addEventListener(ev, (e) => {
                    e.preventDefault();
                    this.dropzone.classList.add('drag-over');
                });
            });
            ['dragleave', 'drop'].forEach(ev => {
                this.dropzone.addEventListener(ev, (e) => {
                    e.preventDefault();
                    this.dropzone.classList.remove('drag-over');
                });
            });
            this.dropzone.addEventListener('drop', (e) => {
                const files = e.dataTransfer.files;
                if (files.length > 0) this.handleUploadedFile(files[0]);
            });
        }

        if (this.inputFile) {
            this.inputFile.addEventListener('change', (e) => {
                if (this.inputFile.files.length > 0) this.handleUploadedFile(this.inputFile.files[0]);
            });
        }

        if (this.btnClearFile) {
            this.btnClearFile.addEventListener('click', () => {
                this.parsedSeries = [];
                if (this.inputFile) this.inputFile.value = '';
                if (this.fileStatusBar) this.fileStatusBar.classList.add('hidden');
                const previewBox = document.getElementById('revenue-input-preview-box');
                if (previewBox) previewBox.classList.add('hidden');
                if (this.resultsPanel) this.resultsPanel.classList.add('hidden');
            });
        }

        if (this.btnAnalyze) {
            this.btnAnalyze.addEventListener('click', () => this.runAnalysis());
        }

        // Expand / Collapse Audit Accordions
        if (this.btnExpandAllAudit) {
            this.btnExpandAllAudit.addEventListener('click', () => {
                document.querySelectorAll('.audit-category-card').forEach(card => card.classList.add('expanded'));
            });
        }
        if (this.btnCollapseAllAudit) {
            this.btnCollapseAllAudit.addEventListener('click', () => {
                document.querySelectorAll('.audit-category-card').forEach(card => card.classList.remove('expanded'));
            });
        }

        // Delegate Peer clicks
        if (this.revenuePeersList) {
            this.revenuePeersList.addEventListener('click', (e) => {
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
        }
    }

    handleUploadedFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => this.parseAndSetRevenueSeries(e.target.result, file.name);
        reader.readAsText(file);
    }

    parseAndSetRevenueSeries(content, filename = 'sales_data.csv') {
        const lines = content.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
        const series = [];

        if (filename.endsWith('.json')) {
            try {
                const jsonObj = JSON.parse(content);
                const arr = Array.isArray(jsonObj) ? jsonObj : (jsonObj.data || jsonObj.revenue_series || []);
                arr.forEach(item => {
                    series.push({
                        period: item.period || item.date || item.quarter || 'Q1',
                        revenue: parseFloat(item.revenue || item.sales || item.value || 0),
                        change_pct: parseFloat(item.change_pct || item.change || 0),
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
                    const val = parseFloat(parts[1]) || 0.0;
                    const chg = parts.length >= 3 ? (parseFloat(parts[2]) || 0.0) : 0.0;
                    const notes = parts.length >= 4 ? parts.slice(3).join(', ') : '';
                    series.push({ period, revenue: val, change_pct: chg, notes: notes });
                }
            });
        }

        if (series.length === 0) {
            alert('No valid revenue rows detected in file.');
            return;
        }

        this.parsedSeries = series;
        if (this.fileNameLabel) this.fileNameLabel.textContent = filename;
        if (this.fileCountTag) this.fileCountTag.textContent = `${series.length} periods loaded`;
        if (this.fileStatusBar) this.fileStatusBar.classList.remove('hidden');

        // Render preview table
        const previewBox = document.getElementById('revenue-input-preview-box');
        const previewTbody = document.getElementById('revenue-preview-tbody');
        if (previewTbody) {
            previewTbody.innerHTML = series.map(item => {
                const chgColor = item.change_pct < 0 ? '#ff4d4f' : (item.change_pct > 0 ? '#00FF66' : '#8892b0');
                const chgSign = item.change_pct > 0 ? '+' : '';
                return `
                    <tr>
                        <td style="font-weight: 600; color: #fff; padding: 6px 10px;">${CompanyIntelligence.escapeHtml(item.period)}</td>
                        <td style="color: var(--text-muted); font-family: monospace; padding: 6px 10px;">$${Number(item.revenue).toLocaleString()}</td>
                        <td style="font-weight: 700; color: ${chgColor}; font-family: monospace; padding: 6px 10px;">${chgSign}${item.change_pct.toFixed(1)}%</td>
                        <td style="color: var(--text-muted); font-style: italic; padding: 6px 10px;">${CompanyIntelligence.escapeHtml(item.notes || 'Operational Performance')}</td>
                    </tr>
                `;
            }).join('');
        }
        if (previewBox) previewBox.classList.remove('hidden');
    }

    async runAnalysis() {
        if (this.parsedSeries.length === 0) {
            alert('Please drag & drop or select a sales CSV file first, or click a Sample Dataset.');
            return;
        }

        this.btnAnalyze.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Fluctuations & Evaluating Lagging Indicator News...`;
        this.btnAnalyze.disabled = true;

        try {
            const data = await SalesApi.matchRevenueClusters(this.parsedSeries, this.state.groqApiKey);
            if (data.error) throw new Error(data.error);

            this.state.activePestleVector = data.pestle_vector || [0.3, 0.3, 0.3, 0.3, 0.3, 0.3];
            this.state.activePorterVector = data.porter_vector || [0.3, 0.3, 0.3, 0.3, 0.3];
            this.state.activeUser11DVector = data.user_11d_vector || [...this.state.activePestleVector, ...this.state.activePorterVector];
            this.state.activeNearestCvps = data.nearest_cvps || [];

            this.renderFluctuationClusters(data.active_clusters || []);
            this.renderLaggingNewsMatrix(data.matched_news || []);
            
            ChartVisualizer.drawPestleCanvas(this.canvasPestle, this.state.activePestleVector);
            ChartVisualizer.drawPorterCanvas(this.canvasPorter, this.state.activePorterVector);
            ChartVisualizer.updateSalesLegendValues(this.state.activePestleVector, this.state.activePorterVector);



            this.renderStrategicEvidence(data.audit_categories || null, data.evidence_records || []);
            this.renderRevenuePeers(this.state.activeNearestCvps);

            if (this.resultsPanel) {
                this.resultsPanel.classList.remove('hidden');
                this.resultsPanel.scrollIntoView({ behavior: 'smooth' });
            }

            if (this.callbacks.onSalesAnalyzed) {
                this.callbacks.onSalesAnalyzed(data);
            }
        } catch (err) {
            alert(`Sales Analysis Error: ${err.message}`);
        } finally {
            this.btnAnalyze.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Match Revenue Fluctuation & Filter Relevant Market Clusters`;
            this.btnAnalyze.disabled = false;
        }
    }

    renderFluctuationClusters(clusters) {
        if (!this.clustersList) return;
        if (!clusters || clusters.length === 0) {
            this.clustersList.innerHTML = '<p class="text-dim">No fluctuation clusters detected.</p>';
            return;
        }

        this.clustersList.innerHTML = clusters.map(c => `
            <div class="fluctuation-cluster-card cluster-${CompanyIntelligence.escapeHtml(c.severity)}">
                <div class="cluster-card-header">
                    <div class="cluster-title-wrap">
                        <h4>${CompanyIntelligence.escapeHtml(c.cluster_name)}</h4>
                        <span class="cluster-band-badge badge-band-${CompanyIntelligence.escapeHtml(c.severity)}">${CompanyIntelligence.escapeHtml(c.badge)}</span>
                    </div>
                    <span style="font-weight:700; font-family:var(--font-heading); color:${c.avg_change_pct >= 0 ? 'var(--accent-green)' : '#f87171'}; font-size:14px;">
                        Average Fluctuation: ${c.avg_change_pct >= 0 ? '+' : ''}${c.avg_change_pct.toFixed(1)}%
                    </span>
                </div>
                <div class="cluster-meta-row">
                    <span><i class="fa-solid fa-calendar-days"></i> Periods (${c.period_count}): ${c.periods.map(p => `<span class="cluster-period-pill">${CompanyIntelligence.escapeHtml(p)}</span>`).join(' ')}</span>
                    <span class="dominant-category-tag"><i class="fa-solid fa-tag"></i> Dominant News Category: ${CompanyIntelligence.escapeHtml(c.dominant_category)} (${c.dominant_category_pct}% frequency)</span>
                </div>
                <div class="collective-decision-box">
                    <i class="fa-solid fa-lightbulb decision-icon"></i>
                    <div class="decision-text">
                        <strong>COLLECTIVE STRATEGIC DECISION:</strong><br>
                        ${CompanyIntelligence.escapeHtml(c.collective_decision)}
                    </div>
                </div>
            </div>
        `).join('');
    }

    renderLaggingNewsMatrix(newsItems) {
        if (!this.correlationMatrixList) return;
        if (!newsItems || newsItems.length === 0) {
            this.correlationMatrixList.innerHTML = '<p class="text-dim">No market events matched.</p>';
            return;
        }

        this.correlationMatrixList.innerHTML = newsItems.map(it => {
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
                            <div class="news-headline-text">${CompanyIntelligence.escapeHtml(it.news_headline)}</div>
                            <span class="news-category-badge"><i class="fa-solid fa-layer-group"></i> ${CompanyIntelligence.escapeHtml(it.category)}</span>
                            <div style="font-size:12px; color:var(--text-muted); margin-top:5px;">
                                <i class="fa-solid fa-calendar-days"></i> Recorded Period: <strong>${CompanyIntelligence.escapeHtml(it.period)}</strong> | Sales Fluctuation: <span class="${isDip ? 'fluctuation-pill-dip' : 'fluctuation-pill-spike'}">${it.change_pct >= 0 ? '+' : ''}${it.change_pct.toFixed(1)}%</span>
                            </div>
                        </div>
                        <div class="likelihood-meter-box">
                            <span class="likelihood-badge ${likelihoodClass}">
                                <i class="fa-solid fa-crosshairs"></i> ${it.likelihood_score}% Likelihood
                            </span>
                            <div class="likelihood-bar-track">
                                <div class="likelihood-bar-fill" style="width: ${it.likelihood_score}%; background: ${fillColor};"></div>
                            </div>
                            <span style="font-size:10.5px; color:var(--text-dim); margin-top:3px;">${CompanyIntelligence.escapeHtml(it.causal_status)}</span>
                        </div>
                    </div>
                    <div class="lagging-rationale-box">
                        <strong>Lagging Indicator Relationship:</strong> ${CompanyIntelligence.escapeHtml(it.lag_window)}<br>
                        <strong>Filter Rationale:</strong> ${CompanyIntelligence.escapeHtml(it.filter_rationale)}
                    </div>
                </div>
            `;
        }).join('');
    }

    renderStrategicEvidence(auditCategories, flatEvidences) {
        if (!auditCategories) return;

        const renderCatList = (cats, container) => {
            if (!container) return;
            container.innerHTML = cats.map(cat => {
                const scorePct = Math.round((cat.score || 0.3) * 100);
                const items = cat.news_items || [];
                const newsHtml = items.length === 0 
                    ? '<p style="font-size:12px; color:var(--text-dim); padding:8px 0;">No direct news items linked to this dimension in the selected time window.</p>'
                    : items.map(n => `
                        <div class="evidence-news-item">
                            <div class="ev-item-headline">${CompanyIntelligence.escapeHtml(n.headline)}</div>
                            <div class="ev-item-meta">
                                <span><i class="fa-solid fa-calendar"></i> ${CompanyIntelligence.escapeHtml(n.date || 'July-Aug 2026')}</span>
                                <span><i class="fa-solid fa-chart-line"></i> Associated Revenue Fluctuation: <strong style="color:${(n.fluctuation_pct||0) >= 0 ? 'var(--accent-green)' : '#f87171'};">${(n.fluctuation_pct||0) >= 0 ? '+' : ''}${n.fluctuation_pct}%</strong></span>
                                ${n.source_link ? `<a href="${n.source_link}" target="_blank" class="ev-item-source-link"><i class="fa-solid fa-arrow-up-right-from-square"></i> Source Link</a>` : ''}
                            </div>
                        </div>
                    `).join('');

                return `
                    <div class="audit-category-card" onclick="this.classList.toggle('expanded')">
                        <div class="audit-category-header">
                            <div class="audit-header-left">
                                <i class="fa-solid fa-chevron-right audit-chevron"></i>
                                <div>
                                    <h5 class="audit-cat-title">${CompanyIntelligence.escapeHtml(cat.name)}</h5>
                                    <div class="audit-cat-evidence-count"><i class="fa-solid fa-newspaper"></i> ${cat.evidence_count} News Evidence Items Linked</div>
                                </div>
                            </div>
                            <div class="audit-header-right">
                                <span class="audit-score-pill">${scorePct}% Risk Score</span>
                            </div>
                        </div>
                        <div class="audit-category-body">
                            <div class="audit-rationale-box">
                                <strong>Rationale for Assigned Score:</strong> ${CompanyIntelligence.escapeHtml(cat.rationale)}
                            </div>
                            <div class="evidence-news-list">
                                ${newsHtml}
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        };

        if (auditCategories.pestle) renderCatList(auditCategories.pestle, this.auditPestleList);
        if (auditCategories.porter) renderCatList(auditCategories.porter, this.auditPorterList);
    }

    renderRevenuePeers(matches) {
        if (!this.revenuePeersList) return;
        if (!matches || matches.length === 0) {
            this.revenuePeersList.innerHTML = '<p class="text-dim">No benchmark matches found.</p>';
            return;
        }

        const borderColors = ['#00E5FF', '#00FF66', '#10B981'];
        this.revenuePeersList.innerHTML = matches.map((m, idx) => `
            <div class="cvp-match-card" style="border-left: 4px solid ${borderColors[idx % 3]};">
                <div class="cvp-match-header">
                    <span>
                        <button type="button" class="company-profile-btn" data-company="${CompanyIntelligence.escapeHtml(m.company)}" title="Click to view on-DB company intelligence">
                            <span>${CompanyIntelligence.escapeHtml(m.company)}</span>
                            <i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 11px; opacity: 0.8;"></i>
                        </button>
                        <span class="cvp-match-sector-tag"><i class="fa-solid fa-building"></i> ${CompanyIntelligence.escapeHtml(m.sector || 'Enterprise')}</span>
                    </span>
                    <span class="cvp-match-badge" style="background: rgba(0, 229, 255, 0.12); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3);">${m.similarity_pct}% Vector Similarity</span>
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
    }
}
