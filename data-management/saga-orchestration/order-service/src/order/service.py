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
        logger.info("persisting %s...", order.orderId)
        # print(f"service.py: orderId: {order.orderId}, productIds: {order.productIds}, customerId: {order.customerId}, creditCardNumber: {order.creditCardNumber}, status: {order.status}",flush=True)
        existing = (
            self.db.query(Order)
            .filter(Order.orderId == order.orderId)
            .first()
        )
        if not existing:
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)

    def delete_pending_order(self, orderId: str):
        logger.info("rejecting %s...", orderId)
        existing = (
            self.db.query(Order)
            .filter(Order.order_id == orderId)
            .first()
        )
        if existing:
            existing.status = OrderStatus.REJECTED
            self.db.commit()
            self.db.refresh(existing)

    def confirm_pending_order(self, orderId: str):
        logger.info("confirming %s...", orderId)
        existing = (
            self.db.query(Order)
            .filter(Order.order_id == orderId)
            .first()
        )
        if existing:
            existing.status = OrderStatus.APPROVED
            self.db.commit()
            self.db.refresh(existing)
