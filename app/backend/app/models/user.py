from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    PLANNER = "planner"
    STOCK_PLANNER = "stock_planner"
    BRANDING_COORDINATOR = "branding_coordinator"
    SUPERVISOR = "supervisor"
    DEPARTMENT_MANAGER = "department_manager"
    HOD = "hod"
    MAINTENANCE_SUPERVISOR = "maintenance_supervisor"
    MAINTENANCE_TECHNICIAN = "maintenance_technician"
    QUALITY_COORDINATOR = "quality_coordinator"
    FINANCE_USER = "finance_user"
    OPERATOR = "operator"


class User(Base):
    """User/Employee accounts with role-based access control"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    employee_number = Column(String(100), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    # Operator-specific fields
    is_operator = Column(Boolean, default=False)
    operator_badge_id = Column(String(50), nullable=True)
    
    # Additional metadata
    permissions = Column(JSON, nullable=True)  # Field-level permissions
    preferences = Column(JSON, nullable=True)  # User preferences
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    department = relationship("Department", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")
    maintenance_tickets_assigned = relationship("MaintenanceTicket", 
                                               foreign_keys="MaintenanceTicket.assigned_to_id",
                                               back_populates="assigned_technician")
    maintenance_tickets_reported = relationship("MaintenanceTicket",
                                               foreign_keys="MaintenanceTicket.reported_by_id",
                                               back_populates="reported_by_user")
    job_allocations = relationship("JobAllocation", back_populates="operator")
    sop_escalations = relationship("SOPFailureTicket",
                                  foreign_keys="SOPFailureTicket.escalated_to_hod_id",
                                  back_populates="escalated_to_hod")
