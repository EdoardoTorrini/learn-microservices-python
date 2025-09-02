# Data Management
## CQRS
```mermaid
flowchart TD
  Client-Write -->|POST /order| OrderService-Write
  Client-Read -->|GET /order| OrderService-Read
  OrderService-Write -->|order.created| PaymentService
  OrderService-Write -->|order.confirmed| OrderService-Read
  PaymentService -->|payment.valid| InventoryService
  PaymentService -->|payment.invalid| OrderService-Write
  InventoryService -->|inventory.valid| OrderService-Write
  InventoryService -->|inventory.invalid| OrderService-Write
```

### Introduction

In this exercise, three services collaborate to implement a **Saga Pattern** using asynchronous messaging.\
The services are:
- **Order service**: Accepts a POST request and create an order, starting the workflow.
- **Payment service**: Validates the customer's payment.
- **Inventory service**: Checks products availability and reserve the items for the order.

The communication occurs via **RabbitMQ**, defining a queue for each service.\
Every service has its own database.

### Commands

```bash
curl -X POST http://172.20.8.11:9000/order  -H "Content-Type: application/json"  -d '{"customerId": "user", "productIds": ["PROD-A1", "PROD-D4"], "creditCardNumber": "7777-1234-5678-0000"}'
```


```bash
curl -X GET "http://172.20.8.14:9003/order?customerId=user&year=2025&month=8" -H "Accept: application/json"
```

