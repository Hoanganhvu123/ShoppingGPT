from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cart import Cart, CartCreate
from app.services.cart import get_cart, get_carts, create_cart
from app.db.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/carts/", response_model=Cart)
def create_new_cart(cart: CartCreate, db: Session = Depends(get_db)):
    return create_cart(db=db, cart=cart)

@router.get("/carts/{cart_id}", response_model=Cart)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = get_cart(db, cart_id=cart_id)
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart

@router.get("/carts/", response_model=list[Cart])
def read_carts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    carts = get_carts(db, skip=skip, limit=limit)
    return carts
