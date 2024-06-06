import os
from typing import Dict, Any

from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq
from langchain_experimental.tools.python.tool import PythonAstREPLTool
import pandas as pd
from langchain_core.runnables import RunnablePassthrough

from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain_core.tracers.langchain import wait_for_all_tracers
from langchain_core.tracers.base import BaseCallbackHandler


os.environ["LANGCHAIN_TRACING"] = "true"
os.environ["LANGCHAIN_SESSION"] = "agent_workflow"



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


def create_product_manager_toolkit(input: Dict[str, Any]) -> Any:
    """Construct a product manager chain from an LLM and dataframe."""

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
    try:
        result = chain.invoke(input)
    finally:
        wait_for_all_tracers()
    return result


product_search_tool =  StructuredTool.from_function(
            name = "ProductSearch",
            func = create_product_manager_toolkit,
            description="Useful for when you need to answer questions about product information",
        )
