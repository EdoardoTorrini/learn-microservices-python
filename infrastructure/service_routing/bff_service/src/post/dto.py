from pydantic import BaseModel, Field
from uuid import uuid4


class PostDTO(BaseModel):

    uuid: str = Field(default_factory=lambda: str(uuid4()))
    user_uuid: str
    content: str