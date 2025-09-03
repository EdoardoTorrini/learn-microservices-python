# utils/model.py
from sqlalchemy import Column, Integer, String, Enum as SqlEnum
import uuid
from enum import Enum
from utils.config import Config

class OrderStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Order(Config.base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    orderId = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    productIds = Column(String(length=1024), nullable=True)
    customerId = Column(String(length=255), nullable=True)     # <-- fix qui
    creditCardNumber = Column(String(length=64), nullable=True)
    status = Column(SqlEnum(OrderStatus, name="order_status"), nullable=False, default=OrderStatus.PENDING)

    def __init__(self, productIds: str, customerId: str, creditCardNumber: str):
        self.productIds = productIds
        self.customerId = customerId
        self.creditCardNumber = creditCardNumber

    def __repr__(self):
        return f"<Order {self.order_id} status={self.status}>"
