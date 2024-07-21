from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    review_text = Column(String)
    rating = Column(Integer)
