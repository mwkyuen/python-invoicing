from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.invoice import (
    InvoiceCreateRequest,
    InvoiceResponse,
    InvoiceUpdateStatusRequest
)
from app.use_cases import (
    create_invoice_use_case,
    list_invoices_use_case,
    update_invoice_status_use_case
)

router = APIRouter(prefix="/api/invoices", tags=["invoices"])


@router.post("", response_model=InvoiceResponse, status_code=201)
def create_invoice(
    request: InvoiceCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new invoice with line items"""
    try:
        # Convert Pydantic line items to dict format for use-case
        line_items_data = [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price
            }
            for item in request.line_items
        ]

        # Call use-case
        invoice = create_invoice_use_case.execute(
            db=db,
            client_id=request.client_id,
            line_items_data=line_items_data
        )
        # Convert domain to Pydantic response
        return InvoiceResponse.from_domain(invoice)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[InvoiceResponse])
def list_invoices(db: Session = Depends(get_db)):
    """List all invoices with line items"""
    try:
        # Call use-case
        invoices = list_invoices_use_case.execute(db)
        # Convert domain models to Pydantic responses
        return [InvoiceResponse.from_domain(invoice) for invoice in invoices]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{invoice_id}", response_model=InvoiceResponse | None)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Get a single invoice by ID with line items, returns None if not found"""
    try:
        from app.daos.invoice_dao import InvoiceDAO
        invoice_dao = InvoiceDAO(db)
        invoice = invoice_dao.get_by_id(invoice_id)
        if not invoice:
            return None
        return InvoiceResponse.from_domain(invoice)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice_status(
    invoice_id: int,
    request: InvoiceUpdateStatusRequest,
    db: Session = Depends(get_db)
):
    """Update invoice status"""
    try:
        # Call use-case
        invoice = update_invoice_status_use_case.execute(
            db=db,
            invoice_id=invoice_id,
            new_status=request.status
        )
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return InvoiceResponse.from_domain(invoice)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{invoice_id}/pdf")
def download_invoice_pdf(invoice_id: int, db: Session = Depends(get_db)):
    """Download invoice PDF with cache-busting to ensure latest version"""
    try:
        from pathlib import Path
        from app.daos.invoice_dao import InvoiceDAO

        # Get invoice
        invoice_dao = InvoiceDAO(db)
        invoice = invoice_dao.get_by_id(invoice_id)

        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        if not invoice.pdf_path:
            raise HTTPException(
                status_code=404, detail="PDF not yet generated"
            )

        # Verify PDF file exists
        pdf_file = Path(invoice.pdf_path)
        if not pdf_file.exists():
            raise HTTPException(
                status_code=404,
                detail="PDF file not found on server"
            )

        # Return with cache-busting headers to ensure fresh download
        return FileResponse(
            invoice.pdf_path,
            media_type="application/pdf",
            filename=f"{invoice.invoice_number}.pdf",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
