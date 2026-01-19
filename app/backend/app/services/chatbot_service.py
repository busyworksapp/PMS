"""
WhatsApp Chatbot Service
Handles conversational interactions and intelligent message responses
Integrates with Twilio WhatsApp API to send real replies
"""

import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from twilio.rest import Client

logger = logging.getLogger(__name__)


class ChatbotService:
    """
    WhatsApp Chatbot Service
    Processes incoming messages and generates intelligent responses
    """

    # Menu options
    MAIN_MENU = """🤖 *Welcome to Barron Production System*

Select an option:
1️⃣ Check Order Status
2️⃣ Report Defect
3️⃣ View Production Schedule
4️⃣ Get Help
5️⃣ Back to Menu

*Just reply with the number!*"""

    ORDER_MENU = """📦 *Order Status Menu*

What would you like to do?
1️⃣ Check your orders
2️⃣ Track specific order
3️⃣ Check estimated delivery
4️⃣ Back to Menu

Reply with the number"""

    DEFECT_MENU = """⚠️ *Report Defect*

1️⃣ Report a defect
2️⃣ View defect history
3️⃣ Track defect resolution
4️⃣ Back to Menu

Reply with the number"""

    SCHEDULE_MENU = """📅 *Production Schedule*

1️⃣ Today's schedule
2️⃣ This week's schedule
3️⃣ Production status
4️⃣ Back to Menu

Reply with the number"""

    HELP_MENU = """🆘 *Help & Support*

1️⃣ FAQs
2️⃣ Contact Support
3️⃣ Report Issue
4️⃣ Back to Menu

Reply with the number"""

    def __init__(self):
        """Initialize chatbot service"""
        self.conversation_states = {}

    def get_user_state(
        self, phone_number: str
    ) -> Dict[str, Any]:
        """Get or create user conversation state"""
        if phone_number not in self.conversation_states:
            self.conversation_states[phone_number] = {
                "state": "main_menu",
                "last_interaction": datetime.now(),
                "order_id": None,
                "context": {},
            }
        return self.conversation_states[phone_number]

    def set_user_state(
        self, phone_number: str, state: str
    ) -> None:
        """Update user conversation state"""
        if phone_number in self.conversation_states:
            self.conversation_states[phone_number]["state"] = state
            self.conversation_states[
                phone_number
            ]["last_interaction"] = datetime.now()

    async def process_message(
        self,
        phone_number: str,
        message_text: str,
        db: Session,
    ) -> tuple[str, Optional[List[Dict[str, str]]]]:
        """
        Process incoming message and generate response

        Returns: (response_text, interactive_buttons)
        """
        message_text = message_text.strip().lower()
        user_state = self.get_user_state(phone_number)
        current_state = user_state["state"]

        logger.info(
            f"Processing message from {phone_number}: "
            f"'{message_text}' in state: {current_state}"
        )

        # Handle greeting messages
        if message_text in ["hi", "hello", "hey", "start", "menu"]:
            return self.MAIN_MENU, None

        # Handle main menu selections
        if current_state == "main_menu":
            return self._handle_main_menu(
                message_text, phone_number, db
            )

        # Handle order menu
        if current_state == "order_menu":
            return self._handle_order_menu(
                message_text, phone_number, db
            )

        # Handle defect menu
        if current_state == "defect_menu":
            return self._handle_defect_menu(
                message_text, phone_number, db
            )

        # Handle schedule menu
        if current_state == "schedule_menu":
            return self._handle_schedule_menu(
                message_text, phone_number, db
            )

        # Handle help menu
        if current_state == "help_menu":
            return self._handle_help_menu(
                message_text, phone_number, db
            )

        # Handle order details
        if current_state == "order_details":
            return self._handle_order_details(
                message_text, phone_number, db
            )

        # Handle defect report
        if current_state == "defect_report":
            return self._handle_defect_report(
                message_text, phone_number, db
            )

        # Default response
        return "Sorry, I didn't understand. Type *menu* for options", None

    def _handle_main_menu(
        self, message_text: str, phone_number: str, db: Session
    ) -> tuple[str, None]:
        """Handle main menu selections"""
        if message_text == "1":
            self.set_user_state(phone_number, "order_menu")
            return self.ORDER_MENU, None

        elif message_text == "2":
            self.set_user_state(phone_number, "defect_menu")
            return self.DEFECT_MENU, None

        elif message_text == "3":
            self.set_user_state(phone_number, "schedule_menu")
            return self.SCHEDULE_MENU, None

        elif message_text == "4":
            self.set_user_state(phone_number, "help_menu")
            return self.HELP_MENU, None

        elif message_text == "5":
            return self.MAIN_MENU, None

        else:
            return (
                "Invalid option. "
                "Please select 1-5 from the menu.",
                None,
            )

    def _handle_order_menu(
        self, message_text: str, phone_number: str, db: Session
    ) -> tuple[str, None]:
        """Handle order menu selections"""
        if message_text == "1":
            # Show recent orders
            self.set_user_state(phone_number, "order_list")
            response = (
                "📦 *Your Recent Orders*\n\n"
                "ORD-001: In Production (Est. 5 days)\n"
                "ORD-002: Quality Check (Est. 2 days)\n"
                "ORD-003: Completed ✅\n\n"
                "Reply with order number to track"
            )
            return response, None

        elif message_text == "2":
            self.set_user_state(phone_number, "order_details")
            return (
                "📦 Enter order number "
                "(e.g., ORD-001):",
                None,
            )

        elif message_text == "3":
            response = (
                "🚚 *Estimated Delivery*\n\n"
                "ORD-001: 5 business days\n"
                "ORD-002: 2 business days\n\n"
                "Reply 1️⃣ for Order Menu or "
                "type *menu* for Main Menu"
            )
            return response, None

        elif message_text == "4":
            self.set_user_state(phone_number, "main_menu")
            return self.MAIN_MENU, None

        else:
            return (
                "Invalid option. "
                "Please select 1-4 from the menu.",
                None,
            )

    def _handle_defect_menu(
        self, message_text: str, phone_number: str, db: Session
    ) -> tuple[str, None]:
        """Handle defect menu selections"""
        if message_text == "1":
            self.set_user_state(phone_number, "defect_report")
            return (
                "⚠️ *Report a Defect*\n\n"
                "Please describe the defect:\n"
                "(Type your message, max 500 chars)",
                None,
            )

        elif message_text == "2":
            # Get user's defect reports
            try:
                from app.models.whatsapp import WhatsAppMessage
                
                defects = db.query(WhatsAppMessage).filter(
                    WhatsAppMessage.from_phone_number == phone_number,
                    WhatsAppMessage.message_type == "text",
                    WhatsAppMessage.status == "submitted",
                    WhatsAppMessage.direction == "inbound"
                ).all()
                
                if not defects:
                    response = (
                        "📋 *Your Defect Reports*\n\n"
                        "No defect reports yet.\n\n"
                        "Reply 1️⃣ to submit one"
                    )
                else:
                    response = "📋 *Your Defect Reports*\n\n"
                    for i, defect in enumerate(defects[-5:], 1):  # Last 5
                        date_str = defect.sent_at.strftime('%Y-%m-%d')
                        response += (
                            f"{i}. ID: {defect.message_id}\n"
                            f"   {defect.message_text[:30]}...\n"
                            f"   Date: {date_str}\n\n"
                        )
                    response += "Reply 1️⃣ for Defect Menu"
            except Exception:
                response = (
                    "Error retrieving defects."
                    "Please try again.\n\n"
                    "Reply 1️⃣ for Defect Menu"
                )

            return response, None

        elif message_text == "3":
            response = (
                "🔄 *Defect Resolution Status*\n\n"
                "DEF-001: 60% complete\n"
                "DEF-003: 45% complete\n\n"
                "Reply 1️⃣ for Defect Menu"
            )
            return response, None

        elif message_text == "4":
            self.set_user_state(phone_number, "main_menu")
            return self.MAIN_MENU, None

        else:
            return (
                "Invalid option. "
                "Please select 1-4 from the menu.",
                None,
            )

    def _handle_schedule_menu(
        self, message_text: str, phone_number: str, db: Session
    ) -> tuple[str, None]:
        """Handle production schedule menu"""
        if message_text == "1":
            response = (
                "📅 *Today's Schedule*\n\n"
                "09:00 - 10:30: Assembly (Line 1)\n"
                "10:30 - 12:00: Quality Check\n"
                "13:00 - 15:00: Packaging\n"
                "15:00 - 16:30: Inspection\n\n"
                "✅ All tasks on track"
            )
            return response, None

        elif message_text == "2":
            response = (
                "📅 *This Week's Schedule*\n\n"
                "Monday: Assembly & QC\n"
                "Tuesday: Assembly & Packaging\n"
                "Wednesday: QC & Inspection\n"
                "Thursday: Packaging & Dispatch\n"
                "Friday: Final Review\n\n"
                "✅ Schedule on track"
            )
            return response, None

        elif message_text == "3":
            response = (
                "⚙️ *Production Status*\n\n"
                "Lines Running: 3/3 ✅\n"
                "Completion Rate: 94%\n"
                "Quality Score: 98.5%\n"
                "On-time Delivery: 99%\n\n"
                "Production Status: *OPTIMAL* 🟢"
            )
            return response, None

        elif message_text == "4":
            self.set_user_state(phone_number, "main_menu")
            return self.MAIN_MENU, None

        else:
            return (
                "Invalid option. "
                "Please select 1-4 from the menu.",
                None,
            )

    def _handle_help_menu(
        self, message_text: str, phone_number: str, db: Session
    ) -> tuple[str, None]:
        """Handle help menu selections"""
        if message_text == "1":
            response = (
                "❓ *Frequently Asked Questions*\n\n"
                "Q: How to track my order?\n"
                "A: Select option 1 from main menu\n\n"
                "Q: How long is delivery?\n"
                "A: Typically 5-7 business days\n\n"
                "Q: How to report defects?\n"
                "A: Select option 2 from main menu\n\n"
                "Type *menu* to return"
            )
            return response, None

        elif message_text == "2":
            response = (
                "📞 *Contact Support*\n\n"
                "Email: support@barron.co.za\n"
                "Phone: +27 (0)11 XXX XXXX\n"
                "Hours: Mon-Fri 8:00 AM - 5:00 PM\n\n"
                "Type *menu* to return"
            )
            return response, None

        elif message_text == "3":
            self.set_user_state(phone_number, "defect_report")
            return (
                "📝 *Report an Issue*\n\n"
                "Please describe the issue "
                "you're experiencing:",
                None,
            )

        elif message_text == "4":
            self.set_user_state(phone_number, "main_menu")
            return self.MAIN_MENU, None

        else:
            return (
                "Invalid option. "
                "Please select 1-4 from the menu.",
                None,
            )

    def _handle_order_details(
        self, message_text: str, phone_number: str, db: Session
    ) -> tuple[str, None]:
        """Handle order details request"""
        order_id = message_text.upper()

        # Simulate order lookup
        if order_id.startswith("ORD-"):
            response = (
                f"📦 *Order Details: {order_id}*\n\n"
                f"Status: In Production\n"
                f"Created: 2025-01-10\n"
                f"Quantity: 100 units\n"
                f"Est. Completion: 2025-01-25\n"
                f"Quality Score: 99%\n\n"
                f"🟢 On Schedule\n\n"
                f"Reply 1️⃣ for Order Menu"
            )
            self.set_user_state(phone_number, "order_menu")
            return response, None
        else:
            return (
                "Invalid order number. "
                "Please use format: ORD-001",
                None,
            )

    def _handle_defect_report(
        self, message_text: str, phone_number: str, db: Session
    ) -> tuple[str, None]:
        """Handle defect report submission"""
        if len(message_text) < 10:
            return (
                "Please provide more details "
                "(at least 10 characters)",
                None,
            )

        # Save defect report to database
        try:
            from app.models.whatsapp import WhatsAppMessage
            
            defect_id = f"DEF-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Store in WhatsApp messages with defect marker
            defect_msg = WhatsAppMessage(
                message_id=defect_id,
                from_phone_number=phone_number,
                to_phone_number=phone_number,
                message_type="text",
                message_text=message_text,
                status="submitted",
                direction="inbound",
                sent_at=datetime.utcnow(),
            )
            db.add(defect_msg)
            db.commit()

            response = (
                "✅ *Defect Report Submitted*\n\n"
                f"Report ID: {defect_id}\n"
                f"Description: {message_text[:40]}...\n"
                f"Status: Under Review\n\n"
                f"We'll investigate and follow up soon.\n\n"
                f"Reply 1️⃣ for Defect Menu or "
                f"type *menu*"
            )
        except Exception:
            response = (
                "❌ Error saving report. "
                "Please try again.\n\n"
                "Reply 1️⃣ for Defect Menu"
            )

        self.set_user_state(phone_number, "main_menu")
        return response, None

    async def send_via_twilio_api(
        self,
        phone_number: str,
        message_text: str,
    ) -> bool:
        """
        Send message to user via Twilio WhatsApp API

        Args:
            phone_number: Recipient phone number with format
                whatsapp:+27123456789
            message_text: Message text to send

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Get credentials from environment
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

            if not account_sid or not auth_token or not twilio_whatsapp_number:
                logger.error("Missing Twilio credentials")
                return False

            # Initialize Twilio client
            client = Client(account_sid, auth_token)

            # Ensure phone number has whatsapp: prefix
            if not phone_number.startswith("whatsapp:"):
                phone_number = f"whatsapp:{phone_number}"

            # Send message via Twilio
            message = client.messages.create(
                body=message_text,
                from_=twilio_whatsapp_number,
                to=phone_number,
            )

            logger.info(
                f"Message sent via Twilio to {phone_number}: "
                f"SID={message.sid}"
            )
            return True

        except Exception as e:
            logger.error(f"Error sending via Twilio API: {str(e)}")
            return False


# Initialize global chatbot service
chatbot_service = ChatbotService()
