from fastapi import APIRouter, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi_class import View

from cb.time import get_time

import time


route = APIRouter()

@View(route, path="/time")
class TimeView:

    async def get(self, request: Request, response: Response):
        return JSONResponse(
            content=get_time(),
            status_code=status.HTTP_200_OK,
            headers=request.headers
        )
        

def get_time_route() -> APIRouter:
    return route