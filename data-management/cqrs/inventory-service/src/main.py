from service.inventory_service import run_inventory_service

'''
curl -X POST http://localhost:9000/order \
 -H "Content-Type: application/json" \
 -d '{
   "productIds": ["PROD-A1", "PROD-D4"],
   "creditCardNumber": "7777-1234-5678-0000"
 }'
'''

if __name__ == "__main__":
    run_inventory_service()