from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrderBase(BaseModel):
    order_number: str
    customer_name: str
    order_value: float
    start_date: datetime
    end_date: datetime
    department_id: int
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrderScheduleBase(BaseModel):
    order_id: int
    department_id: int
    scheduled_date: datetime
    assigned_machine_id: Optional[int] = None
    assigned_operator_id: Optional[int] = None


class OrderScheduleResponse(OrderScheduleBase):
    id: int
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
