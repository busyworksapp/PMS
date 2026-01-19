---
title: WhatsApp Chatbot with Twilio - Complete Setup Guide
---

# 🚀 WhatsApp Chatbot with Twilio - Complete Setup Guide

## ✅ What You're Getting

**Real WhatsApp Integration Using Twilio**
- ✅ Users message your WhatsApp number
- ✅ Auto-responses via Twilio API (not mock)
- ✅ Full form submission (defects, feedback, etc.)
- ✅ Database storage of all interactions
- ✅ Production-ready code

---

## 📋 Prerequisites

Before starting, you need:

1. **Twilio Account** (free trial available at https://www.twilio.com)
2. **WhatsApp Business Account** (linked to Twilio)
3. **Python 3.8+** installed
4. **Existing FastAPI backend** running on port 8000

---

## 🔐 Step 1: Set Up Twilio Account

### 1.1 Create Twilio Account
1. Go to https://www.twilio.com/try-twilio
2. Sign up for a free account (includes $15 credit)
3. Verify your phone number

### 1.2 Get Twilio Credentials

1. Go to **Twilio Console** (https://console.twilio.com)
2. Find your **Account SID** and **Auth Token**
3. Copy both values (keep them secret!)

```
Account SID: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Auth Token: your_auth_token_here
```

### 1.3 Enable WhatsApp in Twilio

1. In Twilio Console, go to **Messaging → Channels → WhatsApp**
2. Click "Get Started"
3. Complete WhatsApp Business Account setup
4. Get your **Twilio WhatsApp Number** (e.g., `whatsapp:+1234567890`)

⚠️ **Note:** Trial accounts can only message verified numbers. Premium accounts can message any number.

---

## 🔧 Step 2: Update Environment Variables

### 2.1 Create/Update `.env` file

In your backend directory, add these variables:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890

# Your WhatsApp Number (for testing)
YOUR_WHATSAPP_NUMBER=whatsapp:+27123456789

# FastAPI Config
DATABASE_URL=sqlite:///./test.db
ENVIRONMENT=development
```

### 2.2 Verify Environment Variables

Run this to check they're loaded correctly:

```bash
# In your backend directory
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('ACCOUNT_SID:', os.getenv('TWILIO_ACCOUNT_SID')[:10] + '...')"
```

---

## 📦 Step 3: Install Twilio Package

### 3.1 Install via pip

```bash
# In your backend directory
pip install twilio
```

### 3.2 Verify Installation

```bash
python -c "from twilio.rest import Client; print('Twilio installed successfully!')"
```

### 3.3 Update requirements.txt

If you have a `requirements.txt`, add:

```
twilio>=8.0.0
```

Then install:

```bash
pip install -r requirements.txt
```

---

## 🔄 Step 4: Webhook Configuration

### 4.1 Understanding Webhooks

When someone sends a WhatsApp message to your Twilio number:

```
User's WhatsApp → Twilio Servers → Your FastAPI Webhook → Process & Respond
```

### 4.2 Set Webhook URL in Twilio

1. Go to **Twilio Console → Messaging → Settings → WhatsApp Sandbox**
2. Find "When a message comes in" webhook
3. Set URL to: `https://yourdomain.com/api/whatsapp/webhook`
4. Click "Save"

**For Local Development:**
- Use **ngrok** to expose local server to internet

```bash
# In a new terminal
ngrok http 8000

# You'll get a URL like: https://abc123.ngrok.io
# Set Twilio webhook to: https://abc123.ngrok.io/api/whatsapp/webhook
```

### 4.3 Test Webhook Connection

Send a test message:

```bash
curl -X POST http://localhost:8000/api/whatsapp/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "SmsMessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "NumMedia": "0",
    "ProfileName": "Test User",
    "SmsSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "WaId": "27123456789",
    "SmsStatus": "received",
    "Body": "Hi from WhatsApp",
    "To": "whatsapp:+1234567890",
    "NumSegments": "1",
    "ReferralNumMedia": "0",
    "MessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "AccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "From": "whatsapp:+27123456789",
    "SmsDate": "2025-01-19"
  }'
```

---

## ✨ Step 5: Code Changes (Already Done)

The chatbot service has been updated:

### 5.1 Import Changed

**Before (Meta API):**
```python
import httpx
```

**After (Twilio):**
```python
from twilio.rest import Client
```

### 5.2 Method Renamed

**Before:**
```python
async def send_via_meta_api(self, phone_number, message_text)
```

**After:**
```python
async def send_via_twilio_api(self, phone_number, message_text)
```

### 5.3 Implementation Changed

**Twilio method (new):**
```python
async def send_via_twilio_api(self, phone_number: str, message_text: str) -> bool:
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

        if not phone_number.startswith("whatsapp:"):
            phone_number = f"whatsapp:{phone_number}"

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_text,
            from_=twilio_whatsapp_number,
            to=phone_number,
        )

        logger.info(f"Message sent via Twilio: SID={message.sid}")
        return True

    except Exception as e:
        logger.error(f"Error sending via Twilio: {str(e)}")
        return False
```

### 5.4 Routes Updated

All calls from `send_via_meta_api` → `send_via_twilio_api` (automatically done)

---

## 🚀 Step 6: Start the Backend

### 6.1 Activate Virtual Environment (if using one)

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 6.2 Start FastAPI Server

```bash
cd app/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 6.3 Verify API is Running

```bash
curl http://localhost:8000/docs
```

Should open Swagger UI at `http://localhost:8000/docs`

---

## 🧪 Step 7: Test the Chatbot

### 7.1 Send Test Message

Using your **verified WhatsApp number**, send a message to your **Twilio WhatsApp number**:

```
User sends: "hi"
Bot responds: "Welcome to Barron Production System! Select 1-5..."
```

### 7.2 Test Menu Navigation

```
User: "hi"
Bot: Welcome menu

User: "1"
Bot: Order status menu

User: "back" or "5"
Bot: Back to main menu
```

### 7.3 Test Form Submission

```
User: "2" (Report Defect)
Bot: Defect menu

User: "1" (Report a defect)
Bot: "Please describe the defect:"

User: "Surface has scratches and paint peeling"
Bot: "✅ Defect Report Submitted! Report ID: DEF-20250119143022"

User: "2" (View defect history)
Bot: Shows all submitted defects
```

---

## 🔍 Step 8: Debug & Monitor

### 8.1 Check Twilio Console Logs

1. Go to **Twilio Console**
2. **Logs → WhatsApp** to see message history
3. Check status of each message (delivered, failed, etc.)

### 8.2 Check FastAPI Logs

In your terminal running FastAPI:

```
INFO:     127.0.0.1:59402 "POST /api/whatsapp/webhook HTTP/1.1" 200 OK
INFO:app.services.chatbot_service:Message processed for +27123456789
INFO:app.services.chatbot_service:Message sent via Twilio: SID=SMxxxxxxx
```

### 8.3 Common Issues

**Issue: "Missing Twilio credentials"**
- ✅ Check `.env` file exists
- ✅ Reload terminal after editing `.env`
- ✅ Use `python -c "import os; print(os.getenv('TWILIO_ACCOUNT_SID'))"`

**Issue: "Message failed to send"**
- ✅ Check phone number format (should be `whatsapp:+27123456789`)
- ✅ Verify number is whitelisted in Twilio console (trial accounts)
- ✅ Check Twilio account has credit

**Issue: "Webhook not receiving messages"**
- ✅ Check webhook URL in Twilio console
- ✅ Ensure ngrok is running (for local development)
- ✅ Check firewall/network settings

---

## 📊 Step 9: Database & Storage

### 9.1 Check Submitted Forms

```bash
# In your backend directory
python -c "
from app.db.database import SessionLocal
from app.models.whatsapp import WhatsAppMessage

db = SessionLocal()
messages = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.status == 'submitted'
).all()

for msg in messages:
    print(f'ID: {msg.message_id}')
    print(f'Phone: {msg.from_phone_number}')
    print(f'Message: {msg.message_text}')
    print(f'Date: {msg.sent_at}')
    print('---')
"
```

### 9.2 View Database File

SQLite database is stored at:
```
app/backend/test.db
```

You can view it with:
```bash
# Install sqlite3 tools
pip install sqlite3

# Or use a GUI tool like DB Browser for SQLite
```

---

## 🌐 Step 10: Deploy to Production

### 10.1 Update Environment Variables

On your production server:

```bash
export TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export TWILIO_AUTH_TOKEN=your_auth_token_here
export TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
export DATABASE_URL=postgresql://...  # Use PostgreSQL in production
```

### 10.2 Update Webhook URL

1. Go to **Twilio Console → WhatsApp Settings**
2. Change webhook URL from ngrok to your production domain:
   ```
   https://yourdomain.com/api/whatsapp/webhook
   ```

### 10.3 Use Production Database

Replace SQLite with PostgreSQL:

```bash
pip install psycopg2-binary
```

Update `DATABASE_URL`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/barron_db
```

### 10.4 Deploy FastAPI

Using **Gunicorn** with **Uvicorn**:

```bash
pip install gunicorn

gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  app.main:app --bind 0.0.0.0:8000
```

Or use **Docker**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
```

---

## 📞 Comparison: Twilio vs Meta API

| Feature | Twilio | Meta API |
|---------|--------|----------|
| **Setup Time** | 5-10 minutes | 30+ minutes |
| **Trial Account** | Yes ($15 credit) | Limited |
| **Message Sending** | Simple SDK | Complex HTTP requests |
| **Cost** | $0.007 per message | Variable |
| **Support** | Excellent | Good |
| **Webhook Verification** | Built-in | Manual |
| **Scalability** | High | High |
| **Documentation** | Very good | Good |

---

## 🎯 Key Features Now Available

### ✅ User Interactions
- Users send WhatsApp message to your Twilio number
- Bot responds automatically with menu
- Users navigate via numbered replies (1-5)

### ✅ Form Submissions
- Users submit defect reports
- Unique IDs generated automatically
- Data stored in database
- Users can retrieve their submissions

### ✅ Auto-Response
- Messages processed in real-time
- Replies sent via Twilio API
- Logged and tracked

### ✅ Database Integration
- All messages stored
- User conversation history
- Form submission tracking
- Analytics ready

---

## 🚀 Next Steps

1. **Test locally** with ngrok
2. **Verify WhatsApp connection** in Twilio console
3. **Submit test forms** via WhatsApp
4. **Monitor logs** for any errors
5. **Deploy to production** when ready

---

## 📚 Useful Resources

- **Twilio Docs:** https://www.twilio.com/docs/whatsapp
- **Twilio WhatsApp API:** https://www.twilio.com/docs/whatsapp/api
- **Twilio Python SDK:** https://www.twilio.com/docs/python/install
- **Ngrok:** https://ngrok.com/ (for local testing)

---

## 💬 Support

If you encounter issues:

1. Check **Twilio Console → Logs** for message delivery status
2. Check **FastAPI console** for error messages
3. Verify `.env` variables are loaded
4. Ensure webhook URL is correct in Twilio
5. Test with curl/Postman to isolate issues

---

## ✅ You're Ready!

Your WhatsApp chatbot with Twilio is now:
- ✅ Integrated with Twilio API
- ✅ Processing messages in real-time
- ✅ Storing forms in database
- ✅ Sending auto-responses
- ✅ Ready to deploy

**Happy chatting! 🚀**
