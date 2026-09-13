/**
 * Omniscope AI - API Client Module
 * Centralized, typed, and resilient HTTP client mirror for all backend endpoints.
 */

export class ApiClient {
    static async get(url, params = {}) {
        const query = new URLSearchParams(params).toString();
        const fullUrl = query ? `${url}?${query}` : url;
        const res = await fetch(fullUrl);
        if (!res.ok) {
            const err = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
            throw new Error(err.error || `HTTP ${res.status}`);
        }
        return res.json();
    }

    static async post(url, body = {}) {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
            throw new Error(err.error || `HTTP ${res.status}`);
        }
        return res.json();
    }
}

export const CvpApi = {
    evaluate: (cvpText, groqApiKey = '') => 
        ApiClient.post('/api/evaluate_cvp', { cvp_text: cvpText, groq_api_key: groqApiKey })
};

export const SalesApi = {
    matchRevenueClusters: (revenueSeries, groqApiKey = '') => 
        ApiClient.post('/api/match_revenue_clusters', { revenue_series: revenueSeries, groq_api_key: groqApiKey })
};

export const ChatApi = {
    sendMessage: (payload) => 
        ApiClient.post('/api/chat', payload)
};

export const CompanyApi = {
    getProfile: (companyName) => 
        ApiClient.get('/api/company_profile', { name: companyName })
};

export const AdminApi = {
    // Stage 1
    ingestStage1: (startDate, endDate) => 
        ApiClient.post('/api/stage1/ingest', { start_date: startDate, end_date: endDate }),
    getStage1Progress: () => 
        ApiClient.get('/api/stage1/progress'),
    getStage1Files: () => 
        ApiClient.get('/api/stage1/files'),
    getStage1Records: (page = 1, perPage = 15, search = '') => 
        ApiClient.get('/api/stage1/records', { page, per_page: perPage, search }),
    getStage1NextDate: () =>
        ApiClient.get('/api/stage1/next-date'),
    deleteStage1Files: (ids = [], dates = []) =>
        ApiClient.post('/api/stage1/files/delete', { ids, dates }),
    deleteStage1Records: (ids = [], deleteAll = false) =>
        ApiClient.post('/api/stage1/records/delete', { ids, all: deleteAll }),

    // Stage 2
    getStage2Files: () => 
        ApiClient.get('/api/stage2/files'),
    processStage2: (batchSize = 100, targetDate = null, dates = null) => 
        ApiClient.post('/api/stage2/process', { batch_size: batchSize, date: targetDate, dates: dates }),
    getStage2Progress: () => 
        ApiClient.get('/api/stage2/progress'),
    getStage2Records: (page = 1, perPage = 15, search = '', location = '') => 
        ApiClient.get('/api/stage2/records', { page, per_page: perPage, search, location }),
    deleteStage2Records: (ids = [], dates = [], deleteAll = false) =>
        ApiClient.post('/api/stage2/records/delete', { ids, dates, all: deleteAll }),

    // Stage 3
    processStage3: (batchSize = 50, targetDate = null, dates = null) => 
        ApiClient.post('/api/stage3/process', { batch_size: batchSize, date: targetDate, dates: dates }),
    getStage3Progress: () => 
        ApiClient.get('/api/stage3/progress'),
    getStage3Articles: (limit = 15, search = '', minImpact = 0.2) => 
        ApiClient.get('/api/stage3/articles', { limit, search, min_impact: minImpact }),
    deleteStage3Articles: (ids = [], dates = [], deleteAll = false) =>
        ApiClient.post('/api/stage3/articles/delete', { ids, dates, all: deleteAll }),
    getStage3DbStatus: () => 
        ApiClient.get('/api/stage3/db-status'),
    getStage3Companies: (limit = 15, search = '') => 
        ApiClient.get('/api/stage3/companies', { limit, search }),
    projectHeadline: (headline) => 
        ApiClient.post('/api/stage3/project-headline', { headline })
};
