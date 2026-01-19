---
title: WhatsApp Chatbot - Quick Reference Card
---

# 🚀 WhatsApp Chatbot - Quick Reference Card

**Print this or bookmark it!**

---

## ⚡ 5-Minute Setup

### 1. Get Credentials
- Go to: https://developers.facebook.com
- Create App → WhatsApp
- Create/verify phone number
- Generate System User Token

### 2. Update .env
```env
WHATSAPP_BUSINESS_ACCOUNT_ID=your_id
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_API_TOKEN=your_token
WHATSAPP_WEBHOOK_VERIFY_TOKEN=random_32_chars
WHATSAPP_WEBHOOK_URL=https://yourdomain.com/api/whatsapp/webhook
```

### 3. Configure Meta
- Dashboard → WhatsApp → Configuration
- Webhook URL: your URL
- Verify Token: your token
- Subscribe: messages

### 4. Test
- Send "hi" to your number
- Get auto-response with menu

---

## 🎯 Menu Structure

```
1️⃣ Order Status (check orders, track shipment, delivery dates)
2️⃣ Report Defect (report, view history, track resolution)
3️⃣ Production Schedule (today, this week, status)
4️⃣ Help & Support (FAQs, contact support, report issue)
5️⃣ Back to Menu
```

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/whatsapp/webhook` | POST | Receive messages |
| `/api/whatsapp/send` | POST | Send message |
| `/api/whatsapp/messages` | GET | Get history |
| `/api/whatsapp/contacts` | GET | Get contacts |
| `/api/whatsapp/health` | GET | Check status |

---

## 🧪 Quick Test

**cURL:**
```bash
# Check health
curl http://localhost:8000/api/whatsapp/health

# Get contacts
curl http://localhost:8000/api/whatsapp/contacts

# Get messages
curl "http://localhost:8000/api/whatsapp/messages?phone_number=%2B27123456789"

# Send message
curl -X POST http://localhost:8000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"+27123456789","message":"Hi!"}'
```

**PowerShell:**
```powershell
# Check health
Invoke-WebRequest "http://localhost:8000/api/whatsapp/health"

# Get contacts
Invoke-WebRequest "http://localhost:8000/api/whatsapp/contacts"

# Send message
$body = @{phone_number="+27123456789";message="Hi!"} | ConvertTo-Json
Invoke-WebRequest "http://localhost:8000/api/whatsapp/send" `
  -Method POST -ContentType "application/json" -Body $body
```

---

## 📂 Key Files

**Code:**
- `app/services/chatbot_service.py` - Main logic
- `app/routes/whatsapp.py` - Webhook handler
- `app/models/whatsapp.py` - Database models

**Docs:**
- `WHATSAPP_CHATBOT_QUICK_START.md` - 5-min guide
- `WHATSAPP_CHATBOT_SETUP.md` - Complete guide
- `WHATSAPP_CHATBOT_DEPLOYMENT.md` - Production

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Webhook not connecting | Check HTTPS, firewall, token match |
| No auto-response | Verify API token, phone ID, logs |
| Messages not saving | Check database permissions |
| Menu not working | Check message format (numbers only) |
| Signature failed | Verify webhook token matches exactly |

---

## 🔐 Security Checklist

- [ ] `.env` file not committed
- [ ] HTTPS only (no HTTP)
- [ ] API token rotated regularly
- [ ] Webhook signature verified
- [ ] Logs don't expose secrets
- [ ] Database backed up
- [ ] Firewall configured
- [ ] Error monitoring enabled

---

## 📊 Database Tables

```sql
-- View all messages
SELECT * FROM whatsapp_message;

-- View all contacts
SELECT * FROM whatsapp_contact;

-- Get specific contact's messages
SELECT * FROM whatsapp_message 
WHERE from_phone_number = '+27...';

-- Count messages per contact
SELECT from_phone_number, COUNT(*) 
FROM whatsapp_message GROUP BY from_phone_number;
```

---

## 🎓 Code Snippets

**Add menu option:**
```python
# In MAIN_MENU constant:
6️⃣ New Option

# In _handle_main_menu():
elif message_text == "6":
    self.set_user_state(phone_number, "new_menu")
    return self.NEW_MENU, None

# Create handler:
def _handle_new_menu(self, message_text, phone_number, db):
    if message_text == "1":
        return "Response...", None
```

**Query database:**
```python
orders = db.query(Order).filter(
    Order.customer_phone == phone_number
).all()

response = "Your orders:\n"
for order in orders:
    response += f"- {order.id}: {order.status}\n"

return response, None
```

---

## 🚀 Deployment Checklist

**Before Going Live:**
- [ ] HTTPS domain configured
- [ ] SSL certificate installed
- [ ] API token secure
- [ ] Database backed up
- [ ] Logs configured
- [ ] Monitoring enabled
- [ ] Support contact info updated
- [ ] Business verified with Meta

**After Deployment:**
- [ ] Test webhook connection
- [ ] Send test message
- [ ] Check auto-response
- [ ] Verify database storage
- [ ] Monitor logs for 24h
- [ ] Collect user feedback
- [ ] Make improvements

---

## 📞 Help Resources

**Setup:** WHATSAPP_CHATBOT_QUICK_START.md
**Complete:** WHATSAPP_CHATBOT_SETUP.md
**Production:** WHATSAPP_CHATBOT_DEPLOYMENT.md
**Testing:** WHATSAPP_CHATBOT_API_EXAMPLES.md
**All Docs:** WHATSAPP_CHATBOT_DOCS_INDEX.md

---

## 🔑 Key Concepts

**Webhook:** Meta sends messages to your app
**State:** Tracks what menu user is in
**Handler:** Method that processes menu option
**Response:** Message sent back to user
**Database:** Stores all messages & contacts
**Meta API:** Sends responses to WhatsApp

---

## ⏱️ Timing

| Task | Time |
|------|------|
| Get credentials | 10 min |
| Update .env | 1 min |
| Configure webhook | 2 min |
| Local testing | 5 min |
| Deploy to prod | 15 min |
| Test production | 5 min |
| **Total** | **~40 min** |

---

## 💰 Costs

**Free:**
- Meta WhatsApp Business API (first 1000 messages/month)
- FastAPI server (your infrastructure)
- Documentation & code

**Paid (Optional):**
- Domain & SSL ($12-20/year)
- Server hosting ($5-50/month)
- Message overages (after 1000/month)

---

## 📈 Metrics to Track

- Messages sent/received
- Unique users per day
- Menu option usage
- Response times
- Error rates
- User satisfaction
- Conversion rates
- Message trends

---

## 🎯 Next 30 Days

**Week 1:** Setup & Testing
- Get credentials
- Configure webhook
- Deploy to production
- Test with real users

**Week 2:** Monitor & Improve
- Analyze usage patterns
- Collect user feedback
- Fix any issues
- Optimize responses

**Week 3:** Customize
- Add database queries
- Enhance menu options
- Improve responses
- Add new features

**Week 4:** Optimize
- Analyze metrics
- Performance tune
- Add analytics
- Plan next phase

---

## 🔗 Important Links

| Resource | URL |
|----------|-----|
| Meta Developers | https://developers.facebook.com |
| WhatsApp API Docs | https://developers.facebook.com/docs/whatsapp |
| FastAPI Docs | https://fastapi.tiangolo.com |
| Your Setup Guide | WHATSAPP_CHATBOT_SETUP.md |
| Deployment Guide | WHATSAPP_CHATBOT_DEPLOYMENT.md |

---

## ✨ Features at a Glance

✅ Real-time message receiving
✅ Auto-response system
✅ Multi-level menus (5 main + 15+ sub)
✅ Database storage
✅ Message history
✅ Contact tracking
✅ Signature verification
✅ Error handling
✅ Production ready
✅ Fully documented

---

## 🎓 Learning Path

1. Read this card (5 min)
2. Read QUICK_START.md (5 min)
3. Get Meta credentials (10 min)
4. Update .env (1 min)
5. Test locally (5 min)
6. Deploy (15 min)
7. Monitor (ongoing)

**Total: 40 minutes to go live!**

---

## 📋 Credentials Checklist

Get these from Meta:
- [ ] Business Account ID
- [ ] Phone Number ID
- [ ] API Token
- [ ] Generate Webhook Token

Store in `.env`:
- [ ] WHATSAPP_BUSINESS_ACCOUNT_ID
- [ ] WHATSAPP_PHONE_NUMBER_ID
- [ ] WHATSAPP_API_TOKEN
- [ ] WHATSAPP_WEBHOOK_VERIFY_TOKEN
- [ ] WHATSAPP_WEBHOOK_URL

---

## 🚀 You're Ready!

Everything is set up and documented. Pick a guide and deploy!

**Questions?** Check WHATSAPP_CHATBOT_DOCS_INDEX.md

**Let's go! 🎉**
