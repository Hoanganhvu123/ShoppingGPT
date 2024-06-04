from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq
from langchain_experimental.tools.python.tool import PythonAstREPLTool
import pandas as pd
from langchain_core.runnables import RunnablePassthrough

PRODUCT_MANAGER_PROMPT = """
You are a data scientist specializing in product data analysis using Pandas in Python. 
Your task is to generate a single Python command to retrieve all information about a specific product
based on user queries.

The dataframe `df` contains the following columns:

- `product_code`: A unique identifier for each product (string)
- `product_name`: The name of the product (string)
- `material`: The material composition of the product (string)
- `size`: The size of the product (string)
- `color`: The color of the product (string)
- `brand`: The brand that manufactures or sells the product (string)
- `gender`: The target gender for the product (e.g., male, female, unisex) (string)
- `stock_quantity`: The quantity of the product available in stock (integer)
- `price`: The price of the product, which can be a string or numeric value (string or numeric)

Your Python command should:

1. Handle product names in a case-insensitive manner and allow for partial matches.
2. Retrieve all relevant columns of information about the requested product.
3. Use efficient indexing and filtering techniques to retrieve data.
4. Convert string values to float for the 'price' column if necessary.
5. Ensure code readability and maintainability.
6. Validate input to prevent potential errors.

Output only the Python command. Do not include any explanations, comments, quotation marks, or additional information. Only output the command itself.

Start!
Question: {input}
"""






def create_product_manager_chain(
    llm: ChatGroq,
    product: pd.DataFrame
) -> RunnableSequence:
    """Construct a product manager chain from an LLM and dataframe."""

    prompt = PromptTemplate(
        template=PRODUCT_MANAGER_PROMPT,
        input_variables=["input"]
    )   
    python_tool = PythonAstREPLTool(globals={"df": product})

    # Construct the chain
    chain = (
        {"input": RunnablePassthrough()} 
        | prompt 
        | llm
        # | (lambda x: print("Đầu ra LLM : " + x.content))
        
        # | (lambda x: print())
        
        | (lambda x: python_tool.invoke(x.content))
    )
    return chain
