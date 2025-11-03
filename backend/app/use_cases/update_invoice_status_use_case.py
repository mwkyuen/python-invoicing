from sqlalchemy.orm import Session
from app.domain.invoice import Invoice
from app.daos.invoice_dao import InvoiceDAO
from typing import Optional


def execute(db: Session, invoice_id: int, new_status: str) -> Optional[Invoice]:
    """
    Update invoice status with validation.
    Business logic layer - works with domain models.
    """
    # Get existing invoice
    invoice_dao = InvoiceDAO(db)
    invoice = invoice_dao.get_by_id(invoice_id)
    if not invoice:
        raise ValueError(f"Invoice with ID {invoice_id} not found")

    # Validate status transition
    if not invoice.can_update_status(new_status):
        raise ValueError(
            f"Cannot update status from '{invoice.status}' to '{new_status}'"
        )

    # Update status via DAO (DAO handles commit)
    updated_invoice = invoice_dao.update_status(invoice_id, new_status)

    return updated_invoice
