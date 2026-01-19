---
title: WhatsApp Chatbot Setup Guide (Meta API Integration)
date: 2025-01-18
---

# 🚀 WhatsApp Chatbot Setup - Complete Integration Guide

## Overview

Your app now includes a **fully integrated WhatsApp chatbot** that:
- ✅ Receives messages from users on WhatsApp
- ✅ Automatically processes messages and generates intelligent responses
- ✅ Sends real replies back via Meta's WhatsApp Business API
- ✅ Maintains conversation context (menu navigation)
- ✅ Works with a multi-level menu system

**How it works:**
```
User sends "Hi" on WhatsApp
    ↓
Meta sends webhook to your app
    ↓
Chatbot processes message
    ↓
Chatbot generates response
    ↓
App sends reply back via Meta API
    ↓
User receives response on WhatsApp
```

---

## Step 1: Setup Meta WhatsApp Business Account

### 1.1 Create Meta Business Account
1. Go to [facebook.com/business](https://facebook.com/business)
2. Click "Create Account"
3. Fill in your business details
4. Verify your email

### 1.2 Get WhatsApp Business API Access
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Navigate to "Apps" → Create App
3. Choose "Business" as app type
4. Add "WhatsApp" as a product
5. Accept terms and conditions

### 1.3 Create a Phone Number
1. In your Meta app dashboard, go to "WhatsApp"
2. Click "Get Started"
3. Choose "Get a new number" OR "Use existing number"
4. Verify your phone number with an SMS code
5. Note your **Phone Number ID** (you'll need this)

---

## Step 2: Generate API Token

### 2.1 Create System User Token
1. Go to [business.facebook.com](https://business.facebook.com)
2. Navigate to Settings → Users and Permissions
3. Click "Admins"
4. Click "Create Accounts"
5. Create a new System User
6. Generate a token (this is your **API Token**)
7. Save the token securely

**Store this securely - you'll need it!**

---

## Step 3: Configure Your App

### 3.1 Update .env File

Create or update `.env` file in your project root:

```env
# WhatsApp Configuration (Meta Cloud API)
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
WHATSAPP_API_TOKEN=your_api_token_here
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_random_webhook_token_here
WHATSAPP_WEBHOOK_URL=https://yourdomain.com/api/whatsapp/webhook
```

**Important:**
- `WHATSAPP_PHONE_NUMBER_ID`: The ID of your WhatsApp phone number (from Step 1.3)
- `WHATSAPP_API_TOKEN`: The system user token (from Step 2.1)
- `WHATSAPP_WEBHOOK_VERIFY_TOKEN`: Generate a random string (e.g., `abc123xyz789`)
- `WHATSAPP_WEBHOOK_URL`: Your public webhook URL

### 3.2 Generate Random Webhook Token
In PowerShell:
```powershell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})
```

---

## Step 4: Setup Webhook (Meta Dashboard)

### 4.1 Configure Webhook URL
1. Go to your Meta App Dashboard
2. Navigate to WhatsApp → Configuration
3. Find "Webhook URL" section
4. Enter: `https://yourdomain.com/api/whatsapp/webhook`
5. Enter your webhook verify token (from Step 3.1)
6. Click "Verify and Save"

### 4.2 Subscribe to Messages
1. Still in Webhook settings
2. Under "Webhook fields", select:
   - ✅ messages
   - ✅ message_template_status_update
   - ✅ message_template_quality_update
3. Save changes

### 4.3 Test Connection
Meta will send a verification request to your webhook:
- Your app should respond with status code `200`
- The webhook handler automatically verifies the token
- Check your logs: `Application startup complete`

---

## Step 5: Testing the Chatbot

### 5.1 Start Your App

**Terminal 1 - Backend:**
```powershell
cd "c:\path\to\app\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```powershell
cd "c:\path\to\app\frontend"
python -m http.server 8080
```

### 5.2 Test with Real WhatsApp (Production)

1. **Add your app to your Meta Business**
   - Go to App Dashboard → Settings → Basic
   - Note your App ID and App Secret

2. **Test using WhatsApp Tester**
   - Go to Meta App Dashboard → WhatsApp → API Setup
   - Click "Send Test Message"
   - Send to your phone number

3. **Test with real contacts**
   - Have someone message your WhatsApp Business number
   - Your app will automatically respond!

### 5.3 Expected Conversation Flow

**User sends:** `hi`
**Bot responds:**
```
🤖 *Welcome to Barron Production System*

Select an option:
1️⃣ Check Order Status
2️⃣ Report Defect
3️⃣ View Production Schedule
4️⃣ Get Help
5️⃣ Back to Menu

*Just reply with the number!*
```

**User sends:** `1`
**Bot responds:**
```
📦 *Order Status Menu*

What would you like to do?
1️⃣ Check your orders
2️⃣ Track specific order
3️⃣ Check estimated delivery
4️⃣ Back to Menu

Reply with the number
```

**User sends:** `1`
**Bot responds:**
```
📦 *Your Recent Orders*

ORD-001: In Production (Est. 5 days)
ORD-002: Quality Check (Est. 2 days)
ORD-003: Completed ✅

Reply with order number to track
```

---

## Menu Structure

```
Main Menu (typing "hi" or "menu")
├── 1: Order Status
│   ├── 1: View recent orders
│   ├── 2: Track specific order
│   ├── 3: Check delivery dates
│   └── 4: Back
├── 2: Report Defect
│   ├── 1: Report new defect
│   ├── 2: View defect history
│   ├── 3: Track resolution
│   └── 4: Back
├── 3: Production Schedule
│   ├── 1: Today's schedule
│   ├── 2: This week's schedule
│   ├── 3: Production status
│   └── 4: Back
├── 4: Help & Support
│   ├── 1: FAQs
│   ├── 2: Contact support
│   ├── 3: Report issue
│   └── 4: Back
└── 5: Back to Menu
```

---

## API Endpoints

### Webhook Endpoint
**POST** `/api/whatsapp/webhook`
- Receives messages from Meta
- Auto-responds to incoming messages
- Returns: `{ "success": true, "message": "Webhook processed successfully" }`

### Send Message Endpoint
**POST** `/api/whatsapp/send`
```json
{
  "phone_number": "+1234567890",
  "message": "Hello!"
}
```

### Get Messages Endpoint
**GET** `/api/whatsapp/messages?phone_number=+1234567890`
- Returns conversation history

### Get Contacts Endpoint
**GET** `/api/whatsapp/contacts`
- Returns all contacts who messaged your business

---

## Troubleshooting

### Issue: Webhook Not Connecting
**Solution:**
1. Verify `WHATSAPP_WEBHOOK_URL` is publicly accessible
2. Check firewall/port 443 is open
3. Verify webhook token matches in Meta dashboard
4. Check app logs: `GET /api/whatsapp/webhook?hub.verify_token=...`

### Issue: Messages Not Sending
**Solution:**
1. Verify API token in `.env` is correct
2. Check phone number format includes country code (e.g., +27...)
3. Ensure webhook receives messages (check logs)
4. Verify meta business account has active WhatsApp access

### Issue: Auto-Response Not Working
**Solution:**
1. Check logs for `Auto-response sent to` message
2. Verify `WHATSAPP_PHONE_NUMBER_ID` is correct
3. Ensure webhook verification passed
4. Check Meta dashboard for any errors/warnings

### Debug Mode
Add to your `.env`:
```env
LOG_LEVEL=DEBUG
```

Then restart backend and check detailed logs.

---

## Production Deployment

### Before Going Live:

1. **Replace localhost with public domain**
   ```env
   WHATSAPP_WEBHOOK_URL=https://yourdomain.com/api/whatsapp/webhook
   ```

2. **Use HTTPS only**
   - Meta requires HTTPS for webhooks
   - Use SSL certificate (Let's Encrypt is free)

3. **Rate limiting**
   - Meta may rate-limit requests
   - Implement queue system for high volume
   - See `WhatsAppQueue` model in database

4. **Business Verification**
   - Meta requires business verification
   - Go to Meta Business → Security Center
   - Verify your business details

5. **Message Templates**
   - For promotional messages, use approved templates
   - Pre-approved templates have higher delivery rate
   - Create in Meta Dashboard → WhatsApp → Message Templates

---

## Code Structure

### Chatbot Service (`app/services/chatbot_service.py`)
- **Class:** `ChatbotService`
- **Methods:**
  - `process_message()` - Main message processor
  - `send_via_meta_api()` - Sends reply via Meta API
  - `get_user_state()` - Gets conversation context
  - `set_user_state()` - Updates conversation state
  - Menu handlers for each section

### WhatsApp Routes (`app/routes/whatsapp.py`)
- **Webhook Handler:** POST `/api/whatsapp/webhook`
  - Verifies signature
  - Calls chatbot service
  - Auto-responds to messages

### Database Models (`app/models/whatsapp.py`)
- `WhatsAppMessage` - Stores all messages
- `WhatsAppContact` - Stores contact info
- `WhatsAppWebhook` - Stores webhook events
- `WhatsAppSession` - Stores conversation state

---

## Advanced: Customizing Responses

### Modify Menu Options
Edit `app/services/chatbot_service.py`:

```python
MAIN_MENU = """🤖 *Your Custom Menu*

Select an option:
1️⃣ Custom Option 1
2️⃣ Custom Option 2
...
"""
```

### Add New Menu Branches
Add a new method to `ChatbotService`:

```python
def _handle_custom_menu(self, message_text: str, phone_number: str, db: Session):
    if message_text == "1":
        return "Your custom response", None
    ...
```

Then add to `process_message()`:
```python
if current_state == "custom_menu":
    return self._handle_custom_menu(message_text, phone_number, db)
```

### Connect to Database
Access database queries in handlers:
```python
from app.models import Order, Contact
orders = db.query(Order).filter(...).all()
```

---

## Support

For issues or questions:
1. Check logs: `tail -f backend.log`
2. Verify Meta credentials in `.env`
3. Test webhook: `curl https://yourdomain.com/api/whatsapp/webhook`
4. Check Meta Dashboard for warnings/errors

---

## Next Steps

✅ Complete this setup guide
✅ Get Meta credentials
✅ Configure webhook in Meta Dashboard
✅ Test with real messages
✅ Customize menu structure
✅ Connect to your database

🎉 **Your WhatsApp chatbot is now live!**
