from persistence.order import OrderStatus
from dto import OrderRepository
from dependencies import SessionLocal
from events.event import Event

class OrderService:
    def __init__(self, event_sender):
        self.event_sender = event_sender

    def handle_payment_invalid(self, order_data: dict):
        order_id = order_data["orderId"]
        with SessionLocal() as session:
            repo = OrderRepository(session)
            db_order = repo.find_by_order_id(order_id)
            if db_order:
                db_order.status = OrderStatus.REJECTED
                repo.save(db_order)
                print(f"Payment invalid → Order {order_id} REJECTED", flush=True)

    def handle_inventory_invalid(self, order_data: dict):
        order_id = order_data["orderId"]
        with SessionLocal() as session:
            repo = OrderRepository(session)
            db_order = repo.find_by_order_id(order_id)
            if db_order:
                db_order.status = OrderStatus.REJECTED
                repo.save(db_order)
                print(f"Inventory invalid → Order {order_id} REJECTED", flush=True)

    def handle_inventory_valid(self, order_data: dict):
        order_id = order_data["orderId"]
        with SessionLocal() as session:
            repo = OrderRepository(session)
            db_order = repo.find_by_order_id(order_id)
            if db_order:
                db_order.status = OrderStatus.APPROVED
                repo.save(db_order)
                print(f"Inventory valid → Order {order_id} APPROVED", flush=True)
            
                event = Event(key="order.confirmed", data={"orderId": order_id, "status": db_order.status.value})
                self.event_sender.send("", "order-confirmed-queue", event)
