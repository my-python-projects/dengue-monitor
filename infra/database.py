from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from infra.config import Settings

engine = create_engine(Settings.DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
