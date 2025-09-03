# order/dto.py
from enum import Enum
from pydantic import BaseModel

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class OrderDTO(BaseModel):
    orderId: str | None = None
    productIds: str
    customerId: str
    creditCardNumber: str
    status: OrderStatus = OrderStatus.PENDING

    def __repr__(self):
        return (f"{self.orderId}: productsIds: {self.productIds}, customerId: {self.customerId}, "
                f"creditCardNumber: {self.creditCardNumber}, status: {self.status}")
