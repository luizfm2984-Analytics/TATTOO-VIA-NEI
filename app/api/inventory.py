from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import InventoryEntry as InventoryEntryModel, Product as ProductModel
from app.schemas.schemas import InventoryEntry, InventoryEntryCreate
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[InventoryEntry])
def list_inventory_entries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all inventory entries"""
    entries = db.query(InventoryEntryModel).filter(
        InventoryEntryModel.client_id == settings.CLIENT_ID
    ).offset(skip).limit(limit).all()
    return entries


@router.post("/", response_model=InventoryEntry)
def create_inventory_entry(
    entry: InventoryEntryCreate,
    db: Session = Depends(get_db)
):
    """Create a new inventory entry"""
    # Verify product exists
    product = db.query(ProductModel).filter(
        ProductModel.id == entry.product_id,
        ProductModel.client_id == settings.CLIENT_ID
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Calculate total cost
    total_cost = entry.quantity * entry.unit_cost
    
    # Create inventory entry
    db_entry = InventoryEntryModel(
        **entry.model_dump(),
        client_id=settings.CLIENT_ID,
        total_cost=total_cost
    )
    db.add(db_entry)
    
    # Update product stock
    if entry.entry_type in ["purchase", "adjustment"]:
        product.stock_quantity += entry.quantity
    elif entry.entry_type == "return":
        product.stock_quantity -= entry.quantity
    
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.get("/{entry_id}", response_model=InventoryEntry)
def get_inventory_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific inventory entry by ID"""
    entry = db.query(InventoryEntryModel).filter(
        InventoryEntryModel.id == entry_id,
        InventoryEntryModel.client_id == settings.CLIENT_ID
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    return entry


@router.get("/product/{product_id}", response_model=List[InventoryEntry])
def get_product_inventory_history(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get inventory history for a specific product"""
    entries = db.query(InventoryEntryModel).filter(
        InventoryEntryModel.product_id == product_id,
        InventoryEntryModel.client_id == settings.CLIENT_ID
    ).all()
    return entries
