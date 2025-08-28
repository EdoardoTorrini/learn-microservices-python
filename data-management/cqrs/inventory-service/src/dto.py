from sqlalchemy.orm import Session
from persistence.inventory import Product

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, order: Product) -> Product:
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def find_by_product_id(self, product_id: str) -> Product | None:
        return self.session.query(Product).filter_by(product_id=product_id).first()

    def find_all(self) -> list[Product]:
        return self.session.query(Product).all()

    def delete(self, order: Product) -> None:
        self.session.delete(order)
        self.session.commit()
