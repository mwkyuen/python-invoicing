from sqlalchemy.orm import Session
from app.domain.invoice import Invoice
from app.daos.invoice_dao import InvoiceDAO
from app.daos.client_dao import ClientDAO
from app.pdf_generator import generate_invoice_pdf
from typing import Optional


def execute(db: Session, invoice_id: int, new_status: str) -> Optional[Invoice]:
    """
    Update invoice status with validation and regenerate PDF.
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
    if not updated_invoice:
        raise ValueError(f"Failed to update invoice {invoice_id}")

    # Regenerate PDF with updated status
    print(
        f"[Use Case] Regenerating PDF for invoice "
        f"{updated_invoice.invoice_number} with status: {new_status}"
    )
    client_dao = ClientDAO(db)
    client = client_dao.get_by_id(updated_invoice.client_id)
    if client:
        pdf_path = generate_invoice_pdf(updated_invoice, client)
        print(f"[Use Case] PDF regenerated at: {pdf_path}")

        # Update the invoice record with the new PDF path
        updated_invoice = invoice_dao.update_pdf_path(invoice_id, pdf_path)
        if updated_invoice:
            print(f"[Use Case] Invoice PDF path updated in database")
        else:
            print(f"[Use Case] Warning: Failed to update PDF path")
    else:
        print(
            f"[Use Case] Warning: Client not found for "
            f"invoice {invoice_id}"
        )

    return updated_invoice
