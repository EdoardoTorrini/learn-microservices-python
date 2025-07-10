from fastapi import APIRouter, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi_class import View

from stresser.prime import PrimeDescriptor
from datetime import datetime
import sympy, hashlib, base64, os


route = APIRouter()

@View(route, path="/stress_test")
class StressView:

    _desc = PrimeDescriptor(lower_bound=1, upper_bound=100, email="")

    def _assign_cookie_if_missing(self, request: Request, response: Response):
        val = request.cookies.get("STRESS_ID")
        if val is None:
            response.set_cookie(
                key="STRESS_ID",
                value=base64.b64encode(hashlib.sha1(os.urandom(8)).digest()).decode(),
                httponly=False,
                max_age=3600,
                path="/"
            )

    async def get(self, request: Request, response: Response):
        self._assign_cookie_if_missing(request, response)
        ret, start = [sympy.nextprime(self._desc.lower_bound)], int(datetime.now().timestamp() * 1e3)
        while ret[-1] < self._desc.upper_bound:
            ret.append(sympy.nextprime(ret[-1]))
        end = int(datetime.now().timestamp() * 1e3)
        
        return JSONResponse(
            content={"email": self._desc.email, "exec_time [ms]": int(end-start), "primes": ret,}, 
            status_code=status.HTTP_200_OK,
            headers=response.headers
        )
    
    async def post(self, request: Request, response: Response, desc: PrimeDescriptor):
        self._desc = desc
        self._assign_cookie_if_missing(request, response)
        return JSONResponse(content={"message": "ok"}, status_code=status.HTTP_202_ACCEPTED, headers=response.headers)
    
def get_stress_route() -> APIRouter:
    return route