from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import os, uvicorn
from controller.read_order import get_order_route
from threading import Thread
from events.receive import EventReceiver

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

Instrumentator().instrument(app).expose(app)
app.include_router(get_order_route())

receiver = EventReceiver()

def start_receiver():
    receiver.start()

ip = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "9003"))

'''
curl -X POST http://172.20.8.11:9000/order  -H "Content-Type: application/json"  -d '{"customerId": "user", "productIds": ["PROD-A1", "PROD-D4"], "creditCardNumber": "7777-1234-5678-0000"}'

curl -X GET "http://172.20.8.14:9003/order?customerId=user&year=2025&month=8" -H "Accept: application/json"
'''

if __name__ == "__main__":
    t = Thread(target=start_receiver, daemon=True)
    t.start()
    
    uvicorn.run(app, host=ip, port=port)