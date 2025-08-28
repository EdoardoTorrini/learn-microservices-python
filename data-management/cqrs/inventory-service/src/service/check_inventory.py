from dto import OrderRepository

class InventoryCheck:
    def __init__(self, inv_repo: OrderRepository):
        self.inv_repo = inv_repo

    def inventory_check(self, order: dict) -> bool:
        product_ids = order.get("productIds", [])
        if not product_ids:
            return False
        
        product_ids = product_ids[0].split(",")
        print(f"1. {product_ids = }")
        products_to_update = []
        for pid in product_ids:
            pid = pid.strip()
            product = self.inv_repo.find_by_product_id(pid)
            if not product or product.quantity <= 0:
                print(f"[InventoryCheck] Prodotto {pid} NON trovato in inventario o esaurito", flush=True)
                return False
            products_to_update.append(product)
        
        for product in products_to_update:
            product.quantity -= 1

            self.inv_repo.save(product)
        
        return True