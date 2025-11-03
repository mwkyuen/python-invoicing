"""
Quick test script to verify database initialization.
Run this to ensure SQLAlchemy relationships are working correctly.
"""
from app.db import init_db, get_db, Base
from app.schemas.client import ClientTable
from app.schemas.invoice import InvoiceTable
from app.schemas.line_item import LineItemTable

def test_db_init():
    print("Testing database initialization...")

    # Initialize the database (creates tables)
    init_db()
    print("✓ Database initialized successfully")

    # Verify all tables are registered
    tables = Base.metadata.tables.keys()
    print(f"✓ Tables created: {list(tables)}")

    # Test that we can create a session
    db = next(get_db())
    print("✓ Database session created successfully")
    db.close()

    # Verify relationships are properly configured
    print("\nChecking relationships...")
    invoice_rels = InvoiceTable.__mapper__.relationships.keys()
    print(f"✓ InvoiceTable relationships: {list(invoice_rels)}")

    line_item_rels = LineItemTable.__mapper__.relationships.keys()
    print(f"✓ LineItemTable relationships: {list(line_item_rels)}")

    print("\n✅ All checks passed! Database is ready to use.")

if __name__ == "__main__":
    test_db_init()
