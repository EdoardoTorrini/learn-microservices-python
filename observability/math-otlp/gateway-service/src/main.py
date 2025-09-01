from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import os, uvicorn
from controller.gateway import get_gateway_divisors_route

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

Instrumentator().instrument(app).expose(app)

app.include_router(get_gateway_divisors_route())

ip = os.getenv("HOST", "127.0.0.1")
port = int(os.getenv("PORT", "8080"))

if __name__ == "__main__":
    uvicorn.run(app, host=ip, port=port)