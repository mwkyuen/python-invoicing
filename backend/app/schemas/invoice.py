from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


class InvoiceTable(Base):
    """SQLAlchemy model for invoices table"""
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_number = Column(String, unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="draft")
    pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    line_items = relationship(
        "LineItemTable",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )
