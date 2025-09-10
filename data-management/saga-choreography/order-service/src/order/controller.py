from fastapi import APIRouter, status
from fastapi_class import View
import logging

from dto.dto import OrderDTO
from order.model import Order, OrderStatus
from order.service import OrderService
from events.sender import EventSender
from events.event import Event

router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@View(router, path="/order")
class OrderController:

    orderService = OrderService()
    eventSender = EventSender()

    async def post(self, orderDTO: OrderDTO):
        logger.info("Starting orderflow for %s", getattr(orderDTO, "orderId", None))


        order = Order(
            productIds=orderDTO.productIds,
            customerId=orderDTO.customerId,
            creditCardNumber=orderDTO.creditCardNumber
        )
        order.orderId = orderDTO.orderId
        order.status = OrderStatus.PENDING
        
        self.orderService.place_pending_order(order)

        event = Event(key="order.created", data=orderDTO)
        
        self.eventSender.send("order.created", event)

        return {"Order Processed": getattr(orderDTO, "orderId", None)}, status.HTTP_202_ACCEPTED


def get_order_view():
    return router
