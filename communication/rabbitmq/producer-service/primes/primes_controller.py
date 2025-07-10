from common.rabbitmq import RabbitMQClient
from common.event import Event, EventType
from common.params import params

from fastapi_class import View
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from primes.prime import Prime

from uuid import uuid4
import os, json


router = APIRouter()

@View(router, path="/gen_primes")
class PrimeView:

    _rabbitmq = RabbitMQClient(**params)
    _queue = "cpu-intensive"

    async def post(self, prime: Prime):
        try:
            event = Event[str, dict](
                type=EventType.CREATE,
                key=str(uuid4()),
                data={
                    "lower_bound": prime.lower_bound, 
                    "upper_bound": prime.upper_bound,
                    "email": prime.email
                }
            )
            self._rabbitmq.publish(self._queue, dict(event))
            return JSONResponse(content={"message": "ok"}, status_code=status.HTTP_202_ACCEPTED)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    async def get(self):

        example = {"lower_bound": 1, "upper_bound": 100, "email": "example@gmail.com"}

        return JSONResponse(
            content={
                "message": "make a post request with a dictionary of: lower_bound, upper_bound, email",
                "example": f'''curl -X POST 'http://{os.getenv("HOST")}:{int(os.getenv("PORT"))}/gen_primes' -H 'Content-Type: application/json' -d {json.dumps(example)}'''
            }, 
            status_code=status.HTTP_200_OK
        )
    
def get_prime_route() -> APIRouter:
    return router