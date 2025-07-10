from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_class import View

from post.dto import PostDTO
from utils.config import Config

import requests


router = APIRouter()

@View(router, path="/posts")
class PostController:

    async def get(self, uuid: str = None):
        req = requests.get(Config.post_url, params={"uuid": uuid})
        return JSONResponse(
            content=req.json(),
            status_code=req.status_code
        )

    async def post(self, post: PostDTO):
        req = requests.post(Config.post_url, json=dict(post))
        return JSONResponse(
            content=req.json(),
            status_code=req.status_code
        )


def get_post_router() -> APIRouter:
    return router