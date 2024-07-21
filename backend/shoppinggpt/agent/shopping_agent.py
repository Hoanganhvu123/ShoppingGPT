import os
from typing import Dict, Any, List
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain import hub
from langchain.memory import ConversationBufferWindowMemory

# from shoppinggpt.tool.product_search import ProductSearchTool
from shoppinggpt.tool.policy_search import PolicySearchTool
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Set environment variables
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
        self.human_input = ""

    @property
    def input_keys(self) -> List[str]:
        return ["query"]

    @property
    def output_keys(self) -> List[str]:
        return ["response"]

    def human_step(self, query: str) -> None:
        self.human_input = query
        self.memory.chat_memory.add_user_message(self.human_input)

    def agent_step(self):
        tools = [PolicySearchTool()]
        inputs = {
            "chat_history": self.memory.chat_memory.messages,
            "input": self.human_input,
        }
        prompt = hub.pull("hwchase17/openai-tools-agent")
        agent = create_tool_calling_agent(self.llm, tools, prompt)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=self.verbose,
            handle_parsing_errors=True,
        )

        ai_message = agent_executor.invoke(inputs)
        agent_output = ai_message['output']
        self.memory.chat_memory.add_ai_message(agent_output)
        return agent_output

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        query = inputs["query"]
        self.human_step(query)
        response = self.agent_step()
        return {"response": response}


# Initialize ShoppingGPT
llm = ChatGroq(temperature=0.5, model="llama3-70b-8192")
shopping_agent = ShoppingGPT(llm=llm, verbose=True)
