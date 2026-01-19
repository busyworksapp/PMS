# 🤖 Phase 4: WhatsApp Integration - IMPLEMENTATION IN PROGRESS

**Status:** 🟡 Starting now (January 18, 2026)  
**Estimated Duration:** 4-6 hours  
**Deliverables:** 1,500+ lines of production code  

---

## 📋 Phase 4 Implementation Roadmap

### Part 1: Database Schema & Models (30 minutes)

**Database Tables to Create:**

```sql
-- Messages table
CREATE TABLE whatsapp_messages (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    from_phone_number VARCHAR(20) NOT NULL,
    to_phone_number VARCHAR(20) NOT NULL,
    message_text TEXT,
    media_url VARCHAR(500),
    media_type VARCHAR(50),
    status VARCHAR(20),  -- 'pending', 'sent', 'delivered', 'read', 'failed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_from (from_phone_number),
    INDEX idx_to (to_phone_number),
    INDEX idx_created (created_at)
);

-- Contacts table
CREATE TABLE whatsapp_contacts (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    last_message_time TIMESTAMP,
    unread_count INTEGER DEFAULT 0,
    is_pinned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_phone (phone_number)
);

-- Webhooks for tracking incoming messages
CREATE TABLE whatsapp_webhooks (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    webhook_id VARCHAR(100),
    event_type VARCHAR(50),
    payload JSON,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**SQLAlchemy Models:**

```python
# app/models/whatsapp.py (100 lines)

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WhatsAppMessage(Base):
    __tablename__ = "whatsapp_messages"
    
    id = Column(Integer, primary_key=True)
    from_phone_number = Column(String(20), nullable=False)
    to_phone_number = Column(String(20), nullable=False)
    message_text = Column(Text, nullable=True)
    media_url = Column(String(500), nullable=True)
    media_type = Column(String(50), nullable=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WhatsAppContact(Base):
    __tablename__ = "whatsapp_contacts"
    
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    display_name = Column(String(100))
    last_message_time = Column(DateTime)
    unread_count = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WhatsAppWebhook(Base):
    __tablename__ = "whatsapp_webhooks"
    
    id = Column(Integer, primary_key=True)
    webhook_id = Column(String(100))
    event_type = Column(String(50))
    payload = Column(JSON)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

### Part 2: Backend WhatsApp Service (1-1.5 hours)

**WhatsApp Integration Module:**

```python
# app/integrations/whatsapp.py (350-400 lines)

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import hashlib
import hmac
import json
from datetime import datetime
from app.db.database import SessionLocal
from app.models.whatsapp import WhatsAppMessage, WhatsAppContact

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])

class WhatsAppService:
    def __init__(self, business_account_id, phone_number_id, api_token, webhook_verify_token):
        self.business_account_id = business_account_id
        self.phone_number_id = phone_number_id
        self.api_token = api_token
        self.webhook_verify_token = webhook_verify_token
        self.base_url = "https://graph.instagram.com/v18.0"
        self.client = httpx.AsyncClient()
    
    async def send_message(self, phone_number: str, message_text: str, media_url: str = None):
        """Send WhatsApp message via Meta API"""
        # Implementation: 50 lines
        pass
    
    async def handle_webhook(self, payload: dict):
        """Process incoming webhook from Meta"""
        # Implementation: 80 lines
        pass
    
    async def verify_webhook(self, signature: str, body: str) -> bool:
        """Verify webhook authenticity using HMAC"""
        # Implementation: 20 lines
        pass
    
    async def get_message_history(self, phone_number: str, limit: int = 50):
        """Retrieve message history with contact"""
        # Implementation: 40 lines
        pass

# Initialize service
whatsapp_service = WhatsAppService(
    business_account_id=os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID"),
    phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    api_token=os.getenv("WHATSAPP_API_TOKEN"),
    webhook_verify_token=os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN")
)

@router.post("/webhook")
async def receive_webhook(request: Request):
    """Receive incoming WhatsApp messages from Meta"""
    # Implementation: 60 lines
    pass

@router.post("/send")
async def send_message(phone_number: str, message: str):
    """Send WhatsApp message"""
    # Implementation: 40 lines
    pass

@router.get("/messages")
async def get_messages(contact_number: str, limit: int = 50):
    """Get message history with contact"""
    # Implementation: 30 lines
    pass

@router.get("/contacts")
async def get_contacts():
    """Get all contacts with unread counts"""
    # Implementation: 35 lines
    pass

@router.post("/read/{contact_number}")
async def mark_as_read(contact_number: str):
    """Mark messages as read"""
    # Implementation: 25 lines
    pass
```

**Pydantic Schemas:**

```python
# app/schemas/whatsapp.py (80 lines)

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WhatsAppMessageCreate(BaseModel):
    phone_number: str
    message_text: str
    media_url: Optional[str] = None

class WhatsAppMessageResponse(BaseModel):
    id: int
    from_phone_number: str
    to_phone_number: str
    message_text: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class WhatsAppContactResponse(BaseModel):
    phone_number: str
    display_name: Optional[str]
    last_message_time: Optional[datetime]
    unread_count: int
    is_pinned: bool
    
    class Config:
        from_attributes = True
```

---

### Part 3: Frontend WhatsApp Widget (1.5-2 hours)

**HTML Integration in dashboard.html:**

```html
<!-- WhatsApp Widget Section -->
<div id="whatsapp-widget" class="whatsapp-widget">
    <div class="whatsapp-header">
        <h3>WhatsApp Messages</h3>
        <div class="whatsapp-controls">
            <button class="search-btn" id="search-toggle">🔍</button>
            <button class="minimize-btn" id="minimize-btn">−</button>
        </div>
    </div>
    
    <div class="whatsapp-container">
        <!-- Contact List -->
        <div class="whatsapp-contacts">
            <input type="text" id="contact-search" class="contact-search" placeholder="Search contacts...">
            <div id="contact-list" class="contact-list"></div>
        </div>
        
        <!-- Chat Area -->
        <div class="whatsapp-chat">
            <div class="chat-header" id="chat-header"></div>
            <div class="chat-messages" id="chat-messages"></div>
            <div class="chat-input-area">
                <input type="text" id="message-input" class="message-input" placeholder="Type a message...">
                <button id="send-btn" class="send-btn">📤</button>
            </div>
        </div>
    </div>
</div>

<script src="js/whatsapp-widget.js"></script>
<link rel="stylesheet" href="css/whatsapp-styles.css">
```

**JavaScript Widget Class (450+ lines):**

```javascript
// js/whatsapp-widget.js

class WhatsAppWidget {
    constructor() {
        this.contacts = [];
        this.currentContact = null;
        this.messages = [];
        this.apiBase = 'http://127.0.0.1:8000/api/whatsapp';
        this.pollingInterval = 5000; // 5 seconds
        this.init();
    }
    
    async init() {
        this.attachEventListeners();
        await this.loadContacts();
        this.startPollingUpdates();
    }
    
    async loadContacts() {
        try {
            const response = await fetch(`${this.apiBase}/contacts`);
            if (!response.ok) throw new Error('Failed to load contacts');
            
            this.contacts = await response.json();
            this.renderContactList();
        } catch (error) {
            console.error('Error loading contacts:', error);
            this.showNotification('Failed to load contacts', 'error');
        }
    }
    
    async selectContact(phoneNumber) {
        this.currentContact = this.contacts.find(c => c.phone_number === phoneNumber);
        await this.loadMessages(phoneNumber);
        this.renderChatHeader();
        this.renderMessages();
        await this.markAsRead(phoneNumber);
    }
    
    async loadMessages(phoneNumber) {
        try {
            const response = await fetch(
                `${this.apiBase}/messages?contact_number=${phoneNumber}`
            );
            if (!response.ok) throw new Error('Failed to load messages');
            
            this.messages = await response.json();
        } catch (error) {
            console.error('Error loading messages:', error);
            this.showNotification('Failed to load messages', 'error');
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('message-input');
        const text = input.value.trim();
        
        if (!text || !this.currentContact) return;
        
        try {
            const response = await fetch(`${this.apiBase}/send`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    phone_number: this.currentContact.phone_number,
                    message: text
                })
            });
            
            if (!response.ok) throw new Error('Failed to send message');
            
            input.value = '';
            await this.loadMessages(this.currentContact.phone_number);
            this.renderMessages();
            this.scrollToBottom();
        } catch (error) {
            console.error('Error sending message:', error);
            this.showNotification('Failed to send message', 'error');
        }
    }
    
    renderContactList() {
        const container = document.getElementById('contact-list');
        container.innerHTML = this.contacts.map(contact => `
            <div class="contact-item ${contact.unread_count > 0 ? 'unread' : ''}" 
                 data-phone="${contact.phone_number}">
                <div class="contact-info">
                    <div class="contact-name">${contact.display_name || contact.phone_number}</div>
                    <div class="contact-preview">Last message...</div>
                </div>
                ${contact.unread_count > 0 ? `
                    <div class="unread-badge">${contact.unread_count}</div>
                ` : ''}
            </div>
        `).join('');
        
        container.querySelectorAll('.contact-item').forEach(item => {
            item.addEventListener('click', () => {
                this.selectContact(item.dataset.phone);
                document.querySelectorAll('.contact-item').forEach(i => 
                    i.classList.remove('active')
                );
                item.classList.add('active');
            });
        });
    }
    
    renderMessages() {
        const container = document.getElementById('chat-messages');
        container.innerHTML = this.messages.map(msg => `
            <div class="message-bubble ${msg.from_phone_number === this.currentContact.phone_number ? 'received' : 'sent'}">
                <div class="message-text">${this.escapeHtml(msg.message_text)}</div>
                <div class="message-time">${new Date(msg.created_at).toLocaleTimeString()}</div>
                <div class="message-status">${this.getStatusIcon(msg.status)}</div>
            </div>
        `).join('');
        
        this.scrollToBottom();
    }
    
    renderChatHeader() {
        if (!this.currentContact) return;
        
        const header = document.getElementById('chat-header');
        header.innerHTML = `
            <div class="header-info">
                <h3>${this.currentContact.display_name || this.currentContact.phone_number}</h3>
                <span class="header-status">Active now</span>
            </div>
        `;
    }
    
    startPollingUpdates() {
        setInterval(async () => {
            if (this.currentContact) {
                await this.loadMessages(this.currentContact.phone_number);
                this.renderMessages();
            }
            await this.loadContacts();
        }, this.pollingInterval);
    }
    
    async markAsRead(phoneNumber) {
        try {
            await fetch(`${this.apiBase}/read/${phoneNumber}`, { method: 'POST' });
        } catch (error) {
            console.error('Error marking as read:', error);
        }
    }
    
    showNotification(message, type = 'info') {
        // Use existing toast.js
        window.toastManager?.show(message, type);
    }
    
    scrollToBottom() {
        const container = document.getElementById('chat-messages');
        container.scrollTop = container.scrollHeight;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    getStatusIcon(status) {
        const icons = {
            'sent': '✓',
            'delivered': '✓✓',
            'read': '✓✓',
            'failed': '✗'
        };
        return icons[status] || '';
    }
    
    attachEventListeners() {
        document.getElementById('send-btn').addEventListener('click', () => this.sendMessage());
        document.getElementById('message-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.whatsappWidget = new WhatsAppWidget();
});
```

**CSS Styling (250+ lines):**

```css
/* css/whatsapp-styles.css */

.whatsapp-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 400px;
    height: 600px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 5px 40px rgba(0, 0, 0, 0.16);
    display: flex;
    flex-direction: column;
    z-index: 1000;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.whatsapp-header {
    background: linear-gradient(135deg, #25D366 0%, #20BA5A 100%);
    color: white;
    padding: 15px;
    border-radius: 12px 12px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.whatsapp-header h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
}

.whatsapp-controls {
    display: flex;
    gap: 8px;
}

.whatsapp-controls button {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.2s;
}

.whatsapp-controls button:hover {
    background: rgba(255, 255, 255, 0.3);
}

.whatsapp-container {
    display: flex;
    flex: 1;
    overflow: hidden;
}

.whatsapp-contacts {
    width: 35%;
    border-right: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.contact-search {
    padding: 12px;
    border: none;
    border-bottom: 1px solid #e0e0e0;
    font-size: 14px;
    outline: none;
}

.contact-list {
    flex: 1;
    overflow-y: auto;
}

.contact-item {
    padding: 12px;
    border-bottom: 1px solid #f0f0f0;
    cursor: pointer;
    transition: background 0.2s;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
}

.contact-item:hover {
    background: #f5f5f5;
}

.contact-item.active {
    background: #e8f5e9;
}

.contact-item.unread {
    background: #f0f8ff;
    font-weight: 600;
}

.contact-info {
    flex: 1;
}

.contact-name {
    font-size: 14px;
    font-weight: 500;
    color: #000;
    margin-bottom: 4px;
}

.contact-preview {
    font-size: 12px;
    color: #666;
}

.unread-badge {
    background: #25D366;
    color: white;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
}

.whatsapp-chat {
    width: 65%;
    display: flex;
    flex-direction: column;
    background: white;
}

.chat-header {
    padding: 15px;
    border-bottom: 1px solid #e0e0e0;
    background: #f5f5f5;
}

.header-info h3 {
    margin: 0 0 4px 0;
    font-size: 14px;
}

.header-status {
    font-size: 12px;
    color: #666;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.message-bubble {
    margin-bottom: 8px;
    padding: 10px 12px;
    border-radius: 12px;
    max-width: 80%;
    word-wrap: break-word;
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 14px;
}

.message-bubble.sent {
    background: #DCF8C6;
    margin-left: auto;
    text-align: right;
}

.message-bubble.received {
    background: #fff;
    border: 1px solid #e0e0e0;
}

.message-text {
    word-break: break-word;
}

.message-time {
    font-size: 12px;
    color: #999;
}

.message-status {
    font-size: 12px;
    color: #25D366;
    text-align: right;
}

.chat-input-area {
    padding: 12px;
    border-top: 1px solid #e0e0e0;
    display: flex;
    gap: 8px;
    background: #f9f9f9;
}

.message-input {
    flex: 1;
    border: 1px solid #e0e0e0;
    border-radius: 20px;
    padding: 10px 15px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
}

.message-input:focus {
    border-color: #25D366;
}

.send-btn {
    background: #25D366;
    color: white;
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}

.send-btn:hover {
    background: #20BA5A;
}

.send-btn:active {
    transform: scale(0.95);
}

/* Mobile responsive */
@media (max-width: 768px) {
    .whatsapp-widget {
        width: 100%;
        height: 100%;
        bottom: 0;
        right: 0;
        border-radius: 0;
    }
    
    .whatsapp-contacts {
        width: 40%;
    }
    
    .whatsapp-chat {
        width: 60%;
    }
}
```

---

### Part 4: Environment Configuration

**Add to .env:**

```
WHATSAPP_BUSINESS_ACCOUNT_ID=your_account_id
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_API_TOKEN=your_api_token
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_webhook_verify_token
WHATSAPP_WEBHOOK_URL=https://yourdomain.com/api/whatsapp/webhook
```

**Update requirements.txt:**

```
requests==2.31.0
httpx==0.24.1
python-dotenv==1.0.0
```

---

### Part 5: Integration & Testing

**Add to main.py:**

```python
from app.integrations import whatsapp

def register_routes():
    """Register routes after app is initialized."""
    from app.routes import auth, master, orders, defects
    from app.routes import maintenance, sop_ncr, jobs
    
    app.include_router(auth.router)
    app.include_router(master.router)
    app.include_router(orders.router)
    app.include_router(jobs.router)
    app.include_router(defects.router)
    app.include_router(maintenance.router)
    app.include_router(sop_ncr.router)
    app.include_router(whatsapp.router)  # ← ADD THIS

register_routes()
```

---

## 🎯 Phase 4 Implementation Timeline

| Step | Time | What | Status |
|------|------|------|--------|
| 1 | 30 min | Database schema + models | ⏳ Next |
| 2 | 1-1.5 hr | Backend service + endpoints | ⏳ Next |
| 3 | 1.5-2 hr | Frontend widget + styling | ⏳ Next |
| 4 | 1 hr | Integration + testing | ⏳ Next |
| **Total** | **4-6 hrs** | **Complete WhatsApp** | ⏳ Next |

---

## 📊 Deliverables (Phase 4)

✅ Backend WhatsApp integration (350 lines)  
✅ API endpoints (5 endpoints)  
✅ Database schema (3 tables)  
✅ Frontend widget (450 lines)  
✅ CSS styling (250 lines)  
✅ Complete documentation  
✅ Error handling & retry logic  
✅ Real-time message updates  

**Total: 1,500+ lines of production code**

---

## 🚀 Ready to Begin Phase 4?

All planning is complete. Ready to implement WhatsApp integration now!

