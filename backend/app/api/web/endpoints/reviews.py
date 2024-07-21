from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.review import Review, ReviewCreate
from app.services.review import get_review, get_reviews, create_review
from app.db.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/reviews/", response_model=Review)
def create_new_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return create_review(db=db, review=review)

@router.get("/reviews/{review_id}", response_model=Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@router.get("/reviews/", response_model=list[Review])
def read_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = get_reviews(db, skip=skip, limit=limit)
    return reviews
