import pandas as pd
from dotenv import load_dotenv
import os

from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain_groq import ChatGroq
from shoppinggpt.agent_toolkit.product_search import create_product_manager_chain

# Đường dẫn tới file .env
dotenv_path = 'E:/ShoppingGPT/packages/.env'
load_dotenv(dotenv_path)

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

def main():
    # Example data
    path = "E:\\ShoppingGPT\\packages\\shoppinggpt\\data\\products.csv"
    df = pd.read_csv(path)

    llm_chain = create_product_manager_chain(llm, df)

    result = llm_chain.invoke("Thông tin sản phẩm áo sơ mi")

    print("Result:", result)

if __name__ == "__main__":
    main()
