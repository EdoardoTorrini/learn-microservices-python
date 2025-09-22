import logging
from contextlib import contextmanager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from inventory.model import Inventory
from dto.dto import OrderDTO
from utils.config import get_db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class InventoryService:

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

    def inventoryCheck(self, order: OrderDTO) -> bool:
        logger.info("Verifying inventory %s...", getattr(order, "productIds", None))
        productIds = order.productIds.split(",") if order.productIds else []

        if not productIds:
            logger.info("No productIds provided")
            return False

        with self._session() as db:
            inventories: dict[str, Inventory] = {}

            # 1. Verifica preliminare
            for pid in productIds:
                inventory: Inventory = (
                    db.query(Inventory)
                    .filter(Inventory.productId == pid)
                    .first()
                )
                if not inventory or inventory.quantity <= 0:
                    logger.info("Inventory check failed for productId %s", pid)
                    logger.info(f"Quantity: {inventory.quantity}" if inventory else "Inventory not found")
                    return False
                inventories[pid] = inventory  # salvo per il secondo step

            # 2. Tutto ok → aggiornamento
            for pid, inventory in inventories.items():
                inventory.quantity -= 1
                db.add(inventory)
                db.flush()
                db.refresh(inventory)
                logger.info(
                    "Inventory updated for productId %s, remaining quantity %d",
                    pid,
                    inventory.quantity,
                )

            return True
