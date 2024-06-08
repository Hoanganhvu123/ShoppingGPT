import os
from typing import Dict, Any
import pandas as pd
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents.openai_functions_agent.base import (
    OpenAIFunctionsAgent,
    create_openai_functions_agent,
)
from langchain.agents import AgentExecutor  
from langchain import hub

from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents.react.agent import create_react_agent

from shoppinggpt.tool.product_search import ProductSearchTool
from shoppinggpt.tool.policy_search import PolicySearchTool
from shoppinggpt.agent.prompt import shopping_assistant_prompt
 
 
 
# Load environment variables
load_dotenv()
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_SMITH_API_KEY")
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')



class ShoppingGPT:
    def __init__(self, llm, verbose=False, **kwargs):
        self.llm = llm
        self.verbose = verbose

        self.memory = ConversationBufferWindowMemory()
        self.human_chat_memory = []
        

    def human_step(self) -> str:
        self.human_input = input("User: ")
        print(self.human_input)
        self.memory.chat_memory.add_user_message(self.human_input)
 
 
    def agent_step(self):
        tools = [ProductSearchTool(), PolicySearchTool()]
        inputs = {
            "chat_history": self.memory.chat_memory,
            "input": self.human_input,
        }
        agent = create_tool_calling_agent(self.llm, tools ,shopping_assistant_prompt)
        
        agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools , 
            verbose = True,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
            # max_iterations: 5, 
        )
        
        ai_message = agent_executor.invoke(inputs)
        agent_output = ai_message['output']
        self.memory.chat_memory.add_ai_message(agent_output)  
        print("AI : " + agent_output)
