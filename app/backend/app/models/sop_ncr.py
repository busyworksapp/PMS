from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class SOPTicketStatusEnum(str, enum.Enum):
    OPEN = "open"
    IN_INVESTIGATION = "in_investigation"
    ESCALATED = "escalated"
    CLOSED = "closed"


class SOPFailureTicket(Base):
    __tablename__ = "sop_failure_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(100), unique=True, nullable=False)
    sop_reference = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    impact_description = Column(Text, nullable=True)
    charged_department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    charging_department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    status = Column(String(50), default=SOPTicketStatusEnum.OPEN)
    rejection_reason = Column(String(500), nullable=True)
    reassignment_reason = Column(String(500), nullable=True)
    reassigned_from_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    escalated_to_hod_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    hod_decision = Column(String(500), nullable=True)
    closed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class NonConformanceReport(Base):
    __tablename__ = "non_conformance_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    sop_ticket_id = Column(Integer, ForeignKey("sop_failure_tickets.id"), nullable=False)
    root_cause = Column(Text, nullable=False)
    corrective_actions = Column(Text, nullable=False)
    preventive_measures = Column(Text, nullable=False)
    submitted_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
