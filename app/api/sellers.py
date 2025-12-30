from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Seller as SellerModel
from app.schemas.schemas import Seller, SellerCreate, SellerUpdate
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[Seller])
def list_sellers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all sellers"""
    sellers = db.query(SellerModel).filter(
        SellerModel.client_id == settings.CLIENT_ID
    ).offset(skip).limit(limit).all()
    return sellers


@router.post("/", response_model=Seller)
def create_seller(
    seller: SellerCreate,
    db: Session = Depends(get_db)
):
    """Create a new seller"""
    db_seller = SellerModel(
        **seller.model_dump(),
        client_id=settings.CLIENT_ID
    )
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller


@router.get("/{seller_id}", response_model=Seller)
def get_seller(
    seller_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific seller by ID"""
    seller = db.query(SellerModel).filter(
        SellerModel.id == seller_id,
        SellerModel.client_id == settings.CLIENT_ID
    ).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller


@router.put("/{seller_id}", response_model=Seller)
def update_seller(
    seller_id: int,
    seller_update: SellerUpdate,
    db: Session = Depends(get_db)
):
    """Update a seller"""
    seller = db.query(SellerModel).filter(
        SellerModel.id == seller_id,
        SellerModel.client_id == settings.CLIENT_ID
    ).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    for field, value in seller_update.model_dump(exclude_unset=True).items():
        setattr(seller, field, value)
    
    db.commit()
    db.refresh(seller)
    return seller


@router.delete("/{seller_id}")
def delete_seller(
    seller_id: int,
    db: Session = Depends(get_db)
):
    """Delete a seller"""
    seller = db.query(SellerModel).filter(
        SellerModel.id == seller_id,
        SellerModel.client_id == settings.CLIENT_ID
    ).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    db.delete(seller)
    db.commit()
    return {"message": "Seller deleted successfully"}
