from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class OrderConfirmed(Base):
    __tablename__ = "orders_read"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String)
    month = Column(Integer)
    year =Column(Integer)
    n = Column(Integer, default=0, nullable=False)

    __table_args__ = (
        UniqueConstraint("customer_id", "month", "year", name="uq_customer_month_year"),
    )

    def __repr__(self):
        return (f"<Order(id={self.id}, customer_id={self.customer_id}, month={self.month}), year={self.year}, n={self.n})>")
