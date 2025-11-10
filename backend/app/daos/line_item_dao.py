from sqlalchemy.orm import Session
from app.schemas.line_item import LineItemTable
from app.domain.line_item import LineItem
from typing import List


class LineItemDAO:
    """Data Access Object for LineItem operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, line_item: LineItem) -> LineItem:
        """Create a new line item in the database"""
        db_line_item = LineItemTable(
            invoice_id=line_item.invoice_id,
            description=line_item.description,
            quantity=line_item.quantity,
            unit_price=line_item.unit_price,
            amount=line_item.amount  # Calculated property from domain
        )
        self.db.add(db_line_item)
        self.db.flush()

        # Convert back to domain model with ID
        return self._to_domain(db_line_item)

    def get_by_invoice_id(self, invoice_id: int) -> List[LineItem]:
        """Get all line items for an invoice"""
        db_line_items = (
            self.db.query(LineItemTable)
            .filter(LineItemTable.invoice_id == invoice_id)
            .all()
        )
        return [self._to_domain(item) for item in db_line_items]

    def _to_domain(self, db_line_item: LineItemTable) -> LineItem:
        """Convert SQLAlchemy model to domain model"""
        return LineItem(
            id=db_line_item.id,
            invoice_id=db_line_item.invoice_id,
            description=db_line_item.description,
            quantity=db_line_item.quantity,
            unit_price=db_line_item.unit_price
        )
