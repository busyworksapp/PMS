"""
Defects Module Routes - COMPLETE IMPLEMENTATION
Internal rejects, customer returns, replacement tickets, approval workflows
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime
from typing import List, Optional
from app.db.database import get_db
from app.models.defect import InternalReject, CustomerReturn
from app.models.job_planning import Order
from app.models.product import Product
from app.models.department import Department
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/api/defects", tags=["defects"])


@router.get("/rejects")
async def list_rejects(
    status: Optional[str] = None,
    order_id: Optional[int] = None,
    department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List internal rejects with filtering and pagination
    Query params: status, order_id, department_id, skip, limit
    """
    try:
        query = db.query(InternalReject).order_by(
            desc(InternalReject.created_at)
        )

        if status:
            query = query.filter(InternalReject.status == status)
        if order_id:
            query = query.filter(InternalReject.order_id == order_id)
        if department_id:
            query = query.filter(
                InternalReject.department_id == department_id
            )

        total = query.count()
        rejects = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": r.id,
                    "ticket_number": r.ticket_number,
                    "order_id": r.order_id,
                    "product_id": r.product_id,
                    "quantity_rejected": r.quantity_rejected,
                    "production_stage": r.production_stage,
                    "department_id": r.department_id,
                    "reason": r.reason,
                    "status": r.status,
                    "created_by_id": r.created_by_id,
                    "created_at": r.created_at.isoformat(),
                    "approved_by_id": r.approved_by_id,
                    "approved_at": (
                        r.approved_at.isoformat()
                        if r.approved_at
                        else None
                    ),
                }
                for r in rejects
            ],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving rejects: {str(e)}",
        )


@router.post("/rejects", status_code=201)
async def create_reject(
    reject_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create internal reject ticket
    Request body:
    {
        "order_id": 1,
        "product_id": 1,
        "quantity_rejected": 50,
        "production_stage": "Cutting",
        "department_id": 1,
        "reason": "Dimension out of spec"
    }
    """
    try:
        # Validate required fields
        required_fields = [
            "order_id",
            "quantity_rejected",
            "production_stage",
            "department_id",
            "reason",
        ]
        for field in required_fields:
            if field not in reject_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}",
                )

        # Verify order exists
        order = db.query(Order).filter(
            Order.id == reject_data["order_id"]
        ).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        # Verify department exists
        dept = db.query(Department).filter(
            Department.id == reject_data["department_id"]
        ).first()
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found",
            )

        # Verify product if provided
        if reject_data.get("product_id"):
            product = db.query(Product).filter(
                Product.id == reject_data["product_id"]
            ).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found",
                )

        # Generate ticket number
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        ticket_number = f"RJT-{timestamp}"

        reject = InternalReject(
            ticket_number=ticket_number,
            order_id=reject_data["order_id"],
            product_id=reject_data.get("product_id"),
            quantity_rejected=reject_data["quantity_rejected"],
            production_stage=reject_data["production_stage"],
            department_id=reject_data["department_id"],
            reason=reject_data["reason"],
            status="pending",
            created_by_id=current_user.id,
        )

        db.add(reject)
        db.commit()
        db.refresh(reject)

        # Auto-hold order if No Stock status set
        if reject_data.get("status") == "no_stock":
            order.status = "on_hold"
            db.commit()

        return {
            "id": reject.id,
            "ticket_number": reject.ticket_number,
            "status": reject.status,
            "created_at": reject.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating reject: {str(e)}",
        )


@router.get("/rejects/{reject_id}")
async def get_reject(
    reject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed reject information"""
    try:
        reject = db.query(InternalReject).filter(
            InternalReject.id == reject_id
        ).first()
        if not reject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reject not found",
            )

        # Load relationships
        order = db.query(Order).filter(
            Order.id == reject.order_id
        ).first()
        dept = db.query(Department).filter(
            Department.id == reject.department_id
        ).first()

        return {
            "id": reject.id,
            "ticket_number": reject.ticket_number,
            "order_id": reject.order_id,
            "order_number": order.order_number if order else None,
            "product_id": reject.product_id,
            "quantity_rejected": reject.quantity_rejected,
            "production_stage": reject.production_stage,
            "department_id": reject.department_id,
            "department_name": dept.name if dept else None,
            "reason": reject.reason,
            "status": reject.status,
            "created_by_id": reject.created_by_id,
            "created_at": reject.created_at.isoformat(),
            "approved_by_id": reject.approved_by_id,
            "approved_at": (
                reject.approved_at.isoformat()
                if reject.approved_at
                else None
            ),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving reject: {str(e)}",
        )


@router.patch("/rejects/{reject_id}/approve", status_code=200)
async def approve_reject(
    reject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Approve replacement ticket (manager/QC approval)
    Changes status: pending → approved
    """
    try:
        reject = db.query(InternalReject).filter(
            InternalReject.id == reject_id
        ).first()
        if not reject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reject not found",
            )

        if reject.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot approve reject with status: {reject.status}",
            )

        reject.status = "approved"
        reject.approved_at = datetime.utcnow()
        reject.approved_by_id = current_user.id

        db.commit()

        return {
            "id": reject.id,
            "ticket_number": reject.ticket_number,
            "status": reject.status,
            "approved_at": reject.approved_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error approving reject: {str(e)}",
        )


@router.patch("/rejects/{reject_id}/status", status_code=200)
async def update_reject_status(
    reject_id: int,
    status_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update reject status
    Request body: {"status": "no_stock|replacement_processed|rejected"}
    """
    try:
        reject = db.query(InternalReject).filter(
            InternalReject.id == reject_id
        ).first()
        if not reject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reject not found",
            )

        valid_statuses = [
            "pending",
            "approved",
            "no_stock",
            "replacement_processed",
            "rejected",
        ]
        new_status = status_update.get("status")
        if not new_status or new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {valid_statuses}",
            )

        # Auto-hold order if No Stock
        if new_status == "no_stock":
            order = db.query(Order).filter(
                Order.id == reject.order_id
            ).first()
            if order:
                order.status = "on_hold"

        reject.status = new_status
        reject.updated_at = datetime.utcnow()

        db.commit()

        return {
            "id": reject.id,
            "status": reject.status,
            "updated_at": reject.updated_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating status: {str(e)}",
        )


@router.get("/returns")
async def list_returns(
    order_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List customer returns with filtering and pagination"""
    try:
        query = db.query(CustomerReturn).order_by(
            desc(CustomerReturn.created_at)
        )
        if order_id:
            query = query.filter(CustomerReturn.order_id == order_id)

        total = query.count()
        returns = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": r.id,
                    "ticket_number": r.ticket_number,
                    "order_id": r.order_id,
                    "product_id": r.product_id,
                    "quantity_returned": r.quantity_returned,
                    "reason": r.reason,
                    "logged_by_id": r.logged_by_id,
                    "created_at": r.created_at.isoformat(),
                }
                for r in returns
            ],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving returns: {str(e)}",
        )


@router.post("/returns", status_code=201)
async def create_return(
    return_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Log customer return
    Request body:
    {
        "order_id": 1,
        "product_id": 1,
        "quantity_returned": 25,
        "reason": "Customer reported defect"
    }
    """
    try:
        # Validate required fields
        required_fields = [
            "order_id",
            "quantity_returned",
            "reason",
        ]
        for field in required_fields:
            if field not in return_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}",
                )

        # Verify order exists
        order = db.query(Order).filter(
            Order.id == return_data["order_id"]
        ).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        # Verify product if provided
        if return_data.get("product_id"):
            product = db.query(Product).filter(
                Product.id == return_data["product_id"]
            ).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found",
                )

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        ticket_number = f"RET-{timestamp}"

        ret = CustomerReturn(
            ticket_number=ticket_number,
            order_id=return_data["order_id"],
            product_id=return_data.get("product_id"),
            quantity_returned=return_data["quantity_returned"],
            reason=return_data["reason"],
            logged_by_id=current_user.id,
        )

        db.add(ret)
        db.commit()
        db.refresh(ret)

        return {
            "id": ret.id,
            "ticket_number": ret.ticket_number,
            "created_at": ret.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating return: {str(e)}",
        )


@router.get("/returns/{return_id}")
async def get_return(
    return_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed customer return information"""
    try:
        ret = db.query(CustomerReturn).filter(
            CustomerReturn.id == return_id
        ).first()
        if not ret:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Return not found",
            )

        order = db.query(Order).filter(
            Order.id == ret.order_id
        ).first()

        return {
            "id": ret.id,
            "ticket_number": ret.ticket_number,
            "order_id": ret.order_id,
            "order_number": order.order_number if order else None,
            "product_id": ret.product_id,
            "quantity_returned": ret.quantity_returned,
            "reason": ret.reason,
            "logged_by_id": ret.logged_by_id,
            "created_at": ret.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving return: {str(e)}",
        )
