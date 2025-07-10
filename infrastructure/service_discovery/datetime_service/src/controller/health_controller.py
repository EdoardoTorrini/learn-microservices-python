from fastapi_class import View
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import json


router = APIRouter()


@View(router, path="/health")
class HealthController:

    async def get(self):
        return JSONResponse(
            content={"status": "ok"},
            status_code=status.HTTP_200_OK
        )

def get_heartbeat_route() -> APIRouter:
    return router