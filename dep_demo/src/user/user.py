from uuid import uuid4
from pydantic import BaseModel, PrivateAttr


class User(BaseModel):

    _id: str = PrivateAttr(default_factory=lambda: str(uuid4))
    email: str
    name: str
    country: str = ""