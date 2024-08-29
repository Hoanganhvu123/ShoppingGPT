import os
import sqlite3
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Union, List, Dict

from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


load_dotenv(r"E:\chatbot\ShoppingGPT\.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


PRODUCT_RECOMMENDATION_PROMPT = """
    You are a chatbot assistant specializing in providing product information and
    recommendations using SQL queries.
    Your primary tasks are:

    Provide detailed information about a specific product based on user queries.
    Recommend relevant products to users based on their preferences and requirements.

    The database table 'products' contains the following columns about product information:

    product_code: A unique identifier for each product (TEXT)
    product_name: The name of the product (TEXT)
    material: The material composition of the product (TEXT)
    size: The available sizes of the product (TEXT)
    color: The available colors of the product (TEXT)
    brand: The brand that manufactures or sells the product (TEXT)
    gender: The product for target gender(e.g., male, female, unisex) (TEXT)
    stock_quantity: The quantity of the product available in stock (INTEGER)
    price: The price of the product (REAL)

    To provide product information or recommend products, generate an SQL query that:

    Handles product names in a case-insensitive manner and allows for partial matches.
    Retrieves all relevant columns of information about the requested product or filters products based on criteria.
    Uses efficient indexing and filtering techniques to retrieve data.
    Ensures SQL injection prevention by using parameterized queries.

    Output only the SQL query. Do not include any explanations, comments, quotation marks, or additional information. Only output the query itself.
    Start!
    Question: {input}
"""

class ProductDataLoader:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)

    def close(self):
        if self.conn:
            self.conn.close()

    def clean_sql_query(self, query: str) -> str:
        # Loại bỏ các ký tự backtick và từ khóa 'sql'
        return query.replace('```sql', '').replace('```', '').strip()

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cleaned_query = self.clean_sql_query(query)
        cursor.execute(cleaned_query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    
@tool
def product_search_tool(input: str) -> Union[List[Dict], str]:
    """
    Tìm kiếm thông tin liên quan tới sản phẩm và trả về các thông tin liên quan sử dụng SQLite.

    Args:
        input (str): Chuỗi tìm kiếm để tìm các sản phẩm.

    Returns:
        Union[List[Dict], str]: Kết quả tìm kiếm dưới dạng danh sách từ điển hoặc thông báo lỗi nếu có.
    """
    try:
        llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash")
        prompt = PromptTemplate(
            template=PRODUCT_RECOMMENDATION_PROMPT,
            input_variables=["input"]
        )
        product_data_loader = ProductDataLoader("E:\\chatbot\\ShoppingGPT\\data\\products.db")
        
        def execute_sql_query(query: str) -> List[Dict]:
            return product_data_loader.execute_query(query)
        
        # Construct the chain
        chain = (
            {"input": RunnablePassthrough()}
            | prompt
            | llm
            # | (lambda x: x.content)
            | (lambda x: execute_sql_query(x.content))
        )
        result = chain.invoke(input)
        return result
    except Exception as e:
        return repr(e)
    finally:
        if product_data_loader:  
            product_data_loader.close()



# def main():
#     query = "Tìm sản phẩm có màu đen"
#     result = product_search_tool(query) 
#     print(result)

# if __name__ == "__main__":
#     main()