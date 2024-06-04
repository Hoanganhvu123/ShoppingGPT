import os
from typing import Dict, Any
import asyncio

from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain.agents import AgentExecutor, create_openai_functions_agent, create_react_agent
from langchain import hub
from langchain.prompts import ChatPromptTemplate 
from langchain_groq import Groq

 
# os.environ["LANGCHAIN_TRACING_V2"]="true"
# os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
# os.environ["LANGCHAIN_API_KEY"]="{YOUE_LANGSMITH_APIKEY}"
# os.environ["LANGCHAIN_PROJECT"]="{YOUR_LANSMITH_PROJECTNAME}"

class LeadGPT:
    def __init__(self, llm, verbose=False, **kwargs):
        self.llm = llm
        self.verbose = verbose
        self.data_path = "E:\\my-app\\packages\\leadgpt\\data\\Epacific.txt"
        self.vectorstore_path = "E:\\my-app\\packages\\leadgpt\\data\\vectorstore"
        
        self.current_stage_id = None 
        self.chat_memory = ChatMessageHistory()
        self.human_chat_memory = []
        
        self.lead_name = kwargs.get("lead_name", "lead_name")
        self.lead_role = kwargs.get("lead_role", "lead_role")
        self.company_name = kwargs.get("company_name", "company_name")
        self.company_business = kwargs.get("company_business", "company_business")
        self.product_catalog = kwargs.get("product_catalog", "product_catalog")
        self.company_values = kwargs.get("company_values", "company_values")
        self.conversation_purpose = kwargs.get("conversation_purpose", "conversation_purpose")
        self.conversation_type = kwargs.get("conversation_type", "conversation_type")
        self.language = kwargs.get("language", "language")
        

        
    def determine_conversation_stage(self) :   
        stage_analyzer_output = self.stage_analyzer_assistant.invoke(   
            input={
                "current_stage" : self.current_stage,
                "conversation_history": self.chat_memory.messages[-6:],
                "current_stage_id": self.current_stage_id,
                "customer_information": self.lead_summary_memory.buffer
            },
            return_only_outputs=False,
        )
        self.current_stage_id = stage_analyzer_output.get("text")
        print(self.current_stage_id)


    def human_step(self) -> str:
        human_input = input("User: ")
        self.chat_memory.add_user_message(human_input)
 
 
    async def agent_step(self):
        tools = get_tools(self.data_path, self.vectorstore_path)
        inputs = {
            "lead_name": self.lead_name,
            "lead_role": self.lead_role,
            "company_name": self.company_name,
            "company_business": self.company_business,
            "product_catalog" : self.product_catalog,
            "company_values": self.company_values,
            "conversation_purpose": self.conversation_purpose,
            "conversation_type": self.conversation_type,
            "language": self.language,
            "conversation_history": self.chat_memory.messages[-6:],
        }
        self.lead_agent = create_openai_functions_agent(self.llm, tools, lead_agent_prompt)
        agent_executor = AgentExecutor(
            agent=self.lead_agent,
            tools=tools,
            verbose=self.verbose,
            max_iterations=2
        )
        ai_message = agent_executor.invoke(inputs)
        agent_output = ai_message['output']
        self.chat_memory.add_ai_message(agent_output)  
        print(agent_output)

    
    async def update_customer_infor(self):
        """
        Update the customer information based on summary memory usage 
        """
        print()
        print(f"Previous_summary : {self.lead_summary_memory.buffer}" + "\n")
        self.lead_summary_memory.buffer = self.lead_summary_memory.predict_new_summary(self.chat_memory.messages[-4:],
                                                                                       self.lead_summary_memory.buffer)                                                                                                                                          
        print(f"Current Summary: {self.lead_summary_memory.buffer}" + "\n")
