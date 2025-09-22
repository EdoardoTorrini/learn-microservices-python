from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Product(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, unique=True, nullable=False)
    quantity = Column(Integer)

    def __repr__(self):
        return (f"<Order(id={self.id}, product_id={self.product_id}, "
                f"quantity={self.quantity})>")
