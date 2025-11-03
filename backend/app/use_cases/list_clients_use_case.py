from sqlalchemy.orm import Session
from app.domain.client import Client
from app.daos.client_dao import ClientDAO
from typing import List


def execute(db: Session) -> List[Client]:
    """
    List all clients.
    Business logic layer - works with domain models.
    """
    client_dao = ClientDAO(db)
    clients = client_dao.get_all()
    return clients
