from pydantic import BaseModel

class OrderDTO(BaseModel):
    orderId: str
    productIds: str
    customerId: str
    creditCardNumber: str
    status: str = "PENDING"

    
