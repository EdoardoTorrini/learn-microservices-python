from pydantic import BaseModel, Field
from uuid import uuid4


class CommentDTO(BaseModel):

    uuid: str = Field(default_factory=lambda: str(uuid4()))
    post_uuid: str
    content: str