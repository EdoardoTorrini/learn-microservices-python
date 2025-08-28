from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import os, uvicorn
from threading import Thread

from controller.order import get_order_route
from order_service import OrderService
from events.sender import EventSender
from events.receive import EventReceiver
from dependencies import get_db
from dto import OrderRepository

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

Instrumentator().instrument(app).expose(app)
app.include_router(get_order_route())


db_session = next(get_db())
repo = OrderRepository(db_session)
order_service = OrderService(repo=repo)
#event_sender = EventSender()
receiver = EventReceiver(order_service)

def start_receiver():
    receiver.start()

ip = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "9000"))
'''
curl -X POST http://localhost:9000/order \
 -H "Content-Type: application/json" \
 -d '{
   "productIds": ["PROD-A1", "PROD-D4"],
   "creditCardNumber": "7777-1234-5678-0000"
 }'
'''

if __name__ == "__main__":
    t = Thread(target=start_receiver, daemon=True)
    t.start()

    uvicorn.run(app, host=ip, port=port)