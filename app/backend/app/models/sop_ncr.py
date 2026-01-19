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


class SOPTicketStatusEnum(str, enum.Enum):
    OPEN = "open"
    IN_INVESTIGATION = "in_investigation"
    AWAITING_HOD = "awaiting_hod"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"


class HODDecisionEnum(str, enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    REQUEST_INFO = "request_info"
    REASSIGN = "reassign"


class SOPFailureTicket(Base):
    """SOP Failure tickets with NCR and escalation"""
    __tablename__ = "sop_failure_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    sop_reference = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    impact_description = Column(Text, nullable=True)
    
    # Department routing
    charged_department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )
    charging_department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )
    
    # Status
    status = Column(
        String(50),
        default=SOPTicketStatusEnum.OPEN,
        index=True
    )
    
    # Rejection & reassignment
    rejection_reason = Column(String(500), nullable=True)
    rejection_count = Column(Integer, default=0)
    reassignment_reason = Column(String(500), nullable=True)
    reassigned_from_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True
    )
    
    # Investigation tracking
    investigation_start = Column(DateTime, nullable=True)
    investigation_notes = Column(Text, nullable=True)
    
    # HOD escalation & decision
    created_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    escalated_to_hod_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    escalated_at = Column(DateTime, nullable=True)
    hod_decision = Column(String(50), nullable=True)
    hod_decision_notes = Column(Text, nullable=True)
    hod_decided_at = Column(DateTime, nullable=True)
    
    # Resolution
    closed_at = Column(DateTime, nullable=True)
    closed_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    
    # Metadata
    priority = Column(String(50), default="normal")
    attachments = Column(JSON, nullable=True)
    audit_trail = Column(JSON, nullable=True)  # All status changes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    charged_department = relationship(
        "Department",
        foreign_keys=[charged_department_id]
    )
    charging_department = relationship(
        "Department",
        foreign_keys=[charging_department_id]
    )
    created_by = relationship(
        "User",
        foreign_keys=[created_by_id]
    )
    escalated_to_hod = relationship(
        "User",
        foreign_keys=[escalated_to_hod_id],
        back_populates="sop_escalations"
    )
    closed_by = relationship(
        "User",
        foreign_keys=[closed_by_id]
    )
    ncr = relationship(
        "NonConformanceReport",
        back_populates="sop_ticket",
        uselist=False,
        cascade="all, delete-orphan"
    )


class NonConformanceReport(Base):
    """Root cause analysis and corrective actions"""
    __tablename__ = "non_conformance_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    sop_ticket_id = Column(
        Integer,
        ForeignKey("sop_failure_tickets.id"),
        nullable=False,
        unique=True
    )
    
    # Analysis
    root_cause = Column(Text, nullable=False)
    corrective_actions = Column(Text, nullable=False)
    preventive_measures = Column(Text, nullable=False)
    
    # Timeline
    investigation_period_start = Column(DateTime, nullable=True)
    investigation_period_end = Column(DateTime, nullable=True)
    
    # Submission
    submitted_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    submission_status = Column(
        String(50),
        default="submitted",
        index=True
    )
    submission_notes = Column(Text, nullable=True)
    
    # Verification
    verified_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    verified_at = Column(DateTime, nullable=True)
    verification_notes = Column(Text, nullable=True)
    
    # Effectiveness check
    effectiveness_verified = Column(Boolean, default=False)
    effectiveness_verified_at = Column(DateTime, nullable=True)
    effectiveness_notes = Column(Text, nullable=True)
    
    # Metadata
    attachments = Column(JSON, nullable=True)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    sop_ticket = relationship(
        "SOPFailureTicket",
        back_populates="ncr"
    )
    submitted_by = relationship(
        "User",
        foreign_keys=[submitted_by_id]
    )
    verified_by = relationship(
        "User",
        foreign_keys=[verified_by_id]
    )
