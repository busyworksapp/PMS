from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class OrderStatusEnum(str, enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False)
    customer_name = Column(String(255), nullable=False)
    order_value = Column(Numeric(12, 2), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(50), default=OrderStatusEnum.SCHEDULED)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = relationship("Department", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    schedules = relationship("OrderSchedule", back_populates="order", cascade="all, delete-orphan")
    rejects = relationship("InternalReject", back_populates="order")


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


class OrderSchedule(Base):
    __tablename__ = "order_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    status = Column(String(50), default=OrderStatusEnum.SCHEDULED)
    assigned_machine_id = Column(Integer, ForeignKey("machines.id"), nullable=True)
    assigned_operator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="schedules")
