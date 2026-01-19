---
title: Twilio WhatsApp Setup - Step-by-Step Visual Guide
---

# 📸 Twilio WhatsApp Chatbot - Step-by-Step Visual Guide

**Get your WhatsApp chatbot running in 5 easy steps!**

---

## 🎯 The Big Picture

```
Your Phone                  Twilio Servers              Your Backend
     │                            │                           │
     └──► Send "hi" ──────────►  │                           │
     │                            │                           │
     │                            └─► POST /webhook ──────►  ┌─────────┐
     │                                                        │ Process │
     │                                                        │ Message │
     │                            ┌──────────────────────────┤ Generate│
     │                            │                          │ Response│
     │                            │                          └─────────┘
     │◄────── Reply ◄──────────────┘                           │
     │      (via Twilio)                                       │
     │                                                         ✅ Logged
```

---

## 📋 Prerequisites

### Do You Have?
- ✅ A phone number
- ✅ Internet connection
- ✅ Python 3.8+ installed
- ✅ Existing backend code

### You'll Get
- ✅ Twilio account (free $15 credit)
- ✅ WhatsApp Business Account (linked to Twilio)
- ✅ Twilio WhatsApp number

---

## 🔐 STEP 1: Create Twilio Account (2 minutes)

### 1.1 Go to Twilio Website
```
Visit: https://www.twilio.com/try-twilio
```

### 1.2 Sign Up
```
┌─────────────────────────────────┐
│  Full Name                      │
│  Email                          │
│  Password                       │
│                                 │
│  [ Sign Up ]                    │
└─────────────────────────────────┘
```

### 1.3 Verify Email
```
Check your email → Click verification link
```

### 1.4 Verify Phone
```
Enter your phone number
Receive code via SMS
Enter code
```

### What You Get
```
✅ Account created
✅ $15 free credit
✅ Ready to use
```

---

## 🔑 STEP 2: Get Credentials (1 minute)

### 2.1 Go to Console
```
Visit: https://console.twilio.com
```

### 2.2 Copy Account SID

```
┌─ Twilio Console ─────────────────────────┐
│                                          │
│  Account                                 │
│  ├─ Account SID:  ACxxxxxxxxxxxxxxxx    │ ◄── COPY THIS
│  ├─ Auth Token:   your_token_here       │ ◄── COPY THIS
│                                          │
└──────────────────────────────────────────┘
```

**Save these values:**
```
Account SID: AC...
Auth Token: ...
```

### 2.3 Get WhatsApp Number

```
Click: Messaging → WhatsApp

Select: Sandbox (for testing)

You get: whatsapp:+1234567890

COPY THIS!
```

---

## 📝 STEP 3: Create `.env` File (1 minute)

### 3.1 Open Text Editor
```
Windows: Notepad
Mac: TextEdit
Linux: nano, vim
```

### 3.2 Type Credentials
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
DATABASE_URL=sqlite:///./test.db
```

### 3.3 Save File
```
Location: app/backend/.env
Name: .env (exactly this, no extension)
```

### 3.4 Directory Structure
```
app/
├── backend/
│   ├── .env ◄────── Your new file here
│   ├── app/
│   │   ├── services/
│   │   │   └── chatbot_service.py (updated)
│   │   ├── routes/
│   │   │   └── whatsapp.py (updated)
│   │   └── models/
│   │       └── whatsapp.py
│   └── requirements.txt
└── ...
```

---

## 📦 STEP 4: Install Twilio (1 minute)

### 4.1 Open Terminal/Command Prompt

```bash
# Windows
cmd

# Mac
Terminal

# Linux
Terminal
```

### 4.2 Navigate to Backend Directory

```bash
# Windows
cd "c:\Users\YourName\OneDrive - Barron (Pty) Ltd\Desktop\th\app\backend"

# Mac/Linux
cd ~/Desktop/th/app/backend
```

### 4.3 Install Twilio

```bash
pip install twilio
```

**Expected output:**
```
Successfully installed twilio-8.0.0
```

### 4.4 Verify Installation

```bash
python -c "from twilio.rest import Client; print('✅ Twilio installed!')"
```

---

## 🚀 STEP 5: Start Backend (1 minute)

### 5.1 In Same Terminal

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 5.2 Expected Output

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 5.3 Check it's Running

```
Visit: http://localhost:8000/docs

You should see Swagger UI with all API endpoints
```

---

## ✅ BONUS: Test It! (1 minute)

### 6.1 Open WhatsApp on Your Phone

### 6.2 Start Conversation with Twilio Number

```
Your Twilio WhatsApp Number:
whatsapp:+1234567890

(You can find this in Twilio Console → Messaging → WhatsApp)
```

### 6.3 Send Message

```
You type: "hi"

Twilio: "hi"
  ↓ (sent to your backend)
Backend: Processes message
  ↓ (generates response)
Twilio: Sends back response
  ↓
You receive: "Welcome to Barron Production System! Select 1-5"
```

### 6.4 Test Menu Navigation

```
You: "1"
Bot: "Order Status Menu..."

You: "2"  
Bot: "Report Defect Menu..."

You: "5"
Bot: "Back to Menu"
```

### Success! 🎉
```
✅ Message received
✅ Bot responded
✅ Menu working
✅ WhatsApp chatbot is LIVE!
```

---

## 📊 What Happens Behind the Scenes

```
SEND MESSAGE
    │
    ├─► Twilio receives message
    │
    ├─► Sends POST request to your backend
    │   URL: http://localhost:8000/api/whatsapp/webhook
    │   Body: message details
    │
    ├─► Your backend processes it
    │   ├─ Checks who sent it
    │   ├─ Reads the message
    │   ├─ Generates response
    │   └─ Saves to database
    │
    ├─► Backend calls Twilio API
    │   ├─ Creates Twilio client
    │   ├─ Sends response message
    │   └─ Returns success
    │
    └─► User sees response in WhatsApp
```

---

## 🧪 Quick Test Scenarios

### Scenario 1: Main Menu
```
You: "hi"
Bot: "Welcome! Select 1-5"
Status: ✅ WORKING
```

### Scenario 2: Defect Report
```
You: "2"
Bot: "Report Defect Menu..."

You: "1"
Bot: "Please describe the defect:"

You: "Screen is broken"
Bot: "✅ Defect Submitted! Report ID: DEF-20250119..."
Status: ✅ WORKING
```

### Scenario 3: View Submissions
```
You: "2"
Bot: "Report Defect Menu..."

You: "2"
Bot: "Your Defect Reports:
      1. ID: DEF-20250119143022
         Screen is broken...
         Date: 2025-01-19"
Status: ✅ WORKING
```

---

## 📍 Troubleshooting Quick Reference

### Issue: Backend won't start
```
Error: ModuleNotFoundError: No module named 'twilio'
Solution: pip install twilio
```

### Issue: No .env file error
```
Error: Missing Twilio credentials
Solution: 
  1. Create .env file in app/backend/
  2. Add credentials
  3. Restart terminal
```

### Issue: Message not sending
```
Error: Failed to send message
Solution:
  1. Check phone number format (whatsapp:+27...)
  2. Verify in Twilio console
  3. Check account has credit
```

### Issue: No response received
```
Error: Webhook not getting messages
Solution:
  1. Verify webhook URL in Twilio console
  2. Use ngrok for local: ngrok http 8000
  3. Update webhook URL in Twilio
```

---

## 📱 Using Twilio Sandbox

### Sandbox vs Production

**Sandbox (Free):**
- ✅ Get started immediately
- ✅ $15 credit included
- ⚠️ Only message verified numbers
- ⚠️ Not for production

**Production:**
- ✅ Message any number
- ✅ Professional support
- ✅ Advanced features
- ❌ Costs money

### Verify Your Number for Sandbox

```
1. Go to Twilio Console
2. Messaging → WhatsApp → Sandbox Settings
3. Find "Joined" option
4. Send "join CODE" to Twilio WhatsApp number
5. You receive confirmation
6. Now you can test!
```

---

## 🔄 Flow Diagram

```
TWILIO CONSOLE
    │
    ├─ Account SID
    ├─ Auth Token  
    ├─ WhatsApp Number (sandbox)
    └─ Webhook Settings
    
            │
            ├─────────────┐
            │             │
            ▼             ▼
        .env FILE    YOUR BACKEND
            │             │
            │ loads        │
            │             ├─ /api/whatsapp/webhook
            │             │
            │             ├─ chatbot_service.py
            │             │  └─ send_via_twilio_api()
            │             │
            │             └─ database
            │                └─ stores messages
            │
        YOUR PHONE
            │
            ├─ Send message
            │
            ├─ Twilio processes
            │
            ├─ Backend responds
            │
            └─ You receive reply
```

---

## ✨ Next Steps After Getting Started

### Short Term
1. ✅ Test all menu options (1-5)
2. ✅ Test form submission
3. ✅ Test form retrieval
4. ✅ Check database for stored data

### Medium Term
1. Deploy to production server
2. Update webhook URL in Twilio
3. Test with multiple users
4. Monitor costs

### Long Term
1. Add new form types
2. Create admin dashboard
3. Integrate with other systems
4. Scale based on usage

---

## 📚 Full Documentation

After this quick start, read:

1. **[WHATSAPP_TWILIO_SETUP.md](WHATSAPP_TWILIO_SETUP.md)** - Complete guide
2. **[WHATSAPP_CHATBOT_FORMS_GUIDE.md](WHATSAPP_CHATBOT_FORMS_GUIDE.md)** - Form features
3. **[WHATSAPP_MIGRATION_META_TO_TWILIO.md](WHATSAPP_MIGRATION_META_TO_TWILIO.md)** - Technical details

---

## ✅ Success Checklist

After 5 minutes, you should have:

- [ ] Twilio account created
- [ ] Credentials copied
- [ ] `.env` file created with credentials
- [ ] Twilio package installed
- [ ] Backend started successfully
- [ ] Message received and response sent
- [ ] Menu navigation working
- [ ] Database has stored messages

---

## 🎉 Congratulations!

Your WhatsApp chatbot is now running with Twilio!

**You've accomplished:**
- ✅ Set up Twilio account
- ✅ Got credentials
- ✅ Configured environment
- ✅ Installed dependencies
- ✅ Started backend
- ✅ Tested with WhatsApp

**Next:** Test all features and deploy to production!

---

**Ready to chat? Send that first message! 🚀**
