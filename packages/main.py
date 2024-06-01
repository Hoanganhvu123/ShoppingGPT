import os
import json
import requests
import asyncio

from langchain.agents import AgentExecutor, create_openai_functions_agent, create_react_agent
from langchain.llms import OpenAI
from langchain.memory import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import Tool

class AirtableAgent:
    def __init__(self, base_id, table_id, api_key):
        self.base_id = base_id
        self.table_id = table_id
        self.api_key = api_key

    def fetch_airtable_data(self, url, params):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def load_all(self):
        url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_id}"
        params = {'pageSize': 100}
        all_records = []
        while True:
            data = self.fetch_airtable_data(url, params)
            all_records.extend(data.get('records', []))
            if 'offset' in data:
                params['offset'] = data['offset']
            else:
                break
        return [record['fields'] for record in all_records]

    def load_limit(self, limit):
        url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_id}"
        params = {'maxRecords': limit}
        data = self.fetch_airtable_data(url, params)
        return [record['fields'] for record in data.get('records', [])]

class BookingGPT:
    def __init__(self, llm, base_id, table_id, api_key, use_tools=True, verbose=False, **kwargs):
        self.llm = llm
        self.verbose = verbose
        self.use_tools = use_tools
        self.api_key = api_key
        self.base_id = base_id
        self.table_id = table_id
        self.current_stage_id = None
        
        self.chat_memory = ChatMessageHistory()
        self.human_chat_memory = []
        
        self.agent_name = kwargs.get("agent_name", "BookingGPT Agent")
        self.agent_role = kwargs.get("agent_role", "Assistant")
        
        self.airtable_agent = AirtableAgent(base_id, table_id, api_key)
        
    def fetch_data(self, query):
        if self.use_tools:
            data = self.airtable_agent.load_all()
        else:
            data = self.airtable_agent.load_limit(100)
        return data
    
    async def process_query(self, query):
        inputs = {
            "agent_name": self.agent_name,
            "agent_role": self.agent_role,
            "query": query,
            "conversation_history": self.chat_memory.messages[-6:]
        }

        if self.use_tools:
            tools = self.get_tools()
            self.booking_agent = create_openai_functions_agent(self.llm, tools)
            agent_executor = AgentExecutor(
                agent=self.booking_agent,
                tools=tools,
                verbose=self.verbose,
                max_iterations=2
            )
        else:
            self.booking_agent = create_react_agent(self.llm, "ReactAgentPrompt")
            agent_executor = AgentExecutor(
                agent=self.booking_agent,
                tools=[],
                verbose=self.verbose,
                max_iterations=2
            )

        ai_message = agent_executor.invoke(inputs)
        agent_output = ai_message['output']
        self.chat_memory.add_ai_message(agent_output)  
        print(agent_output)
        return agent_output
    
    def get_tools(self):
        tools = [
            Tool(
                name="AirtableDataFetch",
                func=lambda query: self.fetch_data(query),
                description="Fetch data from Airtable"
            )
        ]
        return tools

# Example usage
if __name__ == "__main__":
    llm = OpenAI(model_name="gpt-3.5-turbo")
    booking_gpt = BookingGPT(
        llm, 
        base_id="app11RobdGoX0YNsC", 
        table_id="tblJdmvbrgizbYICO", 
        api_key="your_airtable_api_key",
        use_tools=True,
        agent_name="Booking Assistant"
    )
    asyncio.run(booking_gpt.process_query("What are the available bookings for next week?"))
