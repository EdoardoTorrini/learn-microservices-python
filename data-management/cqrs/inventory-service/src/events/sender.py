import pika
from events.event import Event
import os

class EventSender:
    def __init__(self):
        url = os.getenv("RABBITMQ_URL", "amqp://admin:admin@rabbitmq_cqrs:5672/")
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="queue", durable=True)

    def send(self, exchange: str, routing_key: str, event: Event):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=event.to_json()
        )
        print(f"Sent {event.key} in {routing_key}", flush=True) 