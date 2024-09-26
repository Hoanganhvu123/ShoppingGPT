# config.py
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv(r"E:\chatbot\ShoppingGPT\.env")

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Paths
DATA_PRODUCT_PATH = r"E:\chatbot\ShoppingGPT\data\products.db"
DATA_TEXT_PATH = r"E:\chatbot\ShoppingGPT\data\policy.txt"
STORE_DIRECTORY = r"E:\chatbot\ShoppingGPT\data\datastore"

# Embeddings
load_dotenv(r"E:\chatbot\ShoppingGPT\.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDINGS = GoogleGenerativeAIEmbeddings(model="models/embedding-001")