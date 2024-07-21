from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import Base, engine
from app.api.web.router import web_router
from app.api.chatbot.router import ai_router  # Đảm bảo import đúng

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="RESTful API for ShoppingGPT using FastAPI",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "web", "description": "Web related operations"},
        {"name": "chatbot", "description": "Chatbot related operations"},
        {"name": "api", "description": "General API operations"}
    ],
)

# Set CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(web_router, prefix=settings.WEB_API_STR)
app.include_router(ai_router, prefix="/api/chatbot", tags=["chatbot"])  # Include chatbot router

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to ShoppingGPT API!"}

# Run the application with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
