"""
WhatsApp Integration Pydantic Schemas
Request/Response models for WhatsApp API endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MessageTypeEnum(str, Enum):
    """Message types"""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    TEMPLATE = "template"


class MessageStatusEnum(str, Enum):
    """Message status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


# ==================== REQUEST SCHEMAS ====================

class SendMessageRequest(BaseModel):
    """Request to send a WhatsApp message"""
    phone_number: str = Field(
        ..., description="Recipient phone number with country code"
    )
    message_text: str = Field(..., description="Message content")
    media_url: Optional[str] = Field(
        None, description="URL to media file (if sending media)"
    )
    message_type: MessageTypeEnum = Field(
        MessageTypeEnum.TEXT, description="Type of message"
    )
    template_name: Optional[str] = Field(
        None, description="Template name (if using template)"
    )
    template_variables: Optional[List[str]] = Field(
        None, description="Variables for template"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Custom metadata"
    )


class SendBulkMessageRequest(BaseModel):
    """Request to send bulk messages"""
    phone_numbers: List[str] = Field(
        ..., description="List of recipient phone numbers"
    )
    message_text: str = Field(..., description="Message content")
    template_name: Optional[str] = Field(None, description="Template name")
    priority: int = Field(0, description="Message priority")
    scheduled_for: Optional[datetime] = Field(
        None, description="Schedule message for later"
    )


class MarkAsReadRequest(BaseModel):
    """Request to mark message as read"""
    message_ids: List[int] = Field(
        ..., description="List of message IDs to mark as read"
    )


class UpdateContactRequest(BaseModel):
    """Request to update contact information"""
    phone_number: str
    display_name: Optional[str] = None
    business_name: Optional[str] = None
    is_pinned: Optional[bool] = None
    tags: Optional[List[str]] = None
    is_blocked: Optional[bool] = None


# ==================== RESPONSE SCHEMAS ====================

class WhatsAppMessageResponse(BaseModel):
    """WhatsApp message response"""
    id: int
    message_id: Optional[str] = None
    from_phone_number: str
    to_phone_number: str
    message_type: str
    message_text: Optional[str] = None
    status: str
    direction: str
    is_read: bool
    created_at: datetime
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class WhatsAppContactResponse(BaseModel):
    """WhatsApp contact response"""
    id: int
    phone_number: str
    display_name: Optional[str] = None
    business_name: Optional[str] = None
    profile_picture_url: Optional[str] = None
    status_text: Optional[str] = None
    is_verified: bool
    is_blocked: bool
    is_pinned: bool
    last_message_time: Optional[datetime] = None
    unread_count: int
    conversation_closed: bool
    tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WhatsAppConversationResponse(BaseModel):
    """Full conversation with contact"""
    contact: WhatsAppContactResponse
    messages: List[WhatsAppMessageResponse]
    unread_count: int


class SendMessageResponse(BaseModel):
    """Response after sending message"""
    success: bool
    message_id: str
    status: str
    timestamp: datetime
    error: Optional[str] = None


class WhatsAppStatusResponse(BaseModel):
    """WhatsApp service status"""
    is_connected: bool
    business_account_id: Optional[str]
    phone_number: Optional[str]
    webhook_url: Optional[str]
    last_api_call: Optional[datetime]
    rate_limit_remaining: Optional[int]


class WebhookEventResponse(BaseModel):
    """Webhook event response"""
    success: bool
    message: str
    event_id: Optional[str] = None


class MessageStatsResponse(BaseModel):
    """Message statistics"""
    total_messages: int
    total_contacts: int
    unread_messages: int
    messages_sent_today: int
    messages_received_today: int
    delivery_rate: float  # percentage
    error_rate: float  # percentage


class ContactListResponse(BaseModel):
    """List of contacts"""
    contacts: List[WhatsAppContactResponse]
    total_count: int
    unread_count: int


class MessageHistoryResponse(BaseModel):
    """Message history for a contact"""
    contact: WhatsAppContactResponse
    messages: List[WhatsAppMessageResponse]
    total_messages: int
    page: int
    page_size: int


# ==================== ERROR SCHEMAS ====================

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    code: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
