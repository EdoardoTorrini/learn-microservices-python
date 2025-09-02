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
    order_id = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    product_ids = Column(String(length=1024), nullable=True)
    customer_id = Column(String(length=255), nullable=True)     # <-- fix qui
    credit_card_number = Column(String(length=64), nullable=True)
    status = Column(SqlEnum(OrderStatus, name="order_status"), nullable=False, default=OrderStatus.PENDING)

    def __init__(self, product_ids: str, customer_id: str, credit_card_number: str):
        self.product_ids = product_ids
        self.customer_id = customer_id
        self.credit_card_number = credit_card_number

    def __repr__(self):
        return f"<Order {self.order_id} status={self.status}>"
