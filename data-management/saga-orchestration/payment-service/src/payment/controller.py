from fastapi import APIRouter
from fastapi_class import View

import payment.workers as workers

router = APIRouter()

@View(router, path="/payment")
class PaymentController:

    orderWorkers = workers.PaymentWorkers()



def get_order_view():
    return router
