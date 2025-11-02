from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Sweet, User
from app.schemas import (
    SweetCreate,
    SweetUpdate,
    SweetResponse,
    PurchaseRequest,
    RestockRequest
)
from app.auth import get_current_active_user, get_admin_user

router = APIRouter(prefix="/api/sweets", tags=["sweets"])

@router.post("", response_model=SweetResponse, status_code=status.HTTP_201_CREATED)
def create_sweet(
    sweet_data: SweetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new sweet (requires authentication)"""
    new_sweet = Sweet(**sweet_data.dict())
    db.add(new_sweet)
    db.commit()
    db.refresh(new_sweet)
    return new_sweet

@router.get("", response_model=List[SweetResponse])
def get_all_sweets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all sweets (public endpoint)"""
    sweets = db.query(Sweet).offset(skip).limit(limit).all()
    return sweets

@router.get("/search", response_model=List[SweetResponse])
def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    """Search sweets by name, category, or price range"""
    query = db.query(Sweet)
    
    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))
    
    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))
    
    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)
    
    return query.all()

@router.get("/{sweet_id}", response_model=SweetResponse)
def get_sweet_by_id(sweet_id: int, db: Session = Depends(get_db)):
    """Get a specific sweet by ID"""
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sweet with id {sweet_id} not found"
        )
    return sweet

@router.put("/{sweet_id}", response_model=SweetResponse)
def update_sweet(
    sweet_id: int,
    sweet_data: SweetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a sweet's details (requires authentication)"""
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sweet with id {sweet_id} not found"
        )
    
    # Update only provided fields
    update_data = sweet_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sweet, field, value)
    
    db.commit()
    db.refresh(sweet)
    return sweet

@router.delete("/{sweet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Delete a sweet (Admin only)"""
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sweet with id {sweet_id} not found"
        )
    
    db.delete(sweet)
    db.commit()
    return None

@router.post("/{sweet_id}/purchase", response_model=dict)
def purchase_sweet(
    sweet_id: int,
    purchase_data: PurchaseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Purchase a sweet, decreasing its quantity (requires authentication)"""
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sweet with id {sweet_id} not found"
        )
    
    if sweet.quantity < purchase_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Only {sweet.quantity} items available"
        )
    
    sweet.quantity -= purchase_data.quantity
    db.commit()
    db.refresh(sweet)
    
    return {
        "message": "Purchase successful",
        "sweet_id": sweet.id,
        "sweet_name": sweet.name,
        "quantity_purchased": purchase_data.quantity,
        "remaining_stock": sweet.quantity
    }

@router.post("/{sweet_id}/restock", response_model=dict)
def restock_sweet(
    sweet_id: int,
    restock_data: RestockRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Restock a sweet, increasing its quantity (Admin only)"""
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sweet with id {sweet_id} not found"
        )
    
    sweet.quantity += restock_data.quantity
    db.commit()
    db.refresh(sweet)
    
    return {
        "message": "Restock successful",
        "sweet_id": sweet.id,
        "sweet_name": sweet.name,
        "quantity_added": restock_data.quantity,
        "new_stock": sweet.quantity
    }
