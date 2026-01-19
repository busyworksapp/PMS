from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
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
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    employee_number = Column(String(100), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = relationship("Department", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")
