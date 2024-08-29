import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent

from langchain.memory import ConversationBufferMemory
from shoppinggpt.tool.product_search import product_search_tool
from shoppinggpt.tool.policy_search import policy_search_tool
from langchain.prompts import ChatPromptTemplate
from langchain import hub

load_dotenv(r"E:\chatbot\ShoppingGPT\.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash")

class ShoppingAgent:
    def __init__(self, llm, shared_memory: ConversationBufferMemory, verbose: bool = False):
        self.llm = llm
        self.verbose = verbose
        self.memory = shared_memory
        self.tools = [product_search_tool, policy_search_tool]
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent and helpful AI assistant for an online fashion store.
            Your task is to answer customer questions about products and store policies.
            Use the available tools to search for accurate information and provide appropriate answers.
            
            Tools you can use:
            {tools}
            
            Always use Vietnamese to communicate with customers."""),
            ("human", "{input}"),
            ("ai", "{agent_scratchpad}")
        ])

    def invoke(self, query: str) -> str:
        inputs = {
            "input": query,
            "tools": "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
        }
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.verbose,
            handle_parsing_errors=True,
            memory=self.memory
        )
        ai_message = agent_executor.invoke(inputs)
        agent_output = ai_message['output']
        return agent_output
    

def main():
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash")
    agent = ShoppingAgent(llm=llm, verbose=True)
    user_input = "cho tôi giá sản phẩm quần tây"
    # user_input = "chính sách đổi trả hàng"
    response = agent.invoke(user_input)
    print(f"AI: {response}")


if __name__ == '__main__':
    main()