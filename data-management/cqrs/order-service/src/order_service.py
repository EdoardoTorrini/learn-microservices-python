from persistence.order import OrderStatus
from dto import OrderRepository

class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def handle_payment_invalid(self, order_data: dict):
        order_id = order_data["orderId"]
        db_order = self.repo.find_by_order_id(order_id)
        if db_order:
            db_order.status = OrderStatus.REJECTED
            self.repo.save(db_order)
            print(f"Payment invalid → Order {order_id} REJECTED", flush=True)

    def handle_inventory_invalid(self, order_data: dict):
        order_id = order_data["orderId"]
        db_order = self.repo.find_by_order_id(order_id)
        if db_order:
            db_order.status = OrderStatus.REJECTED
            self.repo.save(db_order)
            print(f"Inventory invalid → Order {order_id} REJECTED", flush=True)

    def handle_inventory_valid(self, order_data: dict):
        order_id = order_data["orderId"]
        db_order = self.repo.find_by_order_id(order_id)
        if db_order:
            db_order.status = OrderStatus.APPROVED
            self.repo.save(db_order)
            print(f"Inventory valid → Order {order_id} APPROVED", flush=True)
