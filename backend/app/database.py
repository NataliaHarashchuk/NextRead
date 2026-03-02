from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,          
    max_overflow=10,     
    pool_pre_ping=True,   
    echo=False,         
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Для PostgreSQL
)

Base = declarative_base()


def get_db():
    """Database session generator"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@event.listens_for(engine, "connect")
def set_postgres_pragmas(dbapi_conn, connection_record):
    """Setting up PostgreSQL when connecting"""
    cursor = dbapi_conn.cursor()
    try:
        cursor.execute("SET timezone='UTC'")
    finally:
        cursor.close()