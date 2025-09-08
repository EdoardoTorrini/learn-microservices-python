from fastapi import APIRouter
from fastapi_class import View

import payment.workers as workers

router = APIRouter()

@View(router, path="/payment")
class PaymentController:

    paymentWorkers = workers.PaymentWorkers()



def get_payment_view():
    return router
