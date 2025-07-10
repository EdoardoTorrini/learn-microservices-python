from pydantic import BaseModel
from typing import List

class CommentDTO(BaseModel):
    uuid: str
    content: str

class PostComment(BaseModel):
    uuid: str
    content: str
    comment: List[CommentDTO]

class BffDTO(BaseModel):
    uuid: str
    nickname: str
    birthday: str
    post: List[PostComment]
