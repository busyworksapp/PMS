---
title: WhatsApp Chatbot API Examples & Testing
---

# 🧪 WhatsApp Chatbot - API Testing Guide

## Example API Calls

### 1. Health Check
**Purpose:** Verify backend is running

**cURL:**
```bash
curl http://localhost:8000/api/whatsapp/health
```

**PowerShell:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/whatsapp/health"
```

**Response:**
```json
{
  "status": "ok",
  "service": "whatsapp"
}
```

---

### 2. Get All Contacts

**Purpose:** List all contacts who messaged you

**cURL:**
```bash
curl http://localhost:8000/api/whatsapp/contacts
```

**PowerShell:**
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/whatsapp/contacts"
$response.Content | ConvertFrom-Json | Format-Table
```

**Response:**
```json
{
  "total": 3,
  "contacts": [
    {
      "phone_number": "+27123456789",
      "display_name": "+27123456789",
      "last_message_time": "2025-01-18T14:30:00Z"
    },
    {
      "phone_number": "+27987654321",
      "display_name": "John Doe",
      "last_message_time": "2025-01-18T14:25:00Z"
    }
  ]
}
```

---

### 3. Get Messages from Specific Contact

**Purpose:** Get conversation history with one person

**cURL:**
```bash
curl "http://localhost:8000/api/whatsapp/messages?phone_number=%2B27123456789"
```

**PowerShell:**
```powershell
$phone = "+27123456789"
$uri = "http://localhost:8000/api/whatsapp/messages?phone_number=$([System.Web.HttpUtility]::UrlEncode($phone))"
Invoke-WebRequest -Uri $uri | ConvertFrom-Json | ConvertTo-Json
```

**Response:**
```json
{
  "total": 5,
  "messages": [
    {
      "message_id": "msg_001",
      "from_phone_number": "+27123456789",
      "to_phone_number": "+27555666777",
      "message_type": "text",
      "message_text": "hi",
      "status": "delivered",
      "direction": "inbound",
      "sent_at": "2025-01-18T14:30:00Z"
    },
    {
      "message_id": "msg_002",
      "from_phone_number": "+27555666777",
      "to_phone_number": "+27123456789",
      "message_type": "text",
      "message_text": "🤖 Welcome to Barron Production System...",
      "status": "sent",
      "direction": "outbound",
      "sent_at": "2025-01-18T14:30:05Z"
    }
  ]
}
```

---

### 4. Send Message to Contact

**Purpose:** Manually send a message (usually auto-done by chatbot)

**cURL:**
```bash
curl -X POST http://localhost:8000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+27123456789",
    "message": "Hello! This is a test message."
  }'
```

**PowerShell:**
```powershell
$body = @{
    phone_number = "+27123456789"
    message = "Hello! This is a test message."
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/whatsapp/send" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Response:**
```json
{
  "success": true,
  "message_id": "msg_003",
  "status": "sent",
  "timestamp": "2025-01-18T14:35:00Z"
}
```

---

### 5. Test Webhook (Simulate Incoming Message)

**Purpose:** Send test message to webhook (simulates Meta sending message)

**Note:** Only works if you manually send to your local IP or ngrok URL

**cURL:**
```bash
curl -X POST http://localhost:8000/api/whatsapp/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=test_signature" \
  -d '{
    "entry": [
      {
        "id": "123456789",
        "changes": [
          {
            "value": {
              "messages": [
                {
                  "from": "27123456789",
                  "id": "msg_test_001",
                  "timestamp": "1234567890",
                  "type": "text",
                  "text": {
                    "body": "hi"
                  }
                }
              ],
              "contacts": [
                {
                  "profile": {
                    "name": "Test User"
                  },
                  "wa_id": "27123456789"
                }
              ]
            }
          }
        ]
      }
    ]
  }'
```

**PowerShell:**
```powershell
$body = @{
    entry = @(
        @{
            id = "123456789"
            changes = @(
                @{
                    value = @{
                        messages = @(
                            @{
                                from = "27123456789"
                                id = "msg_test_001"
                                timestamp = "1234567890"
                                type = "text"
                                text = @{
                                    body = "hi"
                                }
                            }
                        )
                        contacts = @(
                            @{
                                profile = @{
                                    name = "Test User"
                                }
                                wa_id = "27123456789"
                            }
                        )
                    }
                }
            )
        }
    )
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri "http://localhost:8000/api/whatsapp/webhook" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"X-Hub-Signature-256" = "sha256=test"} `
  -Body $body
```

**Response:**
```json
{
  "success": true,
  "message": "Webhook processed successfully",
  "event_id": "123456789"
}
```

---

## Test Sequence (Complete Flow)

### Step 1: Start Backend
```powershell
cd "c:\Users\4667.KevroAD\OneDrive - Barron (Pty) Ltd\Desktop\th\app\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 2: Check Health
```bash
curl http://localhost:8000/api/whatsapp/health
# Should return: {"status": "ok", "service": "whatsapp"}
```

### Step 3: Get Empty Contacts List
```bash
curl http://localhost:8000/api/whatsapp/contacts
# Should return: {"total": 0, "contacts": []}
```

### Step 4: Simulate Incoming Message
```bash
# User sends "hi" to WhatsApp
# Meta sends webhook to your app (in production)
# For testing: use the webhook test endpoint above
```

### Step 5: Check Contacts List (Updated)
```bash
curl http://localhost:8000/api/whatsapp/contacts
# Should now include the contact from step 4
```

### Step 6: Get Conversation History
```bash
curl "http://localhost:8000/api/whatsapp/messages?phone_number=%2B27123456789"
# Should show the message and auto-response
```

---

## Using with Postman

### Import Collection

Create a new Postman collection:

```json
{
  "info": {
    "name": "WhatsApp Chatbot API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/api/whatsapp/health"
      }
    },
    {
      "name": "Get Contacts",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/api/whatsapp/contacts"
      }
    },
    {
      "name": "Get Messages",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/api/whatsapp/messages?phone_number={{phone_number}}"
      }
    },
    {
      "name": "Send Message",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": "http://localhost:8000/api/whatsapp/send",
        "body": {
          "mode": "raw",
          "raw": "{\"phone_number\": \"{{phone_number}}\", \"message\": \"Hello!\"}"
        }
      }
    }
  ]
}
```

---

## Response Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Message sent successfully |
| 201 | Created | Message created |
| 400 | Bad Request | Invalid phone number format |
| 401 | Unauthorized | Invalid webhook signature |
| 404 | Not Found | No messages found |
| 429 | Too Many Requests | Rate limited |
| 500 | Server Error | Database error |

---

## Example Chat Sequence

### User Flow

```
STEP 1: User sends message on WhatsApp
┌─────────────────────────────────────┐
│ User on WhatsApp                    │
│ Types: "hi"                         │
│ Taps Send                           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ Your Backend (localhost:8000)        │
│ POST /api/whatsapp/webhook          │
│                                      │
│ 1. Verify signature                 │
│ 2. Extract message: "hi"            │
│ 3. Call chatbot_service             │
│ 4. Get response: main menu          │
│ 5. Call Meta API to send response   │
│ 6. Save to database                 │
│ 7. Return success                   │
└──────────────┬──────────────────────┘
               │
STEP 2: Auto-response sent to user
┌──────────────▼──────────────────────┐
│ User's WhatsApp                     │
│ Receives:                           │
│ "🤖 Welcome to Barron..."           │
│ "Select an option: 1, 2, 3..."      │
└──────────────┬──────────────────────┘
               │
STEP 3: User navigates menu
┌──────────────▼──────────────────────┐
│ User Types: "1"                     │
│ (Order Status)                      │
└──────────────┬──────────────────────┘
               │
STEP 4: Auto-response with submenu
┌──────────────▼──────────────────────┐
│ Receives: Order Status Submenu      │
│ (Same flow repeats)                 │
└─────────────────────────────────────┘
```

---

## Database Queries

### View All Messages
```sql
SELECT * FROM whatsapp_message ORDER BY sent_at DESC;
```

### View All Contacts
```sql
SELECT * FROM whatsapp_contact;
```

### Get Messages from Specific Phone
```sql
SELECT * FROM whatsapp_message 
WHERE from_phone_number = '+27123456789'
ORDER BY sent_at DESC;
```

### Get Unread Messages
```sql
SELECT * FROM whatsapp_message 
WHERE status != 'read' 
ORDER BY sent_at DESC;
```

### Count Messages per Contact
```sql
SELECT from_phone_number, COUNT(*) as message_count
FROM whatsapp_message
GROUP BY from_phone_number
ORDER BY message_count DESC;
```

---

## Performance Testing

### Load Test (Simulate 100 Messages)

**PowerShell Script:**
```powershell
$phones = @("+27123456789", "+27987654321", "+27111111111")

for ($i = 0; $i -lt 100; $i++) {
    $phone = $phones[$i % $phones.Length]
    $message = "Test message $i"
    
    $body = @{
        phone_number = $phone
        message = $message
    } | ConvertTo-Json
    
    Invoke-WebRequest -Uri "http://localhost:8000/api/whatsapp/send" `
      -Method POST `
      -ContentType "application/json" `
      -Body $body
    
    Write-Host "Sent $i of 100"
    Start-Sleep -Milliseconds 100
}
```

### Measure Response Time

```powershell
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

$body = @{
    phone_number = "+27123456789"
    message = "Test"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/whatsapp/send" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body

$stopwatch.Stop()

Write-Host "Response time: $($stopwatch.ElapsedMilliseconds)ms"
```

---

## Debugging

### Enable Verbose Logging

**Check logs in backend terminal:**
```
INFO:     POST /api/whatsapp/webhook
INFO:     Webhook processed successfully
INFO:     Auto-response sent to +27123456789
```

### Capture Request/Response

**Using tcpdump (Linux/Mac):**
```bash
tcpdump -i lo -A 'tcp port 8000'
```

**Using NetSh Trace (Windows):**
```powershell
netsh trace start capture=yes tracefile=C:\temp\trace.etl
```

---

## Troubleshooting API Calls

### Issue: 404 Not Found
**Solution:** Check endpoint is correct
```bash
# Wrong:
curl http://localhost:8000/whatsapp/send

# Correct:
curl http://localhost:8000/api/whatsapp/send
```

### Issue: 400 Bad Request
**Solution:** Check request body format
```json
// Wrong:
{"phone": "+27123456789"}

// Correct:
{"phone_number": "+27123456789", "message": "text"}
```

### Issue: Connection Refused
**Solution:** Check backend is running
```bash
# Start backend first:
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Issue: Timeout
**Solution:** Check network/firewall
```bash
# Test connectivity:
curl http://localhost:8000/api/whatsapp/health
```

---

## Success Indicators

✅ All these should return 200 status:
- GET /api/whatsapp/health
- GET /api/whatsapp/contacts
- GET /api/whatsapp/messages
- POST /api/whatsapp/send
- POST /api/whatsapp/webhook

✅ Database should have entries:
- whatsapp_message (all messages)
- whatsapp_contact (all contacts)
- whatsapp_session (user states)

✅ Logs should show:
- "Webhook processed successfully"
- "Auto-response sent to ..."
- No ERROR messages

---

## Next: Real-World Testing

Once API testing passes:

1. **Deploy to production domain**
2. **Configure webhook in Meta Dashboard**
3. **Test with real WhatsApp message**
4. **Monitor logs for 24 hours**
5. **Collect user feedback**

See: `WHATSAPP_CHATBOT_DEPLOYMENT.md`
