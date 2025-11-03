from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict
from app.domain.invoice import Invoice
from app.domain.line_item import LineItem
from app.daos.invoice_dao import InvoiceDAO
from app.daos.client_dao import ClientDAO


def execute(
    db: Session, client_id: int, line_items_data: List[Dict]
) -> Invoice:
    """
    Create a new invoice with line items.
    Business logic layer - works with domain models.
    Generates invoice number, calculates total, and creates PDF.
    """
    # Verify client exists
    client_dao = ClientDAO(db)
    client = client_dao.get_by_id(client_id)
    if not client:
        raise ValueError(f"Client with ID {client_id} not found")

    # Generate invoice number
    invoice_dao = InvoiceDAO(db)
    invoice_number = invoice_dao.generate_next_invoice_number()

    # Create line items domain models
    line_items = []
    for item_data in line_items_data:
        line_item = LineItem(
            description=item_data["description"],
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"]
        )
        line_item.validate()
        line_items.append(line_item)

    # Create invoice domain model
    invoice = Invoice(
        invoice_number=invoice_number,
        client_id=client_id,
        issue_date=datetime.now(),
        status="draft",
        line_items=line_items,
        pdf_path=None
    )

    # Domain validation
    invoice.validate()

    # Persist via DAO
    saved_invoice = invoice_dao.create(invoice)

    # Generate PDF
    try:
        from app.pdf_generator import generate_invoice_pdf
        pdf_path = generate_invoice_pdf(saved_invoice, client)
        invoice_dao.update_pdf_path(saved_invoice.id, pdf_path)
        # Reload to get updated pdf_path
        saved_invoice = invoice_dao.get_by_id(saved_invoice.id)
    except Exception as e:
        # Log error but don't fail the invoice creation
        print(f"Warning: Failed to generate PDF: {e}")

    return saved_invoice
