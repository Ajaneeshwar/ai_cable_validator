"""
Database Configuration Module

Handles SQLite database connection and session management using SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

# Create SQLite engine with check_same_thread=False for FastAPI async compatibility
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

# Session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_database():
    """
    Database session dependency for FastAPI routes.
    
    Yields:
        Session: SQLAlchemy database session.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def initialize_database():
    """Create all database tables defined in models."""
    Base.metadata.create_all(bind=engine)
