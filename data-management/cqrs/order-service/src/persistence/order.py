from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.orm import declarative_base
import enum
import uuid

Base = declarative_base()


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    product_ids = Column(String)
    customer_id = Column(String)
    credit_card_number = Column(String)
    status = Column(SAEnum(OrderStatus), default=OrderStatus.PENDING)

    def __repr__(self):
        return (f"<Order(id={self.id}, order_id={self.order_id}, "
                f"product_ids={self.product_ids}, customer_id={self.customer_id}, "
                f"status={self.status.value})>")
