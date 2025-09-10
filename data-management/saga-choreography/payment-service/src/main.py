import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware      

import threading                                                  

from utils.config import Config
from payment.controller import get_payment_view
from events.receiver import EventReceiver

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_payment_view()) 

# receiver = EventReceiver()

# @app.on_event("startup")
# def _start_consumer():
#     t = threading.Thread(target=receiver.start_consuming, daemon=True)
#     t.start()
# TODO: pensa a come avviare il receiver mantenendo fastapi

if __name__ == "__main__":
    uvicorn.run(app, host=Config.host, port=Config.port)