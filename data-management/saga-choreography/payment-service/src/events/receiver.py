# receiver.py
import os
import logging
import pika
from events.event import Event
from events.sender import EventSender
from payment.service import PaymentService
from dto.dto import OrderDTO

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EventReceiver:
    def __init__(self):
        self.paymentService = PaymentService()
        self.eventSender = EventSender()

        url = os.getenv("RABBITMQ_URL", "amqp://admin:admin@rabbitmq_cqrs:5672/")
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="app.events", exchange_type="topic", durable=True)

        # Coda server-named ed esclusiva (NON durable)
        result = self.channel.queue_declare(queue="", exclusive=True, auto_delete=True)
        self.queue_name = result.method.queue

        # Ascolta SOLO gli eventi che ti interessano
        self.channel.queue_bind(exchange="app.events", queue=self.queue_name, routing_key="order.created")

        # Consuma un messaggio per volta
        self.channel.basic_qos(prefetch_count=1)

        self._consuming = False

    def start_consuming(self):
        self._consuming = True

        def _on_message(ch, method, properties, body):
            try:
                event = Event.from_json(body.decode())
                logger.info(f"Received event: key=%s", getattr(event, "key", None))

                if event.key == "order.created":
                    # Converte il payload in OrderDTO se serve
                    data = event.data
                    if isinstance(data, dict):
                        order_dto = OrderDTO(**data)
                    else:
                        order_dto = data  # già un OrderDTO

                    self.manageOrderCreated(order_dto)

                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                logger.error("Error while processing message: %s", e, exc_info=True)

        logger.info("Waiting for events on queue '%s' (binding: order.created)...", self.queue_name)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=_on_message)

        self.channel.start_consuming()

    # --- Handlers ---
    def manageOrderCreated(self, orderDTO: OrderDTO):
        if self.paymentService.paymentCheck(orderDTO):
            self.eventSender.send("payment.valid", Event(key="payment.valid", data=orderDTO))
        else:
            self.eventSender.send("payment.invalid", Event(key="payment.invalid", data=orderDTO))
