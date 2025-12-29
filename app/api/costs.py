from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Cost as CostModel
from app.schemas.schemas import Cost, CostCreate, CostUpdate
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[Cost])
def list_costs(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    """List all costs"""
    query = db.query(CostModel).filter(
        CostModel.client_id == settings.CLIENT_ID
    )
    
    if category:
        query = query.filter(CostModel.category == category)
    
    costs = query.offset(skip).limit(limit).all()
    return costs


@router.post("/", response_model=Cost)
def create_cost(
    cost: CostCreate,
    db: Session = Depends(get_db)
):
    """Create a new cost entry"""
    db_cost = CostModel(
        **cost.model_dump(),
        client_id=settings.CLIENT_ID
    )
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    return db_cost


@router.get("/{cost_id}", response_model=Cost)
def get_cost(
    cost_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific cost by ID"""
    cost = db.query(CostModel).filter(
        CostModel.id == cost_id,
        CostModel.client_id == settings.CLIENT_ID
    ).first()
    if not cost:
        raise HTTPException(status_code=404, detail="Cost not found")
    return cost


@router.put("/{cost_id}", response_model=Cost)
def update_cost(
    cost_id: int,
    cost_update: CostUpdate,
    db: Session = Depends(get_db)
):
    """Update a cost"""
    cost = db.query(CostModel).filter(
        CostModel.id == cost_id,
        CostModel.client_id == settings.CLIENT_ID
    ).first()
    if not cost:
        raise HTTPException(status_code=404, detail="Cost not found")
    
    for field, value in cost_update.model_dump(exclude_unset=True).items():
        setattr(cost, field, value)
    
    db.commit()
    db.refresh(cost)
    return cost


@router.delete("/{cost_id}")
def delete_cost(
    cost_id: int,
    db: Session = Depends(get_db)
):
    """Delete a cost"""
    cost = db.query(CostModel).filter(
        CostModel.id == cost_id,
        CostModel.client_id == settings.CLIENT_ID
    ).first()
    if not cost:
        raise HTTPException(status_code=404, detail="Cost not found")
    
    db.delete(cost)
    db.commit()
    return {"message": "Cost deleted successfully"}
