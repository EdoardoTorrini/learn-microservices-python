import pika
from events.event import Event
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EventSender:
    def __init__(self):
        url = os.getenv("RABBITMQ_URL", "amqp://admin:admin@rabbitmq_cqrs:5672/")
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="app.events", exchange_type="topic", durable=True)
        
    def send(self, routing_key: str, event: Event) -> None:

        logger.info(f"Sending event {event}")

        self.channel.basic_publish(
            exchange="app.events",
            routing_key=routing_key,
            body=event.to_json()
        )