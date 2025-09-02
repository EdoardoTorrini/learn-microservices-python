# order/service.py
import logging
from sqlalchemy.orm import Session
from utils.model import Order, OrderStatus

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def place_pending_order(self, order: Order):
        logger.info("persisting %s...", order.order_id)
        existing = (
            self.db.query(Order)
            .filter(Order.order_id == order.order_id)
            .first()
        )
        if not existing:
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)

    def delete_pending_order(self, order_id: str):
        logger.info("rejecting %s...", order_id)
        existing = (
            self.db.query(Order)
            .filter(Order.order_id == order_id)
            .first()
        )
        if existing:
            existing.status = OrderStatus.REJECTED
            self.db.commit()
            self.db.refresh(existing)

    def confirm_pending_order(self, order_id: str):
        logger.info("confirming %s...", order_id)
        existing = (
            self.db.query(Order)
            .filter(Order.order_id == order_id)
            .first()
        )
        if existing:
            existing.status = OrderStatus.APPROVED
            self.db.commit()
            self.db.refresh(existing)
