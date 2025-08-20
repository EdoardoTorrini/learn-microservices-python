from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    RABBIT_URL: str = Field(default="amqp://guest:guest@localhost:5672/")
    SERVICE_NAME: str = "unknown"

    ORDER_DATABASE_URL: str | None = None
    PAYMENT_DATABASE_URL: str | None = None
    INVENTORY_DATABASE_URL: str | None = None

    TESTING: int = 0          # 1 nei test unitari
    DISABLE_MQ: int = 0       # 1 per non connettere Rabbit nei test

    class Config:
        env_file = ".env"

settings = Settings()
