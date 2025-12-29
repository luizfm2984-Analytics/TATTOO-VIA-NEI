from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Sale as SaleModel, SaleItem as SaleItemModel, Product as ProductModel
from app.schemas.schemas import Sale, SaleCreate
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[Sale])
def list_sales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all sales"""
    sales = db.query(SaleModel).filter(
        SaleModel.client_id == settings.CLIENT_ID
    ).offset(skip).limit(limit).all()
    return sales


@router.post("/", response_model=Sale)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db)
):
    """Create a new sale"""
    # Calculate totals
    total_amount = 0
    sale_items = []
    
    for item in sale.items:
        # Get product to verify and update stock
        product = db.query(ProductModel).filter(
            ProductModel.id == item.product_id,
            ProductModel.client_id == settings.CLIENT_ID
        ).first()
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product {product.name}"
            )
        
        subtotal = item.quantity * item.unit_price
        total_amount += subtotal
        
        sale_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "subtotal": subtotal
        })
    
    final_amount = total_amount - sale.discount
    
    # Create sale
    db_sale = SaleModel(
        client_id=settings.CLIENT_ID,
        customer_id=sale.customer_id,
        seller_id=sale.seller_id,
        total_amount=total_amount,
        discount=sale.discount,
        final_amount=final_amount,
        payment_method=sale.payment_method,
        status=sale.status,
        notes=sale.notes
    )
    db.add(db_sale)
    db.flush()  # Get the sale ID
    
    # Create sale items and update stock
    for item_data in sale_items:
        sale_item = SaleItemModel(
            sale_id=db_sale.id,
            **item_data
        )
        db.add(sale_item)
        
        # Update product stock
        product = db.query(ProductModel).filter(
            ProductModel.id == item_data["product_id"]
        ).first()
        product.stock_quantity -= item_data["quantity"]
    
    db.commit()
    db.refresh(db_sale)
    return db_sale


@router.get("/{sale_id}", response_model=Sale)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific sale by ID"""
    sale = db.query(SaleModel).filter(
        SaleModel.id == sale_id,
        SaleModel.client_id == settings.CLIENT_ID
    ).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.delete("/{sale_id}")
def cancel_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):
    """Cancel a sale and restore stock"""
    sale = db.query(SaleModel).filter(
        SaleModel.id == sale_id,
        SaleModel.client_id == settings.CLIENT_ID
    ).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Restore stock for each item
    for item in sale.items:
        product = db.query(ProductModel).filter(
            ProductModel.id == item.product_id
        ).first()
        if product:
            product.stock_quantity += item.quantity
    
    # Mark sale as cancelled
    sale.status = "cancelled"
    db.commit()
    
    return {"message": "Sale cancelled and stock restored"}
