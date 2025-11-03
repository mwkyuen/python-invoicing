from sqlalchemy.orm import Session
from app.schemas.client import ClientTable
from app.domain.client import Client
from typing import List, Optional


class ClientDAO:
    """Data Access Object for Client operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, client: Client) -> Client:
        """Create a new client in the database"""
        db_client = ClientTable(
            name=client.name,
            billing_address=client.billing_address,
            email=client.email,
            phone_number=client.phone_number
        )
        self.db.add(db_client)
        self.db.flush()
        self.db.commit()

        # Convert back to domain model with ID
        return self._to_domain(db_client)

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """Get a client by ID"""
        db_client = (
            self.db.query(ClientTable)
            .filter(ClientTable.id == client_id)
            .first()
        )
        if db_client:
            return self._to_domain(db_client)
        return None

    def get_all(self) -> List[Client]:
        """Get all clients"""
        db_clients = self.db.query(ClientTable).all()
        return [self._to_domain(client) for client in db_clients]

    def _to_domain(self, db_client: ClientTable) -> Client:
        """Convert SQLAlchemy model to domain model"""
        return Client(
            id=db_client.id,
            name=db_client.name,
            billing_address=db_client.billing_address,
            email=db_client.email,
            phone_number=db_client.phone_number
        )
