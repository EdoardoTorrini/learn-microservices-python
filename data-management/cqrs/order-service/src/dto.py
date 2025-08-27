from sqlalchemy.orm import Session
from persistence.order import Order

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, order: Order) -> Order:
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def find_by_order_id(self, order_id: str) -> Order | None:
        return self.session.query(Order).filter_by(order_id=order_id).first()

    def find_all(self) -> list[Order]:
        return self.session.query(Order).all()

    def delete(self, order: Order) -> None:
        self.session.delete(order)
        self.session.commit()
