"""
Twilio WhatsApp Integration Service
Handles WhatsApp messaging via Twilio API
"""

import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
import base64
import hmac
import hashlib

from twilio.rest import Client
from app.models.whatsapp import (
    WhatsAppMessage,
    WhatsAppContact,
)
from app.db.database import SessionLocal
from app.core.config import settings

logger = logging.getLogger(__name__)


class TwilioWhatsAppService:
    """
    Twilio WhatsApp Service
    Handles all interactions with Twilio WhatsApp API
    """

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        twilio_whatsapp_number: str,
    ):
        """Initialize Twilio WhatsApp service with credentials"""
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_whatsapp_number = twilio_whatsapp_number
        
        # Initialize Twilio client
        try:
            self.client = Client(account_sid, auth_token)
            logger.info("✓ Twilio WhatsApp service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twilio client: {str(e)}")
            raise

    async def send_message(
        self,
        phone_number: str,
        message_text: str,
        message_type: str = "text",
        media_url: Optional[str] = None,
        db: Optional[Session] = None,
    ) -> Dict[str, Any]:
        """
        Send WhatsApp message via Twilio

        Args:
            phone_number: Recipient phone number (with country code)
            message_text: Message content
            message_type: Type of message
            media_url: URL to media (if applicable)
            db: Database session

        Returns:
            Dict with message_id, status, and timestamp
        """
        try:
            if db is None:
                db = SessionLocal()

            # Format phone number for Twilio WhatsApp
            if not phone_number.startswith("whatsapp:"):
                if not phone_number.startswith("+"):
                    phone_number = "+" + phone_number
                phone_number = f"whatsapp:{phone_number}"

            logger.info(f"Sending WhatsApp message to {phone_number}")

            # Send message based on type
            if message_type == "text":
                message = self.client.messages.create(
                    from_=self.twilio_whatsapp_number,
                    to=phone_number,
                    body=message_text,
                )
            else:
                # Send media messages
                msg_body = (
                    message_text if message_text else f"Shared {message_type}"
                )
                message = self.client.messages.create(
                    from_=self.twilio_whatsapp_number,
                    to=phone_number,
                    body=msg_body,
                    media_url=media_url,
                )

            message_id = message.sid

            # Store in database
            db_message = WhatsAppMessage(
                message_id=message_id,
                from_phone_number=self.twilio_whatsapp_number,
                to_phone_number=phone_number.replace("whatsapp:", ""),
                message_type=message_type,
                message_text=message_text,
                media_url=media_url,
                status="sent",
                direction="outbound",
                sent_at=datetime.utcnow(),
            )
            db.add(db_message)

            # Update or create contact
            clean_phone = phone_number.replace("whatsapp:", "")
            contact = db.query(WhatsAppContact).filter(
                WhatsAppContact.phone_number == clean_phone
            ).first()
            if not contact:
                contact = WhatsAppContact(
                    phone_number=clean_phone,
                    display_name=clean_phone,
                    is_active=True,
                )
                db.add(contact)
            contact.last_message_time = datetime.utcnow()
            db.commit()

            logger.info(f"Message sent successfully: {message_id}")

            return {
                "success": True,
                "message_id": message_id,
                "status": "sent",
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            if db:
                db.rollback()
            return {
                "success": False,
                "message_id": None,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def send_bulk_messages(
        self,
        phone_numbers: List[str],
        message_text: str,
        db: Optional[Session] = None,
    ) -> Dict[str, Any]:
        """
        Send bulk WhatsApp messages
        
        Args:
            phone_numbers: List of recipient phone numbers
            message_text: Message content
            db: Database session
            
        Returns:
            Dict with results summary
        """
        results = {
            "total": len(phone_numbers),
            "sent": 0,
            "failed": 0,
            "messages": [],
        }

        for phone_number in phone_numbers:
            result = await self.send_message(
                phone_number=phone_number,
                message_text=message_text,
                db=db,
            )
            results["messages"].append(result)
            if result["success"]:
                results["sent"] += 1
            else:
                results["failed"] += 1

        return results

    def verify_webhook_signature(
        self,
        signature: str,
        request_body: str
    ) -> bool:
        """
        Verify Twilio webhook signature for security
        
        Args:
            signature: X-Twilio-Signature header value
            request_body: Raw request body
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Construct the URL (Twilio uses the full request URL)
            # Note: In production, use the actual webhook URL
            url = "https://your-domain.com/api/whatsapp/twilio-webhook"

            # Create the signature hash
            mac = hmac.new(
                self.auth_token.encode(),
                (url + request_body).encode(),
                hashlib.sha1
            )
            computed_signature = base64.b64encode(
                mac.digest()
            ).decode()
            
            # Compare signatures
            return hmac.compare_digest(signature, computed_signature)
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {str(e)}")
            return False

    async def handle_incoming_message(
        self,
        payload: Dict[str, Any],
        db: Optional[Session] = None,
    ) -> bool:
        """
        Process incoming webhook from Twilio
        
        Args:
            payload: Webhook payload from Twilio
            db: Database session
            
        Returns:
            True if processed successfully
        """
        try:
            if db is None:
                db = SessionLocal()

            # Extract message details from Twilio webhook
            message_sid = payload.get("MessageSid")
            from_number = payload.get("From", "").replace("whatsapp:", "")
            message_text = payload.get("Body", "")
            num_media = int(payload.get("NumMedia", 0))

            log_msg = (
                f"Received WhatsApp message from {from_number}: "
                f"{message_sid}"
            )
            logger.info(log_msg)

            # Create database message record
            media_url = None
            if num_media > 0:
                media_url = payload.get("MediaUrl0")

            db_message = WhatsAppMessage(
                message_id=message_sid,
                from_phone_number=from_number,
                to_phone_number=(
                    self.twilio_whatsapp_number.replace("whatsapp:", "")
                ),
                message_type="text" if num_media == 0 else "media",
                message_text=message_text,
                media_url=media_url,
                status="received",
                direction="inbound",
                created_at=datetime.utcnow(),
            )
            db.add(db_message)

            # Update or create contact
            contact = db.query(WhatsAppContact).filter(
                WhatsAppContact.phone_number == from_number
            ).first()
            if not contact:
                contact = WhatsAppContact(
                    phone_number=from_number,
                    display_name=from_number,
                    is_active=True,
                )
                db.add(contact)
            contact.last_message_time = datetime.utcnow()
            
            db.commit()
            logger.info(f"Message processed: {message_sid}")

            return True

        except Exception as e:
            logger.error(f"Error handling webhook: {str(e)}")
            if db:
                db.rollback()
            return False

    def get_contact_status(self, phone_number: str) -> Dict[str, Any]:
        """
        Get contact status via Twilio
        
        Args:
            phone_number: Phone number to check
            
        Returns:
            Dict with contact information
        """
        try:
            # Format phone number
            if not phone_number.startswith("+"):
                phone_number = "+" + phone_number

            # In Twilio, you would use the Lookups API for this
            # This is a basic implementation
            return {
                "phone_number": phone_number,
                "status": "active",
                "carrier": "unknown",
            }
        except Exception as e:
            logger.error(f"Error getting contact status: {str(e)}")
            return {
                "phone_number": phone_number,
                "status": "error",
                "error": str(e),
            }


# Initialize Twilio WhatsApp service
try:
    twilio_whatsapp_service = TwilioWhatsAppService(
        account_sid=settings.TWILIO_ACCOUNT_SID,
        auth_token=settings.TWILIO_AUTH_TOKEN,
        twilio_whatsapp_number=settings.TWILIO_WHATSAPP_NUMBER,
    )
    logger.info("✓ Twilio WhatsApp Service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Twilio WhatsApp Service: {str(e)}")
    twilio_whatsapp_service = None
