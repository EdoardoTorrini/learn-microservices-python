import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware                                                        

from comment.config import Config
from comment.controller import get_comment_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_comment_router())

if __name__ == "__main__":
    uvicorn.run(app, host=Config.host, port=Config.port)