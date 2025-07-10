from sqlalchemy import Column, Integer, String, Date
from user.config import Config

class User(Config.base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)