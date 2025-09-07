import uuid
from sqlalchemy import Column, Integer, String
from datetime import datetime
from utils.config import Config

class Payment(Config.base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)

    orderId = Column(
        String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )
    creditCardNumber = Column(String(64))

    createdAt = Column(Integer, nullable=False, default=datetime.now)
    success = Column(bool, nullable=False, default=False)

    def __init__(self, orderId:str, creditCardNumber:str):
        self.orderId = orderId
        self.creditCardNumber = creditCardNumber