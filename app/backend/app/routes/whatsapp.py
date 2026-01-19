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
from app.services.whatsapp_service import whatsapp_service
from app.services.chatbot_service import chatbot_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])


# ==================== WEBHOOK ENDPOINT ====================


@router.post("/webhook", response_model=WebhookEventResponse)
async def receive_webhook(
    request: Request, db: Session = Depends(get_db)
):
    """
    Receive incoming WhatsApp messages from Meta
    Automatically processes and responds to messages via chatbot
    POST /api/whatsapp/webhook
    """
    try:
        # Get signature from header
        signature = request.headers.get("X-Hub-Signature-256", "")

        # Get raw body
        body = await request.body()
        body_str = body.decode("utf-8")

        # Verify webhook signature
        if not await whatsapp_service.verify_webhook(
            signature, body_str
        ):
            logger.warning("Invalid webhook signature")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid signature",
            )

        # Parse payload
        payload = await request.json()

        # Handle webhook
        success = await whatsapp_service.handle_webhook(payload, db)

        # Process incoming message and auto-respond
        if success:
            # Extract message details
            try:
                messages = (
                    payload.get("entry", [{}])[0]
                    .get("changes", [{}])[0]
                    .get("value", {})
                    .get("messages", [])
                )

                if messages:
                    for msg in messages:
                        phone_from = msg.get("from")
                        message_text = (
                            msg.get("text", {}).get("body", "")
                        )

                        if phone_from and message_text:
                            # Process with chatbot
                            response_text, _ = (
                                await chatbot_service
                                .process_message(
                                    phone_from,
                                    message_text,
                                    db,
                                )
                            )

                            # Send auto-response via Twilio API
                            await chatbot_service.send_via_twilio_api(
                                phone_from, response_text
                            )

                            logger.info(
                                f"Auto-response sent to "
                                f"{phone_from}"
                            )
            except Exception as e:
                logger.warning(
                    f"Error in auto-response: {str(e)}"
                )

        if success:
            return WebhookEventResponse(
                success=True,
                message="Webhook processed successfully",
                event_id=payload.get("id"),
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
    Send WhatsApp message
    POST /api/whatsapp/send
    """
    try:
        result = await whatsapp_service.send_message(
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
    Send bulk WhatsApp messages
    POST /api/whatsapp/send-bulk
    """
    try:
        results = []
        for phone_number in request.phone_numbers:
            result = await whatsapp_service.send_message(
                phone_number=phone_number,
                message_text=request.message_text,
                db=db,
            )
            results.append(
                {
                    "phone_number": phone_number,
                    **result,
                }
            )

        return {
            "total": len(results),
            "successful": sum(
                1 for r in results if r["success"]
            ),
            "results": results,
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
    GET /api/whatsapp/messages?contact_number=+1234567890&limit=50
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

        # Get message history
        messages = await whatsapp_service.get_message_history(
            contact_number, limit=limit, db=db
        )

        return MessageHistoryResponse(
            contact=WhatsAppContactResponse.from_orm(contact),
            messages=[
                WhatsAppMessageResponse(**msg) for msg in messages
            ],
            total_messages=len(messages),
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
        contacts_data = await whatsapp_service.get_contacts(db=db)

        contacts = []
        total_unread = 0
        for contact_data in contacts_data:
            contacts.append(
                WhatsAppContactResponse(**contact_data)
            )
            total_unread += contact_data.get("unread_count", 0)

        return ContactListResponse(
            contacts=contacts,
            total_count=len(contacts),
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
        await whatsapp_service.mark_as_read(phone_number, db=db)
        return {"success": True, "message": "Marked as read"}

    except Exception as e:
        logger.error(f"Error marking as read: {str(e)}")
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
        whatsapp_service.business_account_id
        and whatsapp_service.phone_number_id
        and whatsapp_service.api_token
    )

    return {
        "status": "healthy" if is_configured else "misconfigured",
        "is_configured": is_configured,
        "message": (
            "WhatsApp integration ready"
            if is_configured
            else "Missing configuration"
        ),
    }
