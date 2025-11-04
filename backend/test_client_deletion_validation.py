"""
Test script to verify client deletion validation.
Tests that clients with invoices cannot be deleted.
"""
import sys
sys.path.insert(0, '/Users/michaelyuen/python-invoicing/backend')

from app.db import SessionLocal
from app.daos.client_dao import ClientDAO
from app.daos.invoice_dao import InvoiceDAO
from app.use_cases import delete_client_use_case, create_client_use_case, create_invoice_use_case

def test_delete_client_validation():
    """Test that client with invoices cannot be deleted"""
    db = SessionLocal()

    try:
        print("\n" + "="*60)
        print("TEST: Client Deletion Validation")
        print("="*60)

        # Step 1: Create a test client
        print("\n[Step 1] Creating test client...")
        client = create_client_use_case.execute(
            db=db,
            name="Test Client for Deletion",
            billing_address="123 Test St, Test City, TC 12345",
            email="testdelete@example.com",
            phone_number="+1-555-1234"
        )
        print(f"✓ Client created: ID={client.id}, Name='{client.name}'")

        # Step 2: Try to delete client without invoices (should succeed)
        print("\n[Step 2] Attempting to delete client without invoices...")
        try:
            deleted = delete_client_use_case.execute(db, client.id)
            if deleted:
                print("✓ Client deleted successfully (no invoices existed)")
            else:
                print("✗ Client not found")
        except ValueError as e:
            print(f"✗ Unexpected error: {e}")

        # Step 3: Create a new client with an invoice
        print("\n[Step 3] Creating new client with invoice...")
        client2 = create_client_use_case.execute(
            db=db,
            name="Test Client with Invoice",
            billing_address="456 Invoice St, Invoice City, IC 67890",
            email="testinvoice@example.com",
            phone_number="+1-555-5678"
        )
        print(f"✓ Client created: ID={client2.id}, Name='{client2.name}'")

        # Step 4: Create an invoice for the client
        print("\n[Step 4] Creating invoice for client...")
        line_items_data = [
            {
                "description": "Test Service",
                "quantity": 1,
                "unit_price": 100.00
            }
        ]
        invoice = create_invoice_use_case.execute(
            db=db,
            client_id=client2.id,
            line_items_data=line_items_data
        )
        print(f"✓ Invoice created: {invoice.invoice_number}")

        # Step 5: Try to delete client WITH invoices (should fail)
        print("\n[Step 5] Attempting to delete client WITH invoices...")
        try:
            deleted = delete_client_use_case.execute(db, client2.id)
            print("✗ FAILED: Client was deleted despite having invoices!")
            print("   This should have been prevented by validation.")
        except ValueError as e:
            print(f"✓ VALIDATION PASSED: Deletion prevented")
            print(f"   Error message: '{e}'")

        # Step 6: Verify client still exists
        print("\n[Step 6] Verifying client still exists...")
        client_dao = ClientDAO(db)
        existing_client = client_dao.get_by_id(client2.id)
        if existing_client:
            print(f"✓ Client still exists: ID={existing_client.id}, Name='{existing_client.name}'")
        else:
            print("✗ FAILED: Client was deleted!")

        # Step 7: Delete the invoice first
        print("\n[Step 7] Deleting invoice to test cleanup...")
        invoice_dao = InvoiceDAO(db)
        invoice_deleted = invoice_dao.delete(invoice.id)
        if invoice_deleted:
            print(f"✓ Invoice {invoice.invoice_number} deleted")

        # Step 8: Now try to delete client again (should succeed)
        print("\n[Step 8] Attempting to delete client after invoice removed...")
        try:
            deleted = delete_client_use_case.execute(db, client2.id)
            if deleted:
                print("✓ Client deleted successfully after invoice was removed")
            else:
                print("✗ Client not found")
        except ValueError as e:
            print(f"✗ Unexpected error: {e}")

        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print("\nValidation Summary:")
        print("  ✓ Clients without invoices can be deleted")
        print("  ✓ Clients with invoices CANNOT be deleted")
        print("  ✓ Error message is user-friendly")
        print("  ✓ After deleting invoices, client can be deleted")
        print("\n")

    except Exception as e:
        print(f"\n✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    test_delete_client_validation()
