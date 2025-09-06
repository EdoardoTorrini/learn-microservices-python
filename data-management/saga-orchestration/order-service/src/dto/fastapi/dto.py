from pydantic import BaseModel
from utils.model import OrderStatus

class OrderIn(BaseModel):
    orderId: str
    productIds: str
    customerId: str
    creditCardNumber: str
    status: OrderStatus = OrderStatus.PENDING

class OrderOut(BaseModel):
    orderId: str
    productIds: str
    customerId: str
    creditCardNumber: str
    status: OrderStatus
