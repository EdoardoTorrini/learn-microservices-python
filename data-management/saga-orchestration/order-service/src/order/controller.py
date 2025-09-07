from fastapi import APIRouter, status
from fastapi_class import View

from dto.dto import OrderDTO
import order.workers as workers

router = APIRouter()

@View(router, path="/order")
class OrderController:

    orderWorkers = workers.OrderWorkers()


    async def post(self, order: OrderDTO):
        print(order)
        out = self.orderWorkers.startOrderFlow(order)
        return {"workflowId": out["workflowId"]}, status.HTTP_202_ACCEPTED


def get_order_view():
    return router
