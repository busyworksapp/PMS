from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    Text,
    JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class RejectStatusEnum(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REPLACEMENT_PROCESSED = "replacement_processed"
    NO_STOCK = "no_stock"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class DefectTypeEnum(str, enum.Enum):
    DIMENSION = "dimension"
    COLOR = "color"
    MATERIAL = "material"
    STITCHING = "stitching"
    PRINTING = "printing"
    DAMAGE = "damage"
    OTHER = "other"


class InternalReject(Base):
    """Internal rejects/defects with replacement tracking"""
    __tablename__ = "internal_rejects"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )
    item_id = Column(
        Integer,
        ForeignKey("order_items.id"),
        nullable=True
    )
    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=True
    )
    quantity_rejected = Column(Integer, nullable=False)
    defect_type = Column(
        String(50),
        default=DefectTypeEnum.OTHER
    )
    production_stage = Column(String(255), nullable=False)
    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )
    reason = Column(String(500), nullable=False)
    detailed_description = Column(Text, nullable=True)
    
    # Status & approvals
    status = Column(
        String(50),
        default=RejectStatusEnum.PENDING,
        index=True
    )
    created_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    approved_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    approved_at = Column(DateTime, nullable=True)
    
    # Replacement details
    replacement_ticket_number = Column(String(100), nullable=True)
    replacement_quantity = Column(Integer, nullable=True)
    
    # Metadata
    attachments = Column(JSON, nullable=True)  # File paths/URLs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    order = relationship("Order", back_populates="rejects")
    item = relationship("OrderItem", back_populates="defects")
    product = relationship("Product")
    department = relationship("Department")
    created_by = relationship(
        "User",
        foreign_keys=[created_by_id]
    )
    approved_by = relationship(
        "User",
        foreign_keys=[approved_by_id]
    )


class CustomerReturn(Base):
    """Customer returns/quality issues with tracking"""
    __tablename__ = "customer_returns"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )
    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=True
    )
    quantity_returned = Column(Integer, nullable=False)
    reason = Column(String(500), nullable=False)
    detailed_description = Column(Text, nullable=True)
    
    # Timeline
    return_date = Column(DateTime, nullable=False)
    logged_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    
    # Resolution
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Financial impact
    replacement_cost = Column(Integer, nullable=True)
    credit_issued = Column(Boolean, default=False)
    credit_amount = Column(Integer, nullable=True)
    
    # Metadata
    attachments = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    order = relationship("Order")
    product = relationship("Product")
    logged_by = relationship("User")
