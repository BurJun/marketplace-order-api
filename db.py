from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DB_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/test"

engine = create_engine(
    DB_URL,
    echo = False,
    future = True,
)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush = False,
    autocommit = False,
    future = True,
)

def get_session() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()