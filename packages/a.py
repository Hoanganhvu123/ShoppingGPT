import os
from typing import Optional, Union, List, Dict, Type
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from dotenv import load_dotenv

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')

index_name = "doan"
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


class DocumentProcessor:
    def __init__(self, data_path: str, vectorstore_path: str):
        self.data_path = data_path
        self.vectorstore_path = vectorstore_path

    def load_and_process_documents(self):
        """Load documents, split into chunks, create embeddings, and store in Pinecone."""
        loader = TextLoader(self.data_path, encoding='utf8')
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100, chunk_overlap=20, separators=[" ", ",", "\n"]
        )
        document_chunks = text_splitter.split_documents(documents)

        vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
        vectorstore.index_documents(document_chunks)


class PolicySearchInput(BaseModel):
    """Input schema for PolicySearchTool."""
    query: str = Field(description="Search query for policy documents.")


class PolicySearchTool(StructuredTool):
    name: str = "policy_search"
    description: str = (
        "Useful for answering questions about shop policies. "
        "Input should be a search query. "
        "This tool searches policy documents and returns relevant information."
    )
    args_schema: Type[BaseModel] = PolicySearchInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[List[Dict], str]:
        try:
            vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={'k': 5}
            )
            result = retriever.invoke(query)
            return result
        except Exception as e:
            return repr(e)


# Test code
if __name__ == "__main__":
    processor = DocumentProcessor(data_path="E:\\ShoppingGPT\\packages\\shoppinggpt\\data\\policy.txt")
    processor.load_and_process_documents()

    policy_tool = PolicySearchTool()
    search_query = "Return policy"
    results = policy_tool._run(search_query)
    print(results)
