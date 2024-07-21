from fastapi import APIRouter
from app.api.web.endpoints import users, products, orders, carts, reviews

web_router = APIRouter()
web_router.include_router(users.router, tags=["users"])
web_router.include_router(products.router, tags=["products"])
web_router.include_router(orders.router, tags=["orders"])
web_router.include_router(carts.router, tags=["carts"])
web_router.include_router(reviews.router, tags=["reviews"])
