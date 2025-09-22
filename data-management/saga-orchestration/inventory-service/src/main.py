import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware                                                        

from utils.config import Config
from inventory.controller import get_inventory_view

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_inventory_view()) 

if __name__ == "__main__":
    uvicorn.run(app, host=Config.host, port=Config.port)