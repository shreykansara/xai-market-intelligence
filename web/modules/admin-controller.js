/**
 * Omniscope AI - Admin Controller Module
 * Modular driver for Stage 1 Ingestion, Stage 2 NLP Filtering, Stage 3 11-D Projection, and Orchestrator.
 */

import { AdminApi } from './api-client.js';

export class AdminController {
    constructor() {
        this.s1Page = 1;
        this.s2Page = 1;
        this.s3Page = 1;
        this.s1PollInterval = null;
        this.s2PollInterval = null;
        this.s3PollInterval = null;
        this.initDom();
    }

    initDom() {
        this.dbStatusPill = document.getElementById('admin-db-status');
        this.statS1 = document.getElementById('stat-s1-count');
        this.statS2 = document.getElementById('stat-s2-count');
        this.statS3 = document.getElementById('stat-s3-count');
        this.statComp = document.getElementById('stat-comp-count');

        // Stage 1
        this.s1Start = document.getElementById('s1-start-date');
        this.s1End = document.getElementById('s1-end-date');
        this.s1Btn = document.getElementById('s1-submit-btn');
        this.s1ProgressBox = document.getElementById('s1-progress-box');
        this.s1ProgressPct = document.getElementById('s1-progress-pct');
        this.s1ProgressFill = document.getElementById('s1-progress-fill');
        this.s1ProgressMsg = document.getElementById('s1-progress-msg');
        this.s1StatusBox = document.getElementById('s1-status-box');
        this.s1FilesBody = document.getElementById('s1-files-body');
        this.s1Search = document.getElementById('s1-search');
        this.s1Tbody = document.getElementById('s1-records-body');
        this.s1PageInfo = document.getElementById('s1-page-info');

        // Stage 2
        this.s2PreviousFilesBody = document.getElementById('s2-previous-files-body');
        this.s2Batch = document.getElementById('s2-batch-size');
        this.s2Btn = document.getElementById('s2-submit-btn');
        this.s2ProgressBox = document.getElementById('s2-progress-box');
        this.s2ProgressPct = document.getElementById('s2-progress-pct');
        this.s2ProgressFill = document.getElementById('s2-progress-fill');
        this.s2ProgressMsg = document.getElementById('s2-progress-msg');
        this.s2StatusBox = document.getElementById('s2-status-box');
        this.s2Search = document.getElementById('s2-search');
        this.s2Location = document.getElementById('s2-location-filter');
        this.s2Tbody = document.getElementById('s2-records-body');
        this.s2PageInfo = document.getElementById('s2-page-info');

        // Stage 3
        this.s3PreviousFilesBody = document.getElementById('s3-previous-files-body');
        this.s3Batch = document.getElementById('s3-batch-size');
        this.s3Btn = document.getElementById('s3-submit-btn');
        this.s3ProgressBox = document.getElementById('s3-progress-box');
        this.s3ProgressPct = document.getElementById('s3-progress-pct');
        this.s3ProgressFill = document.getElementById('s3-progress-fill');
        this.s3ProgressMsg = document.getElementById('s3-progress-msg');
        this.s3StatusBox = document.getElementById('s3-status-box');
        this.s3Search = document.getElementById('s3-search');
        this.s3Tbody = document.getElementById('s3-records-body');
        this.s3PageInfo = document.getElementById('s3-page-info');

        this.bindEvents();
    }

    bindEvents() {
        // Tab switching
        window.switchAdminTab = (tabId) => this.switchTab(tabId);

        // Selection and Bulk Actions
        window.toggleSelectAll = (cbClass, masterEl) => this.toggleSelectAll(cbClass, masterEl);
        window.updateBulkBar = (cbClass, barId, countId) => this.updateBulkBar(cbClass, barId, countId);

        // Stage 1
        this.s1Btn?.addEventListener('click', () => this.startStage1());
        this.s1Search?.addEventListener('keyup', (e) => { if (e.key === 'Enter') this.loadStage1Records(); });
        window.loadStage1Files = () => this.loadStage1Files();
        window.loadStage1Records = () => this.loadStage1Records();
        window.prevPageStage1 = () => { if (this.s1Page > 1) { this.s1Page--; this.loadStage1Records(); } };
        window.nextPageStage1 = () => { this.s1Page++; this.loadStage1Records(); };
        window.goToStage2ForFile = (date) => this.goToStage2ForFile(date);
        window.deleteStage1File = (id, date) => this.deleteStage1File(id, date);
        window.deleteSelectedStage1Files = () => this.deleteSelectedStage1Files();
        window.deleteStage1Record = (id) => this.deleteStage1Record(id);
        window.deleteSelectedStage1Records = () => this.deleteSelectedStage1Records();
        window.deleteAllStage1Records = () => this.deleteAllStage1Records();

        // Stage 2
        this.s2Btn?.addEventListener('click', () => this.startStage2());
        this.s2Search?.addEventListener('keyup', (e) => { if (e.key === 'Enter') this.loadStage2Records(); });
        this.s2Location?.addEventListener('change', () => this.loadStage2Records());
        window.loadStage1FilesForStage2 = () => this.loadStage1FilesForStage2();
        window.convertStage1File = (date) => this.convertStage1File(date);
        window.convertSelectedStage1Files = () => this.convertSelectedStage1Files();
        window.startStage2Processing = () => this.startStage2();
        window.loadStage2Records = () => this.loadStage2Records();
        window.prevPageStage2 = () => { if (this.s2Page > 1) { this.s2Page--; this.loadStage2Records(); } };
        window.nextPageStage2 = () => { this.s2Page++; this.loadStage2Records(); };
        window.deleteStage2Record = (id) => this.deleteStage2Record(id);
        window.deleteSelectedStage2Records = () => this.deleteSelectedStage2Records();
        window.deleteAllStage2Records = () => this.deleteAllStage2Records();

        // Stage 3
        this.s3Btn?.addEventListener('click', () => this.startStage3());
        this.s3Search?.addEventListener('keyup', (e) => { if (e.key === 'Enter') this.loadStage3News(); });
        window.loadStage2FilesForStage3 = () => this.loadStage2FilesForStage3();
        window.convertStage2Batch = (date) => this.convertStage2Batch(date);
        window.convertSelectedStage2Batches = () => this.convertSelectedStage2Batches();
        window.deleteStage2Batch = (date) => this.deleteStage2Batch(date);
        window.deleteSelectedStage2Batches = () => this.deleteSelectedStage2Batches();
        window.startStage3Processing = () => this.startStage3();
        window.loadStage3News = () => this.loadStage3News();
        window.loadStage3DBStatus = () => this.loadDbStatus();
        window.prevPageStage3 = () => { if (this.s3Page > 1) { this.s3Page--; this.loadStage3News(); } };
        window.nextPageStage3 = () => { this.s3Page++; this.loadStage3News(); };
        window.deleteStage3Article = (id) => this.deleteStage3Article(id);
        window.deleteSelectedStage3Articles = () => this.deleteSelectedStage3Articles();

        // Auto initialize
        this.loadDbStatus();
        this.syncNextIngestionDates();
        this.loadStage1Files();
        this.loadStage1Records();
        this.loadStage1FilesForStage2();
        this.loadStage2FilesForStage3();
    }

    // ==========================================
    // SELECTION & BULK UTILITIES
    // ==========================================
    toggleSelectAll(cbClass, masterEl) {
        const checkboxes = document.querySelectorAll(`.${cbClass}`);
        checkboxes.forEach(cb => { cb.checked = masterEl.checked; });
        if (cbClass === 's1-file-cb') {
            this.updateBulkBar('s1-file-cb', 's1-files-bulk-bar', 's1-files-selected-count');
        } else if (cbClass === 's1-record-cb') {
            this.updateBulkBar('s1-record-cb', 's1-records-bulk-bar', 's1-records-selected-count');
        } else if (cbClass === 's2-file-cb') {
            this.updateBulkBar('s2-file-cb', 's2-files-bulk-bar', 's2-files-selected-count');
        } else if (cbClass === 's2-record-cb') {
            this.updateBulkBar('s2-record-cb', 's2-records-bulk-bar', 's2-records-selected-count');
        } else if (cbClass === 's3-batch-cb') {
            this.updateBulkBar('s3-batch-cb', 's3-batches-bulk-bar', 's3-batches-selected-count');
        } else if (cbClass === 's3-article-cb') {
            this.updateBulkBar('s3-article-cb', 's3-articles-bulk-bar', 's3-articles-selected-count');
        }
    }

    updateBulkBar(cbClass, barId, countId) {
        const checked = document.querySelectorAll(`.${cbClass}:checked`);
        const bar = document.getElementById(barId);
        const countEl = document.getElementById(countId);
        if (countEl) countEl.textContent = checked.length;
        if (bar) {
            if (checked.length > 0) {
                bar.classList.add('active');
            } else {
                bar.classList.remove('active');
            }
        }
    }

    resetMasterCheckbox(id, barId, countId) {
        const master = document.getElementById(id);
        if (master) master.checked = false;
        const bar = document.getElementById(barId);
        if (bar) bar.classList.remove('active');
        const countEl = document.getElementById(countId);
        if (countEl) countEl.textContent = '0';
    }

    switchTab(tabId) {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));

        const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick')?.includes(tabId));
        if (targetBtn) targetBtn.classList.add('active');

        const panel = document.getElementById(`panel-${tabId}`);
        if (panel) panel.classList.add('active');

        if (tabId === 'stage1') {
            this.syncNextIngestionDates();
            this.loadStage1Files();
            this.loadStage1Records();
        }
        if (tabId === 'stage2') {
            this.loadStage1FilesForStage2();
            this.loadStage2Records();
        }
        if (tabId === 'stage3') {
            this.loadDbStatus();
            this.loadStage2FilesForStage3();
            this.loadStage3News();
        }
        if (tabId === 'orchestrator') this.loadDbStatus();
    }

    async syncNextIngestionDates() {
        try {
            const data = await AdminApi.getStage1NextDate();
            if (data && data.success && data.next_date) {
                if (this.s1Start) this.s1Start.value = data.next_date;
                if (this.s1End) this.s1End.value = data.next_date;
            }
        } catch (err) {
            console.error('Error syncing next ingestion date:', err);
        }
    }

    async loadDbStatus() {
        try {
            const data = await AdminApi.getStage3DbStatus();
            if (data.connected) {
                if (this.statS1) this.statS1.textContent = (data.stage1_raw_count || 0).toLocaleString();
                if (this.statS2) this.statS2.textContent = (data.stage2_filtered_count || 0).toLocaleString();
                if (this.statS3) this.statS3.textContent = (data.news_articles_count || 0).toLocaleString();
                if (this.statComp) this.statComp.textContent = (data.benchmark_companies_count || 500).toLocaleString();

                if (this.dbStatusPill) {
                    this.dbStatusPill.innerHTML = `
                        <span class="status-dot"></span> Supabase Vector DB Connected (${data.news_articles_count.toLocaleString()} Master News Live)
                    `;
                }
            }
        } catch (err) {
            console.error('Error loading DB status:', err);
        }
    }

    // ==========================================
    // STAGE 1: INGESTION & FILES
    // ==========================================
    async startStage1() {
        const sDate = this.s1Start?.value;
        const eDate = this.s1End?.value;
        if (!sDate || !eDate) {
            alert('Please select start and end dates.');
            return;
        }

        this.s1Btn.disabled = true;
        if (this.s1ProgressBox) this.s1ProgressBox.style.display = 'block';
        if (this.s1StatusBox) this.s1StatusBox.style.display = 'none';

        try {
            const res = await AdminApi.ingestStage1(sDate, eDate);
            if (!res.success) throw new Error(res.error);

            if (this.s1PollInterval) clearInterval(this.s1PollInterval);
            this.s1PollInterval = setInterval(async () => {
                const prog = await AdminApi.getStage1Progress();
                if (this.s1ProgressPct) this.s1ProgressPct.textContent = `${prog.progress_pct || 0}%`;
                if (this.s1ProgressFill) this.s1ProgressFill.style.width = `${prog.progress_pct || 0}%`;
                if (this.s1ProgressMsg) this.s1ProgressMsg.textContent = prog.message || 'Processing...';

                if (prog.status === 'completed' || prog.status === 'error') {
                    clearInterval(this.s1PollInterval);
                    this.s1PollInterval = null;
                    this.s1Btn.disabled = false;
                    this.loadDbStatus();
                    this.loadStage1Files();
                    this.loadStage1Records();
                    this.loadStage1FilesForStage2();
                    this.syncNextIngestionDates();

                    if (this.s1StatusBox) {
                        this.s1StatusBox.style.display = 'block';
                        this.s1StatusBox.style.background = prog.status === 'completed' ? 'rgba(0, 229, 255, 0.12)' : 'rgba(255, 0, 85, 0.12)';
                        this.s1StatusBox.style.border = `1px solid ${prog.status === 'completed' ? 'var(--accent-cyan)' : 'var(--danger-accent)'}`;
                        this.s1StatusBox.style.color = prog.status === 'completed' ? 'var(--accent-cyan)' : '#FF4D6D';
                        this.s1StatusBox.innerHTML = `<strong>${prog.status.toUpperCase()}:</strong> ${prog.message}`;
                    }
                }
            }, 800);
        } catch (err) {
            this.s1Btn.disabled = false;
            alert(`Stage 1 Error: ${err.message}`);
        }
    }

    async loadStage1Files() {
        if (!this.s1FilesBody) return;
        this.resetMasterCheckbox('s1-files-select-all', 's1-files-bulk-bar', 's1-files-selected-count');
        try {
            const res = await AdminApi.getStage1Files();
            const activeFiles = (res.files || []).filter(f => f.remaining_count > 0);
            if (res.success && activeFiles.length > 0) {
                this.s1FilesBody.innerHTML = activeFiles.map(f => {
                    const statusTag = f.remaining_count < f.raw_count 
                        ? `<span class="badge-tag tag-amber">PARTIALLY CONVERTED</span>`
                        : `<span class="badge-tag tag-cyan">INGESTED (READY)</span>`;

                    return `
                        <tr>
                            <td style="text-align: center;">
                                <input type="checkbox" class="table-checkbox s1-file-cb" data-id="${f.id}" data-date="${f.date}" onchange="updateBulkBar('s1-file-cb', 's1-files-bulk-bar', 's1-files-selected-count')">
                            </td>
                            <td style="font-weight: 600; color: var(--text-main); font-family: monospace;">
                                <i class="fa-solid fa-file-zipper" style="color: var(--accent-cyan); margin-right: 6px;"></i>
                                ${f.filename}
                            </td>
                            <td style="white-space: nowrap;">${f.date}</td>
                            <td>${f.size_mb > 0 ? f.size_mb + ' MB' : 'In-Memory Stream'}</td>
                            <td style="font-weight: 700;">${f.raw_count.toLocaleString()} items</td>
                            <td>
                                <span class="badge-tag tag-cyan">
                                    ${f.remaining_count.toLocaleString()} remaining in S1
                                </span>
                            </td>
                            <td>${statusTag}</td>
                            <td>
                                <div style="display: flex; gap: 0.4rem; align-items: center;">
                                    <button class="btn btn-secondary" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;" onclick="goToStage2ForFile('${f.date}')">
                                        Proceed to Stage 2 Filter <i class="fa-solid fa-arrow-right"></i>
                                    </button>
                                    <button class="btn-danger-mini" title="Delete file and raw records from database" onclick="deleteStage1File('${f.id}', '${f.date}')">
                                        <i class="fa-solid fa-trash-can"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    `;
                }).join('');
            } else {
                this.s1FilesBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">No active Stage 1 archives found in database. All processed archives are immediately purged once moved.</td></tr>`;
            }
        } catch (err) {
            console.error('Error loading Stage 1 files:', err);
        }
    }

    async deleteStage1File(id, date) {
        if (!confirm(`Are you sure you want to permanently delete archive "${id || date}" and all its raw news records from Stage 1?`)) {
            return;
        }
        try {
            const res = await AdminApi.deleteStage1Files([id], [date]);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage1Files();
                this.loadStage1Records();
                this.loadStage1FilesForStage2();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }

    async deleteSelectedStage1Files() {
        const checked = document.querySelectorAll('.s1-file-cb:checked, .s2-file-cb:checked');
        const ids = [];
        const dates = [];
        checked.forEach(cb => {
            const id = cb.getAttribute('data-id');
            const date = cb.getAttribute('data-date');
            if (id && !ids.includes(id)) ids.push(id);
            if (date && !dates.includes(date)) dates.push(date);
        });

        if (dates.length === 0 && ids.length === 0) {
            alert('Please select at least one file to delete.');
            return;
        }

        if (!confirm(`Are you sure you want to delete ${dates.length || ids.length} selected Stage 1 file(s) and their raw records?`)) {
            return;
        }

        try {
            const res = await AdminApi.deleteStage1Files(ids, dates);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage1Files();
                this.loadStage1Records();
                this.loadStage1FilesForStage2();
            } else {
                alert(`Bulk delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Bulk Delete Error: ${err.message}`);
        }
    }

    async loadStage1Records() {
        const search = this.s1Search?.value || '';
        this.resetMasterCheckbox('s1-records-select-all', 's1-records-bulk-bar', 's1-records-selected-count');
        try {
            const data = await AdminApi.getStage1Records(this.s1Page, 15, search);
            if (this.s1Tbody) {
                if (data.records && data.records.length > 0) {
                    this.s1Tbody.innerHTML = data.records.map(r => `
                        <tr>
                            <td style="text-align: center;">
                                <input type="checkbox" class="table-checkbox s1-record-cb" data-id="${r.id}" onchange="updateBulkBar('s1-record-cb', 's1-records-bulk-bar', 's1-records-selected-count')">
                            </td>
                            <td style="white-space: nowrap;">${r.date}</td>
                            <td style="font-weight: 500;">${r.actor1 || '--'}</td>
                            <td>${r.actor2 || '--'}</td>
                            <td><span class="badge-tag tag-cyan">${r.country || 'Global'}</span></td>
                            <td style="max-width: 320px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                                <a href="${r.source_url}" target="_blank" style="color: var(--accent-cyan); text-decoration: none;">
                                    ${r.source_url}
                                </a>
                            </td>
                            <td><span class="badge-tag tag-green">${r.status || 'RAW'}</span></td>
                            <td>
                                <button class="btn-danger-mini" title="Delete raw record" onclick="deleteStage1Record('${r.id}')">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('');
                    if (this.s1PageInfo) this.s1PageInfo.textContent = `Page ${data.page} of ${data.pages} (${data.total.toLocaleString()} total raw records)`;
                } else {
                    this.s1Tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 2rem;">No raw records found.</td></tr>`;
                }
            }
        } catch (err) {
            console.error(err);
        }
    }

    async deleteStage1Record(id) {
        if (!confirm('Delete this raw record from Stage 1?')) return;
        try {
            const res = await AdminApi.deleteStage1Records([id]);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage1Records();
                this.loadStage1Files();
                this.loadStage1FilesForStage2();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }

    async deleteSelectedStage1Records() {
        const checked = document.querySelectorAll('.s1-record-cb:checked');
        const ids = Array.from(checked).map(cb => cb.getAttribute('data-id')).filter(Boolean);
        if (ids.length === 0) {
            alert('Please select at least one record to delete.');
            return;
        }
        if (!confirm(`Delete ${ids.length} selected raw record(s)?`)) return;

        try {
            const res = await AdminApi.deleteStage1Records(ids);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage1Records();
                this.loadStage1Files();
                this.loadStage1FilesForStage2();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }

    async deleteAllStage1Records() {
        if (!confirm('CAUTION: Are you sure you want to permanently delete ALL raw records and exports from Stage 1?')) return;
        try {
            const res = await AdminApi.deleteStage1Records([], true);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage1Records();
                this.loadStage1Files();
                this.loadStage1FilesForStage2();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }

    goToStage2ForFile(date) {
        this.switchTab('stage2');
        const targetRow = document.getElementById(`s2-file-row-${date}`);
        if (targetRow) {
            targetRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
            targetRow.style.backgroundColor = 'rgba(168, 85, 247, 0.15)';
            setTimeout(() => { targetRow.style.backgroundColor = ''; }, 2000);
        }
    }

    // ==========================================
    // STAGE 2: PREVIOUS STAGE FILES & NLP FILTER
    // ==========================================
    async loadStage1FilesForStage2() {
        if (!this.s2PreviousFilesBody) return;
        this.resetMasterCheckbox('s2-files-select-all', 's2-files-bulk-bar', 's2-files-selected-count');
        try {
            const res = await AdminApi.getStage1Files();
            const activeFiles = (res.files || []).filter(f => f.remaining_count > 0);
            if (res.success && activeFiles.length > 0) {
                this.s2PreviousFilesBody.innerHTML = activeFiles.map(f => {
                    return `
                        <tr id="s2-file-row-${f.date}">
                            <td style="text-align: center;">
                                <input type="checkbox" class="table-checkbox s2-file-cb" data-id="${f.id}" data-date="${f.date}" onchange="updateBulkBar('s2-file-cb', 's2-files-bulk-bar', 's2-files-selected-count')">
                            </td>
                            <td style="font-weight: 600; color: var(--text-main); font-family: monospace;">
                                <i class="fa-solid fa-file-zipper" style="color: var(--accent-purple); margin-right: 6px;"></i>
                                ${f.filename}
                            </td>
                            <td style="white-space: nowrap;">${f.date}</td>
                            <td>
                                <span class="badge-tag tag-cyan">${f.remaining_count.toLocaleString()} raw records waiting</span>
                            </td>
                            <td>
                                <select id="s2-file-batch-${f.date}" style="padding: 0.35rem 0.6rem; font-size: 0.82rem; background: var(--bg-dark); border: 1px solid var(--border-color); color: var(--text-main); border-radius: var(--radius-sm);">
                                    <option value="50">50 Items</option>
                                    <option value="100" selected>100 Items</option>
                                    <option value="250">250 Items</option>
                                    <option value="500">500 Items</option>
                                    <option value="1000">1,000 Items</option>
                                    <option value="-1">All ${f.remaining_count.toLocaleString()} Items</option>
                                </select>
                            </td>
                            <td>
                                <div style="display: flex; gap: 0.4rem; align-items: center;">
                                    <button class="btn btn-purple" id="btn-s1-convert-${f.date}" style="padding: 0.4rem 0.85rem; font-size: 0.82rem;" onclick="convertStage1File('${f.date}')">
                                        <i class="fa-solid fa-play"></i> Convert / Filter File
                                    </button>
                                    <button class="btn-danger-mini" title="Delete file and its raw records" onclick="deleteStage1File('${f.id}', '${f.date}')">
                                        <i class="fa-solid fa-trash-can"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    `;
                }).join('');
            } else {
                this.s2PreviousFilesBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">No Stage 1 archives pending conversion. All completed archives have been purged from Stage 1.</td></tr>`;
            }
        } catch (err) {
            console.error('Error loading Stage 1 files for Stage 2:', err);
        }
    }

    async convertStage1File(date) {
        const batchSelect = document.getElementById(`s2-file-batch-${date}`);
        const batchSize = batchSelect ? parseInt(batchSelect.value) : 100;
        const btn = document.getElementById(`btn-s1-convert-${date}`);

        if (btn) {
            btn.disabled = true;
            btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Filtering...`;
        }

        if (this.s2ProgressBox) this.s2ProgressBox.style.display = 'block';
        if (this.s2StatusBox) this.s2StatusBox.style.display = 'none';

        try {
            const res = await AdminApi.processStage2(batchSize, date);
            if (!res.success) throw new Error(res.error);

            this.trackStage2Progress(btn);
        } catch (err) {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = `<i class="fa-solid fa-play"></i> Convert / Filter File`;
            }
            alert(`Conversion Error for ${date}: ${err.message}`);
        }
    }

    async convertSelectedStage1Files() {
        const checked = document.querySelectorAll('.s2-file-cb:checked');
        const dates = Array.from(checked).map(cb => cb.getAttribute('data-date')).filter(Boolean);
        if (dates.length === 0) {
            alert('Please select at least one Stage 1 file to convert.');
            return;
        }

        if (this.s2ProgressBox) this.s2ProgressBox.style.display = 'block';
        if (this.s2StatusBox) this.s2StatusBox.style.display = 'none';

        try {
            const res = await AdminApi.processStage2(-1, null, dates);
            if (!res.success) throw new Error(res.error);

            this.trackStage2Progress();
        } catch (err) {
            alert(`Bulk Conversion Error: ${err.message}`);
        }
    }

    trackStage2Progress(btn = null) {
        if (this.s2PollInterval) clearInterval(this.s2PollInterval);
        this.s2PollInterval = setInterval(async () => {
            const prog = await AdminApi.getStage2Progress();
            if (this.s2ProgressPct) this.s2ProgressPct.textContent = `${prog.progress_pct || 0}%`;
            if (this.s2ProgressFill) this.s2ProgressFill.style.width = `${prog.progress_pct || 0}%`;
            if (this.s2ProgressMsg) this.s2ProgressMsg.textContent = prog.message || 'Processing...';

            if (prog.status === 'completed' || prog.status === 'error') {
                clearInterval(this.s2PollInterval);
                this.s2PollInterval = null;
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = `<i class="fa-solid fa-play"></i> Convert / Filter File`;
                }
                this.loadDbStatus();
                this.loadStage1FilesForStage2();
                this.loadStage2Records();
                this.loadStage1Files();
                this.loadStage2FilesForStage3();

                if (this.s2StatusBox) {
                    this.s2StatusBox.style.display = 'block';
                    this.s2StatusBox.style.background = prog.status === 'completed' ? 'rgba(168, 85, 247, 0.12)' : 'rgba(255, 0, 85, 0.12)';
                    this.s2StatusBox.style.border = `1px solid ${prog.status === 'completed' ? 'var(--accent-purple)' : 'var(--danger-accent)'}`;
                    this.s2StatusBox.style.color = prog.status === 'completed' ? 'var(--accent-purple)' : '#FF4D6D';
                    this.s2StatusBox.innerHTML = `<strong>${prog.status.toUpperCase()}:</strong> ${prog.message}`;
                }
            }
        }, 800);
    }

    async startStage2() {
        const batch = parseInt(this.s2Batch?.value || '100');
        this.s2Btn.disabled = true;
        if (this.s2ProgressBox) this.s2ProgressBox.style.display = 'block';
        if (this.s2StatusBox) this.s2StatusBox.style.display = 'none';

        try {
            const res = await AdminApi.processStage2(batch);
            if (!res.success) throw new Error(res.error);

            this.trackStage2Progress();
            const resetBtn = setInterval(() => {
                if (!this.s2PollInterval) {
                    this.s2Btn.disabled = false;
                    clearInterval(resetBtn);
                }
            }, 800);
        } catch (err) {
            this.s2Btn.disabled = false;
            alert(`Stage 2 Error: ${err.message}`);
        }
    }

    async loadStage2Records() {
        const search = this.s2Search?.value || '';
        const loc = this.s2Location?.value || '';
        this.resetMasterCheckbox('s2-records-select-all', 's2-records-bulk-bar', 's2-records-selected-count');
        try {
            const data = await AdminApi.getStage2Records(this.s2Page, 15, search, loc);
            if (this.s2Tbody) {
                if (data.records && data.records.length > 0) {
                    this.s2Tbody.innerHTML = data.records.map(r => `
                        <tr>
                            <td style="text-align: center;">
                                <input type="checkbox" class="table-checkbox s2-record-cb" data-id="${r.id}" onchange="updateBulkBar('s2-record-cb', 's2-records-bulk-bar', 's2-records-selected-count')">
                            </td>
                            <td style="white-space: nowrap;">${r.date}</td>
                            <td style="font-weight: 600; color: var(--text-main);">${r.headline}</td>
                            <td><span class="badge-tag tag-purple">${r.category || 'General Market'}</span></td>
                            <td><span class="badge-tag tag-cyan">${r.location_affected}</span></td>
                            <td><a href="${r.source_link}" target="_blank" style="color: var(--accent-cyan); text-decoration: none;"><i class="fa-solid fa-arrow-up-right-from-square"></i> Source</a></td>
                            <td><span class="badge-tag tag-green">${r.status}</span></td>
                            <td>
                                <button class="btn-danger-mini" title="Delete filtered record" onclick="deleteStage2Record('${r.id}')">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('');
                    if (this.s2PageInfo) this.s2PageInfo.textContent = `Page ${data.page} of ${data.pages} (${data.total.toLocaleString()} filtered records)`;
                } else {
                    this.s2Tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 2rem;">No Stage 2 filtered records in database.</td></tr>`;
                }
            }
        } catch (err) {
            console.error(err);
        }
    }

    async deleteStage2Record(id) {
        if (!confirm('Delete this record from Stage 2?')) return;
        try {
            const res = await AdminApi.deleteStage2Records([id]);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage2Records();
                this.loadStage2FilesForStage3();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }

    async deleteSelectedStage2Records() {
        const checked = document.querySelectorAll('.s2-record-cb:checked');
        const ids = Array.from(checked).map(cb => cb.getAttribute('data-id')).filter(Boolean);
        if (ids.length === 0) {
            alert('Please select at least one record to delete.');
            return;
        }
        if (!confirm(`Delete ${ids.length} selected Stage 2 record(s)?`)) return;

        try {
            const res = await AdminApi.deleteStage2Records(ids);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage2Records();
                this.loadStage2FilesForStage3();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }

    async deleteAllStage2Records() {
        if (!confirm('CAUTION: Are you sure you want to permanently delete ALL filtered records from Stage 2?')) return;
        try {
            const res = await AdminApi.deleteStage2Records([], [], true);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage2Records();
                this.loadStage2FilesForStage3();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }

    // ==========================================
    // STAGE 3: PREVIOUS STAGE BATCHES & 11-D PROJECTION
    // ==========================================
    async loadStage2FilesForStage3() {
        if (!this.s3PreviousFilesBody) return;
        this.resetMasterCheckbox('s3-batches-select-all', 's3-batches-bulk-bar', 's3-batches-selected-count');
        try {
            const res = await AdminApi.getStage2Files();
            const activeBatches = (res.files || []).filter(b => b.item_count > 0);
            if (res.success && activeBatches.length > 0) {
                this.s3PreviousFilesBody.innerHTML = activeBatches.map(b => {
                    const categoryBadges = (b.categories || []).slice(0, 3).map(c => 
                        `<span class="badge-tag tag-purple" style="font-size:0.7rem; margin-right:4px;">${c.replace('PESTLE: ', '').replace("Porter's: ", '')}</span>`
                    ).join('');

                    return `
                        <tr id="s3-batch-row-${b.date}">
                            <td style="text-align: center;">
                                <input type="checkbox" class="table-checkbox s3-batch-cb" data-date="${b.date}" onchange="updateBulkBar('s3-batch-cb', 's3-batches-bulk-bar', 's3-batches-selected-count')">
                            </td>
                            <td style="font-weight: 600; color: var(--text-main); font-family: monospace;">
                                <i class="fa-solid fa-layer-group" style="color: var(--accent-green); margin-right: 6px;"></i>
                                ${b.filename}
                            </td>
                            <td style="white-space: nowrap;">${b.date}</td>
                            <td>
                                <span class="badge-tag tag-purple">${b.item_count.toLocaleString()} filtered items waiting</span>
                            </td>
                            <td>${categoryBadges || '<span style="color:var(--text-dim);">General</span>'}</td>
                            <td>
                                <select id="s3-file-batch-${b.date}" style="padding: 0.35rem 0.6rem; font-size: 0.82rem; background: var(--bg-dark); border: 1px solid var(--border-color); color: var(--text-main); border-radius: var(--radius-sm);">
                                    <option value="10">10 Articles</option>
                                    <option value="25">25 Articles</option>
                                    <option value="50" selected>50 Articles</option>
                                    <option value="100">100 Articles</option>
                                    <option value="-1">All ${b.item_count.toLocaleString()} Articles</option>
                                </select>
                            </td>
                            <td>
                                <div style="display: flex; gap: 0.4rem; align-items: center;">
                                    <button class="btn" id="btn-s2-convert-${b.date}" style="padding: 0.4rem 0.85rem; font-size: 0.82rem;" onclick="convertStage2Batch('${b.date}')">
                                        <i class="fa-solid fa-wand-magic-sparkles"></i> Convert & Project 11-D
                                    </button>
                                    <button class="btn-danger-mini" title="Delete this batch from Stage 2" onclick="deleteStage2Batch('${b.date}')">
                                        <i class="fa-solid fa-trash-can"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    `;
                }).join('');
            } else {
                this.s3PreviousFilesBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">No Stage 2 filtered batches waiting for projection. All completed batches have been purged from Stage 2.</td></tr>`;
            }
        } catch (err) {
            console.error('Error loading Stage 2 batches for Stage 3:', err);
        }
    }

    async convertStage2Batch(date) {
        const batchSelect = document.getElementById(`s3-file-batch-${date}`);
        const batchSize = batchSelect ? parseInt(batchSelect.value) : 50;
        const btn = document.getElementById(`btn-s2-convert-${date}`);

        if (btn) {
            btn.disabled = true;
            btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Projecting...`;
        }

        if (this.s3ProgressBox) this.s3ProgressBox.style.display = 'block';
        if (this.s3StatusBox) this.s3StatusBox.style.display = 'none';

        try {
            const res = await AdminApi.processStage3(batchSize, date);
            if (!res.success) throw new Error(res.error);

            this.trackStage3Progress(btn);
        } catch (err) {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Convert & Project 11-D`;
            }
            alert(`Projection Error for ${date}: ${err.message}`);
        }
    }

    async convertSelectedStage2Batches() {
        const checked = document.querySelectorAll('.s3-batch-cb:checked');
        const dates = Array.from(checked).map(cb => cb.getAttribute('data-date')).filter(Boolean);
        if (dates.length === 0) {
            alert('Please select at least one Stage 2 batch to project.');
            return;
        }

        if (this.s3ProgressBox) this.s3ProgressBox.style.display = 'block';
        if (this.s3StatusBox) this.s3StatusBox.style.display = 'none';

        try {
            const res = await AdminApi.processStage3(-1, null, dates);
            if (!res.success) throw new Error(res.error);

            this.trackStage3Progress();
        } catch (err) {
            alert(`Bulk Projection Error: ${err.message}`);
        }
    }

    trackStage3Progress(btn = null) {
        if (this.s3PollInterval) clearInterval(this.s3PollInterval);
        this.s3PollInterval = setInterval(async () => {
            const prog = await AdminApi.getStage3Progress();
            if (this.s3ProgressPct) this.s3ProgressPct.textContent = `${prog.progress_pct || 0}%`;
            if (this.s3ProgressFill) this.s3ProgressFill.style.width = `${prog.progress_pct || 0}%`;
            if (this.s3ProgressMsg) this.s3ProgressMsg.textContent = prog.message || 'Processing...';

            if (prog.status === 'completed' || prog.status === 'error') {
                clearInterval(this.s3PollInterval);
                this.s3PollInterval = null;
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Convert & Project 11-D`;
                }
                this.loadDbStatus();
                this.loadStage2FilesForStage3();
                this.loadStage3News();
                this.loadStage2Records();
                this.syncNextIngestionDates();

                if (this.s3StatusBox) {
                    this.s3StatusBox.style.display = 'block';
                    this.s3StatusBox.style.background = prog.status === 'completed' ? 'rgba(0, 255, 102, 0.12)' : 'rgba(255, 0, 85, 0.12)';
                    this.s3StatusBox.style.border = `1px solid ${prog.status === 'completed' ? 'var(--accent-green)' : 'var(--danger-accent)'}`;
                    this.s3StatusBox.style.color = prog.status === 'completed' ? 'var(--accent-green)' : '#FF4D6D';
                    this.s3StatusBox.innerHTML = `<strong>${prog.status.toUpperCase()}:</strong> ${prog.message}`;
                }
            }
        }, 800);
    }

    async deleteStage2Batch(date) {
        if (!confirm(`Delete all Stage 2 filtered records for date ${date}?`)) return;
        try {
            const res = await AdminApi.deleteStage2Records([], [date]);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage2FilesForStage3();
                this.loadStage2Records();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }

    async deleteSelectedStage2Batches() {
        const checked = document.querySelectorAll('.s3-batch-cb:checked');
        const dates = Array.from(checked).map(cb => cb.getAttribute('data-date')).filter(Boolean);
        if (dates.length === 0) {
            alert('Please select at least one batch to delete.');
            return;
        }
        if (!confirm(`Delete ${dates.length} selected Stage 2 batch(es)?`)) return;

        try {
            const res = await AdminApi.deleteStage2Records([], dates);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage2FilesForStage3();
                this.loadStage2Records();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }

    async startStage3() {
        const batch = parseInt(this.s3Batch?.value || '50');
        this.s3Btn.disabled = true;
        if (this.s3ProgressBox) this.s3ProgressBox.style.display = 'block';
        if (this.s3StatusBox) this.s3StatusBox.style.display = 'none';

        try {
            const res = await AdminApi.processStage3(batch);
            if (!res.success) throw new Error(res.error);

            this.trackStage3Progress();
            const resetBtn = setInterval(() => {
                if (!this.s3PollInterval) {
                    this.s3Btn.disabled = false;
                    clearInterval(resetBtn);
                }
            }, 800);
        } catch (err) {
            this.s3Btn.disabled = false;
            alert(`Stage 3 Error: ${err.message}`);
        }
    }

    async loadStage3News() {
        const search = this.s3Search?.value || '';
        this.resetMasterCheckbox('s3-articles-select-all', 's3-articles-bulk-bar', 's3-articles-selected-count');
        try {
            const data = await AdminApi.getStage3Articles(15, search);
            if (this.s3Tbody) {
                if (data.articles && data.articles.length > 0) {
                    this.s3Tbody.innerHTML = data.articles.map(a => {
                        const vec = Array.isArray(a.strategic_embedding_11d) ? a.strategic_embedding_11d : [];
                        const previewBars = vec.slice(0, 6).map(v => `<span style="display:inline-block; width:6px; height:${Math.max(4, Math.round(v * 16))}px; background:var(--accent-green); margin-right:2px; border-radius:1px;"></span>`).join('');

                        return `
                            <tr>
                                <td style="text-align: center;">
                                    <input type="checkbox" class="table-checkbox s3-article-cb" data-id="${a.id}" onchange="updateBulkBar('s3-article-cb', 's3-articles-bulk-bar', 's3-articles-selected-count')">
                                </td>
                                <td style="white-space: nowrap;">${a.published_date || '--'}</td>
                                <td style="font-weight: 600; color: var(--text-main);">${a.headline}</td>
                                <td><span class="badge-tag tag-green">${a.primary_driver || 'Market Driver'}</span></td>
                                <td style="font-weight: 700; color: var(--accent-cyan);">${Number(a.impact_score || 0).toFixed(2)}</td>
                                <td>
                                    <div style="display: flex; align-items: flex-end; height: 18px; padding-top: 2px;">
                                        ${previewBars}
                                        <span style="font-size: 0.72rem; color: var(--text-dim); margin-left: 4px;">11-D</span>
                                    </div>
                                </td>
                                <td><a href="${a.source_link}" target="_blank" style="color: var(--accent-cyan); text-decoration: none;"><i class="fa-solid fa-arrow-up-right-from-square"></i> Source</a></td>
                                <td>
                                    <button class="btn-danger-mini" title="Delete article from Master Database" onclick="deleteStage3Article('${a.id}')">
                                        <i class="fa-solid fa-trash-can"></i>
                                    </button>
                                </td>
                            </tr>
                        `;
                    }).join('');
                    if (this.s3PageInfo) this.s3PageInfo.textContent = `Showing recent strategic articles`;
                } else {
                    this.s3Tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 2rem;">No Master News records found.</td></tr>`;
                }
            }
        } catch (err) {
            console.error(err);
        }
    }

    async deleteStage3Article(id) {
        if (!confirm('Delete this article from Master News Database?')) return;
        try {
            const res = await AdminApi.deleteStage3Articles([id]);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage3News();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }

    async deleteSelectedStage3Articles() {
        const checked = document.querySelectorAll('.s3-article-cb:checked');
        const ids = Array.from(checked).map(cb => cb.getAttribute('data-id')).filter(Boolean);
        if (ids.length === 0) {
            alert('Please select at least one article to delete.');
            return;
        }
        if (!confirm(`Delete ${ids.length} selected article(s) from Master News Database?`)) return;

        try {
            const res = await AdminApi.deleteStage3Articles(ids);
            if (res.success) {
                this.loadDbStatus();
                this.loadStage3News();
            } else {
                alert(`Delete failed: ${res.error}`);
            }
        } catch (err) {
            alert(`Delete Error: ${err.message}`);
        }
    }
}

