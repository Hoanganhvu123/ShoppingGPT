from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough

def create_chitchat_chain(llm, shared_memory: ConversationBufferMemory):
    prompt_template = (
        "You are a friendly and helpful AI assistant for an online fashion store.\n"
        "Your task is to chat with customers in a friendly manner, while trying to steer "
        "the conversation towards fashion when possible.\n\n"
        "Chat history:\n"
        "{history}\n"
        "User: {input}\n"
        "AI: "
    )

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=prompt_template
    )

    chain = (
        RunnablePassthrough.assign(
            history=lambda _: shared_memory.load_memory_variables({})["history"]
        )
        | prompt
        | llm
    )

    return chain

def main():
    from dotenv import load_dotenv
    import os
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.memory import ConversationBufferMemory
    from shoppinggpt.chain import create_chitchat_chain
    from langchain_groq import ChatGroq


    load_dotenv(r"E:\chatbot\ShoppingGPT\.env")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(temperature=0, model="mixtral-8x7b-32768")
    # llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash")

    # Initialize shared memory
    shared_memory = ConversationBufferMemory(return_messages=True)
    chitchat_chain = create_chitchat_chain(llm, shared_memory)

    # Test conversation
    query = "ngày hôm này đẹp quá"

    chitchat_chain = create_chitchat_chain(llm, shared_memory)
    response = chitchat_chain.invoke({"input": query})
    print(response)

if __name__ == "__main__":
    main()