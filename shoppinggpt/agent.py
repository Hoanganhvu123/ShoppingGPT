from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from shoppinggpt.tool.product_search import product_search_tool
from shoppinggpt.tool.policy_search import policy_search_tool
from langchain.prompts import ChatPromptTemplate


class ShoppingAgent:
    def __init__(self, llm, shared_memory: ConversationBufferMemory):
        self.llm = llm
        self.verbose = False
        self.memory = shared_memory
        self.tools = [product_search_tool, policy_search_tool]
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent and helpful AI assistant for an online fashion store.
            Your task is to answer customer questions about products and store policies.
            Use the available tools to search for accurate information and provide appropriate answers.
                      
            Always use Vietnamese to communicate with customers."""),
            ("human", "{input}"),
            ("ai", "{agent_scratchpad}")
        ])

    def invoke(self, query: str) -> str:
        inputs = {
            "input": query,
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
