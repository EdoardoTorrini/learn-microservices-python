import pika
import os
import logging
import json

from events.event import Event
from dto.dto import OrderDTO
from order.service import OrderService
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EventReceiver:
    def __init__(self):

        self.order_service = OrderService()

        url = os.getenv("RABBITMQ_URL", "amqp://admin:admin@rabbitmq_cqrs:5672/")
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="app.events", exchange_type="topic", durable="True")

        # Creiamo una coda dedicata al servizio
        result = self.channel.queue_declare(queue="", auto_delete="True", exclusive=True)
        self.queue_name = result.method.queue

        # Bind alla coda → ascolta tutti gli eventi
        self.channel.queue_bind(exchange="app.events", queue=self.queue_name, routing_key="#")

        self.channel.basic_qos(prefetch_count=1)

        
    def start_consuming(self):
        def _on_message(ch, method, properties, body):
            try:
                event = Event.from_json(body.decode())
                logger.info(f"Received event {event}")

                raw = event.data
                payload = raw if isinstance(raw, dict) else json.loads(raw)
                order_dto = OrderDTO(**payload)

                match event.key:
                    case "payment.invalid":
                        self.managePaymentInvalid(order_dto)
                    case "inventory.invalid":
                        self.manageInventoryInvalid(order_dto)
                    case "inventory.valid":
                        self.manageInventoryValid(order_dto)

                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                logger.error(f"Error while processing message: {e}", exc_info=True)
                # non ack → il messaggio rimane in coda

        logger.info(f"Waiting for events on queue '{self.queue_name}'...")
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=_on_message)
        self.channel.start_consuming()

    # --- Handlers ---
    def managePaymentInvalid(self, order: OrderDTO):
        self.order_service.delete_pending_order(order.orderId)

    def manageInventoryInvalid(self, order: OrderDTO):
        self.order_service.delete_pending_order(order.orderId)

    def manageInventoryValid(self, order: OrderDTO):
        self.order_service.confirm_pending_order(order.orderId)
