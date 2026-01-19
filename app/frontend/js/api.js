/**
 * API Client Module
 * Handles all HTTP communication with the backend
 */

class APIClient {
    constructor(baseUrl = null) {
        // Determine base URL dynamically based on environment
        if (baseUrl) {
            this.baseUrl = baseUrl;
        } else if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            // Development: use localhost
            this.baseUrl = 'http://127.0.0.1:8000';
        } else {
            // Production: use same domain as frontend
            this.baseUrl = `${window.location.protocol}//${window.location.hostname}:8000`;
        }
        
        this.token = localStorage.getItem('auth_token');
        this.userId = localStorage.getItem('user_id');
        this.role = localStorage.getItem('user_role');
        this.departmentId = localStorage.getItem('department_id');
    }

    /**
     * Set authorization token after login
     */
    setToken(token, userId, role, departmentId) {
        this.token = token;
        this.userId = userId;
        this.role = role;
        this.departmentId = departmentId;
        localStorage.setItem('auth_token', token);
        localStorage.setItem('user_id', userId);
        localStorage.setItem('user_role', role);
        localStorage.setItem('department_id', departmentId);
    }

    /**
     * Clear token and session (logout)
     */
    clearToken() {
        this.token = null;
        this.userId = null;
        this.role = null;
        this.departmentId = null;
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('user_role');
        localStorage.removeItem('department_id');
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        return !!this.token;
    }

    /**
     * Build authorization header
     */
    getAuthHeader() {
        if (!this.token) {
            return {};
        }
        return {
            'Authorization': `Bearer ${this.token}`
        };
    }

    /**
     * Fetch with timeout support
     * @param {string} url - The URL to fetch
     * @param {object} options - Fetch options
     * @param {number} timeout - Timeout in milliseconds (default: 10000)
     */
    async fetchWithTimeout(url, options = {}, timeout = 10000) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            return response;
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error(`Request timeout after ${timeout}ms - server not responding`);
            }
            throw error;
        }
    }

    /**
     * Retry logic with exponential backoff
     * @param {function} requestFn - Async function to retry
     * @param {number} maxRetries - Maximum number of retries (default: 3)
     */
    async retryWithBackoff(requestFn, maxRetries = 3) {
        let lastError;
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                return await requestFn();
            } catch (error) {
                lastError = error;
                
                // Don't retry on authentication errors
                if (error.message && error.message.includes('Unauthorized')) {
                    throw error;
                }
                
                // Calculate delay: 1s, 2s, 4s exponential backoff
                const delay = Math.pow(2, attempt - 1) * 1000;
                
                if (attempt < maxRetries) {
                    console.warn(`Request failed (attempt ${attempt}/${maxRetries}), retrying in ${delay}ms...`, error.message);
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
        }
        throw lastError;
    }

    /**
     * GET request
     */
    async get(endpoint) {
        return this.retryWithBackoff(async () => {
            try {
                const response = await this.fetchWithTimeout(`${this.baseUrl}${endpoint}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        ...this.getAuthHeader()
                    }
                });

                if (response.status === 401) {
                    this.clearToken();
                    window.location.href = '/login.html';
                    throw new Error('Unauthorized - please login');
                }

                if (!response.ok) {
                    const error = await response.json().catch(() => ({ message: response.statusText }));
                    throw new Error(error.message || `HTTP ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error(`GET ${endpoint} failed:`, error);
                throw error;
            }
        });
    }

    /**
     * POST request
     */
    async post(endpoint, data) {
        return this.retryWithBackoff(async () => {
            try {
                const response = await this.fetchWithTimeout(`${this.baseUrl}${endpoint}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        ...this.getAuthHeader()
                    },
                    body: JSON.stringify(data)
                });

                if (response.status === 401) {
                    this.clearToken();
                    window.location.href = '/login.html';
                    throw new Error('Unauthorized - please login');
                }

                if (!response.ok) {
                    const error = await response.json().catch(() => ({ message: response.statusText }));
                    throw new Error(error.message || `HTTP ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error(`POST ${endpoint} failed:`, error);
                throw error;
            }
        });
    }

    /**
     * PUT request
     */
    async put(endpoint, data) {
        try {
            const response = await this.fetchWithTimeout(`${this.baseUrl}${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...this.getAuthHeader()
                },
                body: JSON.stringify(data)
            });

            if (response.status === 401) {
                this.clearToken();
                window.location.href = '/login.html';
                throw new Error('Unauthorized - please login');
            }

            if (!response.ok) {
                const error = await response.json().catch(() => ({ message: response.statusText }));
                throw new Error(error.message || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`PUT ${endpoint} failed:`, error);
            throw error;
        }
    }

    /**
     * DELETE request
     */
    async delete(endpoint) {
        try {
            const response = await this.fetchWithTimeout(`${this.baseUrl}${endpoint}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    ...this.getAuthHeader()
                }
            });

            if (response.status === 401) {
                this.clearToken();
                window.location.href = '/login.html';
                throw new Error('Unauthorized - please login');
            }

            if (!response.ok) {
                const error = await response.json().catch(() => ({ message: response.statusText }));
                throw new Error(error.message || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`DELETE ${endpoint} failed:`, error);
            throw error;
        }
    }

    // ===================== AUTHENTICATION =====================

    async login(email, password) {
        const response = await this.post('/api/auth/login', { email, password });
        if (response.success) {
            this.setToken(
                response.data.token,
                response.data.user_id,
                response.data.role,
                response.data.department_id
            );
        }
        return response;
    }

    async logout() {
        this.clearToken();
    }

    // ===================== ORDERS =====================

    async getOrders(filters = {}) {
        const params = new URLSearchParams();
        if (filters.status) params.append('status', filters.status);
        if (filters.skip) params.append('skip', filters.skip);
        if (filters.limit) params.append('limit', filters.limit);
        return this.get(`/api/orders?${params.toString()}`);
    }

    async getOrderDetail(orderId) {
        return this.get(`/api/orders/${orderId}`);
    }

    async createOrder(orderData) {
        return this.post('/api/orders', orderData);
    }

    async updateOrder(orderId, orderData) {
        return this.put(`/api/orders/${orderId}`, orderData);
    }

    async scheduleOrder(orderId, scheduleData) {
        return this.post(`/api/orders/${orderId}/schedule`, scheduleData);
    }

    // ===================== DEFECTS =====================

    async getDefects(filters = {}) {
        const params = new URLSearchParams();
        if (filters.status) params.append('status', filters.status);
        if (filters.type) params.append('type', filters.type);
        return this.get(`/api/defects?${params.toString()}`);
    }

    async getDefectDetail(defectId) {
        return this.get(`/api/defects/${defectId}`);
    }

    async createDefect(defectData) {
        return this.post('/api/defects', defectData);
    }

    async approveDefect(defectId, approvalData) {
        return this.post(`/api/defects/${defectId}/approve`, approvalData);
    }

    // ===================== SOP/NCR =====================

    async getSOPTickets(filters = {}) {
        const params = new URLSearchParams();
        if (filters.status) params.append('status', filters.status);
        return this.get(`/api/sop-ncr/sop-tickets?${params.toString()}`);
    }

    async getSOPTicketDetail(ticketId) {
        return this.get(`/api/sop-ncr/sop-tickets/${ticketId}`);
    }

    async createSOPTicket(ticketData) {
        return this.post('/api/sop-ncr/sop-tickets', ticketData);
    }

    async assignSOPTicket(ticketId, assignmentData) {
        return this.post(`/api/sop-ncr/sop-tickets/${ticketId}/assign`, assignmentData);
    }

    async completeNCR(ticketId, ncrData) {
        return this.post(`/api/sop-ncr/sop-tickets/${ticketId}/complete-ncr`, ncrData);
    }

    // ===================== MAINTENANCE =====================

    async getMaintenanceTickets(filters = {}) {
        const params = new URLSearchParams();
        if (filters.status) params.append('status', filters.status);
        return this.get(`/api/maintenance/tickets?${params.toString()}`);
    }

    async getMaintenanceDetail(ticketId) {
        return this.get(`/api/maintenance/tickets/${ticketId}`);
    }

    async createMaintenanceTicket(ticketData) {
        return this.post('/api/maintenance/tickets', ticketData);
    }

    async assignMaintenanceTicket(ticketId, assignmentData) {
        return this.post(`/api/maintenance/tickets/${ticketId}/assign`, assignmentData);
    }

    // ===================== MASTER DATA =====================

    async getDepartments() {
        return this.get('/api/master/departments');
    }

    async getProducts() {
        return this.get('/api/master/products');
    }

    async getMachines() {
        return this.get('/api/master/machines');
    }

    // ===================== DASHBOARD =====================

    async getDashboard() {
        return this.get('/api/jobs/dashboard/planning');
    }

    async getSOPDashboard(departmentId = null) {
        const url = departmentId 
            ? `/api/sop-ncr/sop-dashboard?department_id=${departmentId}`
            : '/api/sop-ncr/sop-dashboard';
        return this.get(url);
    }

    // ===================== FORM UTILITIES =====================

    /**
     * Handle form submission with loading state and error handling
     * @param {HTMLFormElement} form - The form element
     * @param {function} submitFn - Async function to execute
     */
    async handleFormSubmit(form, submitFn) {
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn ? submitBtn.textContent : 'Submit';
        
        try {
            // Show loading state
            if (submitBtn) {
                submitBtn.disabled = true;
                const spinner = submitBtn.querySelector('.spinner');
                if (spinner) {
                    spinner.classList.remove('hidden');
                } else {
                    submitBtn.innerHTML = `${originalText} <span class="spinner"></span>`;
                }
            }
            
            // Execute submit function
            const result = await submitFn();
            
            // Show success
            if (window.toast) {
                toast.success('Operation completed successfully!');
            }
            
            return result;
        } catch (error) {
            // Show error
            if (window.toast) {
                toast.error(`Error: ${error.message}`);
            } else {
                alert(`Error: ${error.message}`);
            }
            throw error;
        } finally {
            // Reset loading state
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        }
    }

    /**
     * Get form data as JSON
     * @param {HTMLFormElement} form - The form element
     */
    getFormData(form) {
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        return data;
    }
}

// Create global API client instance
const api = new APIClient();

