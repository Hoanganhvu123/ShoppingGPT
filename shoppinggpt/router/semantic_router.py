import os
from typing import List
from dotenv import load_dotenv

import numpy as np
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Set the Google API key
load_dotenv(r"E:\chatbot\ShoppingGPT\.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Constants
PRODUCT_ROUTE_NAME = 'products'
CHITCHAT_ROUTE_NAME = 'chitchat'
EMBEDDING = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

PRODUCT_SAMPLE = [
    "sản phẩm này giá bao nhiêu",
    "có màu gì cho sản phẩm này",
    "sản phẩm này còn hàng không",
    "bên cửa hàng bạn có những món đồ gì"
]
CHITCHAT_SAMPLE = [
    "bạn có thích xem phim không",
    "món ăn yêu thích của bạn là gì",
    "trời hôm nay xanh quá",
    "nói tieegs việt đi bạn ơi. mà nói ít thôi"
]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class SemanticRouter:
    def __init__(self):
        self.product_prompts = PRODUCT_SAMPLE 
        self.chitchat_prompts = CHITCHAT_SAMPLE
        self.embedding = EMBEDDING
        self.product_embeddings = [self.embedding.embed_query(prompt) for prompt in self.product_prompts]
        self.chitchat_embeddings = [self.embedding.embed_query(prompt) for prompt in self.chitchat_prompts]

    def guide(self, query: str) -> str:
        query_embedding = self.embedding.embed_query(query)

        product_similarities = [cosine_similarity(query_embedding, prod_emb) 
                                for prod_emb in self.product_embeddings]
        chitchat_similarities = [cosine_similarity(query_embedding, chat_emb) 
                                 for chat_emb in self.chitchat_embeddings]

        max_product_similarity = max(product_similarities)
        max_chitchat_similarity = max(chitchat_similarities)

        print(f"Highest value of product similarity: {max_product_similarity}")
        print(f"Highest value of chitchat similarity: {max_chitchat_similarity}")

        if max_product_similarity > max_chitchat_similarity:
            return PRODUCT_ROUTE_NAME
        elif max_chitchat_similarity > max_product_similarity:
            return CHITCHAT_ROUTE_NAME
        else:
            return "unknown"


# def main():
#     # Initialize SemanticRouter
#     router = SemanticRouter(EMBEDDING)
#     while True:
#         # Get user input
#         query = input("\nEnter your question: ")
        
#         if query.lower() == 'exit':
#             print("Thank you for using the system. Goodbye!")
#             break
        
#         # Use SemanticRouter to classify the question
#         result = router.guide(query)
        
#         # Print the result
#         if result == PRODUCT_ROUTE_NAME:
#             print(f"Your question is categorized as: Product")
#         elif result == CHITCHAT_ROUTE_NAME:
#             print(f"Your question is categorized as: Chitchat")
#         else:
#             print("Unable to determine the question type")

# if __name__ == "__main__":
#     main()
