# WhatsApp Integration Setup Guide
**Phase 5 Implementation - Complete Integration Instructions**

---

## 🚀 QUICK START (30 MINUTES)

### Step 1: Install Twilio (5 minutes)
```bash
cd c:\Users\4667.KevroAD\OneDrive - Barron (Pty) Ltd\Desktop\th\app\backend
pip install twilio
```

### Step 2: Create Twilio Account (10 minutes)
```
1. Go to https://www.twilio.com/console
2. Sign up for free account
3. Verify your phone number
4. Go to "Messaging" → "WhatsApp"
5. Click "Get Started" or "Enable WhatsApp"
```

### Step 3: Get Credentials (5 minutes)
```
From Twilio Console:
1. Account SID (Dashboard top left)
2. Auth Token (click "Show")
3. WhatsApp Sandbox Number (usually whatsapp:+14155238886)
```

### Step 4: Configure Environment (5 minutes)
```
Edit your .env file and add:

TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
WHATSAPP_WEBHOOK_URL=http://127.0.0.1:8000/api/whatsapp/webhook
ENABLE_WHATSAPP=true
```

### Step 5: Test WhatsApp Integration (5 minutes)
```
1. Restart backend: python -m uvicorn app.main:app --reload
2. Test endpoint: http://127.0.0.1:8001/docs (in Swagger)
3. Look for "POST /api/whatsapp/test" endpoint
4. Test with: ?phone_number=whatsapp:+YOUR_NUMBER&message=hi
```

---

## 📝 IMPLEMENTATION CHECKLIST

### Backend Setup
- [x] WhatsApp module created (`app/integrations/whatsapp.py`)
- [x] Router registered in `app/main.py`
- [ ] Install Twilio: `pip install twilio`
- [ ] Add Twilio credentials to `.env`
- [ ] Restart backend server
- [ ] Verify endpoints working in Swagger UI

### Twilio Configuration
- [ ] Create Twilio account
- [ ] Create WhatsApp integration
- [ ] Get Account SID and Auth Token
- [ ] Get WhatsApp Sandbox Number
- [ ] Configure webhook URL in Twilio dashboard

### Testing
- [ ] Test with Twilio Sandbox number
- [ ] Send "hi" message
- [ ] Verify menu appears
- [ ] Test all 6 menu options
- [ ] Verify responses are correct

### Production Deployment (Later)
- [ ] Migrate to Meta WhatsApp Business API
- [ ] Move to Redis for session storage
- [ ] Set up error monitoring
- [ ] Configure backup/recovery

---

## 🔧 FILE STRUCTURE

```
app/backend/
├── app/
│   ├── main.py                    [MODIFIED] - Added WhatsApp router
│   ├── integrations/
│   │   └── whatsapp.py           [NEW] - WhatsApp chatbot logic
│   ├── routes/
│   │   ├── auth.py
│   │   ├── orders.py
│   │   ├── defects.py
│   │   └── ... (existing)
│   └── db/
│       └── database.py
├── .env                           [ADD WHATSAPP CONFIG]
└── requirements.txt               [ADD: twilio]
```

---

## 📱 USER WORKFLOWS

### Workflow 1: Create Defect via WhatsApp
```
User: "hi"
Bot:  [Shows 6-option menu]

User: "1"
Bot:  "Order Number (e.g., ORD-12345): ?"

User: "ORD-12345"
Bot:  "✅ Order found: ORD-12345
       Defect Type (Internal Reject / Return / Other): ?"

User: "Internal Reject"
Bot:  "Severity (Low / Medium / High): ?"

User: "High"
Bot:  "Description (brief details): ?"

User: "Bearing defect found during inspection"
Bot:  "✅ Defect Report Created!
       Reference: DEF-20260118143022
       Order is now ON HOLD"
```

### Workflow 2: Check Order Status
```
User: "2"
Bot:  "Order Number (e.g., ORD-12345): ?"

User: "ORD-12345"
Bot:  "📦 Order Status: ORD-12345
       Status: In Progress
       Progress: 75%
       Expected: 2026-01-25
       SLA Status: ✅ On Track"
```

### Workflow 3: Report Maintenance
```
User: "3"
Bot:  "Machine ID (e.g., MACH-001): ?"

User: "MACH-001"
Bot:  "Issue Type (Bearing / Hydraulic / Electrical / Other): ?"

User: "Bearing"
Bot:  "Urgency (Low / Medium / High): ?"

User: "High"
Bot:  "✅ Maintenance Ticket Created!
       Ticket: MAINT-20260118143022
       SLA: 24 hours"
```

### Workflow 4: Check SLA Status
```
User: "5"
Bot:  "Ticket ID (e.g., MAINT-555): ?"

User: "MAINT-555"
Bot:  "⏱️ SLA Status: MAINT-555
       Time Remaining: 44h 32m
       Status: ⚠️ WARNING"
```

---

## 🧪 TESTING YOUR INTEGRATION

### Test 1: Verify Backend Running
```powershell
# In PowerShell
Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/whatsapp/sessions" -UseBasicParsing

# Expected response:
# {"total_sessions": 0, "sessions": {}}
```

### Test 2: Send Test Message
```
1. Open Swagger: http://127.0.0.1:8001/docs
2. Find endpoint: POST /api/whatsapp/test
3. Enter parameters:
   phone_number: whatsapp:+YOUR_PHONE_NUMBER
   message: hi
4. Click "Try it out"
5. Check your WhatsApp
```

### Test 3: Full Workflow
```
1. Open WhatsApp
2. Create group chat with Twilio Sandbox number
3. Send: "join on-demand"
4. Once joined, send: "hi"
5. Test all menu options (1-6)
6. Verify responses
```

### Test 4: Check Sessions
```
Open in browser:
http://127.0.0.1:8001/api/whatsapp/sessions

Shows all active WhatsApp sessions with state and data
```

---

## 🔌 API ENDPOINTS

### POST /api/whatsapp/webhook
**Purpose:** Receive WhatsApp messages from Twilio  
**Method:** POST  
**Authentication:** Twilio signature verification (optional)  
**Expected Form Data:**
```
From: whatsapp:+1234567890
Body: User message text
```

### GET /api/whatsapp/webhook
**Purpose:** Verify webhook URL (Twilio verification)  
**Method:** GET  
**Response:** `{"status": "ok"}`

### POST /api/whatsapp/test
**Purpose:** Send test message (development only)  
**Method:** POST  
**Query Parameters:**
- `phone_number`: whatsapp:+1234567890
- `message`: hi
**Response:** `{"success": true, "phone": "...", "message": "..."}`

### GET /api/whatsapp/sessions
**Purpose:** Get all active WhatsApp sessions (debugging)  
**Method:** GET  
**Response:**
```json
{
  "total_sessions": 2,
  "sessions": {
    "whatsapp:+1234567890": {
      "state": "MENU",
      "data_keys": [],
      "created_at": "2026-01-18T14:30:00",
      "updated_at": "2026-01-18T14:30:00"
    }
  }
}
```

### DELETE /api/whatsapp/sessions/{phone_number}
**Purpose:** Clear session for specific user (debugging)  
**Method:** DELETE  
**URL Parameter:** phone_number (e.g., whatsapp:+1234567890)  
**Response:** `{"success": true, "message": "Session cleared"}`

---

## 🐛 TROUBLESHOOTING

### Issue: "No module named 'twilio'"
**Solution:**
```bash
pip install twilio
```

### Issue: "Twilio credentials not found"
**Solution:**
1. Check `.env` file has TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
2. Restart backend server
3. Verify credentials in Twilio dashboard

### Issue: Messages not arriving
**Solution:**
1. Check webhook URL in Twilio dashboard
2. Verify `/api/whatsapp/webhook` is accessible
3. Check backend logs for errors
4. Verify phone number format (whatsapp:+1234567890)

### Issue: Webhook not responding
**Solution:**
1. Verify backend running on port 8001
2. Check firewall allows port 8001
3. Verify webhook URL is correct
4. Test with: http://localhost:8001/api/whatsapp/webhook

### Issue: Session not persisting
**Solution:**
1. Sessions are in-memory by default
2. For production, configure Redis:
   - Set WHATSAPP_USE_REDIS=true in .env
   - Install redis-py: pip install redis
   - Configure Redis connection URL

---

## 📈 NEXT STEPS (FUTURE ENHANCEMENTS)

### Phase 5A (Current): Basic Implementation ✅
- [x] Menu-based chatbot
- [x] Form submission via WhatsApp
- [x] Data retrieval
- [x] Simple responses

### Phase 5B (Optional): Advanced Features
- [ ] Interactive buttons (instead of text menu)
- [ ] File attachments (images, PDFs)
- [ ] Location sharing
- [ ] Media messages

### Phase 5C (Optional): Production Features
- [ ] Migrate to Meta WhatsApp Business API
- [ ] Redis session persistence
- [ ] SMS fallback
- [ ] Multi-language support

### Phase 5D (Optional): Notifications
- [ ] SLA breach alerts via WhatsApp
- [ ] Order status updates
- [ ] Maintenance reminders
- [ ] Shift notifications

---

## 📞 SUPPORT & RESOURCES

**Twilio Documentation:**
- WhatsApp API: https://www.twilio.com/docs/whatsapp
- Python SDK: https://www.twilio.com/docs/libraries/python
- Webhook: https://www.twilio.com/docs/whatsapp/tutorial/connect-number-to-webhook

**Barron System:**
- Backend API: http://127.0.0.1:8001/docs
- WhatsApp Module: `app/integrations/whatsapp.py`
- Database: Railway MySQL

---

## ✅ DEPLOYMENT CHECKLIST

### Before Going Live
- [ ] Twilio credentials in production `.env`
- [ ] Webhook URL updated in Twilio dashboard
- [ ] Error logging configured
- [ ] Session persistence (Redis) configured
- [ ] Rate limiting configured
- [ ] Monitoring alerts set up
- [ ] Team trained on WhatsApp workflows

### After Deployment
- [ ] Test all workflows end-to-end
- [ ] Monitor error logs
- [ ] Verify response times < 2 seconds
- [ ] Check session cleanup (no memory leaks)
- [ ] Monitor Twilio API usage
- [ ] Get user feedback

---

**Status: ✅ READY FOR IMPLEMENTATION**

Follow the Quick Start (30 minutes) to get WhatsApp working immediately.

See ACTION_PLAN.md for integration with Phase 1-4.
