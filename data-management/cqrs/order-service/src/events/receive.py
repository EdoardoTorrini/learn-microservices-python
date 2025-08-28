import os
import pika
from events.event import Event
from dto import OrderRepository
from order_service import OrderService

class EventReceiver:
    def __init__(self ,order_service: OrderService):
        url = os.getenv("RABBITMQ_URL", "amqp://admin:admin@rabbitmq_cqrs:5672/")
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()

        self.order_service = order_service

    def start(self, queue_name = "payment-order-queue"):
        self.channel.queue_declare(queue=queue_name, durable=True)

        def callback(ch, method, properties, body):
            event = Event.from_json(body.decode())

            if event.key == "payment.invalid":
                self.order_service.handle_payment_invalid(event.data)
            elif event.key == "inventory.invalid":
                self.order_service.handle_inventory_invalid(event.data)
            elif event.key == "inventory.valid":
                self.order_service.handle_inventory_valid(event.data)

        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()