"""
WhatsApp Integration Models
Handles WhatsApp messages, contacts, and webhooks
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class MessageStatusEnum(str, enum.Enum):
    """Message delivery status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class MessageTypeEnum(str, enum.Enum):
    """Type of message"""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    TEMPLATE = "template"


class WhatsAppMessage(Base):
    """
    WhatsApp message model
    Stores incoming and outgoing messages
    """
    __tablename__ = "whatsapp_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(100), unique=True, nullable=True, index=True)
    from_phone_number = Column(String(20), nullable=False, index=True)
    to_phone_number = Column(String(20), nullable=False, index=True)
    message_type = Column(String(20), default=MessageTypeEnum.TEXT)
    message_text = Column(Text, nullable=True)
    media_url = Column(String(500), nullable=True)
    media_type = Column(String(50), nullable=True)
    status = Column(String(20), default=MessageStatusEnum.PENDING, index=True)
    direction = Column(String(10), nullable=False)  # 'inbound' or 'outbound'
    is_read = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)


class WhatsAppContact(Base):
    """
    WhatsApp contact model
    Stores contact information and chat metadata
    """
    __tablename__ = "whatsapp_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=True)
    business_name = Column(String(100), nullable=True)
    profile_picture_url = Column(String(500), nullable=True)
    status_text = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    is_pinned = Column(Boolean, default=False)
    last_message_time = Column(DateTime, nullable=True)
    unread_count = Column(Integer, default=0)
    conversation_closed = Column(Boolean, default=False)
    tags = Column(JSON, nullable=True)  # ['urgent', 'vip', 'support', etc.]
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WhatsAppWebhook(Base):
    """
    WhatsApp webhook event model
    Tracks incoming webhook events from Meta for audit and retry logic
    """
    __tablename__ = "whatsapp_webhooks"
    
    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(String(100), unique=True, nullable=True, index=True)
    event_type = Column(String(50), nullable=False, index=True)  # 'message', 'status_update', 'template_status'
    phone_number = Column(String(20), nullable=True, index=True)
    payload = Column(JSON, nullable=False)
    processed = Column(Boolean, default=False, index=True)
    processing_error = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    last_retry_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)


class WhatsAppTemplate(Base):
    """
    WhatsApp message template model
    Stores pre-approved templates for bulk messaging
    """
    __tablename__ = "whatsapp_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String(100), unique=True, nullable=False, index=True)
    template_id = Column(String(100), unique=True, nullable=True)
    namespace = Column(String(100), nullable=True)
    template_text = Column(Text, nullable=False)
    variables = Column(JSON, nullable=True)  # List of variable names
    category = Column(String(50), default="MARKETING")  # MARKETING, UTILITY, AUTHENTICATION
    status = Column(String(20), default="pending")  # pending, approved, rejected, disabled
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WhatsAppQueue(Base):
    """
    Message queue model for handling bulk sending
    """
    __tablename__ = "whatsapp_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    message_text = Column(Text, nullable=False)
    message_type = Column(String(20), default=MessageTypeEnum.TEXT)
    media_url = Column(String(500), nullable=True)
    template_name = Column(String(100), nullable=True)
    priority = Column(Integer, default=0)  # Higher = more priority
    status = Column(String(20), default="pending", index=True)  # pending, processing, sent, failed
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    error_message = Column(Text, nullable=True)
    scheduled_for = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)


class WhatsAppSession(Base):
    """
    WhatsApp session/authentication model
    Stores authentication tokens and session info
    """
    __tablename__ = "whatsapp_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    business_account_id = Column(String(100), nullable=False, unique=True)
    phone_number_id = Column(String(20), nullable=False, unique=True)
    api_token = Column(String(500), nullable=False)
    webhook_verify_token = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    webhook_url = Column(String(500), nullable=True)
    subscription_status = Column(String(20), default="active")
    last_api_call = Column(DateTime, nullable=True)
    rate_limit_remaining = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
