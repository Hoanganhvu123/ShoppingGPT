import numpy as np
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List, Tuple

load_dotenv(r"E:\chatbot\ShoppingGPT\.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

class Route:
    def __init__(self, name: str, samples: List[str]):
        self.name = name
        self.samples = samples

class SemanticRouter:
    def __init__(self, embedding, routes: List[Route]):
        self.routes = routes
        self.embedding = embedding
        self.routesEmbedding = {}
        
        for route in self.routes:
            self.routesEmbedding[route.name] = self.embedding.embed_documents(route.samples)
    
    def get_routes(self) -> List[Route]:
        return self.routes
    
    def guide(self, query: str) -> Tuple[float, str]:
        queryEmbedding = np.array(self.embedding.embed_query(query))
        
        queryEmbedding = queryEmbedding / np.linalg.norm(queryEmbedding)
        scores = []
        
        for route in self.routes:
            routesEmbedding = np.array(self.routesEmbedding[route.name])
            routesEmbedding = routesEmbedding / np.linalg.norm(routesEmbedding, axis=1)[:, np.newaxis]
            score = np.mean(np.dot(routesEmbedding, queryEmbedding))
            scores.append((score, route.name))
        
        scores.sort(reverse=True)
        return scores[0]

