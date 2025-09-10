import logging
from contextlib import contextmanager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from order.model import Order, OrderStatus
from utils.config import get_db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class OrderService:

    def __init__(self, session_factory: Callable[[], Iterator[Session]] = get_db):
        self._session_factory = session_factory

    @contextmanager
    def _session(self) -> Iterator[Session]:
        db: Session = next(self._session_factory())
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def place_pending_order(self, order: Order):
        logger.info("persisting %s...", getattr(order, "orderId", None))
        with self._session() as db:
            existing = (
                db.query(Order)
                .filter(Order.orderId == order.orderId)
                .first()
            )
            if not existing:
                db.add(order)
                db.flush()
                db.refresh(order)

    def delete_pending_order(self, orderId: str):
        logger.info("rejecting %s...", orderId)
        with self._session() as db:
            existing = (
                db.query(Order)
                .filter(Order.orderId == orderId)  
                .first()
            )
            if existing:
                existing.status = OrderStatus.REJECTED
                db.flush()
                db.refresh(existing)

    def confirm_pending_order(self, orderId: str):
        logger.info("confirming %s...", orderId)
        with self._session() as db:
            existing = (
                db.query(Order)
                .filter(Order.orderId == orderId)
                .first()
            )
            if existing:
                existing.status = OrderStatus.APPROVED
                db.flush()
                db.refresh(existing)
