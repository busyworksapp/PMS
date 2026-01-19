from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
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


class InternalReject(Base):
    __tablename__ = "internal_rejects"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(100), unique=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    quantity_rejected = Column(Integer, nullable=False)
    production_stage = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    reason = Column(String(500), nullable=False)
    status = Column(String(50), default=RejectStatusEnum.PENDING)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="rejects")


class CustomerReturn(Base):
    __tablename__ = "customer_returns"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(100), unique=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    quantity_returned = Column(Integer, nullable=False)
    reason = Column(String(500), nullable=False)
    logged_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
