from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import os


K = TypeVar('K')
T = TypeVar('T')

class EventType(str, Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    UPDATE = "UPDATE"

class Event(BaseModel, Generic[K, T]):
    type: EventType
    key: K
    data: T
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1e6))
    random: int = Field(default_factory=lambda: int.from_bytes(os.urandom(8), byteorder="big"))
