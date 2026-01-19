"""
WhatsApp Integration Service
Handles WhatsApp API interactions with Meta Cloud API
"""

import os
import logging
import hmac
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any
import httpx
from sqlalchemy.orm import Session

from app.models.whatsapp import (
    WhatsAppMessage,
    WhatsAppContact,
    WhatsAppWebhook,
)
from app.db.database import SessionLocal

logger = logging.getLogger(__name__)


class WhatsAppService:
    """
    WhatsApp Cloud API Service
    Handles all interactions with Meta WhatsApp Business Cloud API
    """

    def __init__(
        self,
        business_account_id: str,
        phone_number_id: str,
        api_token: str,
        webhook_verify_token: str,
    ):
        """Initialize WhatsApp service with credentials"""
        self.business_account_id = business_account_id
        self.phone_number_id = phone_number_id
        self.api_token = api_token
        self.webhook_verify_token = webhook_verify_token
        self.base_url = "https://graph.instagram.com/v18.0"
        self.timeout = 30

    async def send_message(
        self,
        phone_number: str,
        message_text: str,
        message_type: str = "text",
        media_url: Optional[str] = None,
        db: Optional[Session] = None,
    ) -> Dict[str, Any]:
        """
        Send WhatsApp message
        
        Args:
            phone_number: Recipient phone number
            message_text: Message content
            message_type: Type of message (text, image, video, document, audio)
            media_url: URL to media (if applicable)
            db: Database session
            
        Returns:
            Dict with message_id, status, and timestamp
        """
        try:
            if db is None:
                db = SessionLocal()

            # Prepare payload based on message type
            if message_type == "text":
                payload = {
                    "messaging_product": "whatsapp",
                    "to": phone_number,
                    "type": "text",
                    "text": {"body": message_text},
                }
            else:
                # Handle media messages
                media_object = self._get_media_object(
                    message_type, media_url
                )
                payload = {
                    "messaging_product": "whatsapp",
                    "to": phone_number,
                    "type": message_type,
                    message_type: media_object,
                }

            # Send to Meta API
            message_id = await self._call_meta_api(
                f"/{self.phone_number_id}/messages",
                method="POST",
                data=payload,
            )

            # Store in database
            db_message = WhatsAppMessage(
                message_id=message_id,
                from_phone_number=f"+{self.phone_number_id}",
                to_phone_number=phone_number,
                message_type=message_type,
                message_text=message_text,
                media_url=media_url,
                status="sent",
                direction="outbound",
                sent_at=datetime.utcnow(),
            )
            db.add(db_message)

            # Update or create contact
            contact = db.query(WhatsAppContact).filter(
                WhatsAppContact.phone_number == phone_number
            ).first()
            if not contact:
                contact = WhatsAppContact(
                    phone_number=phone_number,
                    display_name=phone_number,
                )
                db.add(contact)
            contact.last_message_time = datetime.utcnow()
            db.commit()

            logger.info(f"Message sent to {phone_number}: {message_id}")

            return {
                "success": True,
                "message_id": message_id,
                "status": "sent",
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return {
                "success": False,
                "message_id": None,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def handle_webhook(
        self, payload: Dict[str, Any], db: Optional[Session] = None
    ) -> bool:
        """
        Process incoming webhook from Meta
        
        Args:
            payload: Webhook payload from Meta
            db: Database session
            
        Returns:
            True if processing successful
        """
        try:
            if db is None:
                db = SessionLocal()

            # Store webhook event
            webhook_event = WhatsAppWebhook(
                webhook_id=payload.get("id"),
                event_type=payload.get("type"),
                payload=payload,
            )
            db.add(webhook_event)
            db.commit()

            # Process based on type
            event_type = payload.get("type")

            if event_type == "message":
                await self._process_message_event(payload, db)
            elif event_type == "status_update":
                await self._process_status_update(payload, db)
            elif event_type == "template_status":
                await self._process_template_status(payload, db)

            # Mark as processed
            webhook_event.processed = True
            webhook_event.processed_at = datetime.utcnow()
            db.commit()

            logger.info(f"Webhook processed: {event_type}")
            return True

        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            if db:
                webhook_event.processing_error = str(e)
                webhook_event.retry_count += 1
                db.commit()
            return False

    async def _process_message_event(
        self, payload: Dict[str, Any], db: Session
    ) -> None:
        """Process incoming message event"""
        message_data = payload.get("message", {})
        contact_phone = message_data.get("from")
        message_text = message_data.get("text", {}).get("body", "")
        message_type = message_data.get("type", "text")

        # Store message
        db_message = WhatsAppMessage(
            message_id=message_data.get("id"),
            from_phone_number=contact_phone,
            to_phone_number=f"+{self.phone_number_id}",
            message_type=message_type,
            message_text=message_text,
            status="delivered",
            direction="inbound",
        )
        db.add(db_message)

        # Update or create contact
        contact = db.query(WhatsAppContact).filter(
            WhatsAppContact.phone_number == contact_phone
        ).first()
        if not contact:
            contact = WhatsAppContact(
                phone_number=contact_phone,
                display_name=contact_phone,
            )
            db.add(contact)

        contact.last_message_time = datetime.utcnow()
        contact.unread_count += 1
        db.commit()

    async def _process_status_update(
        self, payload: Dict[str, Any], db: Session
    ) -> None:
        """Process message status update from Meta"""
        status_data = payload.get("status", {})
        message_id = status_data.get("id")
        status = status_data.get("status")
        timestamp = status_data.get("timestamp")

        # Update message status
        db_message = db.query(WhatsAppMessage).filter(
            WhatsAppMessage.message_id == message_id
        ).first()
        if db_message:
            db_message.status = status
            if status == "delivered":
                db_message.delivered_at = datetime.fromtimestamp(
                    int(timestamp)
                )
            elif status == "read":
                db_message.read_at = datetime.fromtimestamp(
                    int(timestamp)
                )
            db.commit()

    async def _process_template_status(
        self, payload: Dict[str, Any], db: Session
    ) -> None:
        """Process template approval/rejection status"""
        template_data = payload.get("template", {})
        logger.info(f"Template status update: {template_data}")

    async def verify_webhook(self, signature: str, body: str) -> bool:
        """
        Verify webhook signature from Meta
        
        Args:
            signature: X-Hub-Signature header value
            body: Request body
            
        Returns:
            True if signature is valid
        """
        expected_signature = (
            "sha256="
            + hmac.new(
                self.webhook_verify_token.encode(),
                body.encode(),
                hashlib.sha256,
            ).hexdigest()
        )
        return hmac.compare_digest(signature, expected_signature)

    async def get_message_history(
        self,
        phone_number: str,
        limit: int = 50,
        db: Optional[Session] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get message history with a contact
        
        Args:
            phone_number: Contact phone number
            limit: Number of messages to retrieve
            db: Database session
            
        Returns:
            List of messages
        """
        if db is None:
            db = SessionLocal()

        messages = (
            db.query(WhatsAppMessage)
            .filter(
                (WhatsAppMessage.from_phone_number == phone_number)
                | (WhatsAppMessage.to_phone_number == phone_number)
            )
            .order_by(WhatsAppMessage.created_at.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": msg.id,
                "message_id": msg.message_id,
                "from": msg.from_phone_number,
                "to": msg.to_phone_number,
                "type": msg.message_type,
                "text": msg.message_text,
                "status": msg.status,
                "direction": msg.direction,
                "is_read": msg.is_read,
                "created_at": msg.created_at.isoformat(),
                "sent_at": msg.sent_at.isoformat() if msg.sent_at else None,
                "delivered_at": (
                    msg.delivered_at.isoformat() if msg.delivered_at else None
                ),
                "read_at": msg.read_at.isoformat() if msg.read_at else None,
            }
            for msg in reversed(messages)
        ]

    async def get_contacts(
        self, db: Optional[Session] = None
    ) -> List[Dict[str, Any]]:
        """Get all contacts with unread counts"""
        if db is None:
            db = SessionLocal()

        contacts = db.query(WhatsAppContact).all()

        return [
            {
                "id": contact.id,
                "phone_number": contact.phone_number,
                "display_name": contact.display_name
                or contact.phone_number,
                "business_name": contact.business_name,
                "profile_picture_url": contact.profile_picture_url,
                "status_text": contact.status_text,
                "is_verified": contact.is_verified,
                "is_blocked": contact.is_blocked,
                "is_pinned": contact.is_pinned,
                "last_message_time": (
                    contact.last_message_time.isoformat()
                    if contact.last_message_time
                    else None
                ),
                "unread_count": contact.unread_count,
                "conversation_closed": contact.conversation_closed,
                "tags": contact.tags,
                "created_at": contact.created_at.isoformat(),
            }
            for contact in contacts
        ]

    async def mark_as_read(
        self, phone_number: str, db: Optional[Session] = None
    ) -> bool:
        """Mark all messages with contact as read"""
        if db is None:
            db = SessionLocal()

        db.query(WhatsAppMessage).filter(
            (WhatsAppMessage.from_phone_number == phone_number)
            & (WhatsAppMessage.direction == "inbound")
            & ~WhatsAppMessage.is_read
        ).update({WhatsAppMessage.is_read: True})

        contact = db.query(WhatsAppContact).filter(
            WhatsAppContact.phone_number == phone_number
        ).first()
        if contact:
            contact.unread_count = 0
            db.commit()

        return True

    async def _call_meta_api(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Call Meta WhatsApp API
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Request body
            
        Returns:
            Response data or message_id
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if method == "GET":
                response = await client.get(url, headers=headers)
            elif method == "POST":
                response = await client.post(
                    url, headers=headers, json=data
                )
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            result = response.json()

            if "messages" in result:
                return result["messages"][0]["id"]
            return result.get("id", "")

    def _get_media_object(
        self, media_type: str, media_url: str
    ) -> Dict[str, Any]:
        """Get media object based on type"""
        if media_type == "image":
            return {"link": media_url}
        elif media_type == "video":
            return {"link": media_url}
        elif media_type == "audio":
            return {"link": media_url}
        elif media_type == "document":
            return {"link": media_url}
        else:
            return {"link": media_url}


# Initialize service from environment
whatsapp_service = WhatsAppService(
    business_account_id=os.getenv(
        "WHATSAPP_BUSINESS_ACCOUNT_ID", ""
    ),
    phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID", ""),
    api_token=os.getenv("WHATSAPP_API_TOKEN", ""),
    webhook_verify_token=os.getenv(
        "WHATSAPP_WEBHOOK_VERIFY_TOKEN", ""
    ),
)
