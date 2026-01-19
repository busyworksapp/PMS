---
title: Twilio WhatsApp Chatbot - 5 Minute Quick Start
---

# ⚡ Twilio WhatsApp Chatbot - 5 Minute Quick Start

**Get your WhatsApp chatbot running with Twilio in 5 minutes!**

---

## ✅ Prerequisites (Must Have)

- ✅ Twilio Account (free at https://twilio.com)
- ✅ Your phone number verified in Twilio
- ✅ Python backend running (or ready to start)

---

## 🔐 Step 1: Get Twilio Credentials (1 min)

1. Go to https://console.twilio.com
2. Copy your **Account SID** (starts with `AC...`)
3. Copy your **Auth Token** (long random string)
4. Go to **Messaging → WhatsApp** and get your **Twilio WhatsApp Number** (e.g., `whatsapp:+1234567890`)

---

## 📝 Step 2: Set Environment Variables (1 min)

Create or update `.env` file in your backend folder:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
```

**Windows:** Create `.env` file in `app/backend/` folder  
**Mac/Linux:** `nano .env` and paste above

---

## 📦 Step 3: Install Twilio (1 min)

```bash
# In your backend directory
pip install twilio
```

Done! ✅

---

## 🚀 Step 4: Start Your Backend (1 min)

```bash
cd app/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 🧪 Step 5: Test It (1 min)

Send a WhatsApp message from your phone:

```
User: hi
Bot: Welcome! Select 1-5

User: 2
Bot: Report Defect menu

User: 1
Bot: Please describe the defect

User: Screen is cracked
Bot: ✅ Defect Submitted! ID: DEF-20250119143022
```

---

## ✅ Done! 🎉

Your chatbot is now:
- ✅ Running on Twilio
- ✅ Responding to WhatsApp messages
- ✅ Storing forms in database

---

## 📞 Need Help?

| Issue | Solution |
|-------|----------|
| Message not received | Check `.env` file has correct credentials |
| Error: Missing credentials | Reload terminal after editing `.env` |
| Message not sending | Verify phone number in Twilio (trial account limits) |

---

## 📚 Next Steps

1. **See full guide:** `WHATSAPP_TWILIO_SETUP.md`
2. **Test with ngrok:** For public webhook testing
3. **Deploy to production:** Update webhook URL in Twilio
4. **Add more forms:** Follow pattern in `WHATSAPP_CHATBOT_FORMS_GUIDE.md`

**Enjoy! 🚀**
