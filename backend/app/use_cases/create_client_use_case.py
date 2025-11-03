from sqlalchemy.orm import Session
from app.domain.client import Client
from app.daos.client_dao import ClientDAO


def execute(db: Session, name: str, billing_address: str, email: str, phone_number: str) -> Client:
    """
    Create a new client with validation.
    Business logic layer - works with domain models.
    """
    # Create domain model
    client = Client(
        name=name,
        billing_address=billing_address,
        email=email,
        phone_number=phone_number
    )

    # Domain validation
    client.validate()

    # Persist via DAO (DAO handles commit)
    client_dao = ClientDAO(db)
    saved_client = client_dao.create(client)

    return saved_client
