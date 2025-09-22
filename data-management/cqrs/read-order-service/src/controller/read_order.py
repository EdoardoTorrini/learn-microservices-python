from fastapi import APIRouter, status, Response, Request, Depends, Query
from fastapi.responses import JSONResponse
from fastapi_class import View
from persistence.dependencies import get_order_repo
from persistence.dto import OrderConfirmedRepository

route = APIRouter()

@View(route, path="/order")
class OrderView:

    async def get(self, request: Request, response: Response, customer_id: str = Query(..., alias="customerId"), month: int = Query(...), year: int = Query(...), repo: OrderConfirmedRepository = Depends(get_order_repo)):
        
        order_db = repo.find_by_customer_month_year(customer_id=customer_id, month=month, year=year)
        if order_db:
            order = {
                "customer_id": order_db.customer_id,
                "month": order_db.month,
                "year": order_db.year,
                "n": order_db.n
            }
        else:
            order = {"message": "No orders found"}
            
        return JSONResponse(content=order, status_code=status.HTTP_200_OK)
        
    
def get_order_route() -> APIRouter:
    return route