from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Product as ProductModel
from app.schemas.schemas import Product, ProductCreate, ProductUpdate
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[Product])
def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all products"""
    products = db.query(ProductModel).filter(
        ProductModel.client_id == settings.CLIENT_ID
    ).offset(skip).limit(limit).all()
    return products


@router.post("/", response_model=Product)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product"""
    # Calculate margin
    margin = ((product.unit_price - product.cost_price) / product.cost_price * 100) if product.cost_price > 0 else 0
    
    db_product = ProductModel(
        **product.model_dump(),
        client_id=settings.CLIENT_ID,
        margin=margin
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific product by ID"""
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id,
        ProductModel.client_id == settings.CLIENT_ID
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id,
        ProductModel.client_id == settings.CLIENT_ID
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    # Recalculate margin if prices changed
    if 'unit_price' in update_data or 'cost_price' in update_data:
        if product.cost_price > 0:
            product.margin = (product.unit_price - product.cost_price) / product.cost_price * 100
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product"""
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id,
        ProductModel.client_id == settings.CLIENT_ID
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
