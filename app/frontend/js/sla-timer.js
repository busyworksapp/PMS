/**
 * SLA Timer
 * Displays countdown timer for SLA deadlines with color changes for urgency
 */

class SLATimer {
    constructor(elementId, deadlineDate, options = {}) {
        this.elementId = elementId;
        this.deadline = new Date(deadlineDate);
        this.element = document.getElementById(elementId);
        this.timerInterval = null;
        
        // Options
        this.warningThreshold = options.warningThreshold || 0.25; // 25% remaining
        this.criticalThreshold = options.criticalThreshold || 0.10; // 10% remaining
        this.onExpire = options.onExpire || null;
        this.updateFrequency = options.updateFrequency || 1000; // Update every 1 second
        
        // State
        this.expired = false;
        this.hasWarned = false;
        this.hasCritical = false;
        
        // Initial calculation
        this.totalDuration = this.deadline - new Date();
        
        // Start timer
        this.start();
    }

    /**
     * Start the timer
     */
    start() {
        if (!this.element) {
            console.warn(`SLATimer: Element not found for #${this.elementId}`);
            return;
        }

        // Update immediately
        this.update();

        // Then update on interval
        this.timerInterval = setInterval(() => this.update(), this.updateFrequency);
    }

    /**
     * Update timer display
     */
    update() {
        const now = new Date();
        const remaining = this.deadline - now;

        if (remaining <= 0) {
            this.handleExpiry();
            return;
        }

        // Format time
        const timeStr = this.formatTime(remaining);
        this.element.textContent = timeStr;

        // Check thresholds
        const percentRemaining = remaining / this.totalDuration;
        
        // Critical state (last 10%)
        if (percentRemaining <= this.criticalThreshold && !this.hasCritical) {
            this.setCritical();
            this.hasCritical = true;
        }
        // Warning state (last 25%)
        else if (percentRemaining <= this.warningThreshold && !this.hasWarned) {
            this.setWarning();
            this.hasWarned = true;
        }
        // Normal state
        else if (percentRemaining > this.warningThreshold) {
            this.setNormal();
            this.hasWarned = false;
            this.hasCritical = false;
        }
    }

    /**
     * Handle expiry
     */
    handleExpiry() {
        if (this.expired) return;
        
        this.expired = true;
        this.stop();

        this.element.textContent = 'EXPIRED';
        this.element.classList.add('sla-expired');
        this.element.classList.remove('sla-normal', 'sla-warning', 'sla-critical');

        // Show warning toast
        if (window.toast) {
            toast.error('⏰ SLA Deadline Breached');
        }

        // Call callback if provided
        if (this.onExpire) {
            this.onExpire();
        }
    }

    /**
     * Set normal state (green)
     */
    setNormal() {
        this.element.classList.remove('sla-warning', 'sla-critical', 'sla-expired');
        this.element.classList.add('sla-normal');
    }

    /**
     * Set warning state (orange)
     */
    setWarning() {
        this.element.classList.remove('sla-normal', 'sla-critical', 'sla-expired');
        this.element.classList.add('sla-warning');

        if (window.toast) {
            toast.warning('⚠️ SLA Deadline Approaching (25% time remaining)');
        }
    }

    /**
     * Set critical state (red with animation)
     */
    setCritical() {
        this.element.classList.remove('sla-normal', 'sla-warning', 'sla-expired');
        this.element.classList.add('sla-critical');

        if (window.toast) {
            toast.error('🚨 CRITICAL: SLA Deadline in Last 10%');
        }
    }

    /**
     * Format time remaining
     * Returns HH:MM:SS format
     */
    formatTime(milliseconds) {
        const totalSeconds = Math.floor(milliseconds / 1000);
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }

    /**
     * Stop the timer
     */
    stop() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    /**
     * Destroy timer
     */
    destroy() {
        this.stop();
        this.element = null;
    }

    /**
     * Get remaining time in milliseconds
     */
    getRemaining() {
        return Math.max(0, this.deadline - new Date());
    }

    /**
     * Check if expired
     */
    isExpired() {
        return this.expired || this.getRemaining() <= 0;
    }

    /**
     * Update deadline (useful if SLA is extended)
     */
    updateDeadline(newDeadline) {
        this.deadline = new Date(newDeadline);
        this.totalDuration = this.deadline - new Date();
        this.expired = false;
        this.hasWarned = false;
        this.hasCritical = false;
        this.update();
    }
}

/**
 * Global helper to initialize SLA timer on an element
 * Usage: initSLATimer('sla-time', '2026-01-20T18:00:00Z')
 */
function initSLATimer(elementId, deadline, options = {}) {
    return new SLATimer(elementId, deadline, options);
}
