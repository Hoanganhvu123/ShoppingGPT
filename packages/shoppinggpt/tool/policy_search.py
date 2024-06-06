import os
from langchain_community.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

class DocumentProcessor:
    def __init__(self, data_path, vectorstore_path):
        self.data_path = data_path
        self.vectorstore_path = vectorstore_path

    def load_and_process_documents(self):
        """
        Load documents from the specified text file, split them into chunks, 
        create embeddings and store in FAISS.
        """
        loader = TextLoader(self.data_path, encoding='utf8')
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100, chunk_overlap=20, separators=[" ", ",", "\n"]
        )
        document_chunks = text_splitter.split_documents(documents)
        
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        vectorstore = FAISS.from_documents(document_chunks, embeddings)
        vectorstore.save_local(self.vectorstore_path)


def retrieve_data(query, top_k=5):
    """
    Check if the FAISS vector store exists. If not, process the data and create it.
    Then create a retriever and get top-K results.
    """
    data_path = "E:\\ShoppingGPT\\packages\\shoppinggpt\\data\\policy.txt"
    vectorstore_folder = "E:\\ShoppingGPT\\packages\\shoppinggpt\\data\\datastore"
    vectorstore_pkl_path = os.path.join(vectorstore_folder, "vectorstore.pkl")

    if not os.path.exists(vectorstore_pkl_path):
        processor = DocumentProcessor(data_path, vectorstore_folder)
        processor.load_and_process_documents()
    
    vectorstore = FAISS.load_local(
        vectorstore_folder, 
        GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_document"), 
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={'k': top_k}
    )
    results = retriever.invoke(query)
    return results

def get_tool():
    tools = [
        Tool(
                name="ProductSearch",
                func=lambda query: retrieve_data(query),
                description="Useful for when you need to answer questions about products related to shop policies",
        )   
    ]
    return tools


# policy_search_tool = Tool(
#     name="ProductSearch",
#     func=lambda query: retrieve_data(query),
#     description="Useful for when you need to answer questions about products related to shop policies",
# )

