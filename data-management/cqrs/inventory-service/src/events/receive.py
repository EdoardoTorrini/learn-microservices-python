import os
import pika
from events.event import Event
from events.sender import EventSender
from service.check_inventory import InventoryCheck

class EventReceiver:
    def __init__(self, event_sender: EventSender, inventory_check: InventoryCheck):
        url = os.getenv("RABBITMQ_URL", "amqp://admin:admin@rabbitmq_cqrs:5672/")
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue="payment-order-queue", durable=True)

        self.event_sender = event_sender
        self.inventory_check = inventory_check
    
    def start(self, queue_name = "payment-inventory-queue"):
        self.channel.queue_declare(queue=queue_name, durable=True)

        def callback(ch, method, properties, body):
            event = Event.from_json(body.decode())

            if event.key == "payment.valid":
                self.manage_order(event.data)
            
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
        
    def manage_order(self, order):
        if self.inventory_check.inventory_check(order):
            print(f"Valid order {order['orderId']}", flush=True)
            self.event_sender.send(exchange="", routing_key="payment-order-queue", event=Event(key="inventory.valid", data=order))
        else:
            print(f"Invalid order {order['orderId']}", flush=True)
            self.event_sender.send(exchange="", routing_key="payment-order-queue", event=Event(key="inventory.invalid", data=order))