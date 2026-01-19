/**
 * Gantt Chart Manager
 * Enhanced Gantt chart with drag-drop rescheduling and API integration
 */

class GanttManager {
    constructor(containerId = 'ganttChart') {
        this.api = new APIClient();
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        this.orders = [];
        this.today = new Date();
        this.daysToShow = 60;
        this.draggingBar = null;
        this.dragStartX = 0;
    }

    /**
     * Initialize Gantt chart
     */
    async initialize() {
        try {
            await this.loadOrders();
            this.renderGantt();
            this.setupDragDrop();
            toast.info('Gantt chart loaded');
        } catch (error) {
            console.error('Failed to initialize Gantt:', error);
            toast.error(`Failed to load Gantt: ${error.message}`);
        }
    }

    /**
     * Load orders from API
     */
    async loadOrders() {
        try {
            const response = await this.api.get('/api/orders/?status=in_progress,pending');
            this.orders = response.data || [];
            console.log(`Gantt: Loaded ${this.orders.length} orders`);
        } catch (error) {
            console.error('Failed to load orders:', error);
            this.orders = [];
            throw error;
        }
    }

    /**
     * Render Gantt chart
     */
    renderGantt() {
        if (!this.container) {
            console.warn('Gantt container not found');
            return;
        }

        // Create timeline header
        let timelineHtml = '<div class="gantt-timeline">';
        for (let i = 0; i < this.daysToShow; i++) {
            const date = new Date(this.today);
            date.setDate(date.getDate() + i);
            const dayName = date.toLocaleDateString('en-ZA', { weekday: 'short' });
            const dayNum = date.getDate();
            
            const isToday = date.toDateString() === this.today.toDateString();
            const classStr = isToday ? 'gantt-day today' : 'gantt-day';
            
            timelineHtml += `<div class="${classStr}" title="${date.toLocaleDateString()}">${dayNum}</div>`;
        }
        timelineHtml += '</div>';

        // Create rows for each order
        let rowsHtml = '';
        this.orders.forEach((order, index) => {
            const startDate = new Date(order.start_date);
            const endDate = new Date(order.end_date);
            const daysFromStart = Math.floor((startDate - this.today) / (1000 * 60 * 60 * 24));
            const duration = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) || 1;

            // Only show if within visible range
            if (daysFromStart < this.daysToShow && (daysFromStart + duration) > 0) {
                rowsHtml += `
                    <div class="gantt-row" data-order-id="${order.id}" data-index="${index}">
                        <div class="gantt-row-label">
                            <strong>#${order.order_number}</strong>
                            <small>${order.customer_name || 'N/A'}</small>
                        </div>
                        <div class="gantt-bars">
                            <div class="gantt-bar" 
                                 data-order-id="${order.id}"
                                 data-start-index="${Math.max(0, daysFromStart)}"
                                 style="left: ${Math.max(0, daysFromStart) * 40}px; width: ${duration * 40}px;"
                                 title="Order #${order.order_number}">
                                ${order.order_number}
                            </div>
                        </div>
                    </div>
                `;
            }
        });

        // Render everything
        this.container.innerHTML = `
            <div class="gantt-header">
                <span class="gantt-header-label">Order / Machine</span>
                <span class="gantt-header-label">Timeline (60 Days)</span>
            </div>
            <div class="gantt-content">
                <div class="gantt-rows">${rowsHtml}</div>
                <div class="gantt-chart">${timelineHtml}</div>
            </div>
        `;
    }

    /**
     * Setup drag-drop functionality for bars
     */
    setupDragDrop() {
        const bars = this.container.querySelectorAll('.gantt-bar');
        
        bars.forEach(bar => {
            bar.draggable = true;
            
            bar.addEventListener('dragstart', (e) => this.onDragStart(e));
            bar.addEventListener('dragend', (e) => this.onDragEnd(e));
        });

        // Add drop zones between timeline units
        const timeline = this.container.querySelector('.gantt-timeline');
        if (timeline) {
            timeline.addEventListener('dragover', (e) => e.preventDefault());
            timeline.addEventListener('drop', (e) => this.onDrop(e));
        }
    }

    /**
     * Handle drag start
     */
    onDragStart(e) {
        this.draggingBar = e.target;
        this.draggingBar.style.opacity = '0.5';
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', e.target.dataset.orderId);
    }

    /**
     * Handle drag end
     */
    onDragEnd(e) {
        if (this.draggingBar) {
            this.draggingBar.style.opacity = '1';
            this.draggingBar = null;
        }
    }

    /**
     * Handle drop on timeline
     */
    async onDrop(e) {
        e.preventDefault();
        
        if (!this.draggingBar) return;

        const orderId = this.draggingBar.dataset.orderId;
        const order = this.orders.find(o => o.id == orderId);
        
        if (!order) return;

        // Calculate new start date based on drop position
        const rect = this.container.querySelector('.gantt-chart').getBoundingClientRect();
        const dropX = e.clientX - rect.left;
        const dayOffset = Math.round(dropX / 40); // 40px per day
        
        const newStartDate = new Date(this.today);
        newStartDate.setDate(newStartDate.getDate() + dayOffset);

        // Calculate new end date (preserve duration)
        const duration = Math.ceil((new Date(order.end_date) - new Date(order.start_date)) / (1000 * 60 * 60 * 24)) || 1;
        const newEndDate = new Date(newStartDate);
        newEndDate.setDate(newEndDate.getDate() + duration);

        // Update order via API
        try {
            await this.updateOrderDates(orderId, newStartDate, newEndDate);
            
            // Re-render
            await this.loadOrders();
            this.renderGantt();
            this.setupDragDrop();
            
            toast.success(`Order #${order.order_number} rescheduled`);
        } catch (error) {
            console.error('Failed to reschedule order:', error);
            toast.error(`Failed to reschedule: ${error.message}`);
        }
    }

    /**
     * Update order dates via API
     */
    async updateOrderDates(orderId, startDate, endDate) {
        const response = await this.api.put(`/api/orders/${orderId}`, {
            start_date: startDate.toISOString().split('T')[0],
            end_date: endDate.toISOString().split('T')[0]
        });
        return response.data;
    }

    /**
     * Refresh chart
     */
    async refresh() {
        try {
            await this.loadOrders();
            this.renderGantt();
            this.setupDragDrop();
            console.log('Gantt chart refreshed');
        } catch (error) {
            console.error('Failed to refresh Gantt:', error);
            toast.error(`Refresh failed: ${error.message}`);
        }
    }

    /**
     * Scroll to today
     */
    scrollToToday() {
        const container = this.container.querySelector('.gantt-content');
        if (container) {
            container.scrollLeft = 0; // First day is today
        }
    }

    /**
     * Zoom in (show fewer days)
     */
    zoomIn() {
        this.daysToShow = Math.max(14, this.daysToShow - 10);
        this.renderGantt();
        this.setupDragDrop();
    }

    /**
     * Zoom out (show more days)
     */
    zoomOut() {
        this.daysToShow = Math.min(180, this.daysToShow + 10);
        this.renderGantt();
        this.setupDragDrop();
    }

    /**
     * Filter by status
     */
    filterByStatus(status) {
        this.orders = this.orders.filter(o => o.status === status);
        this.renderGantt();
        this.setupDragDrop();
    }

    /**
     * Filter by machine
     */
    filterByMachine(machineId) {
        this.orders = this.orders.filter(o => o.machine_id === machineId);
        this.renderGantt();
        this.setupDragDrop();
    }

    /**
     * Get order details
     */
    getOrderDetails(orderId) {
        return this.orders.find(o => o.id == orderId);
    }

    /**
     * Highlight order
     */
    highlightOrder(orderId) {
        const bar = this.container.querySelector(`[data-order-id="${orderId}"]`);
        if (bar) {
            bar.style.background = 'rgba(255, 107, 53, 0.3)';
            bar.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    /**
     * Clear highlight
     */
    clearHighlight() {
        const bars = this.container.querySelectorAll('.gantt-bar');
        bars.forEach(bar => bar.style.background = '');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const gantt = new GanttManager('ganttChart');
    gantt.initialize();
    
    // Store globally for other functions to access
    window.ganttManager = gantt;
});
