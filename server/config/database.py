from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

SERVER_URL = "mysql+pymysql://root:root@localhost/"

temp_engine = create_engine(SERVER_URL)

with temp_engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS afe_mgmt_sys"))

SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://root:root@localhost/afe_mgmt_sys"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()