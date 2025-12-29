from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Client as ClientModel
from app.schemas.schemas import Client, ClientCreate, ClientUpdate
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[Client])
def list_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all clients"""
    clients = db.query(ClientModel).filter(
        ClientModel.client_id == settings.CLIENT_ID
    ).offset(skip).limit(limit).all()
    return clients


@router.post("/", response_model=Client)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    """Create a new client"""
    db_client = ClientModel(
        **client.model_dump(),
        client_id=settings.CLIENT_ID
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.get("/{client_id}", response_model=Client)
def get_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific client by ID"""
    client = db.query(ClientModel).filter(
        ClientModel.id == client_id,
        ClientModel.client_id == settings.CLIENT_ID
    ).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=Client)
def update_client(
    client_id: int,
    client_update: ClientUpdate,
    db: Session = Depends(get_db)
):
    """Update a client"""
    client = db.query(ClientModel).filter(
        ClientModel.id == client_id,
        ClientModel.client_id == settings.CLIENT_ID
    ).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    for field, value in client_update.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    
    db.commit()
    db.refresh(client)
    return client


@router.delete("/{client_id}")
def delete_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """Delete a client"""
    client = db.query(ClientModel).filter(
        ClientModel.id == client_id,
        ClientModel.client_id == settings.CLIENT_ID
    ).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}
