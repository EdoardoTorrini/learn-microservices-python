from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from controller.time import get_time_route

from utils.config import Config

import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

Instrumentator().instrument(app).expose(app)
app.include_router(get_time_route())

if __name__ == "__main__":
    uvicorn.run(app, host=Config.ip, port=Config.port)