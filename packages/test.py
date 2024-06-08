import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Union, List, Dict, Type

from langchain import hub
from langchain.tools import StructuredTool, Tool
from langchain.agents import AgentExecutor, create_structured_chat_agent, create_tool_calling_agent
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from shoppinggpt.agent.prompt import shopping_assistant_prompt 
import os
from dotenv import load_dotenv
from typing import Dict, Any, Type
from pydantic import BaseModel, Field

from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq
from langchain_experimental.tools.python.tool import PythonAstREPLTool
import pandas as pd
from langchain_core.runnables import RunnablePassthrough

from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain_core.tracers.langchain import wait_for_all_tracers
from langchain_core.tracers.base import BaseCallbackHandler

# Load environment variables

GOOGLE_API_KEY ='AIzaSyAG6-vbS8_CV5ydHQNpleDTl31Ok-M1dTA'
GROQ_API_KEY = "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"
LANGCHAIN_SMITH_API_KEY = "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"
AIRTABLE_API_KEY = "patY1JfzlJ4pNSLpE.ee148d7e13fe1ab596be93bee4345f0d4f470cf14019590bb31d24a83f4fca02"
AIRTABLE_BASE_ID = "appx0A1LC30SlBvD4"
AIRTABLE_TABLE_ID = "tbl5xb4OwcvojFjlI"
TAVILY_API_KEY = "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"
PINECONE_API_KEY = "dd4e82e0-a6ea-474f-a7dd-07a6dc1f3eb3"

# Load environment variables
load_dotenv()
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_SMITH_API_KEY")
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

index_name = "doan"
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

PRODUCT_RECOMMENDATION_PROMPT = """
    You are a chatbot assistant specializing in providing product information and r
    ecommendations using Pandas in Python.
    Your primary tasks are:

    Provide detailed information about a specific product based on user queries.
    Recommend relevant products to users based on their preferences and requirements.

    The dataframe df contains the following columns about product information:

    product_code: A unique identifier for each product (string)
    product_name: The name of the product (string)
    material: The material composition of the product (string)
    size: The available sizes of the product (string)
    color: The available colors of the product (string)
    brand: The brand that manufactures or sells the product (string)
    gender: The product for target gender(e.g., male, female, unisex) (string)
    stock_quantity: The quantity of the product available in stock (integer)
    price: The price of the product, which can be a string or numeric value (string or numeric)

    To provide product information, generate a Python command that:

    Handles product names in a case-insensitive manner and allows for partial matches.
    Retrieves all relevant columns of information about the requested product.
    Uses efficient indexing and filtering techniques to retrieve data.
    Converts string values to float for the 'price' column if necessary.
    Validates input to prevent potential errors.

    To recommend products, generate a Python command that:

    Filters products based on user-specified criteria such as price range, material, color, size, or brand.
    Handles multiple criteria combined with logical operators (and, or).
    Recommends a specified number of products that match the criteria.
    Ensures code readability and maintainability.

    Output only the Python command(s). Do not include any explanations, comments, quotation marks, or additional information. Only output the command(s) themselves.
    Start!
    Question: {input}
"""


class ProductSearchInput(BaseModel):
    input: str = Field(description="""Useful for when you need to answer questions about product information, 
                                    Please use Vietnamese input commands when using this tool.""")
    
class ProductSearchTool(StructuredTool):
    name: str = "product_search"
    args_schema: Type[BaseModel] = ProductSearchInput

    def _run(self, input: str) -> Any:
        llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
        prompt = PromptTemplate(
            template=PRODUCT_RECOMMENDATION_PROMPT,
            input_variables=["input"]
        )   
        product_data = pd.read_csv("E:\\ShoppingGPT\\packages\\shoppinggpt\\data\\products.csv")
        python_tool = PythonAstREPLTool(globals={"df": product_data})
        # Construct the chain
        chain = (
            {"input": RunnablePassthrough()} 
            | prompt 
            | llm
            # | (lambda x: print("Đầu ra LLM : " + x.content))
            # | (lambda x: print()) 
            | (lambda x: python_tool.invoke(x.content))
        )
        result = chain.invoke(input)
        return result



if __name__ == "__main__":
    # processor = DocumentProcessor(data_path=r"E:\ShoppingGPT\packages\shoppinggpt\data\policy.txt")
    # processor.load_and_process_documents()

    # policy_tool = PolicySearchTool()
    # search_query = "Return policy"
    # results = policy_tool._run(search_query)
    # print(results)

    tools = [ProductSearchTool()]
    prompt = hub.pull("hwchase17/openai-tools-agent")
    llm = ChatGroq(temperature=0.5, model="llama3-70b-8192")
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        andle_parsing_error = True,
        return_intermediate_steps = True
    )
    
    
    a = agent_executor.invoke({"input": "Có bao nhiêu sản phẩm có chất vải Denim, đó là những sản phẩm nào"})
    print(a['output'])