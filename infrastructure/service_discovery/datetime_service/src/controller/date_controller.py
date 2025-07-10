from fastapi_class import View
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from model.date import Date


router = APIRouter()


@View(router, path="/datetime")
class DateController:

    async def get(self):
        date = Date()
        return JSONResponse(
            content=dict(date),
            status_code=status.HTTP_200_OK
        )

def get_datetime_route() -> APIRouter:
    return router