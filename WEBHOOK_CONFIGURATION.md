# 🔗 Twilio WhatsApp Webhook Configuration Guide

## Current Status

You've tested the Twilio WhatsApp sandbox and received:
```
You said: Hi
Configure your WhatsApp Sandbox's Inbound URL to change this message.
```

This is the **default sandbox response** - it means the webhook is not yet configured to point to your Barron PMS application.

## What You Need to Do

### Step 1: Get Your Public URL

Since you're developing locally, you need to expose your local server to the internet using **ngrok** (free tunneling service).

#### Install ngrok:
1. Download from: https://ngrok.com/download
2. Extract to a folder
3. Create ngrok account (free)

#### Start ngrok tunnel:
```bash
# Open a new terminal/PowerShell and run:
./ngrok http 8000

# You'll see output like:
# Session Status    online
# Session Expires   1 hours 59 minutes 31 seconds
# Forwarding        https://xxxx-xx-xxx-xxx-xx.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://xxxx-xx-xxx-xxx-xx.ngrok.io`)

### Step 2: Configure Twilio Webhook

1. Go to **Twilio Console**: https://www.twilio.com/console
2. Navigate to: **Messaging → WhatsApp → Settings**
3. Find the section: **"When a message comes in"**
4. In the **Webhook URL** field, enter:
   ```
   https://your-ngrok-url/api/whatsapp/twilio-webhook
   ```
   
   Example:
   ```
   https://xxxx-xx-xxx-xxx-xx.ngrok.io/api/whatsapp/twilio-webhook
   ```

5. Keep the method as **HTTP POST**
6. Click **Save**

### Step 3: Start Your Backend

```bash
cd app/backend
python run_server.py
```

Or manually with uvicorn:
```bash
cd app/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Waiting for application startup.
INFO:app.main:Creating database tables...
INFO:app.main:Database tables created successfully
INFO:app.main:✓ WhatsApp routes imported
```

### Step 4: Test the Webhook

Send a WhatsApp message to your Twilio sandbox number (e.g., **+1 415-523-8886**) with the text:
```
join green-tea
```

Then send:
```
Hi from Barron PMS!
```

**Expected Response:**
- Your message should be logged in the application
- The message should be stored in the database
- You should get an **auto-response** from the chatbot

### Step 5: Verify in Database

```bash
# Check if messages were stored
sqlite3 app.db "SELECT * FROM whatsapp_messages;" 2>/dev/null || echo "Check your MySQL database"
```

## Complete Setup Flow

```
┌─────────────┐
│ Your Phone  │  (1) Send WhatsApp message
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  Twilio WhatsApp        │  (2) Receives message
│  (Your Sandbox)         │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  Twilio Cloud           │  (3) Sends to webhook
│  (Processing)           │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  ngrok Tunnel                       │  (4) Forwards to localhost
│  https://xxx.ngrok.io               │
└──────┬──────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  Your Local Backend                      │  (5) Receives webhook
│  localhost:8000                          │
│  /api/whatsapp/twilio-webhook            │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  Chatbot Service                         │  (6) Processes message
│  (Auto-response logic)                   │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  Database                                │  (7) Stores message
│  (WhatsAppMessage table)                 │
└──────┬───────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────┐
│  Send Response Message                          │  (8) Sends reply
│  via Twilio                                     │
└──────┬────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│ Your Phone  │  (9) Receive response
└─────────────┘
```

## Troubleshooting

### Issue: "Webhook not being called"
**Solutions:**
1. Verify ngrok is running and showing the tunnel
2. Double-check the webhook URL in Twilio console (exact match)
3. Check the backend logs for errors
4. Make sure backend is running on port 8000

### Issue: "403 Forbidden" error
**Solution:**
Webhook signature verification might be failing. The application auto-verifies, so ensure:
1. Twilio credentials are correct in `.env`
2. Auth Token matches exactly

### Issue: Messages not storing in database
**Solutions:**
1. Check database connection string in `.env`
2. Verify MySQL is running
3. Check application logs for database errors

### Issue: Auto-response not being sent
**Solutions:**
1. Check chatbot_service is initialized
2. Verify Twilio credits available
3. Check logs for chatbot processing errors

## Configuration Files

### `.env` (Already Configured)
```properties
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155552671
TWILIO_WEBHOOK_VERIFY_TOKEN=BarronPMSWebhookToken2024
```

### Twilio Console Settings
- **Account SID:** [See .env file]
- **Sandbox Number:** +1 415-523-8886
- **Webhook URL:** `https://your-ngrok-url/api/whatsapp/twilio-webhook`
- **HTTP Method:** POST

## Testing Commands

### 1. Test Health Endpoint
```bash
curl http://localhost:8000/api/whatsapp/health
```

Expected response:
```json
{
  "status": "healthy",
  "is_configured": true,
  "provider": "Twilio",
  "message": "Twilio WhatsApp integration ready"
}
```

### 2. Send Test Message Programmatically
```bash
curl -X POST http://localhost:8000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+27123456789",
    "message_text": "Test from Barron PMS",
    "message_type": "text"
  }'
```

### 3. Get Message History
```bash
curl "http://localhost:8000/api/whatsapp/messages?contact_number=%2B27123456789"
```

### 4. List All Contacts
```bash
curl http://localhost:8000/api/whatsapp/contacts
```

## Important Notes

⚠️ **ngrok URL Changes:**
- Free ngrok tunnels expire after **2 hours** of inactivity
- You'll get a new URL each time you restart ngrok
- **Update the webhook URL in Twilio console each time**

✅ **For Production:**
1. Replace ngrok with your actual domain (e.g., api.yourdomain.com)
2. Use HTTPS certificate (Let's Encrypt is free)
3. Update webhook URL to production domain
4. Use production Twilio WhatsApp number (not sandbox)

## Next Steps

1. **Download ngrok** from https://ngrok.com/download
2. **Start ngrok:** `./ngrok http 8000`
3. **Copy the HTTPS URL** from ngrok output
4. **Update Twilio webhook** with ngrok URL
5. **Start backend:** `python run_server.py`
6. **Test by sending WhatsApp message**

## Success Indicators

✅ When everything works:
- You send a message to Twilio sandbox
- Message appears in your backend logs
- Message stored in database
- Auto-response received on your phone
- No errors in application logs

---

**Your Barron PMS is ready to receive and process WhatsApp messages!**

Follow these steps to complete the setup.
