from dataclasses import dataclass


@dataclass
class LineItem:
    """
    A line item on an invoice with automatic amount calculation.
    Example: "10 hours of web development @ $150/hour = $1,500"
    """
    description: str      # "Web Development Services"
    quantity: float       # 10.0 (can be decimal for hours)
    unit_price: float     # 150.00
    id: int | None = None
    invoice_id: int | None = None

    @property
    def amount(self) -> float:
        """
        Automatically calculates the line item total.
        This is a computed property - never set manually!
        """
        return self.quantity * self.unit_price

    def validate(self):
        """Business rule validation"""
        if not self.description or len(self.description) < 3:
            raise ValueError("Description must be at least 3 characters")

        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")
