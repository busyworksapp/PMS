#!/usr/bin/env python3
"""
Database Seed Script - Populate Sample Data
Creates sample departments, products, machines, and admin user
Run AFTER init_database.py to populate the database with test data
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.department import Department
from app.models.product import Product
from app.models.machine import Machine
from app.core.security import hash_password

# Import all models to ensure they're registered
import app.models  # noqa: F401


def seed_data():
    """Populate database with sample data."""
    print("\n" + "="*60)
    print("  BARRON PRODUCTION MANAGEMENT SYSTEM")
    print("  Database Seed Script - Sample Data")
    print("="*60 + "\n")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Ensure tables exist
        Base.metadata.create_all(bind=engine)
        print("[OK] Tables verified\n")
        
        # Check if admin already exists
        admin = db.query(User).filter(
            User.username == "admin"
        ).first()
        
        if admin:
            print("[SKIP] Admin user already exists\n")
        else:
            # Create Admin User
            print("[CREATE] Creating admin user...")
            admin_user = User(
                username="admin",
                email="admin@barron.com",
                full_name="System Administrator",
                employee_number="ADM001",
                role="admin",
                hashed_password=hash_password("admin123"),
                is_active=True,
                created_at=datetime.utcnow(),
            )
            db.add(admin_user)
            db.flush()
            print("   [OK] Admin user created (admin/admin123)\n")
        
        # Create Departments
        print("[CREATE] Creating departments...")
        departments_data = [
            {
                "name": "Production",
                "description": "Main production department",
            },
            {
                "name": "Quality Assurance",
                "description": "Quality control and testing",
            },
            {
                "name": "Maintenance",
                "description": "Equipment maintenance and repair",
            },
        ]
        
        departments = []
        for dept_data in departments_data:
            existing = db.query(Department).filter(
                Department.name == dept_data["name"]
            ).first()
            
            if not existing:
                dept = Department(**dept_data, created_at=datetime.utcnow())
                db.add(dept)
                db.flush()
                departments.append(dept)
                print(f"   [OK] {dept_data['name']}")
            else:
                departments.append(existing)
                print(f"   [SKIP] {dept_data['name']} (exists)")
        
        print()
        
        # Create Products
        print("[CREATE] Creating products...")
        products_data = [
            {
                "code": "PROD001",
                "name": "Industrial Widget A",
                "description": "Premium industrial widget",
            },
            {
                "code": "PROD002",
                "name": "Industrial Widget B",
                "description": "Standard industrial widget",
            },
            {
                "code": "PROD003",
                "name": "Assembly Kit C",
                "description": "Complete assembly kit",
            },
        ]
        
        products = []
        for prod_data in products_data:
            existing = db.query(Product).filter(
                Product.code == prod_data["code"]
            ).first()
            
            if not existing:
                prod = Product(**prod_data, created_at=datetime.utcnow())
                db.add(prod)
                db.flush()
                products.append(prod)
                print(f"   [OK] {prod_data['code']} - {prod_data['name']}")
            else:
                products.append(existing)
                print(f"   [SKIP] {prod_data['code']} (exists)")
        
        print()
        
        # Create Machines
        print("[CREATE] Creating machines...")
        machines_data = [
            {
                "name": "CNC Lathe #1",
                "machine_number": "MACH001",
                "status": "operational",
                "department_id": departments[0].id if departments else None,
            },
            {
                "name": "Press Machine #2",
                "machine_number": "MACH002",
                "status": "operational",
                "department_id": departments[0].id if departments else None,
            },
            {
                "name": "Assembly Station #1",
                "machine_number": "MACH003",
                "status": "operational",
                "department_id": departments[0].id if departments else None,
            },
        ]
        
        for mach_data in machines_data:
            existing = db.query(Machine).filter(
                Machine.machine_number == mach_data["machine_number"]
            ).first()
            
            if not existing:
                mach = Machine(**mach_data, created_at=datetime.utcnow())
                db.add(mach)
                db.flush()
                nm = mach_data["machine_number"]
                print(f"   [OK] {nm} - {mach_data['name']}")
            else:
                nm = mach_data["machine_number"]
                print(f"   [SKIP] {nm} (exists)")
        
        print()
        
        # Commit all changes
        db.commit()
        
        # Summary
        print("="*60)
        print("[OK] DATABASE SEEDING COMPLETE!")
        print("="*60)
        print("\n[INFO] Data Summary:")
        print(f"   Departments: {db.query(Department).count()}")
        print(f"   Products: {db.query(Product).count()}")
        print(f"   Machines: {db.query(Machine).count()}")
        print(f"   Users: {db.query(User).count()}")
        
        print("\n[NEXT] Next steps:")
        print("   1. Start backend: python -m uvicorn app.main:app")
        print("   2. Go to: http://localhost:3000/templates/login.html")
        print("   3. Login with: admin / admin123")
        print("   4. View dashboard and test workflows!")
        print("\n")
        
    except Exception as e:
        db.rollback()
        print("\n[ERROR] Seeding failed!")
        print(f"Error: {str(e)}\n")
        
        print("Troubleshooting:")
        print("   * Run init_database.py first to create tables")
        print("   * Check if models are properly defined")
        print("   * Verify .env file configuration")
        print("\n")
        
        sys.exit(1)
    
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
