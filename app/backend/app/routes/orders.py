"""
Orders Module Routes - CONSOLIDATED VIEW
This module consolidates order data from the Job Planning module
Read-only consolidated view + legacy order support
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from app.db.database import get_db
from app.models.order import Order, OrderItem, OrderSchedule
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("")
async def list_orders(
    status: Optional[str] = None,
    department_id: Optional[int] = None,
    customer_name: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all orders with consolidated view
    This is a read-only view of orders from Job Planning module
    Query params: status, department_id, customer_name, skip, limit
    """
    try:
        query = db.query(Order).order_by(
            desc(Order.created_at)
        )

        if status:
            query = query.filter(Order.status == status)
        if department_id:
            query = query.filter(Order.primary_department_id == (
                department_id
            ))
        if customer_name:
            query = query.filter(
                Order.customer_name.ilike(f"%{customer_name}%")
            )

        total = query.count()
        orders = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": o.id,
                    "order_number": o.order_number,
                    "sales_order_number": o.sales_order_number,
                    "customer_name": o.customer_name,
                    "quantity": o.quantity,
                    "order_value": float(o.order_value)
                    if o.order_value
                    else 0,
                    "status": o.status,
                    "start_date": (
                        o.start_date.isoformat()
                        if o.start_date
                        else None
                    ),
                    "end_date": (
                        o.end_date.isoformat()
                        if o.end_date
                        else None
                    ),
                    "created_at": o.created_at.isoformat(),
                }
                for o in orders
            ],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving orders: {str(e)}",
        )


@router.get("/{order_id}")
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get detailed order information with items and schedules
    Consolidated view of complete order data
    """
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        # Get items
        items = db.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()

        # Get schedules
        schedules = db.query(OrderSchedule).filter(
            OrderSchedule.order_id == order_id
        ).all()

        return {
            "id": order.id,
            "order_number": order.order_number,
            "sales_order_number": order.sales_order_number,
            "customer_name": order.customer_name,
            "quantity": order.quantity,
            "order_value": float(order.order_value)
            if order.order_value
            else 0,
            "status": order.status,
            "start_date": (
                order.start_date.isoformat()
                if order.start_date
                else None
            ),
            "end_date": (
                order.end_date.isoformat()
                if order.end_date
                else None
            ),
            "items": [
                {
                    "id": i.id,
                    "product_id": i.product_id,
                    "quantity": i.quantity,
                }
                for i in items
            ],
            "schedules": [
                {
                    "id": s.id,
                    "machine_id": s.machine_id,
                    "scheduled_start": (
                        s.scheduled_start.isoformat()
                        if s.scheduled_start
                        else None
                    ),
                    "scheduled_end": (
                        s.scheduled_end.isoformat()
                        if s.scheduled_end
                        else None
                    ),
                    "status": s.status,
                }
                for s in schedules
            ],
            "created_at": order.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving order: {str(e)}",
        )


@router.get("/{order_id}/items")
async def get_order_items(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all items for an order"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        items = db.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()

        return {
            "order_id": order_id,
            "order_number": order.order_number,
            "items": [
                {
                    "id": i.id,
                    "product_id": i.product_id,
                    "quantity": i.quantity,
                }
                for i in items
            ],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving items: {str(e)}",
        )


@router.get("/{order_id}/schedules")
async def get_order_schedules(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all schedules for an order"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        schedules = db.query(OrderSchedule).filter(
            OrderSchedule.order_id == order_id
        ).all()

        return {
            "order_id": order_id,
            "order_number": order.order_number,
            "schedules": [
                {
                    "id": s.id,
                    "machine_id": s.machine_id,
                    "scheduled_start": (
                        s.scheduled_start.isoformat()
                        if s.scheduled_start
                        else None
                    ),
                    "scheduled_end": (
                        s.scheduled_end.isoformat()
                        if s.scheduled_end
                        else None
                    ),
                    "status": s.status,
                }
                for s in schedules
            ],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving schedules: {str(e)}",
        )
