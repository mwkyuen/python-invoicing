from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.invoice import InvoiceTable
from app.schemas.line_item import LineItemTable
from app.domain.invoice import Invoice
from app.domain.line_item import LineItem
from typing import List, Optional


class InvoiceDAO:
    """Data Access Object for Invoice operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, invoice: Invoice) -> Invoice:
        """Create a new invoice with line items in the database"""
        db_invoice = InvoiceTable(
            invoice_number=invoice.invoice_number,
            client_id=invoice.client_id,
            issue_date=invoice.issue_date,
            total_amount=invoice.total_amount,  # Calculated from domain
            status=invoice.status,
            pdf_path=invoice.pdf_path
        )
        self.db.add(db_invoice)
        self.db.flush()

        # Create line items
        for line_item in invoice.line_items:
            db_line_item = LineItemTable(
                invoice_id=db_invoice.id,
                description=line_item.description,
                quantity=line_item.quantity,
                unit_price=line_item.unit_price,
                amount=line_item.amount  # Calculated from domain
            )
            self.db.add(db_line_item)

        self.db.flush()
        self.db.commit()

        # Fetch the complete invoice with line items
        return self.get_by_id(db_invoice.id)

    def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """Get an invoice by ID with line items"""
        db_invoice = (
            self.db.query(InvoiceTable)
            .filter(InvoiceTable.id == invoice_id)
            .first()
        )
        if db_invoice:
            return self._to_domain(db_invoice)
        return None

    def get_all(self) -> List[Invoice]:
        """Get all invoices with line items"""
        db_invoices = self.db.query(InvoiceTable).all()
        return [self._to_domain(invoice) for invoice in db_invoices]

    def update_status(self, invoice_id: int, status: str) -> Optional[Invoice]:
        """Update invoice status"""
        db_invoice = (
            self.db.query(InvoiceTable)
            .filter(InvoiceTable.id == invoice_id)
            .first()
        )
        if db_invoice:
            db_invoice.status = status
            self.db.flush()
            self.db.commit()
            return self._to_domain(db_invoice)
        return None

    def update_pdf_path(
        self, invoice_id: int, pdf_path: str
    ) -> Optional[Invoice]:
        """Update invoice PDF path"""
        db_invoice = (
            self.db.query(InvoiceTable)
            .filter(InvoiceTable.id == invoice_id)
            .first()
        )
        if db_invoice:
            db_invoice.pdf_path = pdf_path
            self.db.flush()
            self.db.commit()
            return self._to_domain(db_invoice)
        return None

    def generate_next_invoice_number(self) -> str:
        """Generate next sequential invoice number"""
        # Get the latest invoice number
        latest_invoice = (
            self.db.query(InvoiceTable)
            .order_by(InvoiceTable.id.desc())
            .first()
        )

        if latest_invoice:
            # Extract number from format INV-YYYY-NNNN
            parts = latest_invoice.invoice_number.split("-")
            if len(parts) == 3:
                year = parts[1]
                number = int(parts[2]) + 1
            else:
                # Fallback if format is unexpected
                from datetime import datetime
                year = str(datetime.now().year)
                number = 1
        else:
            # First invoice
            from datetime import datetime
            year = str(datetime.now().year)
            number = 1

        return f"INV-{year}-{number:04d}"

    def _to_domain(self, db_invoice: InvoiceTable) -> Invoice:
        """Convert SQLAlchemy model to domain model"""
        # Fetch line items
        db_line_items = (
            self.db.query(LineItemTable)
            .filter(LineItemTable.invoice_id == db_invoice.id)
            .all()
        )

        line_items = [
            LineItem(
                id=item.id,
                invoice_id=item.invoice_id,
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
            for item in db_line_items
        ]

        return Invoice(
            id=db_invoice.id,
            invoice_number=db_invoice.invoice_number,
            client_id=db_invoice.client_id,
            issue_date=db_invoice.issue_date,
            status=db_invoice.status,
            pdf_path=db_invoice.pdf_path,
            line_items=line_items
        )
