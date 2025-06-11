from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence
import os
from langchain.memory import ConversationBufferMemory

load_dotenv()

API_KEY = os.getenv("YOUR API KEY ")

def ConversationalBOT(query: str, memory: ConversationBufferMemory):
    
    # Retrieve conversation history from memory
    previous_context = "\n".join([
        f"User: {msg.content}" if msg.type == 'human' else f"Response: {msg.content}"
        for msg in memory.chat_memory.messages
    ])
    
    # Updated prompt
    template = f"""
    You are a helpful bot created by the sharp minds. Your name is MentalHealth-GPT.
    You are designed to solve people's queries. Be friendly in tone and avoid abusive language.
    Use the context to give accurate information about Mental health and its activities.
    If asked about non-Mental Health topics, politely redirect to Mental health discussions.

    Previous Conversation:
    {previous_context}

    User Input: {{query}}

    Answer:
    """

    prompt = PromptTemplate(input_variables=["query"], template=template)

    # Google Gemini model initialization
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2,
        google_api_key=API_KEY
    )

    # Create the chain
    chain = RunnableSequence(prompt | llm)

    response = chain.invoke({"query": query})
    full_response = response.content

    # Save to memory
    memory.save_context({"input": query}, {"output": full_response})

    return full_response
