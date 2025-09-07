import logging
from contextlib import contextmanager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from payment.model import Payment
from dto.dto import OrderDTO
from utils.config import get_db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PaymentService:

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

    def paymentCheck(self, order: OrderDTO) -> bool:
        logger.info("Verifying payment %s...", getattr(order, "orderId", None))
        payment = Payment(
            orderId=order.orderId,
            creditCardNumber=order.creditCardNumber
        )
        if self.validateCard(order.creditCardNumber):
            payment.success = True
            logger.info("Verified payment (valid)")

        with self._session() as db:
            existing = (
                db.query(Payment)
                .filter(Payment.orderId == payment.orderId)  # campo coerente
                .first()
            )
            if not existing:
                db.add(payment)
                db.flush()
                db.refresh(payment)

    def validateCard(creditCardNumber: str) -> bool:
        return creditCardNumber.startswith("7777")