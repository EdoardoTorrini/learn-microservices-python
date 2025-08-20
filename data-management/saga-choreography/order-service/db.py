from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from shared.settings import settings

class Base(DeclarativeBase): pass

def get_db_url():
    if settings.ORDER_DATABASE_URL:
        return settings.ORDER_DATABASE_URL
    # fallback per test locali
    return "sqlite+aiosqlite:///./order.db"

engine = create_async_engine(get_db_url(), echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
