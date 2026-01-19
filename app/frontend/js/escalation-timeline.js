/**
 * Escalation Timeline
 * Visual timeline showing workflow status progression
 */

class EscalationTimeline {
    /**
     * Initialize escalation timeline
     * @param {string} containerId - ID of container element
     * @param {object} workflow - Workflow status data
     */
    constructor(containerId, workflow = {}) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        this.workflow = workflow;
        
        if (!this.container) {
            console.warn(`EscalationTimeline: Container #${containerId} not found`);
        }
    }

    /**
     * Render timeline with status stages
     * @param {array} stages - Array of workflow stages
     * @param {string} currentStage - Current active stage
     */
    render(stages, currentStage = null) {
        if (!this.container) return;

        let html = '<div class="sla-timeline">';

        stages.forEach((stage, index) => {
            const isCompleted = currentStage && this.isStageCompleted(stage.id, currentStage);
            const isActive = stage.id === currentStage;
            const isOverdue = stage.overdue || false;

            const statusClass = isCompleted ? 'completed' : isActive ? 'active' : isOverdue ? 'overdue' : '';

            html += `
                <div class="sla-timeline-item ${statusClass}">
                    <span class="sla-timeline-marker"></span>
                    <div class="sla-timeline-content">
                        <strong>${stage.name}</strong>
                        <p>${stage.description || ''}</p>
                        ${stage.timestamp ? `<small>${this.formatDate(stage.timestamp)}</small>` : ''}
                    </div>
                </div>
            `;
        });

        html += '</div>';
        this.container.innerHTML = html;
    }

    /**
     * Render SOP-NCR specific escalation workflow
     * @param {object} sopTicket - SOP ticket data
     */
    renderSOPWorkflow(sopTicket) {
        const stages = [
            {
                id: 'received',
                name: '🔔 Received',
                description: 'SOP failure reported',
                timestamp: sopTicket.created_at,
                overdue: false
            },
            {
                id: 'acknowledged',
                name: '✓ Acknowledged',
                description: 'Manager acknowledged the issue',
                timestamp: sopTicket.acknowledged_at,
                overdue: false
            },
            {
                id: 'under_review',
                name: '📋 Under Review',
                description: 'Manager analyzing the failure',
                timestamp: sopTicket.review_started_at,
                overdue: this.isDateOverdue(sopTicket.review_deadline)
            },
            {
                id: 'escalated',
                name: '⚠️ Escalated to HOD',
                description: 'Escalated for head of department approval',
                timestamp: sopTicket.escalated_at,
                overdue: this.isDateOverdue(sopTicket.escalation_deadline)
            },
            {
                id: 'closed',
                name: '✅ Closed',
                description: 'Issue resolved and closed',
                timestamp: sopTicket.closed_at,
                overdue: false
            }
        ];

        this.render(stages, sopTicket.status);
    }

    /**
     * Render Maintenance task escalation workflow
     * @param {object} maintenanceTask - Maintenance task data
     */
    renderMaintenanceWorkflow(maintenanceTask) {
        const stages = [
            {
                id: 'scheduled',
                name: '📅 Scheduled',
                description: 'Maintenance task scheduled',
                timestamp: maintenanceTask.scheduled_date,
                overdue: false
            },
            {
                id: 'in_progress',
                name: '🔧 In Progress',
                description: 'Maintenance work started',
                timestamp: maintenanceTask.started_at,
                overdue: this.isDateOverdue(maintenanceTask.due_date)
            },
            {
                id: 'completed',
                name: '✅ Completed',
                description: 'Maintenance work finished',
                timestamp: maintenanceTask.completed_at,
                overdue: false
            },
            {
                id: 'verified',
                name: '👤 Verified',
                description: 'Work verified by supervisor',
                timestamp: maintenanceTask.verified_at,
                overdue: false
            }
        ];

        this.render(stages, maintenanceTask.status);
    }

    /**
     * Render Order fulfillment workflow
     * @param {object} order - Order data
     */
    renderOrderWorkflow(order) {
        const stages = [
            {
                id: 'pending',
                name: '📝 Created',
                description: 'Order created and awaiting processing',
                timestamp: order.created_at,
                overdue: false
            },
            {
                id: 'scheduled',
                name: '📅 Scheduled',
                description: 'Order scheduled for production',
                timestamp: order.scheduled_date,
                overdue: this.isDateOverdue(order.scheduled_deadline)
            },
            {
                id: 'in_progress',
                name: '⚙️ In Progress',
                description: 'Production in progress',
                timestamp: order.started_at,
                overdue: this.isDateOverdue(order.due_date)
            },
            {
                id: 'completed',
                name: '✅ Completed',
                description: 'Production completed',
                timestamp: order.completed_at,
                overdue: !this.isOnTime(order.completed_at, order.due_date)
            },
            {
                id: 'delivered',
                name: '🚚 Delivered',
                description: 'Order delivered to customer',
                timestamp: order.delivered_at,
                overdue: false
            }
        ];

        this.render(stages, order.status);
    }

    /**
     * Check if a stage is completed before current stage
     */
    isStageCompleted(stageId, currentStage) {
        const stageOrder = ['received', 'acknowledged', 'under_review', 'escalated', 'closed',
                           'scheduled', 'in_progress', 'completed', 'verified', 'delivered'];
        
        const currentIndex = stageOrder.indexOf(currentStage);
        const stageIndex = stageOrder.indexOf(stageId);
        
        return stageIndex < currentIndex;
    }

    /**
     * Check if date is overdue
     */
    isDateOverdue(dateStr) {
        if (!dateStr) return false;
        return new Date(dateStr) < new Date();
    }

    /**
     * Check if delivery was on time
     */
    isOnTime(completedDate, dueDate) {
        if (!completedDate || !dueDate) return true;
        return new Date(completedDate) <= new Date(dueDate);
    }

    /**
     * Format date for display
     */
    formatDate(dateStr) {
        if (!dateStr) return '';
        const date = new Date(dateStr);
        return date.toLocaleString('en-ZA', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    /**
     * Update a stage in the timeline
     */
    updateStage(stageId, data) {
        // Find the stage and update its data
        const index = this.workflow.stages?.findIndex(s => s.id === stageId);
        if (index !== undefined && index >= 0) {
            this.workflow.stages[index] = { ...this.workflow.stages[index], ...data };
            this.render(this.workflow.stages, this.workflow.currentStage);
        }
    }

    /**
     * Move to next stage
     */
    nextStage(stageId) {
        const stageOrder = ['received', 'acknowledged', 'under_review', 'escalated', 'closed',
                           'scheduled', 'in_progress', 'completed', 'verified', 'delivered'];
        
        const currentIndex = stageOrder.indexOf(this.workflow.currentStage);
        if (currentIndex >= 0 && currentIndex < stageOrder.length - 1) {
            const nextStage = stageOrder[currentIndex + 1];
            this.workflow.currentStage = nextStage;
            
            // Update stage with current timestamp
            this.updateStage(nextStage, { timestamp: new Date().toISOString() });
            
            // Show toast notification
            if (window.toast) {
                toast.info(`Status updated to: ${nextStage.replace(/_/g, ' ').toUpperCase()}`);
            }
        }
    }

    /**
     * Get current stage details
     */
    getCurrentStage() {
        return this.workflow.stages?.find(s => s.id === this.workflow.currentStage) || null;
    }

    /**
     * Check if workflow is complete
     */
    isComplete() {
        const finalStages = ['closed', 'delivered', 'verified'];
        return finalStages.includes(this.workflow.currentStage);
    }
}

/**
 * Global helper to initialize escalation timeline
 * Usage: initEscalationTimeline('timeline-container', sopTicket)
 */
function initEscalationTimeline(containerId, data, type = 'sop') {
    const timeline = new EscalationTimeline(containerId);
    
    switch(type) {
        case 'sop':
            timeline.renderSOPWorkflow(data);
            break;
        case 'maintenance':
            timeline.renderMaintenanceWorkflow(data);
            break;
        case 'order':
            timeline.renderOrderWorkflow(data);
            break;
        default:
            timeline.render(data.stages, data.currentStage);
    }
    
    return timeline;
}
