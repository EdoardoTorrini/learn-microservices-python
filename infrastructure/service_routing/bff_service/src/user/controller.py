from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_class import View

from user.dto import UserDTO
from utils.config import Config
import requests


router = APIRouter()

@View(router, path="/users")
class UserController:

    async def get(self, uuid: str = None):
        req = requests.get(Config.user_url, params={"uuid": uuid})
        return JSONResponse(
            content=req.json(),
            status_code=req.status_code
        )

    async def post(self, user: UserDTO):
        req = requests.post(Config.user_url, json=dict(user))
        return JSONResponse(
            content=req.json(),
            status_code=req.status_code
        )

def get_user_router() -> APIRouter:
    return router