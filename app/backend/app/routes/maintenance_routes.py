"""
Maintenance Routes
Handles maintenance tickets, SLA tracking, and technician workflow
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from typing import Optional
from app.db.database import get_db
from app.models.maintenance import (
    MaintenanceTicket,
    MaintenanceHistory,
    MaintenanceStatusEnum,
    SeverityEnum
)
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/api/maintenance", tags=["Maintenance"])


# ============== Maintenance Tickets ==============

@router.post("/tickets")
def create_maintenance_ticket(
    machine_id: int,
    department_id: int,
    issue_description: str,
    detailed_description: Optional[str] = None,
    severity: str = "medium",
    priority: str = "normal",
    machine_down: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a maintenance ticket"""
    # Generate ticket number
    count = db.query(MaintenanceTicket).count()
    date_str = datetime.utcnow().strftime('%Y%m%d')
    ticket_number = f"MT-{date_str}-{count + 1:04d}"
    
    # Calculate SLA times based on severity
    response_sla_hours = {
        "critical": 1,
        "high": 4,
        "medium": 8,
        "low": 24
    }.get(severity, 8)
    
    completion_sla_hours = {
        "critical": 4,
        "high": 8,
        "medium": 24,
        "low": 72
    }.get(severity, 24)
    
    now = datetime.utcnow()
    
    ticket = MaintenanceTicket(
        ticket_number=ticket_number,
        machine_id=machine_id,
        department_id=department_id,
        issue_description=issue_description,
        detailed_description=detailed_description,
        severity=severity,
        priority=priority,
        machine_down=machine_down,
        reported_by_id=current_user.id,
        expected_response_time=now + timedelta(hours=response_sla_hours),
        expected_completion_time=now + timedelta(
            hours=completion_sla_hours
        )
    )
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    return {
        "message": "Maintenance ticket created successfully",
        "ticket_number": ticket.ticket_number,
        "ticket_id": ticket.id
    }


@router.get("/tickets")
def list_maintenance_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    status: Optional[str] = None,
    severity: Optional[str] = None,
    machine_down: Optional[bool] = None,
    assigned_to_me: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List maintenance tickets with filters"""
    query = db.query(MaintenanceTicket)
    
    if status:
        query = query.filter(MaintenanceTicket.status == status)
    if severity:
        query = query.filter(MaintenanceTicket.severity == severity)
    if machine_down is not None:
        query = query.filter(MaintenanceTicket.machine_down == machine_down)
    if assigned_to_me:
        query = query.filter(
            MaintenanceTicket.assigned_to_id == current_user.id
        )
    
    total = query.count()
    tickets = query.order_by(
        desc(MaintenanceTicket.created_at)
    ).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "tickets": [
            {
                "id": t.id,
                "ticket_number": t.ticket_number,
                "machine_id": t.machine_id,
                "issue_description": t.issue_description,
                "severity": t.severity,
                "priority": t.priority,
                "status": t.status,
                "assigned_to_id": t.assigned_to_id,
                "machine_down": t.machine_down,
                "created_at": t.created_at
            } for t in tickets
        ]
    }


@router.get("/tickets/{ticket_id}")
def get_maintenance_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get maintenance ticket details"""
    ticket = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.id == ticket_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Maintenance ticket not found"
        )
    
    return {
        "id": ticket.id,
        "ticket_number": ticket.ticket_number,
        "machine_id": ticket.machine_id,
        "department_id": ticket.department_id,
        "issue_description": ticket.issue_description,
        "detailed_description": ticket.detailed_description,
        "severity": ticket.severity,
        "priority": ticket.priority,
        "status": ticket.status,
        "assigned_to_id": ticket.assigned_to_id,
        "reported_by_id": ticket.reported_by_id,
        "expected_response_time": ticket.expected_response_time,
        "expected_completion_time": ticket.expected_completion_time,
        "started_at": ticket.started_at,
        "completed_at": ticket.completed_at,
        "root_cause": ticket.root_cause,
        "corrective_actions": ticket.corrective_actions,
        "preventive_measures": ticket.preventive_measures,
        "parts_required": ticket.parts_required,
        "estimated_cost": ticket.estimated_cost,
        "machine_down": ticket.machine_down,
        "production_impact": ticket.production_impact,
        "created_at": ticket.created_at
    }


@router.put("/tickets/{ticket_id}")
def update_maintenance_ticket(
    ticket_id: int,
    status: Optional[str] = None,
    assigned_to_id: Optional[int] = None,
    root_cause: Optional[str] = None,
    corrective_actions: Optional[str] = None,
    preventive_measures: Optional[str] = None,
    estimated_cost: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update maintenance ticket"""
    ticket = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.id == ticket_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Maintenance ticket not found"
        )
    
    # Record status change for audit trail
    old_status = ticket.status
    
    if status:
        ticket.status = status
    if assigned_to_id is not None:
        ticket.assigned_to_id = assigned_to_id
    if root_cause:
        ticket.root_cause = root_cause
    if corrective_actions:
        ticket.corrective_actions = corrective_actions
    if preventive_measures:
        ticket.preventive_measures = preventive_measures
    if estimated_cost is not None:
        ticket.estimated_cost = estimated_cost
    
    # Set timestamps
    if status == MaintenanceStatusEnum.IN_PROGRESS and not ticket.started_at:
        ticket.started_at = datetime.utcnow()
    
    if status == MaintenanceStatusEnum.COMPLETED:
        ticket.completed_at = datetime.utcnow()
    
    ticket.updated_at = datetime.utcnow()
    db.commit()
    
    # Log the change
    if status and old_status != status:
        history = MaintenanceHistory(
            ticket_id=ticket_id,
            status_before=old_status,
            status_after=status,
            updated_by_id=current_user.id
        )
        db.add(history)
        db.commit()
    
    return {"message": "Maintenance ticket updated successfully"}


@router.post("/tickets/{ticket_id}/assign")
def assign_maintenance_ticket(
    ticket_id: int,
    technician_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign ticket to technician"""
    ticket = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.id == ticket_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Maintenance ticket not found"
        )
    
    ticket.assigned_to_id = technician_id
    ticket.status = MaintenanceStatusEnum.IN_PROGRESS
    ticket.started_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "message": f"Ticket assigned to technician {technician_id}"
    }


@router.post("/tickets/{ticket_id}/complete")
def complete_maintenance_ticket(
    ticket_id: int,
    completion_notes: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark ticket as completed"""
    ticket = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.id == ticket_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Maintenance ticket not found"
        )
    
    ticket.status = MaintenanceStatusEnum.COMPLETED
    ticket.completed_at = datetime.utcnow()
    ticket.corrective_actions = completion_notes
    
    db.commit()
    
    return {"message": "Maintenance ticket completed"}


# ============== SLA Monitoring ==============

@router.get("/sla-status")
def get_sla_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get SLA status across all tickets"""
    tickets = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.status.in_([
            MaintenanceStatusEnum.OPEN,
            MaintenanceStatusEnum.IN_PROGRESS
        ])
    ).all()
    
    now = datetime.utcnow()
    breached = 0
    at_risk = 0
    on_track = 0
    
    for ticket in tickets:
        if ticket.expected_completion_time and ticket.expected_completion_time < now:
            breached += 1
        elif ticket.expected_completion_time and (ticket.expected_completion_time - now).total_seconds() < 3600:
            at_risk += 1
        else:
            on_track += 1
    
    return {
        "total_active": len(tickets),
        "breached": breached,
        "at_risk": at_risk,
        "on_track": on_track,
        "breach_rate": round(
            (breached / len(tickets) * 100) if len(tickets) > 0 else 0,
            2
        )
    }


# ============== Maintenance History ==============

@router.get("/tickets/{ticket_id}/history")
def get_ticket_history(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get ticket status change history"""
    history = db.query(MaintenanceHistory).filter(
        MaintenanceHistory.ticket_id == ticket_id
    ).order_by(desc(MaintenanceHistory.updated_at)).all()
    
    return {
        "ticket_id": ticket_id,
        "history": [
            {
                "status_before": h.status_before,
                "status_after": h.status_after,
                "update_notes": h.update_notes,
                "updated_at": h.updated_at
            } for h in history
        ]
    }


# ============== Maintenance Dashboard ==============

@router.get("/dashboard")
def maintenance_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Maintenance dashboard with KPIs"""
    total_tickets = db.query(MaintenanceTicket).count()
    open_tickets = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.status == MaintenanceStatusEnum.OPEN
    ).count()
    in_progress = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.status == MaintenanceStatusEnum.IN_PROGRESS
    ).count()
    completed = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.status == MaintenanceStatusEnum.COMPLETED
    ).count()
    
    critical_tickets = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.severity == SeverityEnum.CRITICAL
    ).count()
    
    # Average resolution time (completed tickets only)
    completed_tickets = db.query(MaintenanceTicket).filter(
        MaintenanceTicket.status == MaintenanceStatusEnum.COMPLETED,
        MaintenanceTicket.completed_at.isnot(None)
    ).all()
    
    avg_resolution_hours = 0
    if completed_tickets:
        total_hours = sum(
            (t.completed_at - t.created_at).total_seconds() / 3600
            for t in completed_tickets
        )
        avg_resolution_hours = round(
            total_hours / len(completed_tickets),
            2
        )
    
    return {
        "summary": {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress": in_progress,
            "completed": completed,
            "completion_rate": round(
                (completed / total_tickets * 100)
                if total_tickets > 0 else 0,
                2
            ),
            "critical_tickets": critical_tickets
        },
        "metrics": {
            "average_resolution_hours": avg_resolution_hours
        }
    }
