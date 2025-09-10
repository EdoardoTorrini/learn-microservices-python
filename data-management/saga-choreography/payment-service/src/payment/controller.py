from fastapi import APIRouter
from fastapi_class import View

from events.receiver import EventReceiver

router = APIRouter()

@View(router, path="/payment")
class PaymentController:
    pass



def get_payment_view():
    return router
