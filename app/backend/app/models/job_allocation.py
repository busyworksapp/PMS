"""
Job Allocation Models
Handles operator job assignments, tracking, and quantity validation
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class AllocationStatusEnum(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class JobAllocation(Base):
    """Operator job allocations with real-time tracking"""
    __tablename__ = "job_allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    order_item_id = Column(
        Integer,
        ForeignKey("order_items.id"),
        nullable=False
    )
    operator_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    machine_id = Column(
        Integer,
        ForeignKey("machines.id"),
        nullable=True
    )
    
    # Allocation details
    status = Column(
        String(50),
        default=AllocationStatusEnum.PENDING,
        index=True
    )
    allocated_quantity = Column(Integer, nullable=False)
    completed_quantity = Column(Integer, default=0)
    rejected_quantity = Column(Integer, default=0)
    
    # Timeline
    scheduled_start = Column(DateTime, nullable=True)
    scheduled_end = Column(DateTime, nullable=True)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    order_item = relationship("OrderItem")
    operator = relationship("User", back_populates="job_allocations")
    machine = relationship("Machine")
    progress_logs = relationship(
        "JobProgressLog",
        back_populates="allocation",
        cascade="all, delete-orphan"
    )


class JobProgressLog(Base):
    """Real-time tracking of operator progress"""
    __tablename__ = "job_progress_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    allocation_id = Column(
        Integer,
        ForeignKey("job_allocations.id"),
        nullable=False
    )
    
    # Progress snapshot
    quantity_completed = Column(Integer, nullable=False)
    quantity_rejected = Column(Integer, default=0)
    rejection_reason = Column(String(500), nullable=True)
    
    # Timestamp
    logged_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    allocation = relationship(
        "JobAllocation",
        back_populates="progress_logs"
    )
