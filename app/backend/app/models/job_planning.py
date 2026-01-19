"""
Job Planning Models
Handles order scheduling, production stages, capacity planning, and order allocation
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Enum, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class OrderStatusEnum(str, enum.Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderSourceEnum(str, enum.Enum):
    MANUAL = "manual"
    EXCEL = "excel"
    D365 = "d365"


class Order(Base):
    """Main order/job record"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False)
    sales_order_number = Column(String(100), nullable=True)
    customer_name = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_value = Column(Numeric(12, 2), nullable=True)
    
    # Dates
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    scheduled_start = Column(DateTime, nullable=True)
    scheduled_end = Column(DateTime, nullable=True)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    
    # Status & routing
    status = Column(String(50), default=OrderStatusEnum.PENDING)
    source = Column(String(50), default=OrderSourceEnum.MANUAL)
    primary_department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    
    # Tracking
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="orders")
    department = relationship("Department", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    schedules = relationship("OrderSchedule", back_populates="order", cascade="all, delete-orphan")
    defects = relationship("InternalReject", back_populates="order")


class OrderItem(Base):
    """Line items within an order"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_number = Column(Integer, nullable=False)  # Line item number
    description = Column(String(500), nullable=False)
    quantity = Column(Integer, nullable=False)
    completed_quantity = Column(Integer, default=0)
    rejected_quantity = Column(Integer, default=0)
    
    # Current status
    status = Column(String(50), default=OrderStatusEnum.PENDING)
    current_stage_id = Column(Integer, ForeignKey("production_stages.id"), nullable=True)
    assigned_machine_id = Column(Integer, ForeignKey("machines.id"), nullable=True)
    assigned_operator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    current_stage = relationship("ProductionStage", foreign_keys=[current_stage_id])
    assigned_machine = relationship("Machine", foreign_keys=[assigned_machine_id])
    assigned_operator = relationship("User", foreign_keys=[assigned_operator_id])
    defects = relationship("InternalReject", back_populates="item")


class OrderSchedule(Base):
    """Machine & department allocation for orders"""
    __tablename__ = "order_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    sequence = Column(Integer, nullable=False)  # Process order
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=True)
    stage_id = Column(Integer, ForeignKey("production_stages.id"), nullable=False)
    
    # Allocation details
    scheduled_start = Column(DateTime, nullable=True)
    scheduled_end = Column(DateTime, nullable=True)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    
    # Status
    status = Column(String(50), default=OrderStatusEnum.PENDING)
    notes = Column(Text, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="schedules")
    department = relationship("Department")
    machine = relationship("Machine")
    stage = relationship("ProductionStage")


class ProductionStage(Base):
    """Production stages within departments (e.g., Cut, Stitch, Pack)"""
    __tablename__ = "production_stages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    order = Column(Integer, nullable=False)  # Sequence order
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    
    # Configuration
    estimated_duration_minutes = Column(Integer, nullable=True)
    requires_approval = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", foreign_keys=[product_id])
    department = relationship("Department", back_populates="production_stages")


class CapacityTarget(Base):
    """Daily/weekly/monthly capacity targets for departments"""
    __tablename__ = "capacity_targets"
    
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    period_type = Column(String(20), nullable=False)  # daily, weekly, monthly
    target_units = Column(Integer, nullable=False)
    current_allocated = Column(Integer, default=0)
    
    period_date = Column(DateTime, nullable=False)  # Start date of period
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = relationship("Department")


class OrderException(Base):
    """Tracks order exceptions (on hold, reject, etc)"""
    __tablename__ = "order_exceptions"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("order_items.id"), nullable=True)
    
    exception_type = Column(String(50), nullable=False)  # "on_hold", "rejected"
    reason = Column(String(500), nullable=False)
    severity = Column(String(20), nullable=False)  # "info", "warning", "critical"
    
    # Resolution tracking
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("Order")
    item = relationship("OrderItem")
