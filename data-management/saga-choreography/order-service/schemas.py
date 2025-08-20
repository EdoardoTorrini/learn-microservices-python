from pydantic import BaseModel
from enum import Enum
from typing import List

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class OrderItem(BaseModel):
    sku: str
    qty: int

class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItem]
    total_amount: float

class OrderRead(BaseModel):
    id: str
    status: OrderStatus
    customer_id: str
    items: List[OrderItem]
    total_amount: float
