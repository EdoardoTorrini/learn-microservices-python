from pydantic import BaseModel, Field
from datetime import datetime

class Date(BaseModel):
    local_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    local_time: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
