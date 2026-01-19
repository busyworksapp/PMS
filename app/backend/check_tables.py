#!/usr/bin/env python3
"""Check database tables and verify initialization."""

import sys
from pathlib import Path
from sqlalchemy import inspect

sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import Base, engine

# Import all models to register them
import app.models  # noqa: F401

# Get all model tables
print("\n" + "="*60)
print("Database Tables Report")
print("="*60 + "\n")

# Get tables from SQLAlchemy metadata (models)
print("📋 Tables Defined in Models:")
model_tables = Base.metadata.tables.keys()
print(f"Count: {len(model_tables)}\n")
for table in sorted(model_tables):
    print(f"  ✓ {table}")

# Get tables from database
print("\n📊 Tables in Railway Database:")
inspector = inspect(engine)
db_tables = inspector.get_table_names()
print(f"Count: {len(db_tables)}\n")
for table in sorted(db_tables):
    print(f"  ✓ {table}")

if len(db_tables) == 0:
    print("\n⚠️  No tables found in database!")
    print("Run: python init_database.py")
else:
    print(f"\n✅ Database has {len(db_tables)} tables")

print()
