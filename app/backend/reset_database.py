#!/usr/bin/env python3
"""
Database Reset Script
CAUTION: This will DROP ALL TABLES and delete all data!
Only use this to completely reset the database during development
"""

import sys
from pathlib import Path
from app.db.database import Base, engine

sys.path.insert(0, str(Path(__file__).parent))


def reset_db():
    """Drop all tables and recreate them."""
    print("\n" + "="*60)
    print("  BARRON PRODUCTION MANAGEMENT SYSTEM")
    print("  Database Reset Script")
    print("="*60 + "\n")
    
    print("⚠️  WARNING: This will DELETE ALL DATA!")
    print("\nType 'CONFIRM' to proceed with database reset: ", end="")
    
    response = input().strip().upper()
    
    if response != "CONFIRM":
        print("\n❌ Reset cancelled. No changes made.\n")
        return
    
    try:
        print("\n🔄 Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped!\n")
        
        print("🔄 Creating fresh tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Fresh tables created!\n")
        
        print("="*60)
        print("✅ DATABASE RESET COMPLETE!")
        print("="*60)
        print("\n📝 Next steps:")
        print("   1. Run: python seed_data.py (to populate test data)")
        print("   2. Start backend: python -m uvicorn app.main:app")
        print("   3. Go to: http://localhost:3000/templates/login.html")
        print("   4. Login with: admin / admin123")
        print("\n")
        
    except Exception as e:
        print("\n❌ ERROR: Database reset failed!")
        print(f"Error: {str(e)}\n")
        
        print("Troubleshooting:")
        print("   • Check if Railway MySQL is accessible")
        print("   • Verify .env file configuration")
        print("   • Check internet connection")
        print("\n")
        
        sys.exit(1)


if __name__ == "__main__":
    reset_db()
