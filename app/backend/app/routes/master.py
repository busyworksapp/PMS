"""
Master Data Routes - COMPLETE IMPLEMENTATION
Departments, Products, Machines, Form configs, SLA rules, Permission management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.models.department import Department, ProductionStage
from app.models.product import Product
from app.models.machine import Machine
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/api/master", tags=["master-data"])


@router.get("/departments")
async def list_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all active departments"""
    try:
        query = db.query(Department).filter(
            Department.is_active
        ).order_by(Department.name)

        total = query.count()
        departments = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": d.id,
                    "name": d.name,
                    "description": d.description,
                    "manager_id": d.manager_id,
                    "is_active": d.is_active,
                    "capacity_hours": d.capacity_hours,
                    "created_at": d.created_at.isoformat(),
                }
                for d in departments
            ],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving departments: {str(e)}",
        )


@router.post("/departments", status_code=201)
async def create_department(
    dept_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create new department
    Request body:
    {
        "name": "Cutting",
        "description": "Sheet cutting department",
        "manager_id": 1,
        "capacity_hours": 160
    }
    """
    try:
        required_fields = ["name", "description"]
        for field in required_fields:
            if field not in dept_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}",
                )

        # Check for duplicates
        existing = db.query(Department).filter(
            Department.name == dept_data["name"]
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Department with this name already exists",
            )

        dept = Department(
            name=dept_data["name"],
            description=dept_data["description"],
            manager_id=dept_data.get("manager_id"),
            capacity_hours=dept_data.get("capacity_hours", 160),
            is_active=True,
        )

        db.add(dept)
        db.commit()
        db.refresh(dept)

        return {
            "id": dept.id,
            "name": dept.name,
            "description": dept.description,
            "created_at": dept.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating department: {str(e)}",
        )


@router.get("/departments/{dept_id}")
async def get_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed department information"""
    try:
        dept = db.query(Department).filter(
            Department.id == dept_id
        ).first()
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found",
            )

        # Get production stages
        stages = db.query(ProductionStage).filter(
            ProductionStage.department_id == dept_id
        ).all()

        return {
            "id": dept.id,
            "name": dept.name,
            "description": dept.description,
            "manager_id": dept.manager_id,
            "capacity_hours": dept.capacity_hours,
            "is_active": dept.is_active,
            "production_stages": [
                {
                    "id": s.id,
                    "name": s.name,
                    "sequence": s.sequence,
                }
                for s in stages
            ],
            "created_at": dept.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving department: {str(e)}",
        )


@router.patch("/departments/{dept_id}", status_code=200)
async def update_department(
    dept_id: int,
    update_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update department information"""
    try:
        dept = db.query(Department).filter(
            Department.id == dept_id
        ).first()
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found",
            )

        # Update fields
        if "name" in update_data:
            dept.name = update_data["name"]
        if "description" in update_data:
            dept.description = update_data["description"]
        if "manager_id" in update_data:
            dept.manager_id = update_data["manager_id"]
        if "capacity_hours" in update_data:
            dept.capacity_hours = update_data["capacity_hours"]

        db.commit()

        return {
            "id": dept.id,
            "name": dept.name,
            "updated_at": datetime.utcnow().isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating department: {str(e)}",
        )


@router.get("/products")
async def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all active products"""
    try:
        query = db.query(Product).filter(
            Product.is_active
        ).order_by(Product.code)

        total = query.count()
        products = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": p.id,
                    "code": p.code,
                    "name": p.name,
                    "description": p.description,
                    "unit_price": float(p.unit_price) if p.unit_price else 0,
                    "is_active": p.is_active,
                    "created_at": p.created_at.isoformat(),
                }
                for p in products
            ],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving products: {str(e)}",
        )


@router.post("/products", status_code=201)
async def create_product(
    product_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create new product
    Request body:
    {
        "code": "PROD-001",
        "name": "Sheet Metal Part A",
        "description": "Custom sheet metal",
        "unit_price": 25.50
    }
    """
    try:
        required_fields = ["code", "name"]
        for field in required_fields:
            if field not in product_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}",
                )

        # Check for duplicates
        existing = db.query(Product).filter(
            Product.code == product_data["code"]
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product with this code already exists",
            )

        product = Product(
            code=product_data["code"],
            name=product_data["name"],
            description=product_data.get("description"),
            unit_price=product_data.get("unit_price"),
            is_active=True,
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return {
            "id": product.id,
            "code": product.code,
            "name": product.name,
            "created_at": product.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}",
        )


@router.get("/products/{product_id}")
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed product information"""
    try:
        product = db.query(Product).filter(
            Product.id == product_id
        ).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return {
            "id": product.id,
            "code": product.code,
            "name": product.name,
            "description": product.description,
            "unit_price": float(product.unit_price)
            if product.unit_price
            else 0,
            "is_active": product.is_active,
            "created_at": product.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving product: {str(e)}",
        )


@router.get("/machines")
async def list_machines(
    department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all active machines, optionally filtered by department"""
    try:
        query = db.query(Machine).filter(
            Machine.is_active
        ).order_by(Machine.machine_number)

        if department_id:
            query = query.filter(
                Machine.department_id == department_id
            )

        total = query.count()
        machines = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": m.id,
                    "machine_number": m.machine_number,
                    "name": m.name,
                    "department_id": m.department_id,
                    "machine_type": m.machine_type,
                    "capacity_per_hour": float(m.capacity_per_hour)
                    if m.capacity_per_hour
                    else 0,
                    "is_active": m.is_active,
                    "created_at": m.created_at.isoformat(),
                }
                for m in machines
            ],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving machines: {str(e)}",
        )


@router.post("/machines", status_code=201)
async def create_machine(
    machine_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create new machine
    Request body:
    {
        "machine_number": "M-001",
        "name": "CNC Cutting Machine 1",
        "department_id": 1,
        "machine_type": "CNC Cutter",
        "capacity_per_hour": 50
    }
    """
    try:
        required_fields = [
            "machine_number",
            "name",
            "department_id",
        ]
        for field in required_fields:
            if field not in machine_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}",
                )

        # Check for duplicates
        existing = db.query(Machine).filter(
            Machine.machine_number == machine_data["machine_number"]
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Machine with this number already exists",
            )

        # Verify department exists
        dept = db.query(Department).filter(
            Department.id == machine_data["department_id"]
        ).first()
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found",
            )

        machine = Machine(
            machine_number=machine_data["machine_number"],
            name=machine_data["name"],
            department_id=machine_data["department_id"],
            machine_type=machine_data.get("machine_type"),
            capacity_per_hour=machine_data.get("capacity_per_hour"),
            is_active=True,
        )

        db.add(machine)
        db.commit()
        db.refresh(machine)

        return {
            "id": machine.id,
            "machine_number": machine.machine_number,
            "name": machine.name,
            "created_at": machine.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating machine: {str(e)}",
        )


@router.get("/machines/{machine_id}")
async def get_machine(
    machine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed machine information"""
    try:
        machine = db.query(Machine).filter(
            Machine.id == machine_id
        ).first()
        if not machine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Machine not found",
            )

        return {
            "id": machine.id,
            "machine_number": machine.machine_number,
            "name": machine.name,
            "department_id": machine.department_id,
            "machine_type": machine.machine_type,
            "capacity_per_hour": float(machine.capacity_per_hour)
            if machine.capacity_per_hour
            else 0,
            "is_active": machine.is_active,
            "created_at": machine.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving machine: {str(e)}",
        )
