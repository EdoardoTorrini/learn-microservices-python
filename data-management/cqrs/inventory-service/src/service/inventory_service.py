from events.sender import EventSender
from service.check_inventory import InventoryCheck
from events.receive import EventReceiver
from dependencies import SessionLocal
from dto import OrderRepository

def run_inventory_service():
    db_session = SessionLocal()
    repo = OrderRepository(db_session)
    
    checker = InventoryCheck(repo)
    sender = EventSender()
    receiver = EventReceiver(event_sender=sender, inventory_check=checker)
    receiver.start()
