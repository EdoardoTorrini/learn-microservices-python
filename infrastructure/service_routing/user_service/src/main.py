import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware                                                        

from user.config import Config
from user.controller import get_user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_user_router())

if __name__ == "__main__":
    uvicorn.run(app, host=Config.host, port=Config.port)