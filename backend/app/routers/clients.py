from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.client import ClientCreateRequest, ClientResponse
from app.use_cases import (
    create_client_use_case,
    list_clients_use_case,
    delete_client_use_case
)

router = APIRouter(prefix="/api/clients", tags=["clients"])


@router.post("", response_model=ClientResponse, status_code=201)
def create_client(
    request: ClientCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new client"""
    try:
        # Call use-case
        client = create_client_use_case.execute(
            db=db,
            name=request.name,
            billing_address=request.billing_address,
            email=request.email,
            phone_number=request.phone_number
        )
        # Convert domain to Pydantic response
        return ClientResponse.from_domain(client)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    """List all clients"""
    try:
        # Call use-case
        clients = list_clients_use_case.execute(db)
        # Convert domain models to Pydantic responses
        return [ClientResponse.from_domain(client) for client in clients]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{client_id}", response_model=ClientResponse | None)
def get_client(client_id: int, db: Session = Depends(get_db)):
    """Get a single client by ID, returns None if not found"""
    try:
        from app.daos.client_dao import ClientDAO
        client_dao = ClientDAO(db)
        client = client_dao.get_by_id(client_id)
        if not client:
            return None
        return ClientResponse.from_domain(client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Delete a client by ID"""
    try:
        deleted = delete_client_use_case.execute(db, client_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Client not found")
        return None
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
