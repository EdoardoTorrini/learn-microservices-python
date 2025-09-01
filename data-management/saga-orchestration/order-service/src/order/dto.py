from enum import Enum
from pydantic import BaseModel, Field


class OrderStatus(Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2


class OrderDTO(BaseModel):

    order_id: str
    product_ids: str
    customer_id: str
    credit_card_number: str
    status: OrderStatus

    def __repr__(self):
        return f'''
        {self.order_id}: products_ids: {self.product_ids}, customer_id:{self.customer_id}, 
        credit_card: {self.credit_card_number}, status: {self.status.value}
        '''
