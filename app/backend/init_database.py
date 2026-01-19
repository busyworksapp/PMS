#!/usr/bin/env python3
"""
Database Initialization Script
Creates all tables in Railway MySQL database
Run this ONCE after deploying to initialize the database structure
"""

import sys
from pathlib import Path
from sqlalchemy import text
from app.db.database import Base, engine
from app.core.config import settings

# IMPORTANT: Import all models to register them with Base
import app.models  # noqa: F401

# Add the app directory to path
sys.path.insert(0, str(Path(__file__).parent))


def init_db():
    """Initialize the database with all tables."""
    print("\n" + "="*60)
    print("  BARRON PRODUCTION MANAGEMENT SYSTEM")
    print("  Database Initialization Script")
    print("="*60 + "\n")
    
    try:
        print(f"📊 Database: {settings.DATABASE_URL.split('@')[1]}")
        print("🔑 Connection: Checking...")
        
        # Test connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Connection successful!\n")
        
        # Create all tables
        print("📋 Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!\n")
        
        # List created tables
        inspector_tables = Base.metadata.tables.keys()
        print(f"📊 Created {len(inspector_tables)} tables:\n")
        for i, table in enumerate(inspector_tables, 1):
            print(f"   {i:2d}. {table}")
        
        print("\n" + "="*60)
        print("✅ DATABASE INITIALIZATION COMPLETE!")
        print("="*60)
        print("\n📝 Next steps:")
        print("   1. Start backend: python -m uvicorn app.main:app")
        print("   2. Open: http://127.0.0.1:8001/docs")
        print("   3. Create admin user via POST /api/auth/register")
        print("   4. Login and start using the system!")
        print("\n")
        
    except Exception as e:
        print("\n❌ ERROR: Database initialization failed!")
        print(f"Error: {str(e)}\n")
        
        print("Troubleshooting:")
        print("   • Check if .env file exists in app/backend/")
        print("   • Verify DATABASE_URL in .env is correct")
        print("   • Ensure Railway MySQL service is running")
        print("   • Check internet connection to Railway")
        print("\n")
        
        sys.exit(1)


if __name__ == "__main__":
    init_db()
