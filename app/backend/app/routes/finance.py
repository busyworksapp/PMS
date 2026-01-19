"""
Finance Module Routes - COMPLETE IMPLEMENTATION
BOM management, cost calculations, variance analysis, financial reporting
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from app.db.database import get_db
from app.models.bom import BOM, BOMComponent
from app.models.product import Product
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/api/finance", tags=["finance"])


@router.get("/boms")
async def list_boms(
    product_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List active BOMs with component counts"""
    try:
        query = db.query(BOM).filter(BOM.is_active == 1).order_by(
            desc(BOM.created_at)
        )
        if product_id:
            query = query.filter(BOM.product_id == product_id)

        total = query.count()
        boms = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": b.id,
                    "product_id": b.product_id,
                    "version": b.version,
                    "component_count": len(b.components),
                    "total_cost": sum(
                        float(c.quantity) * float(c.unit_cost)
                        for c in b.components
                    ),
                    "created_at": b.created_at.isoformat(),
                }
                for b in boms
            ],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving BOMs: {str(e)}",
        )


@router.post("/boms", status_code=201)
async def create_bom(
    bom_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create new BOM for a product
    Request body:
    {
        "product_id": 1,
        "components": [
            {"code": "COMP-001", "name": "Steel Sheet", "quantity": 10,
             "unit_cost": 5.00, "specifications": "2mm gauge"}
        ]
    }
    """
    try:
        if "product_id" not in bom_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="product_id is required",
            )
        if "components" not in bom_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="components list is required",
            )

        # Verify product exists
        product = db.query(Product).filter(
            Product.id == bom_data["product_id"]
        ).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        # Deactivate previous versions
        db.query(BOM).filter(
            BOM.product_id == bom_data["product_id"]
        ).update({"is_active": 0})
        db.flush()

        # Get next version number
        last_version = (
            db.query(BOM)
            .filter(BOM.product_id == bom_data["product_id"])
            .order_by(desc(BOM.version))
            .first()
        )
        next_version = (last_version.version + 1) if last_version else 1

        # Create BOM
        bom = BOM(
            product_id=bom_data["product_id"],
            version=next_version,
            is_active=1,
            created_by_id=current_user.id,
        )
        db.add(bom)
        db.flush()

        # Add components
        total_cost = 0
        for comp_data in bom_data["components"]:
            required_comp_fields = [
                "code",
                "name",
                "quantity",
                "unit_cost",
            ]
            for field in required_comp_fields:
                if field not in comp_data:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            f"Component missing required "
                            f"field: {field}"
                        ),
                    )

            component = BOMComponent(
                bom_id=bom.id,
                component_code=comp_data["code"],
                component_name=comp_data["name"],
                quantity=comp_data["quantity"],
                unit_cost=comp_data["unit_cost"],
                specifications=comp_data.get("specifications"),
            )
            db.add(component)
            total_cost += (
                float(comp_data["quantity"])
                * float(comp_data["unit_cost"])
            )

        db.commit()
        db.refresh(bom)

        return {
            "id": bom.id,
            "product_id": bom.product_id,
            "version": bom.version,
            "component_count": len(bom_data["components"]),
            "total_cost": total_cost,
            "created_at": bom.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating BOM: {str(e)}",
        )


@router.get("/boms/{bom_id}")
async def get_bom(
    bom_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed BOM with component breakdown"""
    try:
        bom = db.query(BOM).filter(BOM.id == bom_id).first()
        if not bom:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="BOM not found",
            )

        product = db.query(Product).filter(
            Product.id == bom.product_id
        ).first()

        total_cost = 0
        components = []

        for comp in bom.components:
            component_total = (
                float(comp.quantity) * float(comp.unit_cost)
            )
            total_cost += component_total

            components.append(
                {
                    "id": comp.id,
                    "code": comp.component_code,
                    "name": comp.component_name,
                    "quantity": float(comp.quantity),
                    "unit_cost": float(comp.unit_cost),
                    "total_cost": component_total,
                    "specifications": comp.specifications,
                }
            )

        return {
            "id": bom.id,
            "product_id": bom.product_id,
            "product_name": product.name if product else None,
            "version": bom.version,
            "is_active": bom.is_active,
            "components": components,
            "total_cost": total_cost,
            "component_count": len(components),
            "created_at": bom.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving BOM: {str(e)}",
        )


@router.get("/boms/{bom_id}/components")
async def get_bom_components(
    bom_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all components for a specific BOM"""
    try:
        bom = db.query(BOM).filter(BOM.id == bom_id).first()
        if not bom:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="BOM not found",
            )

        total_cost = 0
        components = []

        for comp in bom.components:
            component_total = (
                float(comp.quantity) * float(comp.unit_cost)
            )
            total_cost += component_total

            components.append(
                {
                    "id": comp.id,
                    "code": comp.component_code,
                    "name": comp.component_name,
                    "quantity": float(comp.quantity),
                    "unit_cost": float(comp.unit_cost),
                    "total_cost": component_total,
                    "specifications": comp.specifications,
                }
            )

        return {
            "bom_id": bom.id,
            "product_id": bom.product_id,
            "version": bom.version,
            "total_cost": total_cost,
            "components": components,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving components: {str(e)}",
        )


@router.post("/boms/{bom_id}/cost-impact")
async def calculate_cost_impact(
    bom_id: int,
    impact_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Calculate cost impact of rejects/returns
    Request body:
    {
        "quantity_affected": 10,
        "event_type": "reject|return"
    }
    """
    try:
        bom = db.query(BOM).filter(BOM.id == bom_id).first()
        if not bom:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="BOM not found",
            )

        quantity_affected = impact_data.get("quantity_affected")
        if not quantity_affected:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="quantity_affected is required",
            )

        event_type = impact_data.get("event_type", "reject")

        # Calculate per-unit cost
        unit_cost = sum(
            float(c.quantity) * float(c.unit_cost)
            for c in bom.components
        )

        # Calculate total impact
        total_impact = unit_cost * quantity_affected

        return {
            "bom_id": bom_id,
            "unit_cost": unit_cost,
            "quantity_affected": quantity_affected,
            "total_impact": total_impact,
            "event_type": event_type,
            "currency": "USD",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating cost impact: {str(e)}",
        )


@router.get("/boms/{bom_id}/history")
async def get_bom_history(
    bom_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get version history for a product's BOMs"""
    try:
        # Get BOM to find product_id
        bom = db.query(BOM).filter(BOM.id == bom_id).first()
        if not bom:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="BOM not found",
            )

        # Get all versions for this product
        boms = db.query(BOM).filter(
            BOM.product_id == bom.product_id
        ).order_by(desc(BOM.version)).all()

        return {
            "product_id": bom.product_id,
            "total_versions": len(boms),
            "versions": [
                {
                    "id": b.id,
                    "version": b.version,
                    "is_active": b.is_active,
                    "component_count": len(b.components),
                    "total_cost": sum(
                        float(c.quantity) * float(c.unit_cost)
                        for c in b.components
                    ),
                    "created_at": b.created_at.isoformat(),
                }
                for b in boms
            ],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving history: {str(e)}",
        )


@router.get("/cost-analysis/products/{product_id}")
async def get_product_cost_analysis(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get cost analysis for a product
    Shows current BOM cost vs historical versions
    """
    try:
        product = db.query(Product).filter(
            Product.id == product_id
        ).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        # Get active BOM
        active_bom = db.query(BOM).filter(
            BOM.product_id == product_id, BOM.is_active == 1
        ).first()

        if not active_bom:
            return {
                "product_id": product_id,
                "product_name": product.name,
                "message": "No active BOM",
            }

        active_cost = sum(
            float(c.quantity) * float(c.unit_cost)
            for c in active_bom.components
        )

        # Get all historical versions
        all_boms = db.query(BOM).filter(
            BOM.product_id == product_id
        ).order_by(desc(BOM.version)).all()

        versions = []
        for bom in all_boms:
            bom_cost = sum(
                float(c.quantity) * float(c.unit_cost)
                for c in bom.components
            )
            versions.append(
                {
                    "version": bom.version,
                    "cost": bom_cost,
                    "is_active": bom.is_active,
                    "created_at": bom.created_at.isoformat(),
                }
            )

        # Calculate variance
        previous_cost = (
            versions[1]["cost"]
            if len(versions) > 1
            else versions[0]["cost"]
        )
        variance = active_cost - previous_cost
        variance_percent = (
            (variance / previous_cost * 100)
            if previous_cost > 0
            else 0
        )

        return {
            "product_id": product_id,
            "product_name": product.name,
            "active_bom_version": active_bom.version,
            "current_cost": active_cost,
            "previous_cost": previous_cost,
            "variance": variance,
            "variance_percent": variance_percent,
            "total_versions": len(versions),
            "versions": versions,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing costs: {str(e)}",
        )
