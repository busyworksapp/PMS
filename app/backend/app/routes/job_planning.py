"""
Job Planning Routes
Handles order scheduling, capacity planning, and production management
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.models.order import Order, OrderItem, OrderSchedule, OrderStatusEnum
from app.models.product import ProductionStage
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/api/job-planning", tags=["Job Planning"])


# ============== Order Management ==============

@router.post("/orders")
def create_order(
    order_number: str,
    customer_name: str,
    product_id: int,
    quantity: int,
    start_date: datetime,
    end_date: datetime,
    priority: str = "normal",
    notes: Optional[str] = None,
    primary_department_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new order"""
    # Check if order already exists
    existing = db.query(Order).filter(
        Order.order_number == order_number
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Order number already exists"
        )
    
    # Validate dates
    if start_date >= end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date must be before end date"
        )
    
    new_order = Order(
        order_number=order_number,
        customer_name=customer_name,
        product_id=product_id,
        quantity=quantity,
        start_date=start_date,
        end_date=end_date,
        priority=priority,
        notes=notes,
        primary_department_id=primary_department_id,
        created_by_id=current_user.id
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {
        "message": "Order created successfully",
        "order_id": new_order.id,
        "order_number": new_order.order_number
    }


@router.get("/orders")
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all orders with filters"""
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    if priority:
        query = query.filter(Order.priority == priority)
    
    total = query.count()
    orders = query.order_by(desc(Order.created_at)).offset(
        skip
    ).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "orders": [
            {
                "id": o.id,
                "order_number": o.order_number,
                "customer_name": o.customer_name,
                "quantity": o.quantity,
                "completed_quantity": o.completed_quantity,
                "status": o.status,
                "priority": o.priority,
                "start_date": o.start_date,
                "end_date": o.end_date,
                "progress": round(
                    (o.completed_quantity / o.quantity * 100)
                    if o.quantity > 0 else 0,
                    2
                )
            } for o in orders
        ]
    }


@router.get("/orders/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get order details"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {
        "id": order.id,
        "order_number": order.order_number,
        "customer_name": order.customer_name,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "completed_quantity": order.completed_quantity,
        "rejected_quantity": order.rejected_quantity,
        "status": order.status,
        "priority": order.priority,
        "start_date": order.start_date,
        "end_date": order.end_date,
        "created_at": order.created_at,
        "items_count": len(order.items),
        "schedules_count": len(order.schedules)
    }


@router.put("/orders/{order_id}")
def update_order(
    order_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update order details"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if status:
        order.status = status
    if priority:
        order.priority = priority
    if notes is not None:
        order.notes = notes
    
    order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    
    return {"message": "Order updated successfully"}


@router.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    
    return {"message": "Order deleted successfully"}


# ============== Order Items ==============

@router.post("/orders/{order_id}/items")
def add_order_item(
    order_id: int,
    item_number: int,
    description: str,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add item to order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    item = OrderItem(
        order_id=order_id,
        item_number=item_number,
        description=description,
        quantity=quantity
    )
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return {
        "message": "Item added successfully",
        "item_id": item.id
    }


@router.get("/orders/{order_id}/items")
def list_order_items(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List order items"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    items = db.query(OrderItem).filter(
        OrderItem.order_id == order_id
    ).all()
    
    return {
        "order_id": order_id,
        "items": [
            {
                "id": item.id,
                "item_number": item.item_number,
                "description": item.description,
                "quantity": item.quantity,
                "completed_quantity": item.completed_quantity,
                "rejected_quantity": item.rejected_quantity,
                "status": item.status
            } for item in items
        ]
    }


@router.put("/orders/{order_id}/items/{item_id}")
def update_order_item(
    order_id: int,
    item_id: int,
    status: Optional[str] = None,
    completed_quantity: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update order item"""
    item = db.query(OrderItem).filter(
        OrderItem.id == item_id,
        OrderItem.order_id == order_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    
    if status:
        item.status = status
    if completed_quantity is not None:
        item.completed_quantity = completed_quantity
    
    item.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Item updated successfully"}


# ============== Order Scheduling ==============

@router.post("/orders/{order_id}/schedules")
def create_schedule(
    order_id: int,
    sequence: int,
    department_id: int,
    stage_id: int,
    machine_id: Optional[int] = None,
    scheduled_start: Optional[datetime] = None,
    scheduled_end: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create production schedule for order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    schedule = OrderSchedule(
        order_id=order_id,
        sequence=sequence,
        department_id=department_id,
        stage_id=stage_id,
        machine_id=machine_id,
        scheduled_start=scheduled_start,
        scheduled_end=scheduled_end
    )
    
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    
    return {
        "message": "Schedule created successfully",
        "schedule_id": schedule.id
    }


@router.get("/orders/{order_id}/schedules")
def list_schedules(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List order schedules"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    schedules = db.query(OrderSchedule).filter(
        OrderSchedule.order_id == order_id
    ).order_by(OrderSchedule.sequence).all()
    
    return {
        "order_id": order_id,
        "schedules": [
            {
                "id": s.id,
                "sequence": s.sequence,
                "department_id": s.department_id,
                "stage_id": s.stage_id,
                "machine_id": s.machine_id,
                "scheduled_start": s.scheduled_start,
                "scheduled_end": s.scheduled_end,
                "status": s.status
            } for s in schedules
        ]
    }


@router.put("/schedules/{schedule_id}")
def update_schedule(
    schedule_id: int,
    status: Optional[str] = None,
    actual_start: Optional[datetime] = None,
    actual_end: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update schedule"""
    schedule = db.query(OrderSchedule).filter(
        OrderSchedule.id == schedule_id
    ).first()
    
    if not schedule:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found"
        )
    
    if status:
        schedule.status = status
    if actual_start:
        schedule.actual_start = actual_start
    if actual_end:
        schedule.actual_end = actual_end
    
    schedule.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Schedule updated successfully"}


# ============== Production Stages ==============

@router.get("/production-stages")
def list_production_stages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all production stages"""
    stages = db.query(ProductionStage).filter(
        ProductionStage.is_active == True
    ).all()
    
    return {
        "stages": [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "order": s.order,
                "department_id": s.department_id,
                "estimated_duration_minutes": s.estimated_duration_minutes
            } for s in stages
        ]
    }


# ============== Dashboard & Analytics ==============

@router.get("/dashboard")
def job_planning_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Job planning dashboard with KPIs"""
    total_orders = db.query(Order).count()
    active_orders = db.query(Order).filter(
        Order.status.in_([
            OrderStatusEnum.SCHEDULED,
            OrderStatusEnum.IN_PROGRESS
        ])
    ).count()
    completed_orders = db.query(Order).filter(
        Order.status == OrderStatusEnum.COMPLETED
    ).count()
    
    # Recent orders
    recent = db.query(Order).order_by(
        desc(Order.created_at)
    ).limit(5).all()
    
    # Overdue orders
    overdue = db.query(Order).filter(
        Order.end_date < datetime.utcnow(),
        Order.status != OrderStatusEnum.COMPLETED
    ).count()
    
    return {
        "summary": {
            "total_orders": total_orders,
            "active_orders": active_orders,
            "completed_orders": completed_orders,
            "overdue_orders": overdue,
            "completion_rate": round(
                (completed_orders / total_orders * 100) if total_orders > 0 else 0,
                2
            )
        },
        "recent_orders": [
            {
                "id": o.id,
                "order_number": o.order_number,
                "customer_name": o.customer_name,
                "status": o.status,
                "created_at": o.created_at
            } for o in recent
        ]
    }
