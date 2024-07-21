from sqlalchemy import create_engine
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.cart import Cart
from app.models.review import Review
from app.db.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Tạo tất cả các bảng trong cơ sở dữ liệu
Base.metadata.create_all(bind=engine)
