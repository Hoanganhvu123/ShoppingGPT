import os
from typing import List

from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from shoppinggpt.config import EMBEDDINGS, DATA_TEXT_PATH, STORE_DIRECTORY

class VectorStoreManager:
    def __init__(self, data_path: str, store_directory: str, embeddings):
        self.data_path = data_path
        self.store_directory = store_directory
        self.embeddings = embeddings
        self.vectorstore = self.load_or_create_vectorstore()

    def load_vectorstore(self):
        return FAISS.load_local(
            self.store_directory,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    def create_vectorstore(self):
        loader = TextLoader(self.data_path, encoding='utf8')
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
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
def policy_search_tool(query: str) -> List[str]:
    """
    Search for information related to company policies.

    Args:
        query (str): The search query to find information.

    Returns:
        List[str]: The search results as a list of text strings.
    """
    vector_store_manager = VectorStoreManager.create(
        DATA_TEXT_PATH,
        STORE_DIRECTORY,
        EMBEDDINGS
    )

    results = vector_store_manager.vectorstore.similarity_search(query, k=5)
    return [doc.page_content for doc in results]
