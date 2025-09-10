from sqlalchemy import Column, Integer, String
from utils.config import Config

class Inventory(Config.base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    productId = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)

    def __init__(self, productId: str, quantity: int):
        self.productId = productId
        self.quantity = quantity