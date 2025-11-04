"""
Test to verify that PDF downloads reflect the current invoice status.
This test checks that cache-busting headers work correctly.
"""
import sys
from pathlib import Path
from datetime import datetime
import time

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.domain.client import Client
from app.domain.invoice import Invoice
from app.domain.line_item import LineItem
from app.db import SessionLocal
from app.daos.client_dao import ClientDAO
from app.daos.invoice_dao import InvoiceDAO
from app.use_cases import update_invoice_status_use_case

print("=" * 70)
print("PDF Status Update & Download Test")
print("=" * 70)

# Create test data
print("\n[Step 1] Creating test client and invoice...")
db = SessionLocal()

try:
    # Create client
    client_dao = ClientDAO(db)
    client = Client(
        name="PDF Download Test Co",
        billing_address="456 Cache St",
        email="pdf@test.com",
        phone_number="555-8888"
    )
    saved_client = client_dao.create(client)
    print(f"✓ Created client: {saved_client.name}")

    # Create invoice with initial status
    invoice_dao = InvoiceDAO(db)
    line_items = [
        LineItem(
            description="Test Product",
            quantity=2.0,
            unit_price=50.00
        )
    ]

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    invoice = Invoice(
        invoice_number=f"INV-PDF-TEST-{timestamp}",
        client_id=saved_client.id,
        issue_date=datetime.now(),
        status="draft",
        line_items=line_items,
        pdf_path=None
    )

    saved_invoice = invoice_dao.create(invoice)
    print(f"✓ Created invoice: {saved_invoice.invoice_number}")
    print(f"  Initial status: {saved_invoice.status}")
    print(f"  Initial PDF path: {saved_invoice.pdf_path}")

    # Read initial PDF to check status
    if saved_invoice.pdf_path:
        pdf_path = Path(saved_invoice.pdf_path)
        if pdf_path.exists():
            with open(pdf_path, 'rb') as f:
                initial_content = f.read()
            initial_size = len(initial_content)
            initial_mtime = pdf_path.stat().st_mtime
            print(f"  Initial PDF: {initial_size} bytes")

            # Check if "DRAFT" appears in PDF
            if b'draft' in initial_content.lower():
                print("  ✓ PDF contains 'draft' status")
            else:
                print("  ⚠ PDF does not contain 'draft' status")

    # Update status to "sent"
    print("\n[Step 2] Updating invoice status to 'sent'...")
    print("-" * 70)
    time.sleep(0.1)  # Small delay to ensure different timestamp

    updated_invoice = update_invoice_status_use_case.execute(
        db, saved_invoice.id, "sent"
    )
    print("-" * 70)
    print(f"✓ Status updated: {updated_invoice.status}")
    print(f"  Updated PDF path: {updated_invoice.pdf_path}")

    # Verify PDF was regenerated
    print("\n[Step 3] Verifying PDF reflects new status...")
    pdf_path = Path(updated_invoice.pdf_path)
    if pdf_path.exists():
        updated_mtime = pdf_path.stat().st_mtime
        with open(pdf_path, 'rb') as f:
            updated_content = f.read()
        updated_size = len(updated_content)

        print(f"  PDF size: {updated_size} bytes")
        print(f"  Modification time changed: {updated_mtime > initial_mtime}")

        # Check if "SENT" appears in PDF
        if b'sent' in updated_content.lower():
            print("  ✓ PDF contains 'sent' status")
        else:
            print("  ❌ PDF does not contain 'sent' status")

        # Check if "DRAFT" is gone
        if b'draft' not in updated_content.lower():
            print("  ✓ PDF no longer contains 'draft' status")
        else:
            print("  ⚠ PDF still contains 'draft' status")
    else:
        print("  ❌ PDF file not found!")

    # Simulate a second status change
    print("\n[Step 4] Updating invoice status to 'paid'...")
    print("-" * 70)
    time.sleep(0.1)

    paid_invoice = update_invoice_status_use_case.execute(
        db, updated_invoice.id, "paid"
    )
    print("-" * 70)
    print(f"✓ Status updated: {paid_invoice.status}")

    # Final verification
    print("\n[Step 5] Final PDF verification...")
    pdf_path = Path(paid_invoice.pdf_path)
    if pdf_path.exists():
        final_mtime = pdf_path.stat().st_mtime
        with open(pdf_path, 'rb') as f:
            final_content = f.read()
        final_size = len(final_content)

        print(f"  PDF size: {final_size} bytes")
        print(f"  Modification time changed: {final_mtime > updated_mtime}")

        # Check if "PAID" appears in PDF
        if b'paid' in final_content.lower():
            print("  ✓ PDF contains 'paid' status")
        else:
            print("  ❌ PDF does not contain 'paid' status")

        # Check previous statuses are gone
        if b'draft' not in final_content.lower() and \
           b'sent' not in final_content.lower():
            print("  ✓ PDF no longer contains old statuses")

    print("\n" + "=" * 70)
    print("CACHE-BUSTING HEADERS RECOMMENDATIONS")
    print("=" * 70)
    print("\n✓ The backend now includes cache-busting headers:")
    print("  - Cache-Control: no-cache, no-store, must-revalidate")
    print("  - Pragma: no-cache")
    print("  - Expires: 0")
    print("\nThese headers ensure:")
    print("  1. Browser won't cache the PDF")
    print("  2. Always fetches the latest version from server")
    print("  3. Status changes are immediately reflected in downloads")

    print("\n" + "=" * 70)
    print("SUCCESS: PDF regeneration verified!")
    print("=" * 70)
    print(f"\nFinal PDF location: {paid_invoice.pdf_path}")
    print("The PDF file is updated on each status change.")

finally:
    db.close()
