"""
SOP/NCR Module Routes - COMPLETE IMPLEMENTATION
SOP failure tickets, NCR workflow, HOD escalation, SLA enforcement
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.models.sop_ncr import SOPFailureTicket, NonConformanceReport
from app.models.department import Department
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/api/sop-ncr", tags=["sop-ncr"])

# SLA for SOP Failure tickets (in hours)
SOP_TICKET_SLA = {
    "response": 24,  # 24 hours to charge department to respond
    "completion": 72,  # 72 hours to complete investigation
}


def calculate_sop_sla_status(ticket: SOPFailureTicket) -> dict:
    """
    Calculate SLA status for SOP failure tickets
    Returns: {status: "on_track"|"at_risk"|"breached", hours_remaining: int}
    """
    now = datetime.utcnow()
    created_age = (now - ticket.created_at).total_seconds() / 3600

    if ticket.status in ["closed"]:
        return {
            "status": "completed",
            "hours_remaining": 0,
            "sla_breached": False,
        }

    response_deadline = SOP_TICKET_SLA["response"]
    hours_remaining = response_deadline - created_age

    if hours_remaining <= 0:
        return {
            "status": "breached",
            "hours_remaining": 0,
            "sla_breached": True,
        }
    elif hours_remaining <= 4:
        return {
            "status": "at_risk",
            "hours_remaining": hours_remaining,
            "sla_breached": False,
        }
    else:
        return {
            "status": "on_track",
            "hours_remaining": hours_remaining,
            "sla_breached": False,
        }


@router.get("/tickets")
async def list_sop_tickets(
    status: Optional[str] = None,
    charged_department_id: Optional[int] = None,
    charging_department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List SOP failure tickets with SLA status
    Query params: status, charged_department_id, charging_department_id,
    skip, limit
    """
    try:
        query = db.query(SOPFailureTicket).order_by(
            desc(SOPFailureTicket.created_at)
        )
        if status:
            query = query.filter(SOPFailureTicket.status == status)
        if charged_department_id:
            query = query.filter(
                SOPFailureTicket.charged_department_id == (
                    charged_department_id
                )
            )
        if charging_department_id:
            query = query.filter(
                SOPFailureTicket.charging_department_id == (
                    charging_department_id
                )
            )

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
                    "sop_reference": t.sop_reference,
                    "description": t.description,
                    "charged_department_id": t.charged_department_id,
                    "charging_department_id": t.charging_department_id,
                    "status": t.status,
                    "hod_decision": t.hod_decision,
                    "created_at": t.created_at.isoformat(),
                    "sla": calculate_sop_sla_status(t),
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
async def create_sop_ticket(
    ticket_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create SOP failure ticket
    Request body:
    {
        "sop_reference": "SOP-001-2025",
        "description": "Operator skipped quality check",
        "impact_description": "Potential non-conformance in batch",
        "charged_department_id": 2,
        "charging_department_id": 1
    }
    """
    try:
        # Validate required fields
        required_fields = [
            "sop_reference",
            "description",
            "charged_department_id",
            "charging_department_id",
        ]
        for field in required_fields:
            if field not in ticket_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}",
                )

        # Verify both departments exist
        charged_dept = db.query(Department).filter(
            Department.id == ticket_data["charged_department_id"]
        ).first()
        if not charged_dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Charged department not found",
            )

        charging_dept = db.query(Department).filter(
            Department.id == ticket_data["charging_department_id"]
        ).first()
        if not charging_dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Charging department not found",
            )

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        ticket_number = f"SOP-{timestamp}"

        ticket = SOPFailureTicket(
            ticket_number=ticket_number,
            sop_reference=ticket_data["sop_reference"],
            description=ticket_data["description"],
            impact_description=ticket_data.get("impact_description"),
            charged_department_id=ticket_data["charged_department_id"],
            charging_department_id=ticket_data["charging_department_id"],
            status="open",
            created_by_id=current_user.id,
        )

        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return {
            "id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "status": ticket.status,
            "created_at": ticket.created_at.isoformat(),
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
async def get_sop_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed SOP ticket information"""
    try:
        ticket = db.query(SOPFailureTicket).filter(
            SOPFailureTicket.id == ticket_id
        ).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SOP ticket not found",
            )

        # Load relationships
        charged_dept = db.query(Department).filter(
            Department.id == ticket.charged_department_id
        ).first()
        charging_dept = db.query(Department).filter(
            Department.id == ticket.charging_department_id
        ).first()

        # Get related NCR if exists
        ncr = db.query(NonConformanceReport).filter(
            NonConformanceReport.sop_ticket_id == ticket_id
        ).first()

        return {
            "id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "sop_reference": ticket.sop_reference,
            "description": ticket.description,
            "impact_description": ticket.impact_description,
            "charged_department_id": ticket.charged_department_id,
            "charged_department_name": (
                charged_dept.name if charged_dept else None
            ),
            "charging_department_id": ticket.charging_department_id,
            "charging_department_name": (
                charging_dept.name if charging_dept else None
            ),
            "status": ticket.status,
            "hod_decision": ticket.hod_decision,
            "rejection_reason": ticket.rejection_reason,
            "reassignment_reason": ticket.reassignment_reason,
            "created_at": ticket.created_at.isoformat(),
            "closed_at": (
                ticket.closed_at.isoformat() if ticket.closed_at else None
            ),
            "ncr_id": ncr.id if ncr else None,
            "sla": calculate_sop_sla_status(ticket),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving ticket: {str(e)}",
        )


@router.patch("/tickets/{ticket_id}/reject", status_code=200)
async def reject_ticket(
    ticket_id: int,
    rejection_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Reject SOP failure ticket (charged dept rejects responsibility)
    Escalates to HOD for final decision
    Request body: {"rejection_reason": "Not our fault, bad material"}
    """
    try:
        ticket = db.query(SOPFailureTicket).filter(
            SOPFailureTicket.id == ticket_id
        ).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SOP ticket not found",
            )

        if ticket.status != "open":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Cannot reject ticket with status: {ticket.status}"
                ),
            )

        rejection_reason = rejection_data.get("rejection_reason")
        if not rejection_reason:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="rejection_reason is required",
            )

        ticket.status = "escalated"
        ticket.rejection_reason = rejection_reason
        ticket.updated_at = datetime.utcnow()

        db.commit()

        return {
            "id": ticket.id,
            "status": ticket.status,
            "escalation_reason": "awaiting_hod_decision",
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error rejecting ticket: {str(e)}",
        )


@router.patch("/tickets/{ticket_id}/reassign", status_code=200)
async def reassign_ticket(
    ticket_id: int,
    reassignment_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Reassign SOP failure ticket to another department
    Request body: {
        "reassigned_to_department_id": 3,
        "reassignment_reason": "Actual cause was supplier material"
    }
    """
    try:
        ticket = db.query(SOPFailureTicket).filter(
            SOPFailureTicket.id == ticket_id
        ).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SOP ticket not found",
            )

        new_dept_id = reassignment_data.get("reassigned_to_department_id")
        if not new_dept_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reassigned_to_department_id is required",
            )

        # Verify new department exists
        new_dept = db.query(Department).filter(
            Department.id == new_dept_id
        ).first()
        if not new_dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target department not found",
            )

        ticket.reassigned_from_id = ticket.charged_department_id
        ticket.charged_department_id = new_dept_id
        ticket.reassignment_reason = reassignment_data.get(
            "reassignment_reason"
        )
        ticket.status = "open"  # Reset for new department
        ticket.updated_at = datetime.utcnow()

        db.commit()

        return {
            "id": ticket.id,
            "status": ticket.status,
            "reassigned_to": new_dept_id,
            "message": "Ticket reassigned and reset to open status",
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reassigning ticket: {str(e)}",
        )


@router.patch("/tickets/{ticket_id}/hod-decision", status_code=200)
async def hod_decision(
    ticket_id: int,
    decision_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    HOD makes final decision on escalated ticket
    Request body: {
        "decision": "accept|reject",
        "hod_notes": "Agreed - supplier material was out of spec"
    }
    """
    try:
        ticket = db.query(SOPFailureTicket).filter(
            SOPFailureTicket.id == ticket_id
        ).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SOP ticket not found",
            )

        if ticket.status != "escalated":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Cannot make HOD decision on ticket with "
                    f"status: {ticket.status}"
                ),
            )

        decision = decision_data.get("decision")
        if decision not in ["accept", "reject"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="decision must be 'accept' or 'reject'",
            )

        ticket.escalated_to_hod_id = current_user.id
        ticket.hod_decision = decision
        ticket.updated_at = datetime.utcnow()

        if decision == "accept":
            ticket.status = "in_investigation"
        else:
            ticket.status = "closed"
            ticket.closed_at = datetime.utcnow()

        db.commit()

        return {
            "id": ticket.id,
            "status": ticket.status,
            "hod_decision": decision,
            "decided_at": ticket.updated_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error making HOD decision: {str(e)}",
        )


@router.post("/tickets/{ticket_id}/ncr", status_code=201)
async def submit_ncr(
    ticket_id: int,
    ncr_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit Non-Conformance Report for SOP ticket
    Request body: {
        "root_cause": "Operator skill gap in quality check procedure",
        "corrective_actions": "Provide additional training to operator",
        "preventive_measures": "Implement weekly quality audits"
    }
    """
    try:
        ticket = db.query(SOPFailureTicket).filter(
            SOPFailureTicket.id == ticket_id
        ).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SOP ticket not found",
            )

        if ticket.status != "in_investigation":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Cannot submit NCR for ticket with "
                    f"status: {ticket.status}"
                ),
            )

        # Validate required fields
        required_fields = [
            "root_cause",
            "corrective_actions",
            "preventive_measures",
        ]
        for field in required_fields:
            if field not in ncr_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}",
                )

        ncr = NonConformanceReport(
            sop_ticket_id=ticket_id,
            root_cause=ncr_data["root_cause"],
            corrective_actions=ncr_data["corrective_actions"],
            preventive_measures=ncr_data["preventive_measures"],
            submitted_by_id=current_user.id,
        )
        db.add(ncr)

        ticket.status = "closed"
        ticket.closed_at = datetime.utcnow()
        ticket.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(ncr)

        return {
            "ncr_id": ncr.id,
            "sop_ticket_id": ticket_id,
            "ticket_status": "closed",
            "created_at": ncr.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting NCR: {str(e)}",
        )


@router.get("/ncr/{ncr_id}")
async def get_ncr(
    ncr_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get Non-Conformance Report details"""
    try:
        ncr = db.query(NonConformanceReport).filter(
            NonConformanceReport.id == ncr_id
        ).first()
        if not ncr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="NCR not found",
            )

        ticket = db.query(SOPFailureTicket).filter(
            SOPFailureTicket.id == ncr.sop_ticket_id
        ).first()
        submitter = db.query(User).filter(
            User.id == ncr.submitted_by_id
        ).first()

        return {
            "id": ncr.id,
            "sop_ticket_id": ncr.sop_ticket_id,
            "sop_ticket_number": (
                ticket.ticket_number if ticket else None
            ),
            "root_cause": ncr.root_cause,
            "corrective_actions": ncr.corrective_actions,
            "preventive_measures": ncr.preventive_measures,
            "submitted_by_id": ncr.submitted_by_id,
            "submitted_by_name": (
                submitter.username if submitter else None
            ),
            "created_at": ncr.created_at.isoformat(),
            "updated_at": ncr.updated_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving NCR: {str(e)}",
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
    List all SLA-breached SOP tickets requiring urgent attention
    Auto-escalation alert endpoint
    """
    try:
        query = db.query(SOPFailureTicket).filter(
            SOPFailureTicket.status.in_(
                ["open", "in_investigation"]
            )
        )

        if department_id:
            query = query.filter(
                SOPFailureTicket.charged_department_id == department_id
            )

        tickets = query.all()

        # Filter to breached ones
        breached = [
            t
            for t in tickets
            if calculate_sop_sla_status(t)["sla_breached"]
        ]

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
                    "sop_reference": t.sop_reference,
                    "charged_department_id": t.charged_department_id,
                    "status": t.status,
                    "hours_overdue": (
                        (datetime.utcnow() - t.created_at)
                        .total_seconds()
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
