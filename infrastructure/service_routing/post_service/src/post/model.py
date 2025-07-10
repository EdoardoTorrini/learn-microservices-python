from sqlalchemy import Column, Integer, String, BigInteger
from datetime import datetime

from post.config import Config

class Post(Config.base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    post_uuid = Column(String, unique=True, index=True, nullable=False)
    user_uuid = Column(String, index=True, nullable=False)
    timestamp = Column(BigInteger, default=lambda: int(datetime.now().timestamp()))
    content = Column(String, nullable=False)
