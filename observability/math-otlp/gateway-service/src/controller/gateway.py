from fastapi import APIRouter, status, Response, Request, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi_class import View
import itertools
from cb.circuitbreaker import get_divisors

route = APIRouter()

MATH_SERVICES = ["http://math-service-1:8080/divisors",
                 "http://math-service-2:8080/divisors"]

# Round-Robin
service_cycle = itertools.cycle(MATH_SERVICES)

@View(route, path="/divisors")
class GatewayView:
    async def get(self, request: Request, response: Response, 
                  n: int = Query(..., ge=2), 
                  times: int = Query(1, ge=1), 
                  faults: int = Query(0, ge=0, le=100)):
        
        url = next(service_cycle)
        print(f"Forwarding GetPrimeDivisors({n} - {times}) to {url}", flush=True)

        try:
            result = get_divisors(n=n, times=times, faults=faults, url=url)
            return JSONResponse(content=result, status_code=status.HTTP_200_OK, headers=response.headers)
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {e}")

    

def get_gateway_divisors_route() -> APIRouter:
    return route