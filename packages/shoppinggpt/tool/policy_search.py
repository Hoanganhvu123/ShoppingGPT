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
from shoppinggpt.agent.prompt import shopping_assistant_prompt 


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


class DocumentProcessor:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def load_and_process_documents(self):
        """Load documents, split into chunks, create embeddings, and store in Pinecone."""
        loader = TextLoader(self.data_path, encoding='utf8')
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
        document_chunks = text_splitter.split_documents(documents)
        vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
        vectorstore.add_documents(document_chunks)
        print(f"Successfully indexed {len(document_chunks)} document chunks into Pinecone.")


class PolicySearchInput(BaseModel): 
    query: str = Field(description="Search policy documents and return relevant information.")



class PolicySearchTool(StructuredTool):
    name: str = "policy_search"
    args_schema: Type[BaseModel] = PolicySearchInput

    def _run(self, query: str) -> Union[List[Dict], str]:
        vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={'k': 5})
        try:
            result = retriever.invoke(query)
            return result
        except Exception as e:
            return repr(e)



# if __name__ == "__main__":
    # processor = DocumentProcessor(data_path=r"E:\ShoppingGPT\packages\shoppinggpt\data\policy.txt")
    # processor.load_and_process_documents()

    # policy_tool = PolicySearchTool()
    # search_query = "Return policy"
    # results = policy_tool._run(search_query)
    # print(results)

    # tools = [PolicySearchTool()]
    # prompt = hub.pull("hwchase17/openai-tools-agent")
    # llm = ChatGroq(temperature=0, model="llama3-70b-8192")
    # agent = create_tool_calling_agent(llm, tools, prompt)
    # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_error = True)
    # a = agent_executor.invoke({"input": "Làm cách nào để tôi hủy đơn hàng?, hãy trả lời bằng tiếng việt"})
    # print(a['output'])