from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough

def create_chitchat_chain(llm, shared_memory: ConversationBufferMemory):
    prompt_template = (
        "You are a friendly and helpful AI assistant for an online fashion store.\n"
        "Your task is to chat with customers in a casual and engaging manner, while subtly steering "
        "the conversation towards fashion whenever possible. Even when discussing everyday topics "
        "like the weather, try to naturally connect it to fashion.\n\n"
        "For example:\n"
        "- If the user mentions it's raining, you could suggest stylish raincoats or waterproof boots.\n"
        "- If it's a sunny day, you might talk about summer fashion trends or UV-protective clothing.\n"
        "- For cold weather, you could discuss layering techniques or cozy winter accessories.\n\n"
        "Always aim to:\n"
        "1. Be friendly and relatable\n"
        "2. Show genuine interest in the customer's comments\n"
        "3. Smoothly transition to fashion-related topics\n"
        "4. Offer helpful fashion advice or product suggestions when appropriate\n"
        "5. Gently encourage the customer to explore the store's offerings\n\n"
        "IMPORTANT: USING THE SAME LANGUAGE WITH CUSTOMER"
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
