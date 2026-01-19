from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Numeric, Text, Boolean
)
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
    ARCHIVED = "archived"


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False, index=True)
    sales_order_number = Column(String(100), nullable=True)
    customer_name = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    order_value = Column(Numeric(12, 2), nullable=True)
    quantity = Column(Integer, nullable=False)
    completed_quantity = Column(Integer, default=0)
    rejected_quantity = Column(Integer, default=0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    scheduled_start = Column(DateTime, nullable=True)
    scheduled_end = Column(DateTime, nullable=True)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    status = Column(String(50), default=OrderStatusEnum.PENDING, index=True)
    department_id = Column(
        Integer, ForeignKey("departments.id"), nullable=False
    )
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    product = relationship("Product")
    department = relationship("Department", back_populates="orders")
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    schedules = relationship(
        "OrderSchedule", back_populates="order",
        cascade="all, delete-orphan"
    )
    rejects = relationship("InternalReject", back_populates="order", foreign_keys="InternalReject.order_id")
    exceptions = relationship("ProductionException", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    quantity_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    defects = relationship("InternalReject", back_populates="item", foreign_keys="InternalReject.item_id")


class OrderSchedule(Base):
    __tablename__ = "order_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    department_id = Column(
        Integer, ForeignKey("departments.id"), nullable=False
    )
    scheduled_date = Column(DateTime, nullable=False)
    status = Column(String(50), default=OrderStatusEnum.SCHEDULED)
    assigned_machine_id = Column(
        Integer, ForeignKey("machines.id"), nullable=True
    )
    assigned_operator_id = Column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="schedules")
