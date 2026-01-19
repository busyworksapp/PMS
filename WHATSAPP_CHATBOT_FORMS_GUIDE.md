---
title: WhatsApp Chatbot - Form Submissions Feature
---

# 📝 WhatsApp Chatbot - Form Submissions & Retrieval

## Overview

Users can now **submit forms directly through WhatsApp** and **retrieve all their submitted forms**. Perfect for defect reports, customer feedback, support requests, and more.

---

## 🎯 User Experience

### Submitting a Form (Defect Report)

```
User: "hi"
Bot: Welcome! Select: 1-5

User: "2" (Report Defect)
Bot: Defect Menu options

User: "1" (Report a defect)
Bot: Please describe the defect...

User: "Surface has scratches on corners"
Bot: ✅ Report submitted!
    Report ID: DEF-20250118213045
    Status: Under Review
    We'll follow up soon
```

### Retrieving Submitted Forms

```
User: "2" (Report Defect)
Bot: Defect Menu options

User: "2" (View defect history)
Bot: 📋 Your Defect Reports
    1. ID: DEF-20250118213045
       Surface has scratches...
       Date: 2025-01-18

    2. ID: DEF-20250117095030
       Color mismatch on side...
       Date: 2025-01-17

    [More options for detailed view]
```

---

## 💾 Database Integration

### How Forms Are Stored

**Table:** `whatsapp_message`
```
message_id: "DEF-20250118213045"
from_phone_number: "+27123456789"
to_phone_number: "+27123456789"
message_type: "text"
message_text: "Surface has scratches on corners"
status: "submitted"
direction: "inbound"
sent_at: 2025-01-18 21:30:45
created_at: 2025-01-18 21:30:45
```

### Query Forms by Phone Number

```python
from app.models.whatsapp import WhatsAppMessage

# Get all defect reports from a contact
defects = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.from_phone_number == "+27123456789",
    WhatsAppMessage.status == "submitted"
).all()

# Get latest 5 defects
latest = defects[-5:]

# Get defects from last 30 days
from datetime import datetime, timedelta
recent = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.from_phone_number == "+27123456789",
    WhatsAppMessage.sent_at >= datetime.utcnow() - timedelta(days=30)
).all()
```

---

## 🔧 Current Implementation

### 1. Submit Defect Form

**Menu Path:** Main Menu → 2 (Report Defect) → 1 (Report a defect)

**Flow:**
```
ChatbotService._handle_defect_report()
    ↓
1. Check message length (minimum 10 chars)
2. Generate unique ID: DEF-{timestamp}
3. Save to database
4. Confirm submission to user
5. Show Report ID
```

**Code:**
```python
# In chatbot_service.py
defect_id = f"DEF-{datetime.now().strftime('%Y%m%d%H%M%S')}"

defect_msg = WhatsAppMessage(
    message_id=defect_id,
    from_phone_number=phone_number,
    message_text=message_text,
    status="submitted",
    ...
)
db.add(defect_msg)
db.commit()
```

### 2. View Defect Reports

**Menu Path:** Main Menu → 2 (Report Defect) → 2 (View defect history)

**Flow:**
```
ChatbotService._handle_defect_menu()
    ↓
1. Query database for user's reports
2. Filter by phone_number + status="submitted"
3. Get last 5 reports
4. Format for WhatsApp
5. Send to user
```

**Code:**
```python
defects = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.from_phone_number == phone_number,
    WhatsAppMessage.status == "submitted"
).all()

# Format for display
response = "📋 *Your Defect Reports*\n\n"
for defect in defects[-5:]:
    response += f"ID: {defect.message_id}\n"
    response += f"Description: {defect.message_text[:30]}...\n"
    response += f"Date: {defect.sent_at.strftime('%Y-%m-%d')}\n\n"
```

---

## 📋 Forms You Can Submit

### Current: Defect Reports
- Path: Main Menu → 2 (Report Defect) → 1
- Stores: Defect description, timestamp, unique ID
- Retrieval: Main Menu → 2 → 2

### Easily Extensible To:
- Customer Feedback
- Support Requests
- Quality Issues
- Order Complaints
- Feature Requests
- Any custom form

---

## 🚀 Adding More Form Types

### Example: Customer Feedback Form

**Step 1: Add Menu Option**
```python
MAIN_MENU = """...
6️⃣ Submit Feedback
..."""

# In _handle_main_menu():
elif message_text == "6":
    self.set_user_state(phone_number, "feedback_menu")
    return self.FEEDBACK_MENU, None
```

**Step 2: Create Menu Handler**
```python
FEEDBACK_MENU = """📝 *Customer Feedback*

1️⃣ Submit feedback
2️⃣ View your feedback
3️⃣ Back to Menu"""

def _handle_feedback_menu(self, message_text, phone_number, db):
    if message_text == "1":
        self.set_user_state(phone_number, "feedback_submit")
        return "Please share your feedback...", None
    
    elif message_text == "2":
        feedback = db.query(WhatsAppMessage).filter(
            WhatsAppMessage.from_phone_number == phone_number,
            WhatsAppMessage.message_id.like("FB-%")
        ).all()
        # ... format and return ...
```

**Step 3: Create Submission Handler**
```python
def _handle_feedback_submit(self, message_text, phone_number, db):
    if len(message_text) < 10:
        return "Please provide more details...", None
    
    feedback_id = f"FB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Save to database
    msg = WhatsAppMessage(
        message_id=feedback_id,
        from_phone_number=phone_number,
        message_text=message_text,
        status="submitted",
        ...
    )
    db.add(msg)
    db.commit()
    
    return f"✅ Feedback submitted! ID: {feedback_id}", None
```

**Step 4: Add to State Handler**
```python
# In process_message():
if current_state == "feedback_menu":
    return self._handle_feedback_menu(...)
if current_state == "feedback_submit":
    return self._handle_feedback_submit(...)
```

---

## 📊 API Endpoints for Forms

### Get All User Forms
```
GET /api/whatsapp/messages?phone_number=+27123456789
```

**Response:**
```json
{
  "total": 5,
  "messages": [
    {
      "message_id": "DEF-20250118213045",
      "from_phone_number": "+27123456789",
      "message_text": "Surface scratches",
      "status": "submitted",
      "sent_at": "2025-01-18T21:30:45Z"
    }
  ]
}
```

### Get Forms by Status
```
GET /api/whatsapp/messages?phone_number=+27123456789&status=submitted
```

### Get Forms by Type (using message_id prefix)
```python
# Get all defects
defects = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.message_id.like("DEF-%")
).all()

# Get all feedback
feedback = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.message_id.like("FB-%")
).all()

# Get all support tickets
tickets = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.message_id.like("SUP-%")
).all()
```

---

## 🔄 Form Status Tracking

### Current Flow
```
submitted → In Database → Retrieved via WhatsApp
```

### Enhanced Status Flow (Optional)
```python
# Add statuses in addition to "submitted"
status = "submitted"  # Initial
status = "assigned"   # Assigned to team
status = "in_progress"  # Being worked on
status = "resolved"   # Completed
status = "closed"     # Closed

# Users can query:
User: "What's the status of DEF-20250118213045?"
Bot: "Status: In Progress (60% complete)"
```

---

## 💡 Implementation Details

### Unique ID Generation

**Current Format:** `DEF-{YYYYMMDDHHMMSS}`
```
DEF-20250118213045
├─ DEF    = Defect form type
├─ 2025   = Year
├─ 01     = Month
├─ 18     = Day
├─ 21     = Hour
├─ 30     = Minute
└─ 45     = Second
```

**Alternative ID Formats:**
```python
# With random component
import uuid
defect_id = f"DEF-{uuid.uuid4().hex[:8].upper()}"
# Result: DEF-A1B2C3D4

# With sequential numbering
from app.models.whatsapp import WhatsAppMessage
count = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.message_id.like("DEF-%")
).count()
defect_id = f"DEF-{count + 1:06d}"
# Result: DEF-000001
```

---

## 🔍 Querying & Reporting

### Get Forms by User

```python
def get_user_forms(phone_number: str, db: Session):
    return db.query(WhatsAppMessage).filter(
        WhatsAppMessage.from_phone_number == phone_number,
        WhatsAppMessage.status == "submitted"
    ).order_by(
        WhatsAppMessage.sent_at.desc()
    ).all()
```

### Get Forms by Date Range

```python
from datetime import datetime, timedelta

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 1, 31)

forms = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.sent_at >= start_date,
    WhatsAppMessage.sent_at <= end_date,
    WhatsAppMessage.status == "submitted"
).all()
```

### Get Forms by Type

```python
# Defects only
defects = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.message_id.like("DEF-%")
).all()

# Count by type
from sqlalchemy import func
counts = db.query(
    func.substr(WhatsAppMessage.message_id, 1, 3).label("type"),
    func.count(WhatsAppMessage.id).label("count")
).group_by("type").all()
```

---

## 📈 Analytics

### Track Form Submissions

```python
# Total submissions
total = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.status == "submitted"
).count()

# Submissions per user
from sqlalchemy import func
per_user = db.query(
    WhatsAppMessage.from_phone_number,
    func.count(WhatsAppMessage.id).label("count")
).filter(
    WhatsAppMessage.status == "submitted"
).group_by(WhatsAppMessage.from_phone_number).all()

# Submissions per day
per_day = db.query(
    func.date(WhatsAppMessage.sent_at).label("date"),
    func.count(WhatsAppMessage.id).label("count")
).filter(
    WhatsAppMessage.status == "submitted"
).group_by("date").all()

# Average submission length
avg_length = db.query(
    func.avg(func.length(WhatsAppMessage.message_text))
).filter(
    WhatsAppMessage.status == "submitted"
).scalar()
```

---

## 🔐 Security Considerations

### Validate Input
```python
if len(message_text) < 10:
    return "Message too short", None

if len(message_text) > 500:
    message_text = message_text[:500]

# Sanitize for database
message_text = message_text.strip()
```

### Verify User

```python
# Ensure phone number matches
if phone_number != user_phone:
    return "Unauthorized", None

# Rate limit submissions
recent = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.from_phone_number == phone_number,
    WhatsAppMessage.sent_at >= datetime.utcnow() - timedelta(minutes=1)
).count()

if recent > 5:
    return "Too many submissions. Please wait.", None
```

### Audit Trail

```python
# Log all submissions
audit_log = {
    "timestamp": datetime.utcnow(),
    "phone_number": phone_number,
    "form_id": form_id,
    "form_type": form_type,
    "action": "submitted",
    "ip_address": request.client.host
}
# Store audit_log
```

---

## 📝 Testing Forms

### Test Submission

**cURL:**
```bash
# Simulate user submitting defect
curl -X POST http://localhost:8000/api/whatsapp/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=test" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "from": "27123456789",
            "text": {"body": "Surface has scratches on corners"}
          }]
        }
      }]
    }]
  }'
```

### Test Retrieval

```bash
# Get all forms from user
curl "http://localhost:8000/api/whatsapp/messages?phone_number=%2B27123456789"
```

---

## 🚀 Next Steps

1. **Use Current Implementation**
   - Users can submit defect reports via WhatsApp
   - Users can view their submissions

2. **Add More Form Types**
   - Follow the pattern for feedback, support tickets, etc.
   - Each form type gets its own menu

3. **Enhance Status Tracking**
   - Track form status in database
   - Show users current status

4. **Create Admin Dashboard**
   - View all submissions
   - Filter by type, date, status
   - Export to CSV/PDF

5. **Integrate with Backend Systems**
   - Link forms to actual defect/order systems
   - Auto-create tickets in other platforms
   - Sync data across systems

---

## 📞 Support

**For form submission logic:**
- See: `app/services/chatbot_service.py`
- Method: `_handle_defect_report()`
- Method: `_handle_defect_menu()`

**For database queries:**
- See: `app/models/whatsapp.py`
- Table: `WhatsAppMessage`

**For API endpoints:**
- See: `app/routes/whatsapp.py`
- Endpoint: `GET /api/whatsapp/messages`

---

## ✅ Features Ready to Use

✅ Form submission via WhatsApp
✅ Unique form ID generation
✅ Database storage
✅ User form retrieval
✅ Error handling
✅ Input validation
✅ Extensible design

**All ready to deploy! 🚀**
