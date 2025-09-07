import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware                                                        

from utils.config import Config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_order_view()) # TODO trova come far opartire i worker di payment

if __name__ == "__main__":
    print("run main",flush=True)
    uvicorn.run(app, host=Config.host, port=Config.port)