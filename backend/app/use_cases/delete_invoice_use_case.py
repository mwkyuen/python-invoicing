"""
Use case for deleting an invoice.
Business logic: Delete invoice and associated line items from the system.
"""
from sqlalchemy.orm import Session
from app.daos.invoice_dao import InvoiceDAO


def execute(db: Session, invoice_id: int) -> bool:
    """
    Delete an invoice by ID (cascade deletes line items).

    Args:
        db: Database session
        invoice_id: ID of the invoice to delete

    Returns:
        True if invoice was deleted, False if not found

    Raises:
        ValueError: If invoice_id is invalid
    """
    if invoice_id <= 0:
        raise ValueError("Invoice ID must be positive")

    invoice_dao = InvoiceDAO(db)
    return invoice_dao.delete(invoice_id)
