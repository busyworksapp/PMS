/**
 * WhatsApp Widget
 * Real-time messaging interface for WhatsApp integration
 * 
 * Features:
 * - Contact list with unread badges
 * - Real-time message updates (polling)
 * - Send/receive messages
 * - Mark messages as read
 * - Contact management
 * - Message search
 * - Responsive design
 */

class WhatsAppWidget {
    constructor(config = {}) {
        this.config = {
            apiBase: config.apiBase || 'http://127.0.0.1:8000/api/whatsapp',
            pollingInterval: config.pollingInterval || 5000,
            maxRetries: config.maxRetries || 3,
            retryDelay: config.retryDelay || 1000,
            ...config
        };

        this.contacts = [];
        this.currentContact = null;
        this.messages = [];
        this.isInitialized = false;
        this.isPolling = false;
        this.retryCount = 0;

        this.init();
    }

    /**
     * Initialize widget
     */
    async init() {
        try {
            this.createWidgetHTML();
            this.attachEventListeners();
            await this.loadContacts();
            this.startPolling();
            this.isInitialized = true;
            console.log('✅ WhatsApp widget initialized');
        } catch (error) {
            console.error('❌ Error initializing WhatsApp widget:', error);
            this.showNotification('Failed to initialize WhatsApp widget', 'error');
        }
    }

    /**
     * Create widget HTML structure
     */
    createWidgetHTML() {
        const widget = document.createElement('div');
        widget.id = 'whatsapp-widget';
        widget.className = 'whatsapp-widget';
        widget.innerHTML = `
            <div class="whatsapp-header">
                <div class="header-left">
                    <h3>WhatsApp</h3>
                    <span class="status-indicator"></span>
                </div>
                <div class="whatsapp-controls">
                    <button class="search-btn" id="search-toggle" title="Search">🔍</button>
                    <button class="minimize-btn" id="minimize-btn" title="Minimize">−</button>
                </div>
            </div>

            <div class="whatsapp-container">
                <!-- Contact List -->
                <div class="whatsapp-contacts">
                    <input type="text" id="contact-search" class="contact-search" 
                           placeholder="Search contacts..." />
                    <div id="contact-list" class="contact-list">
                        <div class="loading">Loading contacts...</div>
                    </div>
                </div>

                <!-- Chat Area -->
                <div class="whatsapp-chat">
                    <div class="chat-header" id="chat-header">
                        <div class="no-contact-selected">
                            Select a contact to start messaging
                        </div>
                    </div>
                    <div class="chat-messages" id="chat-messages"></div>
                    <div class="chat-input-area">
                        <input type="text" id="message-input" class="message-input" 
                               placeholder="Type a message..." disabled />
                        <button id="send-btn" class="send-btn" disabled>📤</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(widget);
    }

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Send message
        document.getElementById('send-btn').addEventListener('click', 
            () => this.sendMessage());
        document.getElementById('message-input').addEventListener('keypress', 
            (e) => e.key === 'Enter' && this.sendMessage());

        // Contact search
        document.getElementById('contact-search').addEventListener('input', 
            (e) => this.filterContacts(e.target.value));

        // Minimize
        document.getElementById('minimize-btn').addEventListener('click',
            () => this.toggleMinimize());
    }

    /**
     * Load contacts from API
     */
    async loadContacts() {
        try {
            const response = await fetch(`${this.config.apiBase}/contacts`);
            if (!response.ok) throw new Error('Failed to load contacts');

            const data = await response.json();
            this.contacts = data.contacts || [];
            this.renderContactList();
            this.retryCount = 0;
            this.updateStatus('connected');
        } catch (error) {
            console.error('Error loading contacts:', error);
            this.updateStatus('error');
            
            if (this.retryCount < this.config.maxRetries) {
                this.retryCount++;
                setTimeout(() => this.loadContacts(), this.config.retryDelay);
            }
        }
    }

    /**
     * Select contact and load messages
     */
    async selectContact(phoneNumber) {
        try {
            this.currentContact = this.contacts.find(
                c => c.phone_number === phoneNumber
            );

            if (!this.currentContact) {
                throw new Error('Contact not found');
            }

            await this.loadMessages(phoneNumber);
            this.renderChatHeader();
            this.renderMessages();
            this.enableMessageInput();
            await this.markAsRead(phoneNumber);

            // Update active state
            document.querySelectorAll('.contact-item').forEach(item => {
                item.classList.remove('active');
            });
            document.querySelector(
                `[data-phone="${phoneNumber}"]`
            )?.classList.add('active');
        } catch (error) {
            console.error('Error selecting contact:', error);
            this.showNotification('Error selecting contact', 'error');
        }
    }

    /**
     * Load messages for contact
     */
    async loadMessages(phoneNumber) {
        try {
            const response = await fetch(
                `${this.config.apiBase}/messages?contact_number=${phoneNumber}&limit=50`
            );
            if (!response.ok) throw new Error('Failed to load messages');

            const data = await response.json();
            this.messages = data.messages || [];
        } catch (error) {
            console.error('Error loading messages:', error);
            this.showNotification('Failed to load messages', 'error');
        }
    }

    /**
     * Send message
     */
    async sendMessage() {
        const input = document.getElementById('message-input');
        const text = input.value.trim();

        if (!text || !this.currentContact) {
            return;
        }

        try {
            input.disabled = true;
            const sendBtn = document.getElementById('send-btn');
            sendBtn.disabled = true;
            sendBtn.textContent = '⏳';

            const response = await fetch(`${this.config.apiBase}/send`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    phone_number: this.currentContact.phone_number,
                    message_text: text,
                    message_type: 'text'
                })
            });

            if (!response.ok) throw new Error('Failed to send message');

            input.value = '';
            await this.loadMessages(this.currentContact.phone_number);
            this.renderMessages();
            this.scrollToBottom();
            this.showNotification('Message sent ✓', 'success');
        } catch (error) {
            console.error('Error sending message:', error);
            this.showNotification('Failed to send message', 'error');
        } finally {
            input.disabled = false;
            const sendBtn = document.getElementById('send-btn');
            sendBtn.disabled = false;
            sendBtn.textContent = '📤';
        }
    }

    /**
     * Render contact list
     */
    renderContactList() {
        const container = document.getElementById('contact-list');
        
        if (this.contacts.length === 0) {
            container.innerHTML = '<div class="no-contacts">No contacts yet</div>';
            return;
        }

        container.innerHTML = this.contacts.map(contact => `
            <div class="contact-item ${contact.unread_count > 0 ? 'unread' : ''} 
                     ${this.currentContact?.phone_number === contact.phone_number ? 'active' : ''}"
                 data-phone="${contact.phone_number}">
                <div class="contact-info">
                    <div class="contact-name">${this.escapeHtml(
                        contact.display_name || contact.phone_number
                    )}</div>
                    <div class="contact-preview">Last: ${contact.last_message_time ? 
                        new Date(contact.last_message_time).toLocaleTimeString() : 'Never'}</div>
                </div>
                ${contact.unread_count > 0 ? `
                    <div class="unread-badge">${contact.unread_count}</div>
                ` : ''}
            </div>
        `).join('');

        // Attach click handlers
        container.querySelectorAll('.contact-item').forEach(item => {
            item.addEventListener('click', () => {
                this.selectContact(item.dataset.phone);
            });
        });
    }

    /**
     * Render messages
     */
    renderMessages() {
        const container = document.getElementById('chat-messages');

        if (this.messages.length === 0) {
            container.innerHTML = '<div class="no-messages">No messages yet</div>';
            return;
        }

        container.innerHTML = this.messages.map(msg => {
            const isOutbound = msg.direction === 'outbound';
            const statusIcon = this.getStatusIcon(msg.status);
            const time = new Date(msg.created_at).toLocaleTimeString(
                [], { hour: '2-digit', minute: '2-digit' }
            );

            return `
                <div class="message-bubble ${isOutbound ? 'sent' : 'received'}">
                    <div class="message-text">${this.escapeHtml(msg.message_text)}</div>
                    <div class="message-footer">
                        <span class="message-time">${time}</span>
                        ${isOutbound ? `<span class="message-status">${statusIcon}</span>` : ''}
                    </div>
                </div>
            `;
        }).join('');

        this.scrollToBottom();
    }

    /**
     * Render chat header
     */
    renderChatHeader() {
        if (!this.currentContact) return;

        const header = document.getElementById('chat-header');
        header.innerHTML = `
            <div class="header-info">
                <h3>${this.escapeHtml(
                    this.currentContact.display_name || 
                    this.currentContact.phone_number
                )}</h3>
                <span class="header-status">
                    ${this.currentContact.is_verified ? '✓ Verified' : 'Chat'}
                </span>
            </div>
        `;
    }

    /**
     * Filter contacts by search
     */
    filterContacts(searchTerm) {
        const filtered = this.contacts.filter(contact => {
            const name = (contact.display_name || contact.phone_number).toLowerCase();
            const phone = contact.phone_number.toLowerCase();
            return name.includes(searchTerm.toLowerCase()) || 
                   phone.includes(searchTerm.toLowerCase());
        });

        const container = document.getElementById('contact-list');
        if (filtered.length === 0) {
            container.innerHTML = '<div class="no-contacts">No contacts found</div>';
            return;
        }

        container.innerHTML = filtered.map(contact => `
            <div class="contact-item ${contact.unread_count > 0 ? 'unread' : ''}"
                 data-phone="${contact.phone_number}">
                <div class="contact-info">
                    <div class="contact-name">${this.escapeHtml(
                        contact.display_name || contact.phone_number
                    )}</div>
                    <div class="contact-preview">Last: ${contact.last_message_time ? 
                        new Date(contact.last_message_time).toLocaleTimeString() : 'Never'}</div>
                </div>
                ${contact.unread_count > 0 ? `
                    <div class="unread-badge">${contact.unread_count}</div>
                ` : ''}
            </div>
        `).join('');

        container.querySelectorAll('.contact-item').forEach(item => {
            item.addEventListener('click', () => {
                this.selectContact(item.dataset.phone);
            });
        });
    }

    /**
     * Start polling for updates
     */
    startPolling() {
        if (this.isPolling) return;
        this.isPolling = true;

        setInterval(async () => {
            await this.loadContacts();
            if (this.currentContact) {
                await this.loadMessages(this.currentContact.phone_number);
                this.renderMessages();
            }
        }, this.config.pollingInterval);
    }

    /**
     * Mark messages as read
     */
    async markAsRead(phoneNumber) {
        try {
            await fetch(`${this.config.apiBase}/contacts/${phoneNumber}/read`, {
                method: 'POST'
            });
        } catch (error) {
            console.error('Error marking as read:', error);
        }
    }

    /**
     * Enable message input
     */
    enableMessageInput() {
        const input = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        if (window.toastManager) {
            window.toastManager.show(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }

    /**
     * Scroll to bottom of messages
     */
    scrollToBottom() {
        const container = document.getElementById('chat-messages');
        container.scrollTop = container.scrollHeight;
    }

    /**
     * Escape HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Get status icon
     */
    getStatusIcon(status) {
        const icons = {
            'sent': '✓',
            'delivered': '✓✓',
            'read': '✓✓',
            'failed': '✗',
            'pending': '⏳'
        };
        return icons[status] || '○';
    }

    /**
     * Update status indicator
     */
    updateStatus(status) {
        const indicator = document.querySelector('.status-indicator');
        if (indicator) {
            indicator.className = `status-indicator status-${status}`;
            indicator.title = status.charAt(0).toUpperCase() + status.slice(1);
        }
    }

    /**
     * Toggle minimize
     */
    toggleMinimize() {
        const widget = document.getElementById('whatsapp-widget');
        widget.classList.toggle('minimized');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize if not already initialized
    if (!window.whatsappWidget) {
        window.whatsappWidget = new WhatsAppWidget();
    }
});
