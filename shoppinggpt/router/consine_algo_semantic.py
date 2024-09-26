from typing import List
import numpy as np
from shoppinggpt.config import EMBEDDINGS

PRODUCT_SAMPLE = [
    "how much does this dress cost", "what colors are available for this shirt",
    "is this pair of jeans in stock", "what clothing items do you have in your store",
    "can you show me some shoes", "do you have any discounts on winter coats",
    "what's the warranty on this jacket", "are there any new clothing arrivals this week",
    "do you offer free shipping on clothes", "can I return this sweater if it doesn't fit",
    "what's your best-selling clothing item", "do you have any eco-friendly clothing options",
    "are these t-shirts made locally", "can you gift wrap this scarf",
    "what's the difference between these two styles of pants",
    "do you have a loyalty program for frequent clothing shoppers",
    "what's the material of this blouse", "do you have this dress in a larger size",
    "are these shoes suitable for running", "what's your return policy for online purchases",
    "can you recommend a good winter jacket", "do you have any sales on summer dresses",
    "what's the care instructions for this silk shirt", "do you offer alterations for pants",
    "what accessories would go well with this outfit", "are these sunglasses polarized",
    "do you have any vegan leather options", "what's the difference between slim fit and regular fit",
    "do you have any petite sizes available", "what's the latest fashion trend in your store",
    "do you have any waterproof jackets", "what's the price range for your formal wear",
    "do you have any sustainable fashion lines", "can you help me find a dress for a wedding",
    "what's the fabric composition of these socks", "do you have any UV protection clothing",
    "what's your most comfortable brand of shoes", "do you offer gift cards for your store",
    "what's the warranty on your watches", "can you explain the different types of denim you offer"
]

CHITCHAT_SAMPLE = [
    "do you like watching movies", "what's your favorite food",
    "the sky is so blue today", "speak English, please. but keep it brief",
    "how's the weather where you are", "do you have any hobbies",
    "what's your opinion on artificial intelligence", "tell me a joke",
    "what's your favorite book", "do you believe in aliens",
    "if you could travel anywhere, where would you go", "what's the meaning of life",
    "do you have any pets", "what's your favorite music genre",
    "if you could have any superpower, what would it be",
    "what's the best advice you've ever received", "how was your day",
    "do you dream when you sleep", "what's your favorite season",
    "if you could meet any historical figure, who would it be",
    "what's your favorite holiday", "do you believe in ghosts",
    "what's your idea of a perfect day", "if you could learn any skill instantly, what would it be",
    "what's your favorite type of cuisine", "do you have any phobias",
    "what's your favorite childhood memory", "if you could time travel, which era would you visit",
    "what's your favorite sport to watch", "do you prefer mountains or beaches",
    "what's your favorite board game", "if you could be any animal, what would you choose",
    "what's your go-to karaoke song", "do you believe in love at first sight",
    "what's your favorite way to relax", "if you could have dinner with anyone, who would it be",
    "what's your favorite ice cream flavor", "do you have any hidden talents",
    "what's your favorite quote", "if you won the lottery, what's the first thing you'd buy"
]

# Constants
PRODUCT_ROUTE_NAME = 'products'
CHITCHAT_ROUTE_NAME = 'chitchat'


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
