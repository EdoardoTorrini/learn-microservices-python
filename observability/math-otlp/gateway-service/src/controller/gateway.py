from fastapi import APIRouter, status, Response, Request, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi_class import View
import itertools
import httpx

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
        params = {"n": n, "times": times, "faults": faults}
        print(f"Forwarding GetPrimeDivisors({n} - {times}) to {url}")

        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(url, params=params)
                res.raise_for_status()
                return res.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

    

def get_gateway_divisors_route() -> APIRouter:
    return route