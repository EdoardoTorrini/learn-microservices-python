# receiver.py
import os
import logging
import pika
import json
from events.event import Event
from events.sender import EventSender
from inventory.service import InventoryService
from dto.dto import OrderDTO

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EventReceiver:
    def __init__(self):
        self.paymentService = InventoryService()
        self.eventSender = EventSender()

        url = os.getenv("RABBITMQ_URL", "amqp://admin:admin@rabbitmq_cqrs:5672/")
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="app.events", exchange_type="topic", durable=True)

        # Coda server-named ed esclusiva (NON durable)
        result = self.channel.queue_declare(queue="", exclusive=True, auto_delete=True)
        self.queue_name = result.method.queue

        # Ascolta SOLO gli eventi che ti interessano
        self.channel.queue_bind(exchange="app.events", queue=self.queue_name, routing_key="payment.valid")

        # Consuma un messaggio per volta
        self.channel.basic_qos(prefetch_count=1)

    def start_consuming(self):
        self._consuming = True

        def _on_message(ch, method, properties, body):
            try:
                event = Event.from_json(body.decode())
                logger.info(f"Received event: key=%s", getattr(event, "key", None))
                
                if event.key == "payment.valid":
                    
                    raw = event.data
                    payload = raw if isinstance(raw, dict) else json.loads(raw)
                    order_dto = OrderDTO(**payload)
                    
                    self.manageInventory(order_dto)

                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                logger.error("Error while processing message: %s", e, exc_info=True)

        logger.info("Waiting for events on queue '%s' (binding: payment.valid)...", self.queue_name)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=_on_message)

        self.channel.start_consuming()

    # --- Handlers ---
    def manageInventory(self, orderDTO: OrderDTO):
        if self.paymentService.inventoryCheck(orderDTO):
            self.eventSender.send("inventory.valid", Event(key="inventory.valid", data=orderDTO.model_dump()))
        else:
            self.eventSender.send("inventory.invalid", Event(key="inventory.invalid", data=orderDTO.model_dump()))
