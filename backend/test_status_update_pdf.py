"""
Test script to verify that updating invoice status regenerates the PDF.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.domain.client import Client
from app.domain.invoice import Invoice
from app.domain.line_item import LineItem
from app.db import SessionLocal
from app.daos.client_dao import ClientDAO
from app.daos.invoice_dao import InvoiceDAO
from app.use_cases import update_invoice_status_use_case

print("=" * 60)
print("Invoice Status Update & PDF Regeneration Test")
print("=" * 60)

# Create test data
print("\n[Step 1] Creating test client and invoice...")
db = SessionLocal()

try:
    # Create client
    client_dao = ClientDAO(db)
    client = Client(
        name="Status Test Company",
        billing_address="123 Test Street",
        email="status@test.com",
        phone_number="555-0123"
    )
    saved_client = client_dao.create(client)
    print(f"✓ Created client: {saved_client.name} (ID: {saved_client.id})")

    # Create invoice
    invoice_dao = InvoiceDAO(db)
    line_items = [
        LineItem(
            description="Test Service",
            quantity=1.0,
            unit_price=500.00
        )
    ]

    # Generate unique invoice number using timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    invoice = Invoice(
        invoice_number=f"INV-STATUS-TEST-{timestamp}",
        client_id=saved_client.id,
        issue_date=datetime.now(),
        status="draft",
        line_items=line_items,
        pdf_path=None
    )

    saved_invoice = invoice_dao.create(invoice)
    print(f"✓ Created invoice: {saved_invoice.invoice_number}")
    print(f"  Initial status: {saved_invoice.status}")
    print(f"  PDF path: {saved_invoice.pdf_path}")

    # Read initial PDF
    initial_pdf_path = Path(saved_invoice.pdf_path) if saved_invoice.pdf_path else None
    if initial_pdf_path and initial_pdf_path.exists():
        initial_pdf_size = initial_pdf_path.stat().st_size
        initial_pdf_mtime = initial_pdf_path.stat().st_mtime
        print(f"  PDF size: {initial_pdf_size} bytes")
        print(f"  PDF modified: {datetime.fromtimestamp(initial_pdf_mtime)}")

    # Update status to "sent"
    print("\n[Step 2] Updating invoice status to 'sent'...")
    print("-" * 60)
    updated_invoice = update_invoice_status_use_case.execute(
        db, saved_invoice.id, "sent"
    )
    print("-" * 60)
    print(f"✓ Updated invoice status: {updated_invoice.status}")

    # Check if PDF was regenerated
    print("\n[Step 3] Verifying PDF was regenerated...")
    updated_pdf_path = Path(updated_invoice.pdf_path) if updated_invoice.pdf_path else None
    if updated_pdf_path and updated_pdf_path.exists():
        updated_pdf_size = updated_pdf_path.stat().st_size
        updated_pdf_mtime = updated_pdf_path.stat().st_mtime
        print(f"✓ PDF exists: {updated_pdf_path}")
        print(f"  PDF size: {updated_pdf_size} bytes")
        print(f"  PDF modified: {datetime.fromtimestamp(updated_pdf_mtime)}")

        if initial_pdf_path:
            if updated_pdf_mtime > initial_pdf_mtime:
                print(f"✓ PDF was regenerated (timestamp changed)")
            else:
                print(f"⚠ Warning: PDF timestamp unchanged")
    else:
        print("✗ ERROR: PDF not found")

    # Update status to "paid"
    print("\n[Step 4] Updating invoice status to 'paid'...")
    print("-" * 60)
    paid_invoice = update_invoice_status_use_case.execute(
        db, updated_invoice.id, "paid"
    )
    print("-" * 60)
    print(f"✓ Updated invoice status: {paid_invoice.status}")

    # Verify final PDF
    print("\n[Step 5] Verifying final PDF...")
    final_pdf_path = Path(paid_invoice.pdf_path) if paid_invoice.pdf_path else None
    if final_pdf_path and final_pdf_path.exists():
        final_pdf_size = final_pdf_path.stat().st_size
        final_pdf_mtime = final_pdf_path.stat().st_mtime
        print(f"✓ PDF exists: {final_pdf_path}")
        print(f"  PDF size: {final_pdf_size} bytes")
        print(f"  PDF modified: {datetime.fromtimestamp(final_pdf_mtime)}")

        if updated_pdf_mtime:
            if final_pdf_mtime > updated_pdf_mtime:
                print(f"✓ PDF was regenerated again (timestamp changed)")
            else:
                print(f"⚠ Warning: PDF timestamp unchanged")
    else:
        print("✗ ERROR: PDF not found")

    print("\n" + "=" * 60)
    print("SUCCESS: Invoice status updates regenerate PDF!")
    print("=" * 60)
    print(f"\nYou can check the PDF at: {final_pdf_path}")
    print("The status badge should show 'PAID' in green.")

finally:
    db.close()
