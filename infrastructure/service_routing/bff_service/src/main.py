import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware                                                        

from utils.config import Config
from user.controller import get_user_router
from post.controller import get_post_router
from comment.controller import get_comment_router
from bff.controller import get_bff_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(get_user_router())
app.include_router(get_post_router())
app.include_router(get_comment_router())
app.include_router(get_bff_router())

if __name__ == "__main__":
    uvicorn.run(app, host=Config.host, port=Config.port)