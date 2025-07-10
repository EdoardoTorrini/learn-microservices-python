from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_class import View

from comment.dto import CommentDTO
from utils.config import Config

import requests


router = APIRouter()

@View(router, path="/comments")
class CommentController:

    async def get(self, uuid: str = None):
        req = requests.get(Config.comment_url, params={"uuid": uuid})
        return JSONResponse(
            content=req.json(),
            status_code=req.status_code
        )
    
    async def post(self, comment: CommentDTO):
        req = requests.post(Config.comment_url, json=dict(comment))
        return JSONResponse(
            content=req.json(),
            status_code=req.status_code
        )


def get_comment_router() -> APIRouter:
    return router
