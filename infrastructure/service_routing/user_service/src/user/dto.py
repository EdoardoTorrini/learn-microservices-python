from pydantic import BaseModel, Field
from uuid import uuid4


class UserDTO(BaseModel):

    uuid: str = Field(default_factory=lambda: str(uuid4()))
    nickname: str
    birthday: str