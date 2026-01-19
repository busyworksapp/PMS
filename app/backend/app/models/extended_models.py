"""
Extended Models for Defects, SOP/NCR, Maintenance, and Finance
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    Numeric, Text, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class InternalRejectStatusEnum:
    """Internal reject ticket statuses"""
    PENDING = "pending"
    APPROVED = "approved"
    REPLACEMENT_PROCESSED = "replacement_processed"
    NO_STOCK = "no_stock"
    CLOSED = "closed"


class InternalReject(Base):
    """Internal rejects during production"""
    __tablename__ = "internal_rejects"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("order_items.id"),
                     nullable=True)
    
    # Details
    reject_reason = Column(String(500), nullable=False)
    quantity_rejected = Column(Integer, nullable=False)
    production_stage_id = Column(Integer,
                                 ForeignKey("production_stages.id"),
                                 nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"),
                          nullable=False)
    
    # Status workflow
    status = Column(String(50), default=InternalRejectStatusEnum.PENDING)
    department_manager_approved = Column(Boolean, default=False)
    approved_at = Column(DateTime, nullable=True)
    approved_by_id = Column(Integer, ForeignKey("users.id"),
                           nullable=True)
    
    # Planning action
    planning_notes = Column(Text, nullable=True)
    ordered_by_id = Column(Integer, ForeignKey("users.id"),
                          nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="defects")
    item = relationship("OrderItem", back_populates="defects")
    stage = relationship("ProductionStage")
    department = relationship("Department")
    approved_by = relationship("User", foreign_keys=[approved_by_id])
    ordered_by = relationship("User", foreign_keys=[ordered_by_id])


class CustomerReturn(Base):
    """Customer returns after delivery"""
    __tablename__ = "customer_returns"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    return_reason = Column(String(500), nullable=False)
    quantity_returned = Column(Integer, nullable=False)
    receive_date = Column(DateTime, nullable=False)
    
    # Actions
    action_taken = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    recorded_by_id = Column(Integer, ForeignKey("users.id"),
                           nullable=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("Order")
    recorded_by = relationship("User")


class SOPFailureTicketStatusEnum:
    """SOP failure ticket statuses"""
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    REJECTED = "rejected"
    REASSIGNED = "reassigned"
    ESCALATED_TO_HOD = "escalated_to_hod"
    HOD_DECISION_PENDING = "hod_decision_pending"
    CLOSED = "closed"


class SOPFailureTicket(Base):
    """SOP failure tickets raised by departments"""
    __tablename__ = "sop_failure_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(100), unique=True, nullable=False)
    
    # Who charged whom
    raising_department_id = Column(Integer,
                                   ForeignKey("departments.id"),
                                   nullable=False)
    charged_department_id = Column(Integer,
                                   ForeignKey("departments.id"),
                                   nullable=False)
    
    # Details
    sop_reference = Column(String(100), nullable=False)
    failure_description = Column(Text, nullable=False)
    impact_description = Column(Text, nullable=False)
    
    # Status
    status = Column(String(50), default=SOPFailureTicketStatusEnum.OPEN)
    rejection_reason = Column(Text, nullable=True)
    reassignment_reason = Column(Text, nullable=True)
    reassigned_to_department_id = Column(Integer,
                                         ForeignKey("departments.id"),
                                         nullable=True)
    
    # HOD decision
    hod_decision = Column(String(500), nullable=True)
    hod_decided_by_id = Column(Integer, ForeignKey("users.id"),
                              nullable=True)
    hod_decision_date = Column(DateTime, nullable=True)
    
    # Tracking
    raised_by_id = Column(Integer, ForeignKey("users.id"),
                         nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"),
                           nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    
    # Relationships
    raising_dept = relationship("Department", foreign_keys=[
        raising_department_id])
    charged_dept = relationship("Department", foreign_keys=[
        charged_department_id])
    reassigned_dept = relationship("Department", foreign_keys=[
        reassigned_to_department_id])
    raised_by = relationship("User", foreign_keys=[raised_by_id])
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    hod_decided_by = relationship("User", foreign_keys=[
        hod_decided_by_id])
    ncr = relationship("NonConformanceReport", back_populates="ticket",
                      uselist=False)


class NonConformanceReport(Base):
    """NCR - Non-Conformance Report"""
    __tablename__ = "non_conformance_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("sop_failure_tickets.id"),
                      unique=True, nullable=False)
    
    # NCR Details
    root_cause_analysis = Column(Text, nullable=False)
    corrective_actions = Column(Text, nullable=False)
    preventive_measures = Column(Text, nullable=False)
    
    # Completion
    completed_by_id = Column(Integer, ForeignKey("users.id"),
                            nullable=False)
    completion_date = Column(DateTime, nullable=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    
    # Relationships
    ticket = relationship("SOPFailureTicket", back_populates="ncr")
    completed_by = relationship("User")


class MaintenanceTicket(Base):
    """Equipment maintenance tickets"""
    __tablename__ = "maintenance_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(100), unique=True, nullable=False)
    
    machine_id = Column(Integer, ForeignKey("machines.id"),
                       nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"),
                          nullable=False)
    
    # Issue details
    issue_description = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False)  # low, medium, high
    expected_response_hours = Column(Integer, nullable=True)
    expected_completion_hours = Column(Integer, nullable=True)
    
    # Status
    status = Column(String(50), default="open")  # open, assigned, in_progress, completed
    fault_date = Column(DateTime, nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"),
                           nullable=True)
    assigned_date = Column(DateTime, nullable=True)
    
    # Completion
    completion_notes = Column(Text, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    parts_used = Column(Text, nullable=True)
    
    # Tracking
    created_by_id = Column(Integer, ForeignKey("users.id"),
                          nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    
    # Relationships
    machine = relationship("Machine")
    department = relationship("Department")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    created_by = relationship("User", foreign_keys=[created_by_id])


class BillOfMaterial(Base):
    """Bill of Materials for products"""
    __tablename__ = "bills_of_materials"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"),
                       nullable=False, unique=True)
    version = Column(Integer, default=1)
    
    total_material_cost = Column(Numeric(12, 2), nullable=False)
    total_labor_hours = Column(Numeric(8, 2), nullable=False)
    total_overhead = Column(Numeric(12, 2), nullable=False)
    total_cost_per_unit = Column(Numeric(12, 2), nullable=False)
    
    # Configuration
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime, nullable=False, default=datetime.utcnow)
    valid_to = Column(DateTime, nullable=True)
    
    created_by_id = Column(Integer, ForeignKey("users.id"),
                          nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="bom")
    created_by = relationship("User")
    components = relationship("BOMComponent", back_populates="bom",
                            cascade="all, delete-orphan")


class BOMComponent(Base):
    """Components within a BOM"""
    __tablename__ = "bom_components"
    
    id = Column(Integer, primary_key=True, index=True)
    bom_id = Column(Integer, ForeignKey("bills_of_materials.id"),
                   nullable=False)
    
    component_code = Column(String(100), nullable=False)
    component_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    quantity_per_unit = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(50), nullable=False)
    unit_cost = Column(Numeric(12, 2), nullable=False)
    total_cost = Column(Numeric(12, 2), nullable=False)
    
    sequence = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    
    # Relationships
    bom = relationship("BillOfMaterial", back_populates="components")
