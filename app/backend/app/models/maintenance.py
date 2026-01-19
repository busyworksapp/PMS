from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
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


class MaintenanceTicket(Base):
    __tablename__ = "maintenance_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(100), unique=True, nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    issue_description = Column(String(1000), nullable=False)
    severity = Column(String(50), nullable=False)  # low, medium, high, critical
    status = Column(String(50), default=MaintenanceStatusEnum.OPEN)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reported_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expected_response_time = Column(DateTime, nullable=True)
    expected_completion_time = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    machine = relationship("Machine", back_populates="maintenance_tickets")
