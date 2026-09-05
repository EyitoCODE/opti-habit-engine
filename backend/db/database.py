"""
Opti-Habit Engine: Database Engine and Session Management

Configures the SQLAlchemy ORM connection pool and SQLite backend,
providing a scoped database session dependency for route handlers.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite connection URL storing persistent records in a local habit_engine.db file.
# Fine-tuning and Iteration: Replace with PostgreSQL URI for multi-tenant production setups.
SQLALCHEMY_DATABASE_URL = "sqlite:///./habit_engine.db"

# connect_args={"check_same_thread": False} is required exclusively for SQLite
# to allow FastAPI request workers across multiple threads to access the connection.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Thread-local session factory for database operations.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for ORM model inheritance.
Base = declarative_base()

def get_db():
    """
    FastAPI dependency yielding an isolated database session per request,
    guaranteeing connection closure upon completion or exception.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()