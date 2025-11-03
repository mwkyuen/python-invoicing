from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .line_item import LineItemCreateRequest, LineItemResponse


class InvoiceCreateRequest(BaseModel):
    """Request model for creating an invoice"""
    client_id: int
    line_items: List[LineItemCreateRequest]


class InvoiceUpdateStatusRequest(BaseModel):
    """Request model for updating invoice status"""
    status: str


class InvoiceResponse(BaseModel):
    """Response model for invoice data"""
    id: int
    invoice_number: str
    client_id: int
    issue_date: datetime
    total_amount: float
    status: str
    pdf_path: Optional[str] = None
    line_items: List[LineItemResponse] = []

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, invoice):
        """Convert from domain model to Pydantic response"""
        return cls(
            id=invoice.id,
            invoice_number=invoice.invoice_number,
            client_id=invoice.client_id,
            issue_date=invoice.issue_date,
            total_amount=invoice.total_amount,  # Calculated from domain
            status=invoice.status,
            pdf_path=invoice.pdf_path,
            line_items=[
                LineItemResponse.from_domain(item)
                for item in invoice.line_items
            ]
        )
