"""
WhatsApp Integration Module
Handles WhatsApp chatbot for form submission and data retrieval
Uses Twilio WhatsApp API for messaging
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Optional, Dict, Any
import os
import json
from datetime import datetime
import logging

# For Twilio integration
try:
    from twilio.rest import Client
    from twilio.request_validator import RequestValidator
except ImportError:
    print("WARNING: Twilio not installed. Install with: pip install twilio")

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])

# Configuration from environment
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")  # Twilio sandbox

# Initialize Twilio client if credentials exist
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# In-memory sessions (use Redis in production)
whatsapp_sessions: Dict[str, Dict[str, Any]] = {}


class WhatsAppMenus:
    """WhatsApp message templates"""
    
    MAIN_MENU = """👋 Welcome to Barron Manufacturing!

1️⃣ Create Defect Report
2️⃣ Check Order Status
3️⃣ Report Maintenance Issue
4️⃣ View SOP Failure
5️⃣ Check SLA Status
6️⃣ Submit BOM Update

Reply with number (1-6)"""

    INVALID_OPTION = "❌ Invalid option. Please reply with a number 1-6"
    
    DEFECT_MENU = "📝 Create Defect Report\n\nOrder Number (e.g., ORD-12345): ?"
    ORDER_MENU = "📦 Check Order Status\n\nOrder Number (e.g., ORD-12345): ?"
    MAINTENANCE_MENU = "🔧 Report Maintenance\n\nMachine ID (e.g., MACH-001): ?"
    SOP_MENU = "⚠️ View SOP Failure\n\nSOP ID (e.g., SOP-999): ?"
    SLA_MENU = "⏱️ Check SLA Status\n\nTicket ID (e.g., MAINT-555 or DEF-123): ?"
    BOM_MENU = "📄 Submit BOM Update\n\nBOM ID (e.g., BOM-888): ?"


class WhatsAppSession:
    """Manages WhatsApp conversation state for each user"""
    
    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        self.state = "MENU"  # MENU, DEFECT_ORDER, DEFECT_TYPE, etc.
        self.data: Dict[str, Any] = {}
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def reset(self):
        """Reset to main menu"""
        self.state = "MENU"
        self.data = {}
        self.updated_at = datetime.utcnow()


def get_or_create_session(phone_number: str) -> WhatsAppSession:
    """Get existing session or create new one"""
    if phone_number not in whatsapp_sessions:
        whatsapp_sessions[phone_number] = WhatsAppSession(phone_number)
    return whatsapp_sessions[phone_number]


def send_whatsapp_message(to_number: str, message_text: str) -> bool:
    """Send WhatsApp message via Twilio"""
    if not twilio_client:
        logger.warning("Twilio client not configured")
        return False
    
    try:
        message = twilio_client.messages.create(
            body=message_text,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=to_number
        )
        logger.info(f"WhatsApp message sent to {to_number}: {message.sid}")
        return True
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message: {str(e)}")
        return False


# ==================== WORKFLOW HANDLERS ====================

def handle_main_menu(session: WhatsAppSession, user_input: str) -> str:
    """Handle main menu selection"""
    choice = user_input.strip()
    
    if choice == "1":
        session.state = "DEFECT_ORDER"
        return WhatsAppMenus.DEFECT_MENU
    elif choice == "2":
        session.state = "ORDER_STATUS"
        return WhatsAppMenus.ORDER_MENU
    elif choice == "3":
        session.state = "MAINTENANCE_MACHINE"
        return WhatsAppMenus.MAINTENANCE_MENU
    elif choice == "4":
        session.state = "SOP_ID"
        return WhatsAppMenus.SOP_MENU
    elif choice == "5":
        session.state = "SLA_TICKET"
        return WhatsAppMenus.SLA_MENU
    elif choice == "6":
        session.state = "BOM_ID"
        return WhatsAppMenus.BOM_MENU
    else:
        return WhatsAppMenus.INVALID_OPTION


def handle_defect_workflow(session: WhatsAppSession, user_input: str) -> str:
    """Handle defect creation workflow"""
    
    if session.state == "DEFECT_ORDER":
        session.data['order_number'] = user_input.strip().upper()
        # In production, verify order exists in database
        session.state = "DEFECT_TYPE"
        return f"✅ Order found: {session.data['order_number']}\n\nDefect Type (Internal Reject / Return / Other): ?"
    
    elif session.state == "DEFECT_TYPE":
        session.data['defect_type'] = user_input.strip()
        session.state = "DEFECT_SEVERITY"
        return "Severity (Low / Medium / High): ?"
    
    elif session.state == "DEFECT_SEVERITY":
        session.data['severity'] = user_input.strip()
        session.state = "DEFECT_DESCRIPTION"
        return "Description (brief details): ?"
    
    elif session.state == "DEFECT_DESCRIPTION":
        session.data['description'] = user_input.strip()
        
        # In production, submit to API
        # defect = api.post('/api/defects/', session.data)
        
        response = f"""✅ Defect Report Created!

📋 Details:
Order: {session.data.get('order_number')}
Type: {session.data.get('defect_type')}
Severity: {session.data.get('severity')}
Reference: DEF-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}

⚠️ Order is now ON HOLD

Type 'hi' for menu"""
        
        session.reset()
        return response
    
    return "❌ Error processing defect"


def handle_order_status(session: WhatsAppSession, user_input: str) -> str:
    """Handle order status check"""
    order_number = user_input.strip().upper()
    
    # In production, fetch from API
    # order = api.get(f'/api/orders/{order_number}')
    
    # Mock response
    response = f"""📦 Order Status: {order_number}

Status: In Progress
Progress: 75%
Expected Completion: 2026-01-25
SLA Status: ✅ On Track
Last Updated: 2026-01-18 14:30

Type 'hi' for menu"""
    
    session.reset()
    return response


def handle_maintenance(session: WhatsAppSession, user_input: str) -> str:
    """Handle maintenance issue reporting"""
    
    if session.state == "MAINTENANCE_MACHINE":
        session.data['machine_id'] = user_input.strip().upper()
        session.state = "MAINTENANCE_ISSUE"
        return "Issue Type (Bearing / Hydraulic / Electrical / Other): ?"
    
    elif session.state == "MAINTENANCE_ISSUE":
        session.data['issue_type'] = user_input.strip()
        session.state = "MAINTENANCE_URGENCY"
        return "Urgency (Low / Medium / High): ?"
    
    elif session.state == "MAINTENANCE_URGENCY":
        session.data['urgency'] = user_input.strip()
        
        # In production, submit to API
        sla_hours = 72 if session.data['urgency'].lower() == 'low' else (48 if session.data['urgency'].lower() == 'medium' else 24)
        
        response = f"""✅ Maintenance Ticket Created!

🔧 Details:
Machine: {session.data.get('machine_id')}
Issue: {session.data.get('issue_type')}
Urgency: {session.data.get('urgency')}
Ticket: MAINT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}
SLA: {sla_hours} hours

Type 'hi' for menu"""
        
        session.reset()
        return response
    
    return "❌ Error processing maintenance"


def handle_sop_check(session: WhatsAppSession, user_input: str) -> str:
    """Handle SOP failure check"""
    sop_id = user_input.strip().upper()
    
    # In production, fetch from API
    # sop = api.get(f'/api/sop_ncr/{sop_id}')
    
    response = f"""⚠️ SOP Failure: {sop_id}

Status: Under Review
Failure Type: Process Deviation
Reported: 2026-01-18 10:00
Assigned to: Manager (Pending)
Escalation Status: ⏳ Awaiting HOD Approval

Type 'hi' for menu"""
    
    session.reset()
    return response


def handle_sla_check(session: WhatsAppSession, user_input: str) -> str:
    """Handle SLA status check"""
    ticket_id = user_input.strip().upper()
    
    # In production, fetch from API
    # ticket = api.get(f'/api/maintenance/{ticket_id}')
    
    response = f"""⏱️ SLA Status: {ticket_id}

Time Remaining: 44h 32m 15s
Deadline: 2026-01-20 14:30
Status: ⚠️ WARNING (< 6 hours)
Assigned to: Technician A
Last Update: 2026-01-18 14:00

Type 'hi' for menu"""
    
    session.reset()
    return response


def handle_bom_update(session: WhatsAppSession, user_input: str) -> str:
    """Handle BOM update submission"""
    bom_id = user_input.strip().upper()
    
    # In production, submit to API
    # bom = api.post(f'/api/finance/bom/{bom_id}/update', session.data)
    
    response = f"""✅ BOM Update Submitted!

📄 BOM: {bom_id}
Version: v2.1
Updated: 2026-01-18 14:45
Cost Change: +2.5%
Approval Status: 🔄 Pending Review

Type 'hi' for menu"""
    
    session.reset()
    return response


def process_user_message(session: WhatsAppSession, user_input: str) -> str:
    """Route user input to appropriate handler"""
    
    # Reset on greeting
    if user_input.lower() in ["hi", "hello", "menu"]:
        session.reset()
        return WhatsAppMenus.MAIN_MENU
    
    # Route to appropriate handler
    if session.state == "MENU":
        return handle_main_menu(session, user_input)
    
    elif session.state.startswith("DEFECT"):
        return handle_defect_workflow(session, user_input)
    
    elif session.state == "ORDER_STATUS":
        return handle_order_status(session, user_input)
    
    elif session.state.startswith("MAINTENANCE"):
        return handle_maintenance(session, user_input)
    
    elif session.state == "SOP_ID":
        return handle_sop_check(session, user_input)
    
    elif session.state == "SLA_TICKET":
        return handle_sla_check(session, user_input)
    
    elif session.state == "BOM_ID":
        return handle_bom_update(session, user_input)
    
    else:
        # Unknown state, reset to menu
        session.reset()
        return WhatsAppMenus.MAIN_MENU


# ==================== FASTAPI ENDPOINTS ====================

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Receive WhatsApp messages from Twilio webhook
    
    Expected form data:
    - From: whatsapp:+1234567890
    - Body: User message text
    """
    try:
        # Parse request form data
        data = await request.form()
        from_number = data.get('From', '')
        message_body = data.get('Body', '').strip()
        
        if not from_number or not message_body:
            logger.warning("Invalid webhook data received")
            return {"success": False, "error": "Missing From or Body"}
        
        logger.info(f"WhatsApp message from {from_number}: {message_body}")
        
        # Get or create session
        session = get_or_create_session(from_number)
        
        # Process message
        response_text = process_user_message(session, message_body)
        
        # Send response
        sent = send_whatsapp_message(from_number, response_text)
        
        # Log interaction
        logger.info(f"Response sent to {from_number}")
        
        return {"success": sent, "message": response_text}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"success": False, "error": str(e)}


@router.get("/webhook")
async def verify_webhook(request: Request):
    """
    Verify Twilio webhook (GET request for verification)
    Twilio sends verification request to confirm endpoint
    """
    try:
        params = dict(request.query_params)
        
        # In production, verify with Twilio RequestValidator
        # validator = RequestValidator(TWILIO_AUTH_TOKEN)
        # url = str(request.url)
        # is_valid = validator.validate(url, params, '')
        
        # For development, just return success
        logger.info("Webhook verification request received")
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error verifying webhook: {str(e)}")
        return {"status": "error", "message": str(e)}


@router.get("/sessions")
async def get_sessions():
    """
    Get all active WhatsApp sessions (for debugging)
    """
    return {
        "total_sessions": len(whatsapp_sessions),
        "sessions": {
            phone: {
                "state": session.state,
                "data_keys": list(session.data.keys()),
                "created_at": session.created_at.isoformat(),
                "updated_at": session.updated_at.isoformat()
            }
            for phone, session in whatsapp_sessions.items()
        }
    }


@router.delete("/sessions/{phone_number}")
async def clear_session(phone_number: str):
    """
    Clear WhatsApp session for specific user (for debugging)
    """
    if phone_number in whatsapp_sessions:
        del whatsapp_sessions[phone_number]
        return {"success": True, "message": f"Session cleared for {phone_number}"}
    return {"success": False, "message": f"Session not found for {phone_number}"}


@router.post("/test")
async def test_whatsapp_message(phone_number: str, message: str):
    """
    Send test message (for development only)
    Usage: POST /api/whatsapp/test?phone_number=whatsapp:+1234567890&message=hi
    """
    # Format phone number if needed
    if not phone_number.startswith("whatsapp:"):
        phone_number = f"whatsapp:{phone_number}"
    
    sent = send_whatsapp_message(phone_number, message)
    return {"success": sent, "phone": phone_number, "message": message}


# ==================== DATABASE MODELS ====================
# These should be added to your models.py file

"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WhatsAppSessionDB(Base):
    __tablename__ = "whatsapp_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    current_state = Column(String)  # MENU, DEFECT_ORDER, etc.
    session_data = Column(JSON)  # Store form data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class WhatsAppLogDB(Base):
    __tablename__ = "whatsapp_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    message_type = Column(String)  # "incoming" or "outgoing"
    message_body = Column(Text)
    state_before = Column(String)  # Session state before message
    state_after = Column(String)   # Session state after message
    created_at = Column(DateTime, default=datetime.utcnow)
"""
