from fastapi import APIRouter, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi_class import View

from persistance.noise import get_noise

import time


route = APIRouter()

@View(route, path="/noise")
class NoiseView:

    async def get(self, request: Request, response: Response):
        return JSONResponse(
            content={
                "delay": get_noise().delay,
                "fault": get_noise().get_fault()
            },
            status_code=status.HTTP_200_OK,
            headers=response.headers
        )
    
    async def post(self, request: Request, response: Response):

        body = await request.json()
        get_noise().delay = body.get("delay")

        try:
            get_noise().set_fault(body.get("fault"))
        except Exception as e:
            return JSONResponse(
                content={"err": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return status.HTTP_204_NO_CONTENT
        

def get_noise_route() -> APIRouter:
    return route