# order/flow.py
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes_clients import OrkesClients
from conductor.client.http.models import StartWorkflowRequest

def start_order_flow(order_dto) -> dict:
    cfg = Configuration()
    clients = OrkesClients(configuration=cfg)
    wf = clients.get_workflow_client()

    req = StartWorkflowRequest()
    req.name = "order_saga_orchestration"
    req.input = {
        "orderId": order_dto.order_id,
        "productIds": order_dto.product_ids,
        "customerId": order_dto.customer_id,
        "creditCardNumber": order_dto.credit_card_number,
        "status": order_dto.status,
    }
    workflow_id = wf.start_workflow(req)
    return {"workflowId": workflow_id}
