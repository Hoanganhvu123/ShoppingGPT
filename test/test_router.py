from typing import List, Dict
import numpy as np
from semantic_router import Route, RouteLayer
from semantic_router.encoders.tfidf import TfidfEncoder
from shoppinggpt.router.samples_for_consine_algo import PRODUCT_SAMPLE, CHITCHAT_SAMPLE

# Constants
PRODUCT_ROUTE_NAME = 'products'
CHITCHAT_ROUTE_NAME = 'chitchat'


class SemanticRouter:
    def __init__(self):
        self.embedding = TfidfEncoder(score_threshold=0.5)
        
        # Initialize the routes first
        self.product_route = Route(
            name=PRODUCT_ROUTE_NAME,
            utterances=PRODUCT_SAMPLE,
            score_threshold=0.5
        )
        self.chitchat_route = Route(
            name=CHITCHAT_ROUTE_NAME,
            utterances=CHITCHAT_SAMPLE,
            score_threshold=0.5
        )
        self.routes = [self.product_route, self.chitchat_route]
        
        # Now fit the TfidfEncoder with the routes
        self.embedding.fit(self.routes)

        self.route_layer = RouteLayer(encoder=self.embedding, routes=self.routes)

    def guide(self, query: str) -> str:
        result = self.route_layer(query)
        return result.name if result else "unknown"

def main():
    # Create an instance of SemanticRouter
    router = SemanticRouter()

    # Test queries
    test_queries = [
        "What's the price of this product?",
        "What's your favorite food?",
        "Does this product come in blue?",
        "The weather is beautiful today!",
        "Do you sell jackets in your store?",
        "Can you recommend a good movie?",
        "What's the return policy for this item?",
        "Do you have any vegetarian options?",
        "Are there any discounts on electronics?",
        "Can you show me the latest smartphone models?",
        "What's the shipping time for this product?",
        "Do you have this shirt in a larger size?"
    ]

    # Test the router with each query
    for query in test_queries:
        result = router.guide(query)
        print(f"Query: {query}")
        print(f"Route: {result}")
        print("---")

if __name__ == "__main__":
    main()