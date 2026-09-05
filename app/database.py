from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


from app.config import settings


# print(settings.DATABASE_URL)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass

def create_tables():
    from app.models import (Donors, Donations, Payments,Users, Receipts,Expenses)
    Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()    