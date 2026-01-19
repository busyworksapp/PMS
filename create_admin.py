#!/usr/bin/env python3
"""
Create Admin User Script
Usage: python create_admin.py --username admin --email admin@example.com --password secretpass
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.backend.app.db.database import SessionLocal, Base, engine
from app.backend.app.models.user import User
from app.backend.app.core.security import hash_password


def create_admin(username: str, email: str, password: str, full_name: str = None):
    """Create an admin user."""
    db = SessionLocal()
    
    try:
        # Ensure tables exist
        Base.metadata.create_all(bind=engine)
        print("[OK] Database tables verified\n")
        
        # Check if user already exists
        existing = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing:
            print(f"[ERROR] User already exists: {existing.username} ({existing.email})")
            return False
        
        # Create admin user
        admin_user = User(
            username=username,
            email=email,
            full_name=full_name or "System Administrator",
            hashed_password=hash_password(password),
            role="admin",
            is_active=True,
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"[SUCCESS] Admin user created!")
        print(f"  Username: {username}")
        print(f"  Email: {email}")
        print(f"  Role: admin")
        print(f"  ID: {admin_user.id}\n")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to create admin user: {e}")
        db.rollback()
        return False
    
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create an admin user in the database"
    )
    parser.add_argument(
        "--username",
        required=True,
        help="Admin username"
    )
    parser.add_argument(
        "--email",
        required=True,
        help="Admin email"
    )
    parser.add_argument(
        "--password",
        required=True,
        help="Admin password"
    )
    parser.add_argument(
        "--full-name",
        default="System Administrator",
        help="Full name (default: System Administrator)"
    )
    
    args = parser.parse_args()
    
    success = create_admin(
        username=args.username,
        email=args.email,
        password=args.password,
        full_name=args.full_name,
    )
    
    sys.exit(0 if success else 1)
