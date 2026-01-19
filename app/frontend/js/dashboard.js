/**
 * Dashboard Manager
 * Handles real-time KPI updates, data loading, and auto-refresh
 */

class DashboardManager {
    constructor() {
        this.api = new APIClient();
        this.refreshInterval = null;
        this.autoRefreshSeconds = 30;
    }

    /**
     * Initialize dashboard and start auto-refresh
     */
    async initialize() {
        try {
            // Load initial data
            await this.loadDashboardKPIs();
            
            // Start auto-refresh every 30 seconds
            this.startAutoRefresh();
            
            // Also refresh on window focus (when user returns to tab)
            window.addEventListener('focus', () => {
                console.log('Dashboard: Window focused, refreshing data');
                this.loadDashboardKPIs();
            });
            
            toast.info('Dashboard initialized');
        } catch (error) {
            console.error('Dashboard initialization failed:', error);
            toast.error(`Failed to initialize dashboard: ${error.message}`);
        }
    }

    /**
     * Load all dashboard KPIs from backend
     */
    async loadDashboardKPIs() {
        try {
            // Show loading state
            this.setLoadingState(true);

            // Fetch data from multiple endpoints in parallel
            const [orders, maintenance, defects, capacity] = await Promise.all([
                this.api.get('/api/orders/').catch(() => ({ data: [] })),
                this.api.get('/api/maintenance/').catch(() => ({ data: [] })),
                this.api.get('/api/defects/').catch(() => ({ data: [] })),
                this.api.get('/api/dashboard/').catch(() => ({}))
            ]);

            // Calculate KPI values
            const kpis = this.calculateKPIs(orders.data || [], maintenance.data || [], defects.data || [], capacity.data || {});

            // Update dashboard cards
            this.updateKPICards(kpis);

            // Update table data if visible
            await this.loadRecentOrders();
            await this.loadActiveIssues();

            // Hide loading state
            this.setLoadingState(false);

            console.log('Dashboard KPIs updated successfully:', kpis);
        } catch (error) {
            console.error('Failed to load dashboard KPIs:', error);
            toast.error(`Failed to load KPIs: ${error.message}`);
            this.setLoadingState(false);
        }
    }

    /**
     * Calculate KPI values from raw data
     */
    calculateKPIs(orders, maintenance, defects, capacityData) {
        // Total Orders
        const totalOrders = orders.length;
        const inProgressOrders = orders.filter(o => o.status === 'in_progress').length;
        const completedOrders = orders.filter(o => o.status === 'completed').length;

        // On-time percentage (orders completed by due date)
        const onTimeOrders = orders.filter(o => {
            if (!o.due_date || o.status !== 'completed') return false;
            return new Date(o.completion_date) <= new Date(o.due_date);
        }).length;
        const onTimePercent = totalOrders > 0 ? Math.round((onTimeOrders / totalOrders) * 100) : 0;

        // Maintenance tasks
        const totalMaintenance = maintenance.length;
        const pendingMaintenance = maintenance.filter(m => m.status === 'pending').length;
        const overdueMaintenance = maintenance.filter(m => {
            if (!m.due_date) return false;
            return new Date(m.due_date) < new Date() && m.status !== 'completed';
        }).length;

        // Defects and SOP tickets
        const defectsCount = defects.filter(d => d.type === 'defect').length;
        const sopCount = defects.filter(d => d.type === 'sop_violation').length;
        const totalActiveIssues = defectsCount + sopCount;

        // Capacity utilization (from capacityData or calculate from orders)
        let capacityPercent = capacityData.utilization_percent || 0;
        if (!capacityPercent && orders.length > 0) {
            // Simple calculation: in_progress / total * 100
            capacityPercent = Math.round((inProgressOrders / totalOrders) * 100);
        }

        return {
            totalOrders,
            inProgressOrders,
            completedOrders,
            onTimePercent,
            totalMaintenance,
            pendingMaintenance,
            overdueMaintenance,
            defectsCount,
            sopCount,
            totalActiveIssues,
            capacityPercent
        };
    }

    /**
     * Update KPI cards in the DOM
     */
    updateKPICards(kpis) {
        // Total Orders
        this.updateCard('totalOrders', kpis.totalOrders);
        this.updateCard('onTimePercentage', kpis.onTimePercent);

        // Capacity Utilization
        this.updateCard('capacityPercent', kpis.capacityPercent);

        // Active Issues
        this.updateCard('activeIssues', kpis.totalActiveIssues);
        this.updateCard('defectsCount', kpis.defectsCount);
        this.updateCard('sopCount', kpis.sopCount);

        // Maintenance Tasks
        this.updateCard('maintenanceTasks', kpis.pendingMaintenance);
        this.updateCard('overdueTasks', kpis.overdueMaintenance);
    }

    /**
     * Update a single card value in DOM
     */
    updateCard(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            // Add animation effect
            element.style.opacity = '0.5';
            element.textContent = value;
            
            // Fade back in
            setTimeout(() => {
                element.style.transition = 'opacity 0.3s ease';
                element.style.opacity = '1';
            }, 50);
        }
    }

    /**
     * Load recent orders and display in table
     */
    async loadRecentOrders() {
        try {
            const response = await this.api.get('/api/orders/?limit=10');
            const orders = response.data || [];

            const container = document.getElementById('ordersContainer');
            if (!container) return;

            if (orders.length === 0) {
                container.innerHTML = '<div class="empty-state">No orders found</div>';
                return;
            }

            let html = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Order #</th>
                            <th>Customer</th>
                            <th>Product</th>
                            <th>Qty</th>
                            <th>Status</th>
                            <th>Due Date</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            orders.forEach(order => {
                const dueDate = new Date(order.due_date).toLocaleDateString();
                const statusClass = this.getStatusClass(order.status);
                
                html += `
                    <tr onclick="window.location.href='order-detail.html?id=${order.id}'">
                        <td><strong>#${order.order_number}</strong></td>
                        <td>${order.customer_name || 'N/A'}</td>
                        <td>${order.product_name || 'N/A'}</td>
                        <td>${order.quantity || 0}</td>
                        <td><span class="status-badge ${statusClass}">${this.formatStatus(order.status)}</span></td>
                        <td>${dueDate}</td>
                    </tr>
                `;
            });

            html += `
                    </tbody>
                </table>
            `;

            container.innerHTML = html;
        } catch (error) {
            console.error('Failed to load recent orders:', error);
            const container = document.getElementById('ordersContainer');
            if (container) {
                container.innerHTML = '<div class="empty-state">Failed to load orders. Please try again.</div>';
            }
        }
    }

    /**
     * Load active issues and display in table
     */
    async loadActiveIssues() {
        try {
            const response = await this.api.get('/api/defects/');
            const defects = response.data || [];

            const container = document.getElementById('issuesContainer');
            if (!container) return;

            if (defects.length === 0) {
                container.innerHTML = '<div class="empty-state">No active issues</div>';
                return;
            }

            let html = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Issue Type</th>
                            <th>Order</th>
                            <th>Description</th>
                            <th>Severity</th>
                            <th>Date Reported</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            defects.slice(0, 10).forEach(defect => {
                const reportDate = new Date(defect.created_at).toLocaleDateString();
                const severityClass = this.getSeverityClass(defect.severity || 'medium');
                const issueType = defect.type === 'sop_violation' ? '⚠️ SOP Violation' : '❌ Defect';
                
                html += `
                    <tr>
                        <td>${issueType}</td>
                        <td>${defect.order_id || 'N/A'}</td>
                        <td>${(defect.description || '').substring(0, 50)}...</td>
                        <td><span class="status-badge ${severityClass}">${(defect.severity || 'medium').toUpperCase()}</span></td>
                        <td>${reportDate}</td>
                    </tr>
                `;
            });

            html += `
                    </tbody>
                </table>
            `;

            container.innerHTML = html;
        } catch (error) {
            console.error('Failed to load active issues:', error);
            const container = document.getElementById('issuesContainer');
            if (container) {
                container.innerHTML = '<div class="empty-state">Failed to load issues. Please try again.</div>';
            }
        }
    }

    /**
     * Start auto-refresh timer
     */
    startAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }

        this.refreshInterval = setInterval(() => {
            console.log(`Dashboard: Auto-refreshing (every ${this.autoRefreshSeconds}s)`);
            this.loadDashboardKPIs();
        }, this.autoRefreshSeconds * 1000);

        console.log(`Dashboard: Auto-refresh started (${this.autoRefreshSeconds}s interval)`);
    }

    /**
     * Stop auto-refresh timer
     */
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
            console.log('Dashboard: Auto-refresh stopped');
        }
    }

    /**
     * Set loading state for dashboard
     */
    setLoadingState(isLoading) {
        const ordersContainer = document.getElementById('ordersContainer');
        const issuesContainer = document.getElementById('issuesContainer');

        if (isLoading) {
            if (ordersContainer && !ordersContainer.querySelector('.spinner')) {
                ordersContainer.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
            }
            if (issuesContainer && !issuesContainer.querySelector('.spinner')) {
                issuesContainer.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
            }
        }
    }

    /**
     * Format status string for display
     */
    formatStatus(status) {
        return status
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    /**
     * Get CSS class for status badge
     */
    getStatusClass(status) {
        const statusMap = {
            'completed': 'success',
            'in_progress': 'warning',
            'pending': 'warning',
            'on_hold': 'danger',
            'cancelled': 'danger'
        };
        return statusMap[status] || 'warning';
    }

    /**
     * Get CSS class for severity badge
     */
    getSeverityClass(severity) {
        const severityMap = {
            'high': 'danger',
            'critical': 'danger',
            'medium': 'warning',
            'low': 'success'
        };
        return severityMap[severity] || 'warning';
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new DashboardManager();
    dashboard.initialize();

    // Stop auto-refresh when user leaves page
    window.addEventListener('beforeunload', () => {
        dashboard.stopAutoRefresh();
    });
});
