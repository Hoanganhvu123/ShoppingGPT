from typing import List, Dict
import numpy as np
from semantic_router import Route, RouteLayer
from semantic_router.encoders.tfidf import TfidfEncoder

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


class SemanticRouter:
    def __init__(self):
        self.embedding = TfidfEncoder()
        
        # Initialize the routes first
        self.product_route = Route(
            name=PRODUCT_ROUTE_NAME,
            utterances=PRODUCT_SAMPLE,
        )
        self.chitchat_route = Route(
            name=CHITCHAT_ROUTE_NAME,
            utterances=CHITCHAT_SAMPLE,
        )
        self.routes = [self.product_route, self.chitchat_route]
        
        # Now fit the TfidfEncoder with the routes
        self.embedding.fit(self.routes)

        self.route_layer = RouteLayer(encoder=self.embedding, routes=self.routes)

    def similarity(self, query: str, route: Route) -> float:
        # Calculate similarity between query and route
        # Using the transform method instead of encode
        query_embedding = self.embedding.transform([query])[0]
        route_embedding = self.embedding.transform(route.utterances)
        return np.mean(np.dot(query_embedding, route_embedding.T))

    def guide(self, query: str) -> str:
        # Use the route_layer to determine the best route
        best_route = self.route_layer(query)
        return best_route.name if best_route else CHITCHAT_ROUTE_NAME
