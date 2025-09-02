import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware                                                        

from utils.config import Config
from order.controller import get_order_view

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_order_view())

if __name__ == "__main__":
    print("run main",flush=True)
    uvicorn.run(app, host=Config.host, port=Config.port)