from pydantic import BaseModel
from typing import Literal, Any
from datetime import datetime
import uuid

EventType = Literal["order.created","payment.ok","payment.failed","inventory.ok","inventory.failed"]

class BaseEvent(BaseModel):
    event_id: str
    correlation_id: str  # order_id
    event_type: EventType
    timestamp: datetime
    payload: dict[str, Any]

def new_event(event_type: EventType, correlation_id: str, payload: dict) -> BaseEvent:
    return BaseEvent(
        event_id=str(uuid.uuid4()),
        correlation_id=correlation_id,
        event_type=event_type,
        timestamp=datetime.utcnow(),
        payload=payload or {},
    )
