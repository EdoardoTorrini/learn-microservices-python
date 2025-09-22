from fastapi import APIRouter, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi_class import View

from cb.date import get_date


route = APIRouter()

@View(route, path="/date")
class TimeView:

    async def get(self, request: Request, response: Response):
        return JSONResponse(
            content=get_date(),
            status_code=status.HTTP_200_OK,
            headers=request.headers
        )
        

def get_date_route() -> APIRouter:
    return route