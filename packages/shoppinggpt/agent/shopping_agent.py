import os
from typing import Dict, Any
import pandas as pd

from langchain.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain.agents.openai_functions_agent.base import (
    OpenAIFunctionsAgent,
    create_openai_functions_agent,
)
from langchain.agents import AgentExecutor  

from langchain.memory.buffer_window import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import ChatMessageHistory


from shoppinggpt.tool.product_search import product_search_tool
from shoppinggpt.tool.policy_search import get_tool
from shoppinggpt.agent.prompt import shopping_assistant_prompt
 
# os.environ["LANGCHAIN_TRACING_V2"]="true"
# os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
# os.environ["LANGCHAIN_API_KEY"]="{YOUE_LANGSMITH_APIKEY}"
# os.environ["LANGCHAIN_PROJECT"]="{YOUR_LANSMITH_PROJECTNAME}"


class ShoppingGPT:
    def __init__(self, llm, verbose=False, **kwargs):
        self.llm = llm
        self.verbose = verbose
        
        self.chat_memory = ChatMessageHistory()
        self.memory = ConversationBufferWindowMemory()
        self.human_chat_memory = []
        

    def human_step(self) -> str:
        human_input = input("User: ")
        self.chat_memory.add_user_message(human_input)
 
 
    def agent_step(self):
        # tools = [product_search_tool]
        tools = get_tool()
        inputs = {
            "conversation_history": self.chat_memory.messages[-6:],
        }
        self.lead_agent = create_openai_functions_agent(self.llm, tools, shopping_assistant_prompt)
        agent_executor = AgentExecutor(
            agent=self.lead_agent,
            tools=tools,
            verbose=self.verbose,
            max_iterations=5
        )
        ai_message = agent_executor.invoke(inputs)
        agent_output = ai_message['output']
        self.chat_memory.add_ai_message(agent_output)  
        print("AI : " + agent_output)
