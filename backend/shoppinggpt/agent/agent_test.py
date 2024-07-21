import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Set environment variables
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_SMITH_API_KEY")
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

def create_chain() -> LLMChain:
    # Initialize ChatGroq LLM
    llm = ChatGroq(api_key=os.getenv('GROQ_API_KEY'))
    
    # Create a prompt template
    prompt_template = PromptTemplate(
        input_variables=["input_text"],
        template="Bạn là một trợ lý ảo. Người dùng nói: {input_text}. Trả lời họ một cách chi tiết."
    )
    
    # Create LLMChain
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    return chain

def run_test_chain(input_text: str) -> Dict[str, Any]:
    chain = create_chain()
    result = chain.run({"input_text": input_text})
    return result

if __name__ == "__main__":
    input_text = "Tôi muốn tìm kiếm sản phẩm mới nhất."
    result = run_test_chain(input_text)
    print(result)
