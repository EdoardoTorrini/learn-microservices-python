# order/workers.py
import logging
from typing import Optional

from sqlalchemy.orm import Session
from utils.config import get_db
from utils.model import Order
from order.service import OrderService

# <-- decoratore ufficiale per i worker
from conductor.client.worker.worker_task import worker_task

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Worker che crea/persist l'ordine (come "persist-pending-order")
@worker_task(task_definition_name="persist-pending-order")
def persist_pending_order_worker(orderId: Optional[str] = None,
                                 productIds: Optional[str] = None,
                                 customerId: Optional[str] = None,
                                 creditCardNumber: Optional[str] = None,
                                 status: Optional[str] = None):
    db: Session = next(get_db())
    try:
        svc = OrderService(db)
        entity = Order(
            product_ids=productIds,
            customer_id=customerId,
            credit_card_number=creditCardNumber,
        )
        if orderId:
            entity.order_id = orderId
        svc.place_pending_order(entity)
        return {"result": "PASS"}
    finally:
        db.close()

# Worker che marca REJECTED
@worker_task(task_definition_name="delete-pending-order")
def delete_pending_order_worker(orderId: str):
    db: Session = next(get_db())
    try:
        OrderService(db).delete_pending_order(orderId)
        return {"result": "PASS"}
    finally:
        db.close()

# Worker che marca APPROVED
@worker_task(task_definition_name="confirm-pending-order")
def confirm_pending_order_worker(orderId: str):
    db: Session = next(get_db())
    try:
        OrderService(db).confirm_pending_order(orderId)
        return {"result": "PASS"}
    finally:
        db.close()
