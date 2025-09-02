import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

class Config:
    # service config
    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", 8080)

    # db
    _db_host, _db_port = os.getenv("DB_HOST", "localhost"), int(os.getenv("DB_PORT", "3306"))
    _db_user, _db_pwd = os.getenv("DB_USER","root"), os.getenv("DB_PASSWORD", "")
    _db_name = os.getenv("DB_NAME", "db")

    db_url = f"mysql+pymysql://{_db_user}:{_db_pwd}@{_db_host}:{_db_port}/{_db_name}?charset=utf8mb4"


    engine = create_engine(db_url, pool_pre_ping=True, future=True)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
    base = declarative_base()

def get_db():
    db = Config.session_local()

    try:
        yield db
    finally:
        db.close()