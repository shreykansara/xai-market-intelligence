/**
 * Omniscope AI - API Client Module
 * Centralized, typed, and resilient HTTP client mirror for all backend endpoints.
 */

export class ApiClient {
    // Admin token management
    static getAdminToken() {
        return localStorage.getItem('omniscope_admin_token') || sessionStorage.getItem('omniscope_admin_token') || '';
    }

    static setAdminToken(token, remember = true) {
        if (remember) {
            localStorage.setItem('omniscope_admin_token', token);
        } else {
            sessionStorage.setItem('omniscope_admin_token', token);
        }
    }

    static clearAdminToken() {
        localStorage.removeItem('omniscope_admin_token');
        sessionStorage.removeItem('omniscope_admin_token');
    }

    // End-User token management
    static getUserToken() {
        return localStorage.getItem('omniscope_user_token') || sessionStorage.getItem('omniscope_user_token') || '';
    }

    static setUserToken(token, remember = true) {
        if (remember) {
            localStorage.setItem('omniscope_user_token', token);
        } else {
            sessionStorage.setItem('omniscope_user_token', token);
        }
    }

    static clearUserToken() {
        localStorage.removeItem('omniscope_user_token');
        sessionStorage.removeItem('omniscope_user_token');
    }

    // Backwards compatibility alias
    static getAuthToken() {
        return ApiClient.getAdminToken();
    }

    static setAuthToken(token, remember = true) {
        ApiClient.setAdminToken(token, remember);
    }

    static clearAuthToken() {
        ApiClient.clearAdminToken();
    }

    static getHeaders(isAdmin = false) {
        const headers = { 'Content-Type': 'application/json' };
        const token = isAdmin ? ApiClient.getAdminToken() : (ApiClient.getUserToken() || ApiClient.getAdminToken());
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    static async get(url, params = {}, isAdmin = false) {
        const query = new URLSearchParams(params).toString();
        const fullUrl = query ? `${url}?${query}` : url;
        const res = await fetch(fullUrl, {
            headers: ApiClient.getHeaders(isAdmin)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
            if (res.status === 401 && isAdmin && window.adminController?.handleUnauthorized) {
                window.adminController.handleUnauthorized(err.error || 'Administrator session expired.');
            }
            throw new Error(err.error || `HTTP ${res.status}`);
        }
        return res.json();
    }

    static async post(url, body = {}, isAdmin = false) {
        const res = await fetch(url, {
            method: 'POST',
            headers: ApiClient.getHeaders(isAdmin),
            body: JSON.stringify(body)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
            if (res.status === 401 && isAdmin && window.adminController?.handleUnauthorized) {
                window.adminController.handleUnauthorized(err.error || 'Administrator session expired.');
            }
            throw new Error(err.error || `HTTP ${res.status}`);
        }
        return res.json();
    }

    static async delete(url, params = {}, isAdmin = false) {
        const query = new URLSearchParams(params).toString();
        const fullUrl = query ? `${url}?${query}` : url;
        const res = await fetch(fullUrl, {
            method: 'DELETE',
            headers: ApiClient.getHeaders(isAdmin)
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

export const UserAuthApi = {
    register: (payload) =>
        ApiClient.post('/api/auth/register', payload),
    login: (email, password) =>
        ApiClient.post('/api/auth/login', { email, password }),
    logout: () =>
        ApiClient.post('/api/auth/logout'),
    getMe: () =>
        ApiClient.get('/api/auth/me')
};

export const UserHistoryApi = {
    getAnalyses: (type = null, limit = 50) => {
        const params = { limit };
        if (type) params.type = type;
        return ApiClient.get('/api/user/analyses', params);
    },
    saveAnalysis: (payload) =>
        ApiClient.post('/api/user/analyses', payload),
    getAnalysis: (id) =>
        ApiClient.get(`/api/user/analyses/${encodeURIComponent(id)}`),
    deleteAnalysis: (id) =>
        ApiClient.delete(`/api/user/analyses/${encodeURIComponent(id)}`),

    getConversations: (limit = 50) =>
        ApiClient.get('/api/user/conversations', { limit }),
    saveConversation: (payload) =>
        ApiClient.post('/api/user/conversations', payload),
    getConversation: (id) =>
        ApiClient.get(`/api/user/conversations/${encodeURIComponent(id)}`),
    deleteConversation: (id) =>
        ApiClient.delete(`/api/user/conversations/${encodeURIComponent(id)}`),

    syncGuestData: (payload) =>
        ApiClient.post('/api/user/sync_guest_data', payload)
};

export const AdminApi = {
    // Authentication & Session
    login: (email, password) =>
        ApiClient.post('/api/admin/login', { email, password }, true),
    logout: () =>
        ApiClient.post('/api/admin/logout', {}, true),
    verifyAuth: () =>
        ApiClient.get('/api/admin/verify', {}, true),

    // Stage 1
    ingestStage1: (startDate, endDate) => 
        ApiClient.post('/api/stage1/ingest', { start_date: startDate, end_date: endDate }, true),
    getStage1Progress: () => 
        ApiClient.get('/api/stage1/progress', {}, true),
    getStage1Files: () => 
        ApiClient.get('/api/stage1/files', {}, true),
    getStage1Records: (page = 1, perPage = 15, search = '') => 
        ApiClient.get('/api/stage1/records', { page, per_page: perPage, search }, true),
    getStage1NextDate: () =>
        ApiClient.get('/api/stage1/next-date', {}, true),
    deleteStage1Files: (ids = [], dates = []) =>
        ApiClient.post('/api/stage1/files/delete', { ids, dates }, true),
    deleteStage1Records: (ids = [], deleteAll = false) =>
        ApiClient.post('/api/stage1/records/delete', { ids, all: deleteAll }, true),

    // Stage 2
    getStage2Files: () => 
        ApiClient.get('/api/stage2/files', {}, true),
    processStage2: (batchSize = 100, targetDate = null, dates = null) => 
        ApiClient.post('/api/stage2/process', { batch_size: batchSize, date: targetDate, dates: dates }, true),
    getStage2Progress: () => 
        ApiClient.get('/api/stage2/progress', {}, true),
    getStage2Records: (page = 1, perPage = 15, search = '', location = '') => 
        ApiClient.get('/api/stage2/records', { page, per_page: perPage, search, location }, true),
    deleteStage2Records: (ids = [], dates = [], deleteAll = false) =>
        ApiClient.post('/api/stage2/records/delete', { ids, dates, all: deleteAll }, true),

    // Stage 3
    processStage3: (batchSize = 50, targetDate = null, dates = null) => 
        ApiClient.post('/api/stage3/process', { batch_size: batchSize, date: targetDate, dates: dates }, true),
    getStage3Progress: () => 
        ApiClient.get('/api/stage3/progress', {}, true),
    getStage3Articles: (limit = 15, search = '', minImpact = 0.2) => 
        ApiClient.get('/api/stage3/articles', { limit, search, min_impact: minImpact }, true),
    deleteStage3Articles: (ids = [], dates = [], deleteAll = false) =>
        ApiClient.post('/api/stage3/articles/delete', { ids, dates, all: deleteAll }, true),
    getStage3DbStatus: () => 
        ApiClient.get('/api/stage3/db-status', {}, true),
    getStage3Companies: (limit = 15, search = '') => 
        ApiClient.get('/api/stage3/companies', { limit, search }, true),
    projectHeadline: (headline) => 
        ApiClient.post('/api/stage3/project-headline', { headline }, true)
};
