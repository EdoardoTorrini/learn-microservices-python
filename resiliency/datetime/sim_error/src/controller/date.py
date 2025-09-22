from fastapi import APIRouter, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi_class import View

from persistance.noise import get_noise

import time


route = APIRouter()

@View(route, path="/date")
class DateView:

    async def get(self, request: Request, response: Response):
        time.sleep(get_noise().delay)
        if get_noise().fault_exception():
            return JSONResponse(
                content={"msg": "internal server error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                headers=response.headers
            )

        return JSONResponse(
            content={"date": get_noise().get_date()},
            status_code=status.HTTP_200_OK,
            headers=response.headers
        )
        

def get_date_route() -> APIRouter:
    return route