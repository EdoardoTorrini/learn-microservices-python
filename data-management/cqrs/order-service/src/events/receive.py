import os
import pika
from events.event import Event

class EventReceiver:
    def __init__(self ,order_service, event_sender):
        url = os.getenv("RABBITMQ_URL", "amqp://admin:admin@localhost:5672/")
        self.connection = pika.BlockingConnection(pika.URLParameters(url)   )
        self.channel = self.connection.channel()

        self.order_service = order_service
        self.event_sender = event_sender

        def start(self, queue_name = "payment-order-service"):
            self.channel.queue_declare(queue=queue_name, durable=True)

            def callback(ch, method, properties, body):
                event = Event.from_json(body.decode())

                if event.key == "payment.invalid":
                    self.manage_payment_invalid(event.data)
                elif event.key == "inventory.invalid":
                    self.manage_inventory_invalid(event.data)
                elif event.key == "inventory.valid":
                    self.manage_inventory_valid(event.data)

            self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()