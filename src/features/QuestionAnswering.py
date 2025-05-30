import os
import streamlit as st
from models.langchain_rag import run_rag_pipeline
from models.memory import ChatMemory
from ui.chat_ui import render_chat_ui
from utils.file_manager import process_uploaded_file, process_arxiv_url
from models.ollama_model import answer_question

# Paths for documents and vector index
documents_directory = "data/uploads"
vector_store_path = "data/index/faiss_index"

# Initialize or retrieve chat memory from session state
if "chat_memory" not in st.session_state:
    st.session_state["chat_memory"] = ChatMemory()

chat_memory = st.session_state["chat_memory"]

def ask_questions_page():
    """
    Streamlit page for the Ask Questions feature.
    """
    # File Upload Section or ArXiv URL
    uploaded_file = st.file_uploader("Upload a file (PDF, CSV) or provide an ArXiv URL", type=["pdf", "csv"])
    arxiv_url = st.text_input("Enter an ArXiv URL (e.g., https://arxiv.org/abs/1234.56789)")
    qa_chain = None

    # Handle Uploaded File or ArXiv URL
    try:
        extracted_text = ""
        if uploaded_file:
            st.info("Processing the uploaded file...")
            extracted_text = process_uploaded_file(uploaded_file)
        elif arxiv_url:
            st.info("Processing the ArXiv URL...")
            extracted_text = process_arxiv_url(arxiv_url)
        else:
            st.info("Please upload a file or provide an ArXiv URL to start.")

        if extracted_text:
            st.success("File processed successfully!")

            # Ask Questions Section
            question = st.text_input("Enter your question", key="user_input")
            if st.button("Ask", key="ask_button"):
                try:
                    # Call answer_question with required arguments
                    answer = answer_question(extracted_text, question)

                    # Save the question and answer in memory
                    chat_memory.add_message(question, answer.strip())

                    # Display the answer
                    st.write(f"**Answer:** {answer}")
                except Exception as e:
                    st.error(f"Error fetching the answer: {e}")

            # Render Chat History
            render_chat_ui(chat_memory)
    except Exception as e:
        st.error(f"Error: {e}")
