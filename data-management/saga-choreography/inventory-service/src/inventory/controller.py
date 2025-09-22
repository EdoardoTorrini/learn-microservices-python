from fastapi import APIRouter
from fastapi_class import View

router = APIRouter()

@View(router, path="/inventory")
class InventoryController:
    pass



def get_inventory_view():
    return router
