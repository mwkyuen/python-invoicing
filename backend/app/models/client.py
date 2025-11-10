from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class ClientCreateRequest(BaseModel):
    """Request model for creating a client"""
    name: str
    billing_address: str
    email: EmailStr
    phone_number: str


class ClientResponse(BaseModel):
    """Response model for client data"""
    id: int
    name: str
    billing_address: str
    email: str
    phone_number: str
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, client):
        """Convert from domain model to Pydantic response"""
        return cls(
            id=client.id,
            name=client.name,
            billing_address=client.billing_address,
            email=client.email,
            phone_number=client.phone_number,
            created_at=datetime.now()  # Will be overridden from database
        )
