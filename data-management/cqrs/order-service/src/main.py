from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import os, uvicorn

from controller.order import get_order_route

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

Instrumentator().instrument(app).expose(app)
app.include_router(get_order_route())


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
    uvicorn.run(app, host=ip, port=port)