from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    Text,
    JSON,
    Numeric
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class MaintenanceStatusEnum(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    AWAITING_PARTS = "awaiting_parts"
    COMPLETED = "completed"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class SeverityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PriorityEnum(str, enum.Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class MaintenanceTicket(Base):
    """Maintenance tickets with SLA and technician workflow"""
    __tablename__ = "maintenance_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    machine_id = Column(
        Integer,
        ForeignKey("machines.id"),
        nullable=False
    )
    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )
    issue_description = Column(String(1000), nullable=False)
    detailed_description = Column(Text, nullable=True)
    severity = Column(
        String(50),
        default=SeverityEnum.MEDIUM,
        index=True
    )
    priority = Column(
        String(50),
        default=PriorityEnum.NORMAL,
        index=True
    )
    status = Column(
        String(50),
        default=MaintenanceStatusEnum.OPEN,
        index=True
    )
    
    # Technician assignment
    assigned_to_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    reported_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    
    # SLA tracking
    expected_response_time = Column(DateTime, nullable=True)
    expected_completion_time = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Maintenance details
    root_cause = Column(Text, nullable=True)
    corrective_actions = Column(Text, nullable=True)
    preventive_measures = Column(Text, nullable=True)
    parts_required = Column(JSON, nullable=True)  # List of parts
    estimated_cost = Column(Numeric(12, 2), nullable=True)
    
    # Machine availability impact
    machine_down = Column(Boolean, default=False)
    production_impact = Column(Text, nullable=True)
    
    # Metadata
    attachments = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    machine = relationship("Machine", back_populates="maintenance_tickets")
    department = relationship("Department")
    assigned_technician = relationship(
        "User",
        foreign_keys=[assigned_to_id],
        back_populates="maintenance_tickets_assigned"
    )
    reported_by_user = relationship(
        "User",
        foreign_keys=[reported_by_id],
        back_populates="maintenance_tickets_reported"
    )
    history = relationship(
        "MaintenanceHistory",
        back_populates="ticket",
        cascade="all, delete-orphan"
    )


class MaintenanceHistory(Base):
    """Maintenance ticket update history for audit trail"""
    __tablename__ = "maintenance_history"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(
        Integer,
        ForeignKey("maintenance_tickets.id"),
        nullable=False
    )
    status_before = Column(String(50), nullable=True)
    status_after = Column(String(50), nullable=True)
    update_notes = Column(Text, nullable=True)
    updated_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ticket = relationship("MaintenanceTicket", back_populates="history")
