import os
import streamlit as st
from models.langchain_rag import run_rag_pipeline
from utils.file_handler import process_uploaded_file, process_arxiv_url
from models.ollama_model import summarize_text

# Paths for documents and vector index
documents_directory = "data/uploads"
vector_store_path = "data/index/faiss_index"

# Ensure directories exist
os.makedirs(documents_directory, exist_ok=True)
os.makedirs(os.path.dirname(vector_store_path), exist_ok=True)

def summarize_document_page():
    """
    Streamlit page for the Summarize Document feature.
    """
    uploaded_file = st.file_uploader("Upload a file (PDF, CSV)", type=["pdf", "csv"])
    arxiv_url = st.text_input("Enter an ArXiv URL (e.g., https://arxiv.org/abs/1234.56789)")

    if not uploaded_file and not arxiv_url:
        st.info("Please upload a file or provide an ArXiv URL to start.")
        return

    try:
        extracted_text = ""
        if uploaded_file:
            file_path = os.path.join(documents_directory, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            extracted_text = process_uploaded_file(file_path)
        elif arxiv_url:
            st.info("Processing the ArXiv URL...")
            extracted_text = process_arxiv_url(arxiv_url)

        if not extracted_text.strip():
            st.error("No text could be extracted from the provided file or URL.")
            return

        # Split content into smaller chunks
        chunk_size = 1000  # Limit chunks to manageable size
        small_chunks = [
            extracted_text[i:i + chunk_size]
            for i in range(0, len(extracted_text), chunk_size)
        ]

        # Summarize each chunk
        summaries = []
        for chunk in small_chunks:
            summary = summarize_text(chunk, max_length=150, min_length=30)
            summaries.append(summary)

        # Combine summaries
        final_summary = " ".join(summaries)

        st.subheader("Document Summary")
        st.write(final_summary)

    except Exception as e:
        st.error(f"Error summarizing the document: {e}")
