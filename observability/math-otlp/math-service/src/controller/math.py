from fastapi import APIRouter, status, Response, Request, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi_class import View
import time, random
from sympy import factorint

route = APIRouter()

@View(route, path="/divisors")
class MathView:
    async def get(self, request: Request, response: Response, 
                  n: int = Query(..., ge=2), 
                  times: int = Query(1, ge=1), 
                  faults: int = Query(0, ge=0, le=100)):
    
        print(f"getPrimeDivisors({n} - {times})")

        begin = time.time()
        for _ in range(times):
            find_prime_divisors(n)
        end = time.time()

        throw_error_if_bad_luck(faults)


        return JSONResponse(
            content={
                "n": n,
                "divisors": find_prime_divisors(n),
                "latency": str(int((end-begin)*1000)) + " ms"
            },
            status_code=status.HTTP_200_OK,
            headers=response.headers
        )

def find_prime_divisors(n: int) -> list[int]:
    factors = factorint(n)
    result = []

    for prime, exp in factors.items():
        result.extend([prime] * exp)
    return result

    
def throw_error_if_bad_luck(faults: int):
    if random.randint(1,100) <= faults:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service Unavailable")


def get_divisors_route() -> APIRouter:
    return route