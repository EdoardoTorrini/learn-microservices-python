from fastapi import APIRouter, status, Response, Request, Depends
from fastapi.responses import JSONResponse
from fastapi_class import View
import uuid

from persistence.order import Order, OrderStatus
from dto import OrderRepository
from dependencies import get_order_repo

from events.event import Event
from events.sender import EventSender


route = APIRouter()

@View(route, path="/order")
class OrderView:

  async def post(self, request: Request, response: Response, repo: OrderRepository = Depends(get_order_repo)):
    body = await request.json()

    order = Order(order_id=str(uuid.uuid4()), 
                  customer_id=body.get("customerId", str(uuid.uuid4())) ,
                  product_ids=",".join(body.get("productIds", [])), 
                  credit_card_number=body.get("creditCardNumber"), 
                  status=OrderStatus.PENDING)

    saved_order = repo.save(order)

    event = Event("order.created", {
      "orderId": saved_order.order_id,
      "customerId": saved_order.customer_id,
      "productIds": saved_order.product_ids.split(", "),
      "creditCardNumber": saved_order.credit_card_number,
      "status": saved_order.status.value}
      )
    
    sender = EventSender()
    sender.send(exchange="", routing_key="order-payment-queue", event=event)
    
    print(f"New order created: {order}", flush=True)

    return JSONResponse(content={
            "orderId": saved_order.order_id,
            "productIds": saved_order.product_ids.split(","),
            "customerId": saved_order.customer_id,
            "creditCardNumber": saved_order.credit_card_number,
            "status": saved_order.status.value
        }, status_code=status.HTTP_201_CREATED)

def get_order_route() -> APIRouter:
  return route