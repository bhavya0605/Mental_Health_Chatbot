from langchain_community.vectorstores import Chroma  # Updated import
from langchain_community.embeddings import HuggingFaceEmbeddings  # Updated import
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import json 
import warnings
from langchain.schema import Document  # Import Document from langchain.schema

# File and directory paths
json_file_path = r"mentalhealth.json"
vector_db_dir = r"vector_store"
vector_db_path = os.path.join(vector_db_dir, "vector_store.db")

# Ensure the vector store directory exists
os.makedirs(vector_db_dir, exist_ok=True)

# Suppress deprecation and future warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_community')
warnings.filterwarnings("ignore", category=FutureWarning, module='huggingface_hub')

def process_json_file(json_file_path):
    """ Reads a JSON file and processes it into a list of LangChain Document objects. """
    try:
        with open(json_file_path, "r", encoding='utf-8') as f:  # Added encoding
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {str(e)}")

    documents = []
    for i, doc in enumerate(data):
        if isinstance(doc, str):
            title = doc
            description = ""
        elif isinstance(doc, dict):
            title = doc.get("title", "")  # Added default value
            description = doc.get("description", "")  # Added default value
        else:
            print(f"Skipping item {i} due to unexpected format: {doc}")
            continue

        content = f"{title}\n{description}".strip()  # Ensures clean formatting
        if content:  # Ensure only non-empty documents are added
            document_obj = Document(page_content=content, metadata={"id": title})
            documents.append(document_obj)

    if not documents:
        raise ValueError("No valid documents found in the JSON file.")

    return documents

def get_or_create_vectorstore(json_file_path, vector_db_path):
    """ Loads or creates a vector store from processed documents. """
    documents = process_json_file(json_file_path)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    all_splits = text_splitter.split_documents(documents)

    model_name = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    try:
        if os.path.exists(vector_db_path):
            vectordb = Chroma(persist_directory=vector_db_path, embedding_function=embeddings)
            print(f"Loaded existing vector store from {vector_db_path}.")
        else:
            vectordb = Chroma.from_documents(documents=all_splits, embedding_function=embeddings, persist_directory=vector_db_path)
            vectordb.persist()  # Explicitly persist the database
            print(f"Created new vector store at {vector_db_path}.")
        
        return vectordb

    except Exception as e:
        raise RuntimeError(f"Error creating/loading vector store: {str(e)}")

if __name__ == "__main__":
    try:
        vectordb = get_or_create_vectorstore(json_file_path, vector_db_path)
    except Exception as e:
        print(f"Application error: {str(e)}")
