from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class DynamicForm(Base):
    __tablename__ = "dynamic_forms"
    
    id = Column(Integer, primary_key=True, index=True)
    form_key = Column(String(100), unique=True, nullable=False)
    form_name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    form_config = Column(JSON, nullable=False)  # Stores fields, validation, layout
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FormField(Base):
    __tablename__ = "form_fields"
    
    id = Column(Integer, primary_key=True, index=True)
    form_key = Column(String(100), nullable=False)
    field_name = Column(String(255), nullable=False)
    field_type = Column(String(50), nullable=False)  # text, dropdown, date, number, etc.
    is_required = Column(Integer, default=0)
    validation_rules = Column(JSON, nullable=True)
    conditional_rules = Column(JSON, nullable=True)
    field_config = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
