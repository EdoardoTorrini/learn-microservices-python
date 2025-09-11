import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from threading import Thread
from events.receiver import EventReceiver

from utils.config import Config
from order.controller import get_order_view

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_order_view())

def start_event_receiver():
    receiver = EventReceiver()
    receiver.start_consuming()

if __name__ == "__main__":

    t = Thread(target=start_event_receiver, daemon=True)
    t.start()

    uvicorn.run(app, host=Config.host, port=Config.port)