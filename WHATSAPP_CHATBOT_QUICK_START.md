---
title: WhatsApp Chatbot Quick Start
---

# ⚡ WhatsApp Chatbot - Quick Start (5 Minutes)

## What You Get

✅ Users message your WhatsApp Business number
✅ Your app automatically responds with intelligent replies
✅ Multi-level menu system (Order status, Defects, Schedule, Help)
✅ Real integration with Meta WhatsApp Business API

## Quick Setup

### 1. Get Meta Credentials (10 mins)
```
1. Go to: https://developers.facebook.com
2. Create App → Choose Business
3. Add WhatsApp product
4. Create/Verify phone number → Copy PHONE_NUMBER_ID
5. Generate System User Token → Copy API_TOKEN
```

### 2. Update .env File (1 min)
```env
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_API_TOKEN=your_api_token
WHATSAPP_WEBHOOK_VERIFY_TOKEN=random_string_32_chars
WHATSAPP_WEBHOOK_URL=https://yourdomain.com/api/whatsapp/webhook
```

### 3. Configure Webhook in Meta (2 mins)
```
1. Meta App Dashboard → WhatsApp → Configuration
2. Webhook URL: https://yourdomain.com/api/whatsapp/webhook
3. Verify Token: (your WHATSAPP_WEBHOOK_VERIFY_TOKEN)
4. Subscribe: messages ✅
5. Save
```

### 4. Restart Backend (1 min)
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Test It!
```
Message your WhatsApp Business number with: "hi"
Wait for automatic response with menu
```

## How It Works

```
User: "hi"
  ↓
[App processes]
  ↓
Bot: "🤖 Welcome to Barron Production System..."
  ↓
User: "1"
  ↓
Bot: "📦 Order Status Menu..."
```

## Menu Options

**Main Menu (type "hi" or "menu")**
- 1️⃣ Check Order Status → See orders, track shipments
- 2️⃣ Report Defect → Submit quality issues  
- 3️⃣ View Schedule → Today/week/production status
- 4️⃣ Get Help → FAQs, support contact
- 5️⃣ Back to Menu

## Key Files

```
app/backend/
  ├── app/services/chatbot_service.py        # Chatbot logic
  ├── app/routes/whatsapp.py                 # Webhook handler
  ├── app/models/whatsapp.py                 # Database models
  └── .env                                   # Credentials

Documentation/
  ├── WHATSAPP_CHATBOT_SETUP.md              # Full guide
  └── WHATSAPP_CHATBOT_QUICK_START.md        # This file
```

## Test Endpoints

### Check if backend is running
```bash
curl http://127.0.0.1:8000/api/whatsapp/health
```

### Get all messages
```bash
curl http://127.0.0.1:8000/api/whatsapp/messages
```

### Get all contacts
```bash
curl http://127.0.0.1:8000/api/whatsapp/contacts
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Webhook not connecting | Verify webhook URL is public HTTPS |
| No auto-response | Check API token and phone number ID |
| Messages not saving | Verify database is running |
| Menu not working | Check .env variables are set |

## Need Help?

See full guide: `WHATSAPP_CHATBOT_SETUP.md`

## Architecture

```
Meta WhatsApp Cloud
       ↓
[Your Public Domain]
       ↓
FastAPI Webhook Handler
       ↓
ChatbotService (processes message)
       ↓
Database (stores conversation)
       ↓
Meta API (sends response)
       ↓
User's WhatsApp App
```

---

**Status: Ready to Deploy! 🚀**
