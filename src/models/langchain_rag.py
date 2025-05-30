import os
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config.settings import HUGGINGFACEHUB_API_TOKEN

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize HuggingFace embeddings
def initialize_embeddings():
    """
    Initializes HuggingFace embeddings for vectorization.
    Returns:
        HuggingFaceEmbeddings: The embedding model.
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Load documents from a directory
def load_documents(directory):
    """
    Loads documents from a directory.
    Args:
        directory (str): Path to the directory containing documents.
    Returns:
        list: List of LangChain document objects.
    """
    documents = []
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(directory, file))
            documents.extend(loader.load())
    return documents

# Split documents into chunks
def split_documents(documents, chunk_size=500, chunk_overlap=50):
    """
    Splits documents into smaller chunks.
    Args:
        documents (list): List of LangChain document objects.
        chunk_size (int): Maximum size of each chunk.
        chunk_overlap (int): Overlap between chunks.
    Returns:
        list: List of split document chunks.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

# Create or load vector store
def create_vector_store(documents, embeddings, path):
    """
    Creates or loads a vector store for document retrieval.
    Args:
        documents (list): List of document objects.
        embeddings (HuggingFaceEmbeddings): Embedding model.
        path (str): Path to save/load the vector store.
    Returns:
        FAISS: The vector store.
    """
    if os.path.exists(path):
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(path)
    return vector_store

# Create the RAG QA chain
def create_qa_chain(vector_store, model_name="google/flan-t5-large"):
    """
    Creates a Retrieval-Augmented Generation (RAG) chain for question answering.
    """
    retriever = vector_store.as_retriever()
    llm = HuggingFaceHub(
        repo_id=model_name,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        model_kwargs={"temperature": 0.3, "max_new_tokens": 100},
    )
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

# Wrapper for full RAG pipeline
def run_rag_pipeline(directory, vector_store_path, model_name="google/flan-t5-large"):
    """
    Runs the full RAG pipeline: loading, splitting, embedding, and QA chain creation.
    Args:
        directory (str): Path to the document directory.
        vector_store_path (str): Path to the vector store.
        model_name (str): Name of the LLM to use for answering questions.
    Returns:
        RetrievalQA: The RAG QA chain.
    """
    embeddings = initialize_embeddings()
    documents = load_documents(directory)
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks, embeddings, vector_store_path)
    qa_chain = create_qa_chain(vector_store, model_name=model_name)
    return qa_chain
