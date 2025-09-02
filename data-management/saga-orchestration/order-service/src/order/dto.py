# order/dto.py
from enum import Enum
from pydantic import BaseModel

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class OrderDTO(BaseModel):
    order_id: str | None = None
    product_ids: str
    customer_id: str
    credit_card_number: str
    status: OrderStatus = OrderStatus.PENDING

    def __repr__(self):
        return (f"{self.order_id}: products_ids: {self.product_ids}, customer_id: {self.customer_id}, "
                f"credit_card: {self.credit_card_number}, status: {self.status}")
