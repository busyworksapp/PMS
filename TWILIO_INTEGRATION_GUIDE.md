# Barron PMS - Twilio WhatsApp Integration Guide

## Overview

Your Barron Production Management System now has **full Twilio WhatsApp integration** configured and ready to use.

## Current Status ✅

- **Twilio Account SID:** `[See .env file]`
- **Twilio Service:** ✓ Initialized and ready
- **WhatsApp Routes:** ✓ 9 endpoints available
- **Database Integration:** ✓ Messages stored automatically
- **Webhook Support:** ✓ Ready for incoming messages

## Key Features

### 1. **Send Messages**
```bash
# Send single message
curl -X POST http://localhost:8000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+27123456789",
    "message_text": "Job status update",
    "message_type": "text"
  }'

# Send bulk messages
curl -X POST http://localhost:8000/api/whatsapp/send-bulk \
  -H "Content-Type: application/json" \
  -d '{
    "phone_numbers": ["+27123456789", "+27987654321"],
    "message_text": "Maintenance alert"
  }'
```

### 2. **Receive Messages**
- Webhook endpoint: `POST /api/whatsapp/twilio-webhook`
- Automatically processes with chatbot
- Stores in database
- Sends auto-response

### 3. **Message History**
```bash
curl "http://localhost:8000/api/whatsapp/messages?contact_number=+27123456789&limit=50"
```

### 4. **Contact Management**
```bash
# Get all contacts
curl http://localhost:8000/api/whatsapp/contacts

# Mark messages as read
curl -X POST http://localhost:8000/api/whatsapp/contacts/+27123456789/read
```

### 5. **Health Check**
```bash
curl http://localhost:8000/api/whatsapp/health
```

## Configuration

### Environment Variables (.env)
```properties
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155552671
TWILIO_WEBHOOK_VERIFY_TOKEN=BarronPMSWebhookToken2024
```

### Python Configuration (app/core/config.py)
```python
TWILIO_ACCOUNT_SID: str = "your_account_sid_here"
TWILIO_AUTH_TOKEN: str = "your_auth_token_here"
TWILIO_WHATSAPP_NUMBER: str = "whatsapp:+14155552671"
TWILIO_WEBHOOK_VERIFY_TOKEN: str = "BarronPMSWebhookToken2024"
```

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/whatsapp/send` | Send single message |
| POST | `/api/whatsapp/send-bulk` | Send bulk messages |
| POST | `/api/whatsapp/twilio-webhook` | Receive incoming messages |
| GET | `/api/whatsapp/messages` | Get message history |
| GET | `/api/whatsapp/contacts` | Get all contacts |
| POST | `/api/whatsapp/contacts/{phone}/read` | Mark as read |
| GET | `/api/whatsapp/health` | Health check |

## Integration Points

### With Job Planning Module
Send automated job status updates to team members:
```python
# Example: When job is completed
await twilio_whatsapp_service.send_message(
    phone_number=operator_phone,
    message_text=f"Job {order.order_number} completed",
    db=db
)
```

### With Maintenance Module
Send maintenance alerts:
```python
# Example: Maintenance due
await twilio_whatsapp_service.send_message(
    phone_number=maintenance_tech_phone,
    message_text=f"Machine {machine.name} maintenance due: {ticket.description}",
    db=db
)
```

### With Defects Module
Notify about quality issues:
```python
# Example: Customer return
await twilio_whatsapp_service.send_message(
    phone_number=qc_manager_phone,
    message_text=f"Customer return reported: {defect.description}",
    db=db
)
```

## Starting the Application

### Option 1: Using run_server.py
```bash
cd app/backend
python run_server.py
```

### Option 2: Direct Uvicorn
```bash
cd app/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Verification
```bash
# Check if backend is running
curl http://localhost:8000/api/whatsapp/health

# Expected response:
# {
#   "status": "healthy",
#   "is_configured": true,
#   "provider": "Twilio",
#   "message": "Twilio WhatsApp integration ready"
# }
```

## Setting Up Twilio Webhook

### Step 1: Get Public URL
If running locally, use ngrok for tunneling:
```bash
ngrok http 8000
# This gives you a URL like: https://xxxx.ngrok.io
```

### Step 2: Configure Twilio Console
1. Go to https://www.twilio.com/console
2. Navigate to: **Messaging → WhatsApp → Settings**
3. Find "When a message comes in" webhook
4. Set URL to: `https://xxxx.ngrok.io/api/whatsapp/twilio-webhook`
5. Click Save

### Step 3: Test Webhook
Send a test WhatsApp message to your Twilio sandbox number to verify.

## Message Types Supported

| Type | Description | Example |
|------|-------------|---------|
| `text` | Text message | "Job completed" |
| `image` | Image file | URL to image |
| `video` | Video file | URL to video |
| `audio` | Audio file | URL to audio |
| `document` | Document file | URL to PDF/DOC |

## Database Storage

All messages are automatically stored in:
- **Table:** `whatsapp_messages`
- **Tracked:** Message ID, sender, recipient, content, media, timestamp, status
- **Statuses:** `sent`, `received`, `read`, `failed`

Contacts are stored in:
- **Table:** `whatsapp_contacts`
- **Tracked:** Phone number, display name, last message time, active status

## Error Handling

The service includes error handling for:
- Invalid phone numbers
- Network failures
- Twilio API errors
- Database errors
- Webhook verification failures

Check logs for detailed error messages if issues occur.

## Security Considerations

✅ **Already Implemented:**
- HMAC-SHA1 webhook signature verification
- Token-based authentication
- Secure credential storage in environment variables
- SQL injection protection via ORM

⚠️ **Before Production:**
- [ ] Enable HTTPS for webhook URL
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Monitor API usage
- [ ] Set up Twilio alerts

## Monitoring & Logging

View application logs:
```bash
# Check recent logs
tail -f logs/application.log

# Search for WhatsApp specific logs
grep "WhatsApp" logs/application.log

# Check errors
grep "ERROR" logs/application.log
```

## Troubleshooting

### Problem: Messages not sending
**Solution:** 
1. Check phone number format (should include country code: +27...)
2. Verify Twilio credits available
3. Check logs for specific error messages

### Problem: Webhook not receiving
**Solution:**
1. Verify webhook URL in Twilio console
2. Ensure URL is publicly accessible (use ngrok if local)
3. Check webhook signature verification isn't failing
4. Check application logs for webhook errors

### Problem: Database not storing messages
**Solution:**
1. Verify database connection in `.env`
2. Check that WhatsAppMessage table exists
3. Review database logs for errors

## Production Deployment

When deploying to production:

1. **Update Credentials:**
   - Get production Twilio credentials
   - Update `.env` file on production server

2. **Configure Domain:**
   - Set webhook URL to your production domain
   - Use HTTPS (required by Twilio)

3. **Verify Endpoints:**
   - Test send endpoint
   - Test webhook receiving
   - Monitor logs

4. **Scale Services:**
   - Consider message queue for bulk sends
   - Implement caching for contact lists
   - Monitor Twilio API rate limits

## Support & Documentation

- **Twilio Docs:** https://www.twilio.com/docs/whatsapp
- **API Reference:** http://localhost:8000/docs (Swagger UI)
- **GitHub:** https://github.com/busyworksapp/PMS
- **Status Page:** http://localhost:8000/api/whatsapp/health

## Next Steps

1. ✅ **Verify Setup:** Run health check
2. ✅ **Test Sending:** Send a test message
3. ✅ **Configure Webhook:** Set up incoming messages
4. ✅ **Test Receiving:** Send WhatsApp to your Twilio number
5. ✅ **Integrate:** Add WhatsApp notifications to business processes

---

**Barron PMS - Twilio Integration Complete** 🎉

For any issues or questions, refer to logs or Twilio documentation.
