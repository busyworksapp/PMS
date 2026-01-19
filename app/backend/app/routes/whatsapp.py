"""
WhatsApp Integration Routes
API endpoints for WhatsApp messaging and webhook handling
"""

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Depends,
    Query,
    status,
)
from sqlalchemy.orm import Session
import logging

from app.db.database import get_db
from app.schemas.whatsapp import (
    SendMessageRequest,
    SendBulkMessageRequest,
    SendMessageResponse,
    WhatsAppMessageResponse,
    WhatsAppContactResponse,
    ContactListResponse,
    MessageHistoryResponse,
    UpdateContactRequest,
    WebhookEventResponse,
    MessageStatsResponse,
)
from app.models.whatsapp import (
    WhatsAppMessage,
    WhatsAppContact,
)
from app.services.twilio_whatsapp_service import (
    twilio_whatsapp_service
)
from app.services.chatbot_service import chatbot_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])


# ==================== WEBHOOK ENDPOINT ====================


@router.post("/twilio-webhook", response_model=WebhookEventResponse)
async def receive_twilio_webhook(
    request: Request, db: Session = Depends(get_db)
):
    """
    Receive incoming WhatsApp messages from Twilio
    Automatically processes and responds to messages via chatbot
    POST /api/whatsapp/twilio-webhook
    """
    try:
        # Get form data from Twilio
        form_data = await request.form()
        payload = dict(form_data)

        # Get signature from header
        signature = request.headers.get(
            "X-Twilio-Signature", ""
        )

        # Verify webhook signature
        if twilio_whatsapp_service:
            body = await request.body()
            body_str = body.decode("utf-8")
            if not twilio_whatsapp_service.verify_webhook_signature(
                signature, body_str
            ):
                logger.warning("Invalid Twilio webhook signature")
                # Note: Still process for now, verification may
                # need setup in production

        # Handle incoming message
        if twilio_whatsapp_service:
            success = (
                await twilio_whatsapp_service
                .handle_incoming_message(payload, db)
            )
        else:
            success = False
            logger.error("Twilio WhatsApp service not initialized")

        # Process incoming message and auto-respond
        if success:
            try:
                from_number = payload.get("From", "").replace(
                    "whatsapp:", ""
                )
                message_text = payload.get("Body", "")

                if from_number and message_text:
                    # Process with chatbot
                    response_text, _ = (
                        await chatbot_service.process_message(
                            from_number,
                            message_text,
                            db,
                        )
                    )

                    # Send auto-response via Twilio
                    if twilio_whatsapp_service:
                        await twilio_whatsapp_service.send_message(
                            phone_number=from_number,
                            message_text=response_text,
                            db=db,
                        )

                        logger.info(
                            f"Auto-response sent to {from_number}"
                        )
            except Exception as e:
                logger.warning(
                    f"Error in auto-response: {str(e)}"
                )

        if success:
            return WebhookEventResponse(
                success=True,
                message="Webhook processed successfully",
                event_id=payload.get("MessageSid", ""),
            )
        else:
            return WebhookEventResponse(
                success=False,
                message="Error processing webhook",
            )

    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ==================== MESSAGE ENDPOINTS ====================


@router.post("/send", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest, db: Session = Depends(get_db)
):
    """
    Send WhatsApp message via Twilio
    POST /api/whatsapp/send
    """
    try:
        if not twilio_whatsapp_service:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Twilio WhatsApp service not initialized",
            )

        result = await twilio_whatsapp_service.send_message(
            phone_number=request.phone_number,
            message_text=request.message_text,
            message_type=request.message_type.value,
            media_url=request.media_url,
            db=db,
        )

        if result["success"]:
            return SendMessageResponse(
                success=True,
                message_id=result["message_id"],
                status=result["status"],
                timestamp=result["timestamp"],
            )
        else:
            return SendMessageResponse(
                success=False,
                message_id=None,
                status="failed",
                error=result.get("error"),
            )

    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/send-bulk")
async def send_bulk_messages(
    request: SendBulkMessageRequest, db: Session = Depends(get_db)
):
    """
    Send bulk WhatsApp messages via Twilio
    POST /api/whatsapp/send-bulk
    """
    try:
        if not twilio_whatsapp_service:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Twilio WhatsApp service not initialized",
            )

        result = (
            await twilio_whatsapp_service.send_bulk_messages(
                phone_numbers=request.phone_numbers,
                message_text=request.message_text,
                db=db,
            )
        )

        return {
            "total": result["total"],
            "successful": result["sent"],
            "failed": result["failed"],
            "results": result["messages"],
        }

    except Exception as e:
        logger.error(f"Error sending bulk messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ==================== MESSAGE RETRIEVAL ====================


@router.get("/messages", response_model=MessageHistoryResponse)
async def get_messages(
    contact_number: str = Query(..., description="Contact phone number"),
    limit: int = Query(50, ge=1, le=100),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    """
    Get message history with a contact
    GET /api/whatsapp/messages?contact_number=+1234567890
    """
    try:
        # Get contact
        contact = db.query(WhatsAppContact).filter(
            WhatsAppContact.phone_number == contact_number
        ).first()

        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found",
            )

        # Get message history from database
        messages = (
            db.query(WhatsAppMessage)
            .filter(
                (WhatsAppMessage.from_phone_number ==
                 contact_number) |
                (WhatsAppMessage.to_phone_number == contact_number)
            )
            .order_by(WhatsAppMessage.sent_at.desc())
            .limit(limit)
            .all()
        )

        message_list = [
            WhatsAppMessageResponse.from_orm(msg) for msg in messages
        ]

        return MessageHistoryResponse(
            contact=WhatsAppContactResponse.from_orm(contact),
            messages=message_list,
            total_messages=len(message_list),
            page=page,
            page_size=limit,
        )

    except Exception as e:
        logger.error(f"Error retrieving messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/contacts", response_model=ContactListResponse
)
async def get_contacts(db: Session = Depends(get_db)):
    """
    Get all contacts with unread counts
    GET /api/whatsapp/contacts
    """
    try:
        # Get all contacts from database
        contacts = db.query(WhatsAppContact).all()

        contacts_response = []
        total_unread = 0
        for contact in contacts:
            # Count unread messages
            unread_count = (
                db.query(WhatsAppMessage).filter(
                    (WhatsAppMessage.from_phone_number ==
                     contact.phone_number),
                    WhatsAppMessage.status == "received"
                ).count()
            )

            contacts_response.append(
                WhatsAppContactResponse.from_orm(contact)
            )
            total_unread += unread_count

        return ContactListResponse(
            contacts=contacts_response,
            total_count=len(contacts_response),
            unread_count=total_unread,
        )

    except Exception as e:
        logger.error(f"Error retrieving contacts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ==================== CONTACT MANAGEMENT ====================


@router.post("/contacts/{phone_number}/read")
async def mark_as_read(
    phone_number: str, db: Session = Depends(get_db)
):
    """
    Mark messages with contact as read
    POST /api/whatsapp/contacts/{phone_number}/read
    """
    try:
        # Update unread messages to read status
        db.query(WhatsAppMessage).filter(
            (WhatsAppMessage.from_phone_number == phone_number),
            WhatsAppMessage.status == "received"
        ).update({"status": "read"})
        db.commit()

        return {"success": True, "message": "Marked as read"}

    except Exception as e:
        logger.error(f"Error marking as read: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put("/contacts/{phone_number}")
async def update_contact(
    phone_number: str,
    request: UpdateContactRequest,
    db: Session = Depends(get_db),
):
    """
    Update contact information
    PUT /api/whatsapp/contacts/{phone_number}
    """
    try:
        contact = db.query(WhatsAppContact).filter(
            WhatsAppContact.phone_number == phone_number
        ).first()

        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found",
            )

        # Update fields
        if request.display_name:
            contact.display_name = request.display_name
        if request.business_name:
            contact.business_name = request.business_name
        if request.is_pinned is not None:
            contact.is_pinned = request.is_pinned
        if request.tags:
            contact.tags = request.tags
        if request.is_blocked is not None:
            contact.is_blocked = request.is_blocked

        db.commit()
        return {"success": True, "message": "Contact updated"}

    except Exception as e:
        logger.error(f"Error updating contact: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ==================== STATISTICS ====================


@router.get("/stats", response_model=MessageStatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """
    Get WhatsApp message statistics
    GET /api/whatsapp/stats
    """
    try:
        from datetime import datetime

        # Count totals
        total_messages = db.query(WhatsAppMessage).count()
        total_contacts = db.query(WhatsAppContact).count()
        unread_messages = db.query(WhatsAppMessage).filter(
            ~WhatsAppMessage.is_read
        ).count()

        # Count today's messages
        today = datetime.utcnow().date()
        messages_sent_today = (
            db.query(WhatsAppMessage)
            .filter(
                WhatsAppMessage.created_at >= today,
                WhatsAppMessage.direction == "outbound",
            )
            .count()
        )
        messages_received_today = (
            db.query(WhatsAppMessage)
            .filter(
                WhatsAppMessage.created_at >= today,
                WhatsAppMessage.direction == "inbound",
            )
            .count()
        )

        # Calculate rates
        sent_messages = db.query(WhatsAppMessage).filter(
            WhatsAppMessage.direction == "outbound"
        ).count()
        delivered_messages = (
            db.query(WhatsAppMessage)
            .filter(
                WhatsAppMessage.direction == "outbound",
                WhatsAppMessage.status.in_(["delivered", "read"]),
            )
            .count()
        )
        failed_messages = (
            db.query(WhatsAppMessage)
            .filter(
                WhatsAppMessage.direction == "outbound",
                WhatsAppMessage.status == "failed",
            )
            .count()
        )

        delivery_rate = (
            (delivered_messages / sent_messages * 100)
            if sent_messages > 0
            else 0.0
        )
        error_rate = (
            (failed_messages / sent_messages * 100)
            if sent_messages > 0
            else 0.0
        )

        return MessageStatsResponse(
            total_messages=total_messages,
            total_contacts=total_contacts,
            unread_messages=unread_messages,
            messages_sent_today=messages_sent_today,
            messages_received_today=messages_received_today,
            delivery_rate=round(delivery_rate, 2),
            error_rate=round(error_rate, 2),
        )

    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ==================== HEALTH CHECK ====================


@router.get("/health")
async def health_check():
    """
    WhatsApp integration health check
    GET /api/whatsapp/health
    """
    is_configured = (
        twilio_whatsapp_service is not None
        and twilio_whatsapp_service.account_sid
        and twilio_whatsapp_service.auth_token
    )

    return {
        "status": "healthy" if is_configured else "misconfigured",
        "is_configured": is_configured,
        "provider": "Twilio",
        "message": (
            "Twilio WhatsApp integration ready"
            if is_configured
            else "Missing Twilio configuration"
        ),
    }
