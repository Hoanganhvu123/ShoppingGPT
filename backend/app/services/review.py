from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate

def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Review).offset(skip).limit(limit).all()

def create_review(db: Session, review: ReviewCreate):
    db_review = Review(user_id=review.user_id, product_id=review.product_id, review_text=review.review_text, rating=review.rating)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
