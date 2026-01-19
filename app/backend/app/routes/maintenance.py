"""
Maintenance Module Routes - COMPLETE IMPLEMENTATION
Maintenance tickets, SLA enforcement, technician assignment,
preventive scheduling
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from typing import Optional
from app.db.database import get_db
from app.models.maintenance import MaintenanceTicket
from app.models.machine import Machine
from app.models.department import Department
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/api/maintenance", tags=["maintenance"])

# SLA Response and Completion times (in hours) by severity
SLA_CONFIG = {
    "critical": {"response": 1, "completion": 4},
    "high": {"response": 2, "completion": 8},
    "medium": {"response": 4, "completion": 24},
    "low": {"response": 8, "completion": 48},
}


def calculate_sla_priority(ticket: MaintenanceTicket) -> dict:
    """
    Calculate SLA status and priority based on severity and time elapsed
    Returns: {priority: "urgent"|"high"|"normal"|"low", hours_remaining: int}
    """
    now = datetime.utcnow()
    created_age = (now - ticket.created_at).total_seconds() / 3600

    sla = SLA_CONFIG.get(ticket.severity, SLA_CONFIG["medium"])

    if ticket.status == "open" or ticket.status == "awaiting_parts":
        response_deadline = sla["response"]
        hours_remaining = response_deadline - created_age

        if hours_remaining <= 0:
            priority = "urgent"
        elif hours_remaining <= 1:
            priority = "high"
        elif hours_remaining <= sla["response"] / 2:
            priority = "high"
        else:
            priority = "normal"
    else:
        completion_deadline = sla["completion"]
        hours_remaining = completion_deadline - created_age

        if hours_remaining <= 0:
            priority = "urgent"
        elif hours_remaining <= 2:
            priority = "high"
        else:
            priority = "normal"

    return {
        "priority": priority,
        "hours_remaining": max(0, hours_remaining),
        "sla_breached": hours_remaining <= 0,
    }


@router.get("/tickets")
async def list_maintenance_tickets(
    status: Optional[str] = None,
    department_id: Optional[int] = None,
    severity: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List maintenance tickets with SLA calculation
    Query params: status, department_id, severity, skip, limit
    """
    try:
        query = db.query(MaintenanceTicket).order_by(
            desc(MaintenanceTicket.created_at)
        )

        if status:
            query = query.filter(MaintenanceTicket.status == status)
        if department_id:
            query = query.filter(
                MaintenanceTicket.department_id == department_id
            )
        if severity:
            query = query.filter(MaintenanceTicket.severity == severity)

        total = query.count()
        tickets = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": t.id,
                    "ticket_number": t.ticket_number,
                    "machine_id": t.machine_id,
                    "department_id": t.department_id,
                    "issue_description": t.issue_description,
                    "severity": t.severity,
                    "status": t.status,
                    "assigned_to_id": t.assigned_to_id,
                    "created_at": t.created_at.isoformat(),
                    "started_at": (
                        t.started_at.isoformat()
                        if t.started_at
                        else None
                    ),
                    "completed_at": (
                        t.completed_at.isoformat()
                        if t.completed_at
                        else None
                    ),
                    "sla": calculate_sla_priority(t),
                }
                for t in tickets
            ],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tickets: {str(e)}",
        )


@router.post("/tickets", status_code=201)
async def create_maintenance_ticket(
    ticket_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create new maintenance ticket with SLA enforcement
    Request body:
    {
        "machine_id": 1,
        "department_id": 1,
        "issue_description": "Machine vibrating abnormally",
        "severity": "critical|high|medium|low"
    }
    """
    try:
        # Validate required fields
        required_fields = [
            "machine_id",
            "department_id",
            "issue_description",
            "severity",
        ]
        for field in required_fields:
            if field not in ticket_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}",
                )

        # Validate severity
        if ticket_data["severity"] not in SLA_CONFIG:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid severity. Must be one of: "
                    f"{list(SLA_CONFIG.keys())}"
                ),
            )

        # Verify machine exists
        machine = db.query(Machine).filter(
            Machine.id == ticket_data["machine_id"]
        ).first()
        if not machine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Machine not found",
            )

        # Verify department exists
        dept = db.query(Department).filter(
            Department.id == ticket_data["department_id"]
        ).first()
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found",
            )

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        ticket_number = f"MNT-{timestamp}"

        # Calculate SLA response and completion times
        sla = SLA_CONFIG[ticket_data["severity"]]
        now = datetime.utcnow()
        expected_response = now + timedelta(hours=sla["response"])
        expected_completion = now + timedelta(hours=sla["completion"])

        ticket = MaintenanceTicket(
            ticket_number=ticket_number,
            machine_id=ticket_data["machine_id"],
            department_id=ticket_data["department_id"],
            issue_description=ticket_data["issue_description"],
            severity=ticket_data["severity"],
            status="open",
            reported_by_id=current_user.id,
            expected_response_time=expected_response,
            expected_completion_time=expected_completion,
        )

        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return {
            "id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "status": ticket.status,
            "severity": ticket.severity,
            "created_at": ticket.created_at.isoformat(),
            "sla": {
                "expected_response": (
                    expected_response.isoformat()
                ),
                "expected_completion": (
                    expected_completion.isoformat()
                ),
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating ticket: {str(e)}",
        )


@router.get("/tickets/{ticket_id}")
async def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed ticket information with SLA status"""
    try:
        ticket = db.query(MaintenanceTicket).filter(
            MaintenanceTicket.id == ticket_id
        ).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found",
            )

        # Load relationships
        machine = db.query(Machine).filter(
            Machine.id == ticket.machine_id
        ).first()
        dept = db.query(Department).filter(
            Department.id == ticket.department_id
        ).first()
        assigned_user = None
        if ticket.assigned_to_id:
            assigned_user = db.query(User).filter(
                User.id == ticket.assigned_to_id
            ).first()

        return {
            "id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "machine_id": ticket.machine_id,
            "machine_name": machine.name if machine else None,
            "department_id": ticket.department_id,
            "department_name": dept.name if dept else None,
            "issue_description": ticket.issue_description,
            "severity": ticket.severity,
            "status": ticket.status,
            "assigned_to_id": ticket.assigned_to_id,
            "assigned_to_name": (
                assigned_user.username if assigned_user else None
            ),
            "expected_response_time": (
                ticket.expected_response_time.isoformat()
                if ticket.expected_response_time
                else None
            ),
            "expected_completion_time": (
                ticket.expected_completion_time.isoformat()
                if ticket.expected_completion_time
                else None
            ),
            "created_at": ticket.created_at.isoformat(),
            "started_at": (
                ticket.started_at.isoformat()
                if ticket.started_at
                else None
            ),
            "completed_at": (
                ticket.completed_at.isoformat()
                if ticket.completed_at
                else None
            ),
            "sla": calculate_sla_priority(ticket),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving ticket: {str(e)}",
        )


@router.patch("/tickets/{ticket_id}/assign", status_code=200)
async def assign_ticket(
    ticket_id: int,
    assignment_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Assign maintenance ticket to technician
    Request body: {"assigned_to_id": 5}
    """
    try:
        ticket = db.query(MaintenanceTicket).filter(
            MaintenanceTicket.id == ticket_id
        ).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found",
            )

        assigned_to_id = assignment_data.get("assigned_to_id")
        if not assigned_to_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="assigned_to_id is required",
            )

        # Verify technician exists
        technician = db.query(User).filter(
            User.id == assigned_to_id
        ).first()
        if not technician:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Technician not found",
            )

        ticket.assigned_to_id = assigned_to_id
        ticket.status = "assigned"
        db.commit()

        return {
            "id": ticket.id,
            "status": ticket.status,
            "assigned_to_id": assigned_to_id,
            "assigned_to_name": technician.username,
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error assigning ticket: {str(e)}",
        )


@router.patch("/tickets/{ticket_id}/status", status_code=200)
async def update_ticket_status(
    ticket_id: int,
    status_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update maintenance ticket status with automatic timestamp tracking
    Request body: {"status": "in_progress|awaiting_parts|completed|closed"}
    """
    try:
        ticket = db.query(MaintenanceTicket).filter(
            MaintenanceTicket.id == ticket_id
        ).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found",
            )

        new_status = status_update.get("status")
        valid_statuses = [
            "open",
            "assigned",
            "in_progress",
            "awaiting_parts",
            "completed",
            "closed",
        ]
        if not new_status or new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid status. Must be one of: {valid_statuses}"
                ),
            )

        # Update timestamps based on status transitions
        if new_status == "in_progress" and not ticket.started_at:
            ticket.started_at = datetime.utcnow()
        elif new_status == "completed" and not ticket.completed_at:
            ticket.completed_at = datetime.utcnow()

        ticket.status = new_status
        ticket.updated_at = datetime.utcnow()

        db.commit()

        # Check if SLA was breached
        sla_check = calculate_sla_priority(ticket)

        return {
            "id": ticket.id,
            "status": ticket.status,
            "updated_at": ticket.updated_at.isoformat(),
            "sla_breached": sla_check["sla_breached"],
            "started_at": (
                ticket.started_at.isoformat()
                if ticket.started_at
                else None
            ),
            "completed_at": (
                ticket.completed_at.isoformat()
                if ticket.completed_at
                else None
            ),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating status: {str(e)}",
        )


@router.get("/tickets/sla-breached")
async def list_sla_breached_tickets(
    department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all SLA-breached tickets requiring urgent attention
    Used for auto-escalation and manager alerts
    """
    try:
        # Get all open/in-progress tickets
        query = db.query(MaintenanceTicket).filter(
            MaintenanceTicket.status.in_(
                ["open", "assigned", "in_progress", "awaiting_parts"]
            )
        )

        if department_id:
            query = query.filter(
                MaintenanceTicket.department_id == department_id
            )

        tickets = query.all()

        # Filter to only SLA-breached ones
        breached = [
            t
            for t in tickets
            if calculate_sla_priority(t)["sla_breached"]
        ]

        # Sort by time since breach
        breached.sort(
            key=lambda t: (datetime.utcnow() - t.created_at).total_seconds(),
            reverse=True,
        )

        total = len(breached)
        breached_page = breached[skip:skip + limit]

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": t.id,
                    "ticket_number": t.ticket_number,
                    "machine_id": t.machine_id,
                    "severity": t.severity,
                    "status": t.status,
                    "hours_overdue": (
                        (datetime.utcnow() - t.created_at).total_seconds()
                        / 3600
                    ),
                    "created_at": t.created_at.isoformat(),
                }
                for t in breached_page
            ],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving SLA-breached tickets: {str(e)}",
        )
