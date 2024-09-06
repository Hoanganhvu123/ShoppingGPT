from typing import List
import numpy as np
from config import EMBEDDINGS

# Constants
PRODUCT_ROUTE_NAME = 'products'
CHITCHAT_ROUTE_NAME = 'chitchat'

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
    "nói tiếng việt đi bạn ơi. mà nói ít thôi"
]


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class SemanticRouter:
    def __init__(self):
        self.product_prompts = PRODUCT_SAMPLE
        self.chitchat_prompts = CHITCHAT_SAMPLE
        self.embedding = EMBEDDINGS
        self.product_embeddings = [
            self.embedding.embed_query(prompt) for prompt in self.product_prompts
        ]
        self.chitchat_embeddings = [
            self.embedding.embed_query(prompt) for prompt in self.chitchat_prompts
        ]

    def guide(self, query: str) -> str:
        query_embedding = self.embedding.embed_query(query)

        product_similarities = [
            cosine_similarity(query_embedding, prod_emb)
            for prod_emb in self.product_embeddings
        ]
        chitchat_similarities = [
            cosine_similarity(query_embedding, chat_emb)
            for chat_emb in self.chitchat_embeddings
        ]

        max_product_similarity = max(product_similarities)
        max_chitchat_similarity = max(chitchat_similarities)

        if max_product_similarity > max_chitchat_similarity:
            return PRODUCT_ROUTE_NAME
        elif max_chitchat_similarity > max_product_similarity:
            return CHITCHAT_ROUTE_NAME
        else:
            return "unknown"
