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

        this.btnPresetRetail = document.getElementById('btn-preset-csv-retail') || document.getElementById('btn-preset-retail');
        this.btnPresetTech = document.getElementById('btn-preset-csv-tech') || document.getElementById('btn-preset-tech');

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
        // Preset Buttons
        if (this.btnPresetRetail) {
            this.btnPresetRetail.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.loadPreset('retail');
            });
        }
        if (this.btnPresetTech) {
            this.btnPresetTech.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.loadPreset('tech');
            });
        }

        // Hidden input stop propagation on click
        if (this.inputFile) {
            this.inputFile.addEventListener('click', (e) => e.stopPropagation());
            this.inputFile.addEventListener('change', () => {
                if (this.inputFile.files && this.inputFile.files.length > 0) {
                    this.handleUploadedFile(this.inputFile.files[0]);
                }
            });
        }

        // Browse Files button
        if (this.btnBrowse && this.inputFile) {
            this.btnBrowse.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.inputFile.value = '';
                this.inputFile.click();
            });
        }

        // Drag and Drop Zone
        if (this.dropzone && this.inputFile) {
            this.dropzone.style.cursor = 'pointer';
            this.dropzone.addEventListener('click', (e) => {
                if (e.target.closest('#btn-clear-file') || e.target === this.inputFile) {
                    return;
                }
                this.inputFile.value = '';
                this.inputFile.click();
            });

            ['dragenter', 'dragover'].forEach(ev => {
                this.dropzone.addEventListener(ev, (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.dropzone.classList.add('drag-over');
                });
            });

            ['dragleave'].forEach(ev => {
                this.dropzone.addEventListener(ev, (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.dropzone.classList.remove('drag-over');
                });
            });

            this.dropzone.addEventListener('drop', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.dropzone.classList.remove('drag-over');
                const files = e.dataTransfer?.files;
                if (files && files.length > 0) {
                    this.handleUploadedFile(files[0]);
                }
            });
        }

        // Window dragover/drop guard to prevent accidental navigation
        window.addEventListener('dragover', (e) => {
            if (e.target && e.target.closest && e.target.closest('#revenue-dropzone')) return;
            e.preventDefault();
        }, false);
        window.addEventListener('drop', (e) => {
            if (e.target && e.target.closest && e.target.closest('#revenue-dropzone')) return;
            e.preventDefault();
        }, false);

        if (this.btnClearFile) {
            this.btnClearFile.addEventListener('click', (e) => {
                e.stopPropagation();
                this.parsedSeries = [];
                this.btnPresetRetail?.classList.remove('active');
                this.btnPresetTech?.classList.remove('active');
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
                document.querySelectorAll('.audit-category-accordion').forEach(card => card.classList.add('expanded'));
            });
        }
        if (this.btnCollapseAllAudit) {
            this.btnCollapseAllAudit.addEventListener('click', () => {
                document.querySelectorAll('.audit-category-accordion').forEach(card => card.classList.remove('expanded'));
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
        }
    }

    loadPreset(type) {
        if (type === 'retail') {
            this.btnPresetRetail?.classList.add('active');
            this.btnPresetTech?.classList.remove('active');
            const sampleCsv = `Date,Revenue_USD
2026-07-01 to 2026-07-07,142500
2026-07-08 to 2026-07-14,118500
2026-07-15 to 2026-07-21,112000
2026-07-22 to 2026-07-28,98400
2026-08-01 to 2026-08-07,105000
2026-08-08 to 2026-08-14,133500
2026-08-15 to 2026-08-21,128000
2026-08-22 to 2026-08-28,134100`;
            this.parseAndSetRevenueSeries(sampleCsv, 'retail_apparel_sales_jul_aug_2026.csv');
        } else {
            this.btnPresetTech?.classList.add('active');
            this.btnPresetRetail?.classList.remove('active');
            const sampleCsv = `Date,Revenue_USD
2026-07-01 to 2026-07-07,245000
2026-07-08 to 2026-07-14,230000
2026-07-15 to 2026-07-21,195000
2026-07-22 to 2026-07-28,212000
2026-08-01 to 2026-08-07,219000
2026-08-08 to 2026-08-14,240000
2026-08-15 to 2026-08-21,188000
2026-08-22 to 2026-08-28,205000`;
            this.parseAndSetRevenueSeries(sampleCsv, 'enterprise_tech_saas_jul_aug_2026.csv');
        }
    }

    handleUploadedFile(file) {
        if (!file) return;
        this.btnPresetRetail?.classList.remove('active');
        this.btnPresetTech?.classList.remove('active');
        const reader = new FileReader();
        reader.onload = (e) => this.parseAndSetRevenueSeries(e.target.result, file.name);
        reader.readAsText(file);
    }

    detectIntervalType(dateStr) {
        if (!dateStr) return 'Periodic';
        const lower = dateStr.toLowerCase();
        if (lower.includes('to') || lower.includes(' - ') || lower.includes(' – ') || lower.includes('through') || lower.includes('..')) {
            return 'Weekly / Date Range';
        }
        if (/^\d{4}[-/.]\d{1,2}$/.test(dateStr.trim()) || /^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)/i.test(dateStr.trim()) && !/\d{1,2},/.test(dateStr)) {
            return 'Monthly Aggregate';
        }
        if (/^\d{4}[-/.]\d{1,2}[-/.]\d{1,2}$/.test(dateStr.trim()) || /^\d{1,2}[-/.]\d{1,2}[-/.]\d{4}$/.test(dateStr.trim())) {
            return 'Daily Record';
        }
        return 'Date Interval';
    }

    parseAndSetRevenueSeries(content, filename = 'sales_data.csv') {
        const lines = content.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
        const rawRows = [];

        if (filename.endsWith('.json')) {
            try {
                const jsonObj = JSON.parse(content);
                const arr = Array.isArray(jsonObj) ? jsonObj : (jsonObj.data || jsonObj.revenue_series || []);
                arr.forEach(item => {
                    const dateVal = item.date || item.period || item.date_range || item.range || Object.values(item)[0] || '';
                    const revVal = item.revenue !== undefined ? item.revenue : (item.sales !== undefined ? item.sales : (item.metric !== undefined ? item.metric : Object.values(item)[1]));
                    const revClean = parseFloat(String(revVal).replace(/[\$,\s]/g, '')) || 0.0;
                    if (dateVal) {
                        rawRows.push({ period: String(dateVal).trim(), revenue: revClean });
                    }
                });
            } catch (err) {
                alert('Invalid JSON file format. Expecting array of { date, revenue } objects.');
                return;
            }
        } else {
            let headerFound = false;
            lines.forEach((line, idx) => {
                // Support comma-separated 2 columns
                const parts = line.split(',').map(p => p.trim().replace(/^["']|["']$/g, ''));
                if (parts.length >= 2) {
                    const first = parts[0].toLowerCase();
                    const second = parts[1].toLowerCase();
                    if (!headerFound && (first.includes('date') || first.includes('period') || first.includes('range') || second.includes('rev') || second.includes('sale'))) {
                        headerFound = true;
                        return;
                    }
                    const period = parts[0];
                    const revClean = parseFloat(parts[1].replace(/[\$,\s]/g, '')) || 0.0;
                    if (period) {
                        rawRows.push({ period, revenue: revClean });
                    }
                }
            });
        }

        if (rawRows.length === 0) {
            alert('No valid 2-column (Date, Revenue) data rows detected in file.');
            return;
        }

        // Compute sequential percentage fluctuation (ΔS) automatically from the 2 columns
        const series = rawRows.map((row, idx) => {
            let change_pct = 0.0;
            if (idx > 0) {
                const prevRev = rawRows[idx - 1].revenue;
                if (prevRev > 0) {
                    change_pct = parseFloat((((row.revenue - prevRev) / prevRev) * 100.0).toFixed(1));
                }
            }
            const interval_type = this.detectIntervalType(row.period);
            return {
                period: row.period,
                revenue: row.revenue,
                change_pct: change_pct,
                interval_type: interval_type,
                notes: `${interval_type}: Recorded Revenue of $${Number(row.revenue).toLocaleString()}`
            };
        });

        this.parsedSeries = series;
        if (this.fileNameLabel) this.fileNameLabel.textContent = filename;
        if (this.fileCountTag) this.fileCountTag.textContent = `${series.length} periods loaded (2-column format)`;
        if (this.fileStatusBar) this.fileStatusBar.classList.remove('hidden');

        // Render preview table
        const previewBox = document.getElementById('revenue-input-preview-box');
        const previewTbody = document.getElementById('revenue-preview-tbody');
        if (previewTbody) {
            previewTbody.innerHTML = series.map((item, idx) => {
                const isBaseline = idx === 0;
                const chgColor = isBaseline ? '#8892b0' : (item.change_pct < 0 ? '#ff4d4f' : (item.change_pct > 0 ? '#00FF66' : '#8892b0'));
                const chgSign = item.change_pct > 0 ? '+' : '';
                const chgDisplay = isBaseline ? '0.0% (Baseline)' : `${chgSign}${item.change_pct.toFixed(1)}%`;
                return `
                    <tr>
                        <td style="font-weight: 600; color: #fff; padding: 7px 10px;">
                            <i class="fa-regular fa-calendar-check" style="color: var(--accent-cyan); font-size: 11px; margin-right: 6px;"></i>
                            ${CompanyIntelligence.escapeHtml(item.period)}
                        </td>
                        <td style="color: #00E5FF; font-weight: 600; font-family: monospace; padding: 7px 10px;">
                            $${Number(item.revenue).toLocaleString()}
                        </td>
                        <td style="font-weight: 700; color: ${chgColor}; font-family: monospace; padding: 7px 10px;">
                            ${chgDisplay}
                        </td>
                        <td style="color: var(--text-muted); font-size: 11.5px; padding: 7px 10px;">
                            <span class="badge-tag" style="background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1);">
                                ${CompanyIntelligence.escapeHtml(item.interval_type)}
                            </span>
                        </td>
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
            this.state.activeClusters = data.active_clusters || [];

            this.renderInvestmentScore(data.investment_prognosis || null);
            this.renderLaggingNewsMatrix(data.matched_news || []);
            
            ChartVisualizer.drawPestleCanvas(this.canvasPestle, this.state.activePestleVector);
            ChartVisualizer.drawPorterCanvas(this.canvasPorter, this.state.activePorterVector);
            ChartVisualizer.updateSalesLegendValues(this.state.activePestleVector, this.state.activePorterVector);

            const sideCanvasPestle = document.getElementById('sidebar-canvas-pestle');
            const sideCanvasPorter = document.getElementById('sidebar-canvas-porter');
            if (sideCanvasPestle) ChartVisualizer.drawPestleCanvas(sideCanvasPestle, this.state.activePestleVector);
            if (sideCanvasPorter) ChartVisualizer.drawPorterCanvas(sideCanvasPorter, this.state.activePorterVector);



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

    renderInvestmentScore(prognosis) {
        if (!prognosis) return;

        const badgeTier = document.getElementById('badge-investment-tier');
        const pillRec = document.getElementById('pill-investment-rec');
        const gaugeCircle = document.getElementById('gauge-investment-circle');
        const valScore = document.getElementById('val-investment-score');
        const valMomentum = document.getElementById('val-trailing-momentum');
        const valVelocity = document.getElementById('val-growth-velocity');
        const valOutlook = document.getElementById('val-forward-outlook');
        const boxVerdict = document.getElementById('box-executive-verdict');
        const textVerdict = document.getElementById('text-investment-verdict');

        const statusMomentum = document.getElementById('status-factor-momentum');
        const barMomentum = document.getElementById('bar-factor-momentum');
        const statusGrowth = document.getElementById('status-factor-growth');
        const barGrowth = document.getElementById('bar-factor-growth');
        const statusResilience = document.getElementById('status-factor-resilience');
        const barResilience = document.getElementById('bar-factor-resilience');
        const statusRecovery = document.getElementById('status-factor-recovery');
        const barRecovery = document.getElementById('bar-factor-recovery');

        const listCatalysts = document.getElementById('list-investment-catalysts');
        const listDeterrents = document.getElementById('list-investment-deterrents');

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
        const color = prognosis.color || '#00E5FF';
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
        if (valMomentum) {
            const m = prognosis.growth_rate_trailing ?? 0;
            valMomentum.textContent = `${m >= 0 ? '+' : ''}${m.toFixed(1)}%`;
            valMomentum.style.color = m >= 0 ? 'var(--accent-green)' : '#f87171';
        }
        if (valVelocity) {
            const v = prognosis.acceleration_rate ?? 0;
            valVelocity.textContent = `${v >= 0 ? '+' : ''}${v.toFixed(1)}%`;
            valVelocity.style.color = v >= 0 ? 'var(--accent-green)' : '#f87171';
        }
        if (valOutlook) {
            valOutlook.textContent = prognosis.growth_outlook || '--';
            valOutlook.style.color = color;
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
        if (f.recent_momentum) {
            if (statusMomentum) statusMomentum.textContent = `${f.recent_momentum.status} (${f.recent_momentum.score}/100)`;
            if (barMomentum) {
                barMomentum.style.width = `${Math.min(100, Math.max(0, f.recent_momentum.score))}%`;
                barMomentum.style.background = f.recent_momentum.score >= 60 ? 'linear-gradient(90deg, #00FF66, #00E5FF)' : (f.recent_momentum.score < 45 ? 'linear-gradient(90deg, #f87171, #ef4444)' : 'linear-gradient(90deg, #f59e0b, #eab308)');
            }
        }
        if (f.growth_velocity) {
            if (statusGrowth) statusGrowth.textContent = `${f.growth_velocity.status} (${f.growth_velocity.score}/100)`;
            if (barGrowth) {
                barGrowth.style.width = `${Math.min(100, Math.max(0, f.growth_velocity.score))}%`;
                barGrowth.style.background = f.growth_velocity.score >= 60 ? 'linear-gradient(90deg, #00FF66, #00E5FF)' : (f.growth_velocity.score < 45 ? 'linear-gradient(90deg, #f87171, #ef4444)' : 'linear-gradient(90deg, #f59e0b, #eab308)');
            }
        }
        if (f.macro_resilience) {
            if (statusResilience) statusResilience.textContent = `${f.macro_resilience.status} (${f.macro_resilience.score}/100)`;
            if (barResilience) {
                barResilience.style.width = `${Math.min(100, Math.max(0, f.macro_resilience.score))}%`;
                barResilience.style.background = f.macro_resilience.score >= 60 ? 'linear-gradient(90deg, #00FF66, #00E5FF)' : (f.macro_resilience.score < 45 ? 'linear-gradient(90deg, #f87171, #ef4444)' : 'linear-gradient(90deg, #f59e0b, #eab308)');
            }
        }
        if (f.shock_recovery) {
            if (statusRecovery) statusRecovery.textContent = `${f.shock_recovery.status} (${f.shock_recovery.score}/100)`;
            if (barRecovery) {
                barRecovery.style.width = `${Math.min(100, Math.max(0, f.shock_recovery.score))}%`;
                barRecovery.style.background = f.shock_recovery.score >= 60 ? 'linear-gradient(90deg, #00FF66, #00E5FF)' : (f.shock_recovery.score < 50 ? 'linear-gradient(90deg, #f87171, #ef4444)' : 'linear-gradient(90deg, #f59e0b, #eab308)');
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
                        <i class="fa-solid fa-circle-check color-green"></i>
                        <span>${CompanyIntelligence.escapeHtml(c)}</span>
                    </li>
                `).join('');
            }
        }

        // Deterrents list
        if (listDeterrents) {
            const dets = prognosis.deterrents || [];
            if (dets.length === 0) {
                listDeterrents.innerHTML = '<li><span class="text-dim">No severe systemic deterrents identified.</span></li>';
            } else {
                listDeterrents.innerHTML = dets.map(d => `
                    <li class="insight-bullet-item deterrent-item">
                        <i class="fa-solid fa-triangle-exclamation color-amber"></i>
                        <span>${CompanyIntelligence.escapeHtml(d)}</span>
                    </li>
                `).join('');
            }
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
                const assignedScore = (cat.assigned_score !== undefined && cat.assigned_score !== null)
                    ? cat.assigned_score
                    : ((cat.score !== undefined && cat.score !== null) ? cat.score : 0.30);
                const scorePct = Math.round(assignedScore * 100);

                let scorePillClass = 'score-low';
                let sevClass = 'sev-low';
                if (scorePct >= 65) {
                    scorePillClass = 'score-high';
                    sevClass = 'sev-high';
                } else if (scorePct >= 40) {
                    scorePillClass = 'score-mod';
                    sevClass = 'sev-mod';
                }

                const items = cat.news_items || [];
                const hasShocks = items.length > 0 && (cat.dominant_fluctuation && cat.dominant_fluctuation !== 'Empirical Baseline (0.0%)');
                
                const rationaleText = cat.overall_rationale || cat.rationale || 
                    `Assigned baseline score of ${assignedScore.toFixed(2)} to ${cat.full_name || cat.name}. Empirical database indicators reflect macroeconomic and regulatory equilibrium with no acute abnormal revenue volatility recorded.`;

                const newsHtml = items.length === 0
                    ? '<p style="font-size:12px; color:var(--text-dim); padding:10px 0; font-style:italic;">No direct market shock items linked to this dimension in the analyzed fluctuation window. Baseline equilibrium maintained.</p>'
                    : items.map((n, idx) => {
                        const isPrimary = idx === 0 && hasShocks;
                        const fluctuationText = n.associated_fluctuation || '';
                        const isNegativeFluc = fluctuationText.startsWith('-');
                        const flucColor = isNegativeFluc ? '#ff4d4f' : (fluctuationText.startsWith('+') ? '#00FF66' : 'var(--accent-cyan)');

                        return `
                            <div class="audit-news-card ${isPrimary ? 'primary-shock' : ''}">
                                <div class="audit-news-top">
                                    <div class="audit-news-quote">"${CompanyIntelligence.escapeHtml(n.headline)}"</div>
                                    ${n.source_link ? `
                                        <a href="${CompanyIntelligence.escapeHtml(n.source_link)}" target="_blank" rel="noopener noreferrer" class="evidence-source-link">
                                            <i class="fa-solid fa-arrow-up-right-from-square"></i> Source Article
                                        </a>
                                    ` : ''}
                                </div>
                                <div class="audit-news-meta">
                                    <span><i class="fa-solid fa-calendar-day color-cyan"></i> Published: <strong>${CompanyIntelligence.escapeHtml(n.published_date || 'July–Aug 2026')}</strong></span>
                                    <span><i class="fa-solid fa-location-dot color-cyan"></i> Location: <strong>${CompanyIntelligence.escapeHtml(n.location_affected || 'Global')}</strong></span>
                                    ${fluctuationText ? `<span><i class="fa-solid fa-chart-line color-cyan"></i> Fluctuation: <strong style="color:${flucColor};">${CompanyIntelligence.escapeHtml(fluctuationText)}</strong></span>` : ''}
                                    ${n.likelihood_score ? `<span><i class="fa-solid fa-crosshairs color-cyan"></i> Causal Likelihood: <strong style="color:var(--accent-cyan);">${CompanyIntelligence.escapeHtml(n.likelihood_score)}</strong></span>` : ''}
                                </div>
                                ${n.item_rationale ? `
                                    <div class="audit-news-rationale">
                                        <strong style="color:#cbd5e1;">Lagging Indicator Sensitivity:</strong> ${CompanyIntelligence.escapeHtml(n.item_rationale)}
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    }).join('');

                return `
                    <div class="audit-category-accordion ${hasShocks ? 'active-shock' : ''}">
                        <div class="audit-category-header" onclick="this.parentElement.classList.toggle('expanded')">
                            <div class="audit-cat-left">
                                <i class="fa-solid fa-chevron-down accordion-chevron"></i>
                                <div>
                                    <div class="audit-cat-title">
                                        ${CompanyIntelligence.escapeHtml(cat.name)}
                                        <span class="audit-sev-badge ${sevClass}">${CompanyIntelligence.escapeHtml(cat.severity_level || (scorePct >= 65 ? 'High Exposure' : (scorePct >= 40 ? 'Moderate Exposure' : 'Low Exposure')))}</span>
                                    </div>
                                    <div style="font-size:11.5px; color:var(--text-muted); margin-top:3px; display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                                        <span><i class="fa-solid fa-newspaper color-cyan"></i> ${items.length} News Evidence Item${items.length === 1 ? '' : 's'} Linked</span>
                                        ${cat.dominant_fluctuation && cat.dominant_fluctuation !== 'Empirical Baseline (0.0%)' ? `<span>&bull; Associated Fluctuation: <strong style="color:${cat.dominant_fluctuation.startsWith('-') ? '#ff4d4f' : '#00FF66'};">${CompanyIntelligence.escapeHtml(cat.dominant_fluctuation)}</strong></span>` : ''}
                                    </div>
                                </div>
                            </div>
                            <div class="audit-cat-right">
                                <span class="audit-score-pill ${scorePillClass}">
                                    <i class="fa-solid fa-gauge-high"></i> ${scorePct}% Risk Score
                                </span>
                            </div>
                        </div>
                        <div class="audit-category-body">
                            <div class="category-rationale-box">
                                <strong style="color:var(--accent-cyan); display:flex; align-items:center; gap:6px; margin-bottom:5px;">
                                    <i class="fa-solid fa-circle-info"></i> Empirical Mathematical Rationale:
                                </strong>
                                ${CompanyIntelligence.escapeHtml(rationaleText)}
                            </div>
                            <div class="category-news-subheading">
                                <i class="fa-solid fa-newspaper"></i> Verified Database News Articles (July – August 2026)
                            </div>
                            <div class="audit-news-list">
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
