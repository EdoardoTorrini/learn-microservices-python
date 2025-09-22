from sqlalchemy.orm import Session
from persistence.order_confirmed import OrderConfirmed

class OrderConfirmedRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, order: OrderConfirmed) -> OrderConfirmed:
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def find_by_customer_month_year(self, customer_id: str, month: int, year: int) -> OrderConfirmed | None:
        return self.session.query(OrderConfirmed).filter_by(customer_id=customer_id, month=month, year=year).first()

    def find_all(self) -> list[OrderConfirmed]:
        return self.session.query(OrderConfirmed).all()

    def delete(self, order: OrderConfirmed) -> None:
        self.session.delete(order)
        self.session.commit()
