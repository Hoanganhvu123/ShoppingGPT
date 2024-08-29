import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Union, List, Dict, Type
from langchain import hub
from langchain.tools import StructuredTool
from langchain.agents import AgentExecutor, create_structured_chat_agent, create_tool_calling_agent
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
import pickle
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

# Load environment variables
load_dotenv(r"E:\chatbot\ShoppingGPT\.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

class VectorStoreManager:
    def __init__(self, data_path: str, store_directory: str, embeddings):
        self.data_path = data_path
        self.store_directory = store_directory
        self.embeddings = embeddings
        self.vectorstore = self.load_or_create_vectorstore()
                  
    def load_vectorstore(self):
        return FAISS.load_local(self.store_directory, self.embeddings, allow_dangerous_deserialization=True)
    
    def create_vectorstore(self):
        loader = TextLoader(self.data_path, encoding='utf8')
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        document_chunks = text_splitter.split_documents(documents)
        
        vectorstore = FAISS.from_documents(document_chunks, self.embeddings)
        vectorstore.save_local(self.store_directory)
        return vectorstore
    
    def check_existing_vectorstore(self):
        return os.path.exists(os.path.join(self.store_directory, "index.faiss"))
    
    def load_or_create_vectorstore(self):
        if self.check_existing_vectorstore():
            return self.load_vectorstore()
        else:
            return self.create_vectorstore()
    
    @staticmethod
    def create(data_path: str, store_directory: str, embeddings):
        return VectorStoreManager(data_path, store_directory, embeddings)

@tool
def policy_search_tool(query: str) -> str:
    """
    Tìm kiếm thông tin liên quan tới chính sách công ty, các chính sách vận chuyển, đổi trả hàng, bảo hành, bảo mật thông tin khách hàng
    
    Args:
        query (str): Câu truy vấn để tìm kiếm thông tin.
    
    Returns:
        str: Kết quả tìm kiếm dưới dạng chuỗi văn bản.
    """
    data_path = r"E:\chatbot\ShoppingGPT\data\policy.txt"
    store_directory = r"E:\chatbot\ShoppingGPT\data\datastore"
    vector_store_manager = VectorStoreManager.create(data_path, store_directory, embeddings)
    
    results = vector_store_manager.vectorstore.similarity_search(query, k=5)
    
    return results

# def main():
#     query = "chính sách đổi trả hàng"
#     result = search_vectorstore(query) 
#     print(result)

# if __name__ == "__main__":
#     main()