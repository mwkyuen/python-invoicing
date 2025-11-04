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

    # Create invoice domain model (without ID, for PDF generation)
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

    # Generate PDF before saving to database
    pdf_path = None
    try:
        from app.pdf_generator import generate_invoice_pdf
        pdf_path = generate_invoice_pdf(invoice, client)
        invoice.pdf_path = pdf_path
    except Exception as e:
        # Log error but don't fail the invoice creation
        print(f"Warning: Failed to generate PDF: {e}")

    # Persist via DAO with pdf_path already set (DAO handles commit)
    saved_invoice = invoice_dao.create(invoice)

    return saved_invoice
