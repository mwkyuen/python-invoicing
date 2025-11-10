"""
Test PDF generation with actual invoice data to simulate real usage.
This mimics what happens during invoice creation.
"""
import sys
import time
from datetime import datetime
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("Invoice PDF Generation Test")
print("=" * 60)

# Import domain models
print("\n[Step 1] Importing domain models...")
try:
    from app.domain.client import Client
    from app.domain.invoice import Invoice
    from app.domain.line_item import LineItem
    print("✓ Domain models imported")
except Exception as e:
    print(f"✗ Failed to import domain models: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Create test data
print("\n[Step 2] Creating test invoice and client...")
try:
    test_client = Client(
        id=1,
        name="Test Company Inc.",
        billing_address="123 Main St, City, State 12345",
        email="test@example.com",
        phone_number="+1-555-123-4567"
    )

    line_items = [
        LineItem(
            id=1,
            description="Web Development Services",
            quantity=10.0,
            unit_price=150.0,
            invoice_id=1
        ),
        LineItem(
            id=2,
            description="Design Consultation",
            quantity=5.0,
            unit_price=100.0,
            invoice_id=1
        )
    ]

    test_invoice = Invoice(
        id=1,
        invoice_number="INV-TEST-001",
        client_id=1,
        issue_date=datetime.now(),
        status="draft",
        line_items=line_items,
        pdf_path=None
    )

    print(f"✓ Created test invoice: {test_invoice.invoice_number}")
    print(f"  - Client: {test_client.name}")
    print(f"  - Line items: {len(line_items)}")
    print(f"  - Total: ${test_invoice.total_amount:.2f}")
except Exception as e:
    print(f"✗ Failed to create test data: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Import PDF generator
print("\n[Step 3] Importing PDF generator...")
try:
    from app.pdf_generator import generate_invoice_pdf
    print("✓ PDF generator imported")
except Exception as e:
    print(f"✗ Failed to import PDF generator: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Generate PDF
print("\n[Step 4] Generating PDF (this is where it might hang)...")
print("Watch for diagnostic logs from pdf_generator.py...")
print("-" * 60)
try:
    start_time = time.time()
    pdf_path = generate_invoice_pdf(test_invoice, test_client)
    elapsed = time.time() - start_time
    print("-" * 60)
    print(f"✓ PDF generated in {elapsed:.2f}s")
    print(f"  Path: {pdf_path}")

    # Verify file exists
    if Path(pdf_path).exists():
        file_size = Path(pdf_path).stat().st_size
        print(f"  Size: {file_size} bytes")
        print("✓ PDF file exists on disk")
    else:
        print("✗ PDF file not found on disk!")

except KeyboardInterrupt:
    print("\n✗ Test interrupted by user (Ctrl+C)")
    print("This means the PDF generation is hanging/blocking")
    sys.exit(1)
except Exception as e:
    elapsed = time.time() - start_time
    print("-" * 60)
    print(f"✗ PDF generation failed after {elapsed:.2f}s: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("SUCCESS: Invoice PDF generation works correctly!")
print("=" * 60)
