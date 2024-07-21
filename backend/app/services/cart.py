from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.schemas.cart import CartCreate

def get_cart(db: Session, cart_id: int):
    return db.query(Cart).filter(Cart.id == cart_id).first()

def get_carts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cart).offset(skip).limit(limit).all()

def create_cart(db: Session, cart: CartCreate):
    db_cart = Cart(user_id=cart.user_id, product_id=cart.product_id, quantity=cart.quantity)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart
