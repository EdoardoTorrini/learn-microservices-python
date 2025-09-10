from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Generic, TypeVar
import json

K = TypeVar("K")
T = TypeVar("T")

@dataclass
class Event(Generic[K, T]):
    key: K
    data: T
    event_created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)

    @staticmethod
    def from_json(payload: str) -> "Event":
        raw = json.loads(payload)
        return Event(
            key=raw["key"],
            data=raw["data"],
            event_created_at=datetime.fromisoformat(raw["event_created_at"])
        )