import logging
import signal
import threading
import time

from payment.service import PaymentService
from dto.dto import OrderDTO

from conductor.client.configuration.configuration import Configuration
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.worker.worker_task import worker_task

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@worker_task(task_definition_name="payment-check")
def paymentCheck(orderId: str = "",
                                 productIds: str = "",
                                 customerId: str = "",
                                 creditCardNumber: str = "",
                                 status: str = ""): 
    
    entity = OrderDTO(
        productIds = productIds,
        customerId = customerId,
        creditCardNumber = creditCardNumber
    )
    entity.orderId = orderId
    entity.status = status # TODO: status deve essere definito meglio

    

    if PaymentService().paymentCheck(entity):
        return {"result": "PASS", "reason": ""}
    else:
        return {"result": "FAIL", "reason": ""}



class PaymentWorkers:
    
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