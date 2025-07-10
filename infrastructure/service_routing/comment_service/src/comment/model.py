from sqlalchemy import Column, Integer, String, BigInteger
from datetime import datetime

from comment.config import Config

class Comment(Config.base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    comment_uuid = Column(String, unique=True, index=True, nullable=False)
    post_uuid = Column(String, index=True, nullable=False)
    timestamp = Column(BigInteger, default=lambda: int(datetime.now().timestamp()))
    content = Column(String, nullable=False)
