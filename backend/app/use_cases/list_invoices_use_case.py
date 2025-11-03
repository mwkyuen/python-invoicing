from sqlalchemy.orm import Session
from app.domain.invoice import Invoice
from app.daos.invoice_dao import InvoiceDAO
from typing import List


def execute(db: Session) -> List[Invoice]:
    """
    List all invoices with line items.
    Business logic layer - works with domain models.
    """
    invoice_dao = InvoiceDAO(db)
    invoices = invoice_dao.get_all()
    return invoices
