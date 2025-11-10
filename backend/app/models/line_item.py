from pydantic import BaseModel
from typing import Optional


class LineItemCreateRequest(BaseModel):
    """Request model for creating a line item"""
    description: str
    quantity: float
    unit_price: float


class LineItemResponse(BaseModel):
    """Response model for line item data"""
    id: int
    invoice_id: int
    description: str
    quantity: float
    unit_price: float
    amount: float

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, line_item):
        """Convert from domain model to Pydantic response"""
        return cls(
            id=line_item.id,
            invoice_id=line_item.invoice_id,
            description=line_item.description,
            quantity=line_item.quantity,
            unit_price=line_item.unit_price,
            amount=line_item.amount  # Calculated property from domain
        )
