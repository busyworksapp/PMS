/**
 * Toast Notification System
 * Displays temporary notifications for user feedback
 */

class ToastNotification {
    constructor() {
        this.containerId = 'toast-container';
        this.toastClass = 'toast';
        this.initContainer();
    }

    /**
     * Initialize the toast container if it doesn't exist
     */
    initContainer() {
        let container = document.getElementById(this.containerId);
        if (!container) {
            container = document.createElement('div');
            container.id = this.containerId;
            container.className = this.containerId;
            document.body.appendChild(container);
        }
    }

    /**
     * Show a toast notification
     * @param {string} message - The message to display
     * @param {string} type - Type of notification: 'success', 'error', 'warning', 'info'
     * @param {number} duration - Duration in milliseconds (default: 5000)
     */
    show(message, type = 'info', duration = 5000) {
        const container = document.getElementById(this.containerId);
        
        const toast = document.createElement('div');
        toast.className = `${this.toastClass} ${type}`;
        
        // Create content structure
        const content = document.createElement('div');
        content.className = `${this.toastClass}-content`;
        
        // Add icon based on type
        const icon = document.createElement('span');
        icon.className = `${this.toastClass}-icon`;
        switch(type) {
            case 'success':
                icon.innerHTML = '✓';
                break;
            case 'error':
                icon.innerHTML = '✕';
                break;
            case 'warning':
                icon.innerHTML = '⚠';
                break;
            case 'info':
                icon.innerHTML = 'ⓘ';
                break;
        }
        
        // Add message
        const messageEl = document.createElement('span');
        messageEl.className = `${this.toastClass}-message`;
        messageEl.textContent = message;
        
        content.appendChild(icon);
        content.appendChild(messageEl);
        
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.className = `${this.toastClass}-close`;
        closeBtn.textContent = '×';
        closeBtn.onclick = () => this.remove(toast);
        
        toast.appendChild(content);
        toast.appendChild(closeBtn);
        
        container.appendChild(toast);
        
        // Auto-remove after duration
        const timeoutId = setTimeout(() => this.remove(toast), duration);
        
        // Store timeout ID on toast for manual removal
        toast.timeoutId = timeoutId;
        
        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);
        
        return toast;
    }

    /**
     * Remove a toast notification
     */
    remove(toast) {
        if (!toast) return;
        
        // Clear timeout if exists
        if (toast.timeoutId) {
            clearTimeout(toast.timeoutId);
        }
        
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 300);
    }

    /**
     * Success notification
     */
    success(message, duration = 5000) {
        return this.show(message, 'success', duration);
    }

    /**
     * Error notification
     */
    error(message, duration = 5000) {
        return this.show(message, 'error', duration);
    }

    /**
     * Warning notification
     */
    warning(message, duration = 5000) {
        return this.show(message, 'warning', duration);
    }

    /**
     * Info notification
     */
    info(message, duration = 5000) {
        return this.show(message, 'info', duration);
    }

    /**
     * Clear all toasts
     */
    clear() {
        const container = document.getElementById(this.containerId);
        if (container) {
            const toasts = container.querySelectorAll(`.${this.toastClass}`);
            toasts.forEach(toast => this.remove(toast));
        }
    }
}

// Create global toast instance
const toast = new ToastNotification();
