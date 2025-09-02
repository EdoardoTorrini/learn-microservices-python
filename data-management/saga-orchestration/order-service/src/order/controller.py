from fastapi import APIRouter, status, routing, Depends
from fastapi.responses import JSONResponse
from fastapi_class import View

from order.dto import OrderDTO
from utils.config import get_db
from order.flow import start_order_flow


router = APIRouter()

@View(router, path="/order")
class OrderController:

    async def get(self):
        pass

    async def post(self, order: OrderDTO):
        print(order)
        out = start_order_flow(order)
        return {"workflowId": out["workflowId"]}, status.HTTP_202_ACCEPTED


def get_order_view():
    return router
