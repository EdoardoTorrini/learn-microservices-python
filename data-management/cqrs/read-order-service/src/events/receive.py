import os
import pika
from events.event import Event
from persistence.dependencies import SessionLocal
from persistence.dto import OrderConfirmedRepository
from datetime import datetime
from persistence.order_confirmed import OrderConfirmed

class EventReceiver:
    def __init__(self):
        url = os.getenv("RABBITMQ_URL", "amqp://admin:admin@rabbitmq_cqrs:5672/")
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue="order-confirmed-queue", durable=True)
    
    def start(self, queue_name = "order-confirmed-queue"):
        self.channel.queue_declare(queue=queue_name, durable=True)

        def callback(ch, method, properties, body):
            event = Event.from_json(body.decode())

            if event.key == "order.confirmed":
                self.manage_order(event.data)
            
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
        
    def manage_order(self, order):
        customer_id = order.get("customerId", "UNKNOWN")
        now = datetime.now()


        with SessionLocal() as session:
            repo = OrderConfirmedRepository(session=session)
            existing = repo.find_by_customer_month_year(customer_id=customer_id, month=now.month, year=now.year)

            if existing:
                existing.n += 1
                session.commit()
                print(f"Updated read model: customer {customer_id}, count = {existing.n}", flush=True)
            else:
                new_order = OrderConfirmed(customer_id=customer_id, month=now.month, year=now.year, n=1)
                repo.save(new_order)
                print(f"Created new read model for {customer_id} in {now.month}/{now.year}", flush=True)