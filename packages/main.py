import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from shoppinggpt.agent.shopping_agent import ShoppingGPT

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_SMITH_API_KEY")
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
#------------------------------------------------------------------------



def main():
    llm = ChatGroq(temperature=0.5, model="llama3-70b-8192")
    
    lead = ShoppingGPT(
        llm = llm,
        verbose = False,
    )
    
    
    while True:
        lead.human_step()
        lead.agent_step()


#Run main loop
if __name__ == "__main__":
    main()