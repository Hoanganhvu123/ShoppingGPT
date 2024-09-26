import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from shoppinggpt.router.lib_semantic_router import (
    SemanticRouter,
    PRODUCT_ROUTE_NAME,
    CHITCHAT_ROUTE_NAME
)
from shoppinggpt.chain import create_chitchat_chain
from shoppinggpt.agent import ShoppingAgent
import numpy as np
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()
load_dotenv(r"E:\chatbot\ShoppingGPT\.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM and Embedding setup
# LLM = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash")
LLM = ChatGroq(temperature=0, model="gemma-7b-it")

# Memory setup
SHARED_MEMORY = ConversationBufferMemory(return_messages=True)

# Initialize SemanticRouter
SEMANTIC_ROUTER = SemanticRouter()


def handle_query(query: str) -> dict:
    """Handle user query and return response."""
    try:
        guided_route = SEMANTIC_ROUTER.guide(query)
        print(guided_route)
    except RuntimeWarning:
        # Handle the RuntimeWarning by setting a default route
        guided_route = CHITCHAT_ROUTE_NAME
    
    if guided_route == CHITCHAT_ROUTE_NAME:
        chitchat_chain = create_chitchat_chain(LLM, SHARED_MEMORY)
        response = chitchat_chain.invoke({"input": query})
    elif guided_route == PRODUCT_ROUTE_NAME:
        agent = ShoppingAgent(LLM, SHARED_MEMORY)
        response = agent.invoke(query)  # Pass query directly, not as a dict
    else:
        response = "have error"
    
    # Get content from response
    content = (
        response.content if hasattr(response, 'content')
        else response['output'] if isinstance(response, dict) and 'output' in response
        else str(response)
    )
    
    # Update shared memory
    SHARED_MEMORY.chat_memory.add_user_message(query)
    SHARED_MEMORY.chat_memory.add_ai_message(content)
    
    return {
        'response': content,
        'type': guided_route
    }


def main():
    """Main function to run the chat loop."""
    print("Welcome to the AI chat! Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Ending conversation. Goodbye!")
            break
        
        try:
            # Suppress the RuntimeWarning
            with np.errstate(invalid='ignore'):
                result = handle_query(user_input)
            print(f"AI ({result['type']}): {result['response']}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()