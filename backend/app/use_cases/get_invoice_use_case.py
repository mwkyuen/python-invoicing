from sqlalchemy.orm import Session
from app.domain.invoice import Invoice
from app.daos.invoice_dao import InvoiceDAO
from typing import Optional


def execute(db: Session, invoice_id: int) -> Optional[Invoice]:
    """
    Get a single invoice by ID with line items.
    Returns None if not found.
    Business logic layer - works with domain models.
    """
    invoice_dao = InvoiceDAO(db)
    invoice = invoice_dao.get_by_id(invoice_id)
    return invoice
