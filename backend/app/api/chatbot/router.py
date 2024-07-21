import logging
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict
from shoppinggpt.agent.shopping_agent import ShoppingGPT, llm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShoppingInput(BaseModel):
    query: str = Field(..., description="The shopping query or request from the user")

class ShoppingOutput(BaseModel):
    response: str = Field(..., description="The response from the ShoppingGPT agent")

shopping_agent = ShoppingGPT(llm=llm, verbose=False)

ai_router = APIRouter()

@ai_router.post("/ai_chatbot", response_model=ShoppingOutput, tags=["chatbot"])
async def shopping(input: ShoppingInput):
    try:
        logger.info(f"Received query: {input.query}")
        result = shopping_agent._call({"query": input.query})
        logger.info(f"Generated response: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
