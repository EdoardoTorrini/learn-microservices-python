# order/workers.py
import logging
from typing import Optional

from sqlalchemy.orm import Session
from utils.config import get_db
from utils.model import Order, OrderStatus
from order.service import OrderService

# <-- decoratore ufficiale per i worker
from conductor.client.worker.worker_task import worker_task
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes_clients import OrkesClients
from conductor.client.http.models import StartWorkflowRequest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def start_order_flow(order_dto) -> dict:
    cfg = Configuration() # per la connessione con conductor (carice le variabili d'ambiente che gli servono)
                            # cfg è la configurazione con cui il client parlerà al Conductor
    clients = OrkesClients(configuration=cfg) # client è un oggetto per estrarre i vari client pèer parlare a conductor

    wf = clients.get_workflow_client() # wf è l’oggetto che ti permette di avviare il workflow definito in workflow.json.

    req = StartWorkflowRequest() # rappresenta la richiesta che sarà serializzata in JSON e inviata a Conductor.
    req.name = "order_saga_orchestration"
    req.input = {
        "orderId": order_dto.orderId,
        "productIds": order_dto.productIds,
        "customerId": order_dto.customerId,
        "creditCardNumber": order_dto.creditCardNumber,
        "status": order_dto.status,
    }
    workflow_id = wf.start_workflow(req) # Serializza req in JSON, Esegue una POST verso l’endpoint del Conductor
    return {"workflowId": workflow_id}

# Worker che crea/persist l'ordine (come "persist-pending-order")
@worker_task(task_definition_name="persist-pending-order")
def persist_pending_order_worker(orderId: str = "",
                                 productIds: str = "",
                                 customerId: str = "",
                                 creditCardNumber: str = "",
                                 status: str = OrderStatus.PENDING):
    # print(f"orderId: {orderId}, productIds: {productIds}, customerId: {customerId}, creditCardNumber: {creditCardNumber}, status: {status}",flush=True)
    db: Session = next(get_db())
    try:
        svc = OrderService(db)
        entity = Order(
            productIds = productIds,
            customerId = customerId,
            creditCardNumber = creditCardNumber,
        )
        if orderId:
            entity.orderId = orderId
        # print(f"entity.orderId: {entity.orderId}, entity.productIds: {entity.productIds}, entity.customerId: {entity.customerId}, entity.creditCardNumber: {entity.creditCardNumber}, entity.status: {entity.status}",flush=True)
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
