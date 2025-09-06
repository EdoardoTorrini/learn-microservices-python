import logging
import signal
import threading
import time

from enum import Enum

from utils.model import Order, OrderStatus
from order.service import OrderService

from conductor.client.configuration.configuration import Configuration
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.worker.worker_task import worker_task

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Worker che crea/persist l'ordine (come "persist-pending-order")
@worker_task(task_definition_name="persist-pending-order")
def persist_pending_order_worker(orderId: str = "",
                                 productIds: str = "",
                                 customerId: str = "",
                                 creditCardNumber: str = "",
                                 status: str = OrderStatus.PENDING.value): # TODO: check dato che status è un enum non lo posso passare cosi com'è a conductor
    
    entity = Order(
        productIds = productIds,
        customerId = customerId,
        creditCardNumber = creditCardNumber
    )
    if status:
        try:
            entity.status = OrderStatus(status)          # per valori "PENDING"
        except ValueError:
            # tollera anche "OrderStatus.PENDING" o un nome
            name = status.split(".")[-1]
            entity.status = OrderStatus[name]
    if orderId:
        entity.orderId = orderId
    
    OrderService().place_pending_order(entity)
    return {"result": "PASS", "reason": ""}
    

# Worker che marca REJECTED
@worker_task(task_definition_name="delete-pending-order")
def delete_pending_order_worker(orderId: str):
    
    OrderService().delete_pending_order(orderId)
    return {"result": "PASS", "reason": ""}

# Worker che marca APPROVED
@worker_task(task_definition_name="confirm-pending-order")
def confirm_pending_order_worker(orderId: str):
    OrderService().confirm_pending_order(orderId)
    return {"result": "PASS", "reason": ""}



class OrderWorkers:
    
    def __init__(self):
        
        self.config = Configuration()

        # Esecutore di workflow (per avviare i workflow)
        self.workflow_executor = WorkflowExecutor(configuration=self.config)

        # Handler che crea i processi di polling per i worker
        self.task_handler = TaskHandler(configuration=self.config)

        # Avvio del polling in un thread dedicato, così la classe "parte" subito
        self._run = True
        self._thread = threading.Thread(target=self._start_polling, daemon=True)
        self._thread.start()

        # Hook per chiusura pulita
        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def _start_polling(self):
        # start_processes() avvia i processi che fanno long-poll dei task
        self.task_handler.start_processes()
        # Mantiene vivo il thread finché non viene chiesto stop
        while self._run:
            time.sleep(0.5)

    def _graceful_shutdown(self, *args):
        self.stop()

    def stop(self):
        if self._run:
            self._run = False
            self.task_handler.stop_processes()

    # ------- Metodo pubblico per avviare un workflow -------
    def startOrderFlow(self, order: Order) -> str:
        status_val = order.status.value if isinstance(order.status, Enum) else order.status # TODO: check dato che status è un enum non lo posso passare cosi com'è a conductor
        run = self.workflow_executor.execute(
            name = "order_saga_orchestration",
            version = 1,
            workflow_input = {
                "orderId": order.orderId,
                "productIds": order.productIds,
                "customerId": order.customerId,
                "creditCardNumber": order.creditCardNumber,
                "status": status_val # TODO: check dato che status è un enum non lo posso passare cosi com'è a conductor
            }
        )

        return {"workflowId": run.workflow_id}


