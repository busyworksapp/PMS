"""
Job Planning Additional Models
Handles production exceptions and capacity planning
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class ProductionExceptionEnum(str, enum.Enum):
    EQUIPMENT_FAILURE = "equipment_failure"
    MATERIAL_SHORTAGE = "material_shortage"
    LABOR_SHORTAGE = "labor_shortage"
    QUALITY_ISSUE = "quality_issue"
    REWORK_REQUIRED = "rework_required"
    SUPPLIER_DELAY = "supplier_delay"
    CUSTOMER_REQUEST = "customer_request"


class ProductionException(Base):
    """Tracks exceptions during production"""
    __tablename__ = "production_exceptions"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("order_items.id"), nullable=True)
    
    exception_type = Column(String(50), nullable=False)
    reason = Column(String(500), nullable=False)
    severity = Column(String(20), nullable=False)
    
    # Resolution tracking
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="exceptions")
    item = relationship("OrderItem")


class CapacityTarget(Base):
    """Daily/weekly/monthly capacity targets for departments"""
    __tablename__ = "capacity_targets"
    
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    period_type = Column(String(20), nullable=False)
    target_units = Column(Integer, nullable=False)
    current_allocated = Column(Integer, default=0)
    
    period_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = relationship("Department")
