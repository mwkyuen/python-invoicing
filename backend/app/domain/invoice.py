from dataclasses import dataclass
from datetime import datetime
from typing import List
from .line_item import LineItem


@dataclass
class Invoice:
    """
    An invoice with line items and automatic total calculation.
    The core business entity of the system.
    """
    invoice_number: str           # "INV-2025-0042" (auto-generated)
    client_id: int                # Reference to client
    issue_date: datetime          # When invoice was created
    status: str                   # "draft", "sent", "paid", "cancelled"
    line_items: List[LineItem]    # List of services/products
    pdf_path: str | None = None   # Path to generated PDF
    id: int | None = None

    @property
    def total_amount(self) -> float:
        """
        Automatically calculates invoice total from line items.
        This is ALWAYS the sum of all line item amounts.
        Never set this manually!
        """
        return sum(item.amount for item in self.line_items)

    def validate(self):
        """Business rule validation"""
        if not self.invoice_number:
            raise ValueError("Invoice number is required")

        if not self.line_items:
            raise ValueError("Invoice must have at least one line item")

        if self.total_amount <= 0:
            raise ValueError("Invoice total must be positive")

        # Validate status
        valid_statuses = ["draft", "sent", "paid", "cancelled"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")

        # Validate each line item
        for item in self.line_items:
            item.validate()

    def add_line_item(self, item: LineItem):
        """Business method to add a line item"""
        item.validate()
        self.line_items.append(item)

    @property
    def is_finalized(self) -> bool:
        """Check if invoice has been finalized (PDF generated)"""
        return self.pdf_path is not None

    def can_update_status(self, new_status: str) -> bool:
        """
        Allow all status transitions.
        PDF will be regenerated to reflect current status.
        """
        return True
