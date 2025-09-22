import uuid
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from utils.config import Config

class OrderStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Order(Config.base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    orderId = Column(
        String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    productIds = Column(String(1024))
    customerId = Column(String(255))
    creditCardNumber = Column(String(64))

    status = Column(
        SqlEnum(OrderStatus, name="order_status"),
        nullable=False,
        default=OrderStatus.PENDING
    )

    def __init__(self, productIds: str, customerId: str, creditCardNumber: str):
        self.productIds = productIds
        self.customerId = customerId
        self.creditCardNumber = creditCardNumber