from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.schemas.base import Base

# Import all tables to ensure they're registered with the Base metadata
from app.schemas.client import ClientTable  # noqa: F401
from app.schemas.invoice import InvoiceTable  # noqa: F401
from app.schemas.line_item import LineItemTable  # noqa: F401

# SQLite database URL
DATABASE_URL = "sqlite:///./invoices.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True  # Log SQL queries for debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
