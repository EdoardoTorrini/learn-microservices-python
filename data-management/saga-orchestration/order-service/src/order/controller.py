from fastapi import APIRouter, status, routing, Depends
from fastapi.responses import JSONResponse
from fastapi_class import View

from order.dto import OrderDTO


router = APIRouter()

@View(router, path="/order")
class OrderController:

    async def get(self):
        pass

    async def post(self, order: OrderDTO):
        print(order)
        return status.HTTP_204_NO_CONTENT


def get_order_view():
    return router
