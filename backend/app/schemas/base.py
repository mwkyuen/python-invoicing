"""
Shared SQLAlchemy Base for all schema models.
All table models must inherit from this Base to ensure
relationships can be resolved across tables.
"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()
