from fastapi import APIRouter
from fastapi_class import View

import inventory.workers as workers

router = APIRouter()

@View(router, path="/inventory")
class InventoryController:

    inventoryWorkers = workers.InventoryWorkers()



def get_inventory_view():
    return router
