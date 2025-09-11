from fastapi import APIRouter
from fastapi_class import View

router = APIRouter()

@View(router, path="/payment")
class PaymentController:
    pass



def get_payment_view():
    return router
