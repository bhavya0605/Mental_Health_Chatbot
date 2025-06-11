import sys
import warnings
import google.generativeai as genai
from vectorstore_manager import get_or_create_vectorstore

warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain')
warnings.filterwarnings("ignore", category=FutureWarning, module='huggingface_hub')

genai.configure(api_key='YOUR_API_KEY')

def generate_with_retrieval(prompt, vectordb):
    prompt += " (Answer should be based only on Mental Health.)"  # Force India-specific responses
    top_docs = vectordb.search(prompt, search_type='similarity', k=3)
    
    retrieved_context = " ".join([doc.page_content for doc in top_docs])
    combined_prompt = prompt + "\n" + retrieved_context

    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
    response = model.generate_content(combined_prompt)
    
    return response.text.strip()



negative_responses = ("no", "nope", "nah", "not a chance", "sorry")
exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")

def greet():
    name = input("What is your name?\n")
    will_help = input(f"Hi {name}, I am a Mental Health assistant. Do you need any assistance?\n  ")
    
    if will_help.lower() in negative_responses:
        print("All right! See ya!\n")
        sys.exit()

def make_exit(reply):
    for command in exit_commands:
        if reply.lower() == command:
            print("Hope I could be of help today. Have a nice day!")
            sys.exit()

def run_chatbot(json_file_path, vector_file_path="vector_data.pkl"):
    vectordb = get_or_create_vectorstore(json_file_path, vector_file_path)

    greet()
    
    while True:
        prompt = input("What is your question?\n")
        response = generate_with_retrieval(prompt, vectordb)
        print("Prompt:", prompt)
        print("Response:\n", response)

        more_help = input("Do you need any more assistance?\n")
        if more_help.lower() in negative_responses:
            print("All right! See ya!\n")
            sys.exit()
        make_exit(more_help)

json_file_path = r"mentalhealth.json" 
vector_file_path = r"vector_store"  

if __name__ == "__main__":
    run_chatbot(json_file_path, vector_file_path)
