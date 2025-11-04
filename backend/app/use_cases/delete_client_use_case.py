"""
Use case for deleting a client.
Business logic: Delete client from the system.
Validates that no invoices exist for the client before deletion.
"""
from sqlalchemy.orm import Session
from app.daos.client_dao import ClientDAO
from app.daos.invoice_dao import InvoiceDAO


def execute(db: Session, client_id: int) -> bool:
    """
    Delete a client by ID.
    Prevents deletion if the client has any associated invoices.

    Args:
        db: Database session
        client_id: ID of the client to delete

    Returns:
        True if client was deleted, False if not found

    Raises:
        ValueError: If client_id is invalid or client has invoices
    """
    if client_id <= 0:
        raise ValueError("Client ID must be positive")

    # Check if client has any invoices
    invoice_dao = InvoiceDAO(db)
    if invoice_dao.has_invoices_for_client(client_id):
        raise ValueError(
            "Cannot delete client with existing invoices. "
            "Please delete all invoices for this client first."
        )

    # Proceed with deletion if no invoices exist
    client_dao = ClientDAO(db)
    return client_dao.delete(client_id)
