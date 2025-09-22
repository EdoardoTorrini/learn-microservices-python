import os
import pika
from events.event import Event
from events.sender import EventSender
from service.card_validator_service import CardValidatorService

class EventReceiver:
    def __init__(self ,card_validator_service: CardValidatorService, event_sender: EventSender):
        url = os.getenv("RABBITMQ_URL", "amqp://admin:admin@rabbitmq_cqrs:5672/")
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="payment-inventory-queue", durable=True)
        self.channel.queue_declare(queue="payment-order-queue", durable=True)
        self.channel.queue_declare(queue="order-payment-queue", durable=True)

        self.card_validator_service = card_validator_service
        self.event_sender = event_sender

    def start(self, queue_name = "order-payment-queue"):
        self.channel.queue_declare(queue=queue_name, durable=True)

        def callback(ch, method, properties, body):
            event = Event.from_json(body.decode())

            if event.key == "order.created":
                self.manage_order_created(event.data)

        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
    
    def manage_order_created(self, order):
        if self.card_validator_service.payment_check(order):
            print(f"Payment valid for order {order['orderId']}", flush=True)
            self.event_sender.send(exchange="", 
                                    routing_key="payment-inventory-queue",
                                    event=Event(key="payment.valid", data=order))
        else:
            print(f"Payment invalid for order {order['orderId']}", flush=True)
            self.event_sender.send(exchange="", 
                                    routing_key="payment-order-queue",
                                    event=Event(key="payment.invalid", data=order))