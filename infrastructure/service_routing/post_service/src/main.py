import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware                                                        

from post.config import Config
from post.controller import get_post_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_post_router())

if __name__ == "__main__":
    uvicorn.run(app, host=Config.host, port=Config.port)