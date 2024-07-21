from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ShoppingGPT"
    PROJECT_VERSION: str = "1.0.0"
    WEB_API_STR: str = "/api/web/endpoints"
    AI_API_STR: str = "/api/ai/endpoints"
    DATABASE_URL: str = "sqlite:///./test.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    ALLOWED_HOSTS: list[str] = ["*"]
    
    # GOOGLE_API_KEY: str
    # GROQ_API_KEY: str
    # LANGCHAIN_SMITH_API_KEY: str
    # AIRTABLE_API_KEY: str
    # AIRTABLE_BASE_ID: str
    # AIRTABLE_TABLE_ID: str
    # TAVILY_API_KEY: str
    # PINECONE_API_KEY: str

    # class Config:
    #     env_file = "E:\\chatbot\\ShoppingGPT\\backend\\app\\core\\.env"

settings = Settings()
