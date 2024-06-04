from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq
from langchain_experimental.tools.python.tool import PythonAstREPLTool
import pandas as pd


PRODUCT_MANAGER_PROMPT = """
You are an intelligent agent specializing in providing product information and recommendations 
to customers using a pandas dataframe in Python. Your task is to generate efficient and accurate 
Python commands to retrieve and analyze product data from the dataframe `df` based on customer queries. 
Generate only the Python command(s), without any additional explanation or text.

The dataframe `df` contains the following columns:

Index(['product_code', 'product_name', 'material', 'size', 'color', 'brand',
'gender', 'stock_quantity', 'price'], dtype='object')

- product_code: string product code
- product_name: string product name
- material: string product material
- size: string product size (S, M, L, XL, etc.)
- color: string product color
- brand: string brand name
- gender: string target customer gender (men/women/unisex)
- stock_quantity: integer stock quantity
- price: string or numeric product price (may contain currency symbol)

Your Python command(s) should:
1. Retrieve all relevant information for the mentioned product(s).
2. Handle case-insensitive product names and partial matches.
3. Use appropriate indexing and filtering techniques for efficient data retrieval.
4. Avoid unnecessary computations or data transformations.
5. Optimize for performance with large datasets.
6. Ensure code readability and maintainability.
7. Validate input to prevent potential errors.
8. Convert string values to float where necessary, especially for the 'price' column.
9. Provide recommendations for similar or complementary products if applicable.
10. Ensure all brackets and parentheses are correctly closed.

Start!
Question: {input}
"""




def create_product_manager_chain(
    llm: ChatGroq,
    product: pd.DataFrame
) -> RunnableSequence:
    """Construct a product manager chain from an LLM and dataframe."""

    # Create the prompt template with verbose
    prompt = PromptTemplate(template=PRODUCT_MANAGER_PROMPT, input_variables=["input"])

    # Initialize the PythonAstREPLTool with the provided dataframe and verbose
    python_tool = PythonAstREPLTool(globals={"df": product})

    # Construct the chain
    chain = (
        prompt 
        | llm
        | (lambda x: python_tool.invoke(x.content))
    )
    return chain
