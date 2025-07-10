from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi_class import View

from utils.config import Config
from bff.dto import CommentDTO, BffDTO, PostComment

import requests


router = APIRouter()

@View(router, path="/bff")
class BffController:

    async def get(self, uuid: str = None):
        
        req = requests.get(Config.user_url, params={"uuid": uuid})
        user_list = req.json()

        req = requests.get(Config.post_url)
        post_list = req.json()

        req = requests.get(Config.comment_url)
        comment_list = req.json()

        # mappa i commenti per post_uuid
        comment_map = {
            post_uuid: [ dict(CommentDTO(**c)) for c in comment_list if c.get("post_uuid") == post_uuid ]
            for post_uuid in [ c["post_uuid"] for c in comment_list ]
        }

        # mappa i post per user_uuid
        post_map = {
            user_uuid: [
                PostComment(
                    uuid=post["uuid"],
                    content=post["content"],
                    comment=comment_map.get(post["uuid"], [])
                ).model_dump() for post in post_list if post["user_uuid"] == user_uuid
            ] for user_uuid in { post["user_uuid"] for post in post_list }
        }
        
        if uuid is not None:
            user_list = [ user_list ]

        print(f"{user_list = }", flush=True)
        response = [
            BffDTO(
                uuid=u["uuid"], 
                nickname=u["nickname"], 
                birthday=u["birthday"], 
                post=post_map.get(u["uuid"], [])
            ).model_dump() for u in user_list
        ]

        return JSONResponse(content=response, status_code=status.HTTP_200_OK)


def get_bff_router() -> APIRouter:
    return router
