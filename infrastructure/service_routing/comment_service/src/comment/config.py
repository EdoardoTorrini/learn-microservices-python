from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


class Config:

    # db
    _db_host, _db_port = os.getenv("DB_HOST", "localhost"), int(os.getenv("DB_PORT", "3306"))
    _db_user, _db_pwd = os.getenv("DB_USER", "root"), os.getenv("DB_PASSWORD", "")
    _db_name = os.getenv("DB_NAME", "db")

    db_url = f"mysql://{_db_user}:{_db_pwd}@{_db_host}:{_db_port}/{_db_name}"

    engine = create_engine(db_url)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    base = declarative_base()
    
    # service config
    host, port = os.getenv("HOST", "0.0.0.0"), int(os.getenv("PORT", 80))


def get_db():
    db = Config.session_local()
    
    try:
        yield db
    finally:
        db.close()