# ⚡ QUICK REFERENCE - Twilio WhatsApp Webhook Setup

## 5-Minute Setup

### Step 1: Download ngrok
https://ngrok.com/download

### Step 2: Start ngrok tunnel
```bash
./ngrok http 8000
```

**Copy this URL:** `https://xxxx-xx-xxx-xxx-xx.ngrok.io`

### Step 3: Configure Twilio Webhook
1. Go to: https://www.twilio.com/console
2. Menu: **Messaging → WhatsApp → Settings**
3. Find: **"When a message comes in"**
4. Paste webhook URL:
   ```
   https://xxxx-xx-xxx-xxx-xx.ngrok.io/api/whatsapp/twilio-webhook
   ```
5. Click **Save**

### Step 4: Start Backend
```bash
cd app/backend
python run_server.py
```

### Step 5: Test
Send WhatsApp message to: **+1 415-523-8886**

---

## Your Credentials

| Item | Value |
|------|-------|
| **Account SID** | AC21e03f1ff3792a2fe49435744505c53e |
| **Auth Token** | 0d2692d716bc761af953a161492d2886 |
| **Sandbox Number** | +1 415-523-8886 |
| **Webhook Endpoint** | `/api/whatsapp/twilio-webhook` |

---

## Testing WhatsApp Messages

### Test Command 1: Check Health
```bash
curl http://localhost:8000/api/whatsapp/health
```

### Test Command 2: Send Message
```bash
curl -X POST http://localhost:8000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+27123456789", "message_text": "Hello", "message_type": "text"}'
```

### Test Command 3: Get Messages
```bash
curl "http://localhost:8000/api/whatsapp/messages?contact_number=%2B27123456789"
```

---

## What Happens When You Send a Message

1. You send WhatsApp to Twilio sandbox
2. Twilio receives message
3. Twilio sends to your webhook URL via ngrok
4. Your backend receives message
5. Message stored in database
6. Chatbot processes and sends response
7. Response sent back via Twilio WhatsApp
8. You receive response on your phone

---

## Common Issues & Quick Fixes

| Problem | Fix |
|---------|-----|
| Webhook not called | Restart ngrok, update URL in Twilio |
| 404 error | Check endpoint path: `/api/whatsapp/twilio-webhook` |
| 403 error | Verify credentials in `.env` file |
| Backend won't start | Run: `pip install -r requirements.txt` |
| Database error | Check MySQL connection in `.env` |

---

## Important: ngrok URL Changes

- Free ngrok expires after **2 hours** inactivity
- New URL each time you restart
- **You must update Twilio webhook URL each time**

### Automated: Use ngrok authtoken
```bash
ngrok authtoken <your-token>
ngrok http 8000 --reserve-domain
```

---

## API Endpoints Ready

- `POST /api/whatsapp/send` - Send message
- `POST /api/whatsapp/send-bulk` - Bulk messaging
- `POST /api/whatsapp/twilio-webhook` - Receive messages
- `GET /api/whatsapp/messages` - Message history
- `GET /api/whatsapp/contacts` - All contacts
- `GET /api/whatsapp/health` - Health check

---

## Production Deployment

When ready for production:
1. Get real domain (e.g., api.barronpms.com)
2. Configure HTTPS/SSL certificate
3. Register production Twilio WhatsApp number
4. Update webhook URL to production domain
5. Redeploy backend to production server

---

**You're all set! Follow the 5-minute setup above to get messages flowing.** ✅
