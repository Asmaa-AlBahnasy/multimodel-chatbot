import streamlit as st
from ui.layout import initialize_ui
from features.QuestionAnswering import ask_questions_page
from features.DocumentSummarizing import summarize_document_page
from features.ImageCaptioning import image_captioning_page
from models.ollama_model import answer_question

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

# Initialize the application UI
initialize_ui()

# Sidebar menu for feature selection
selected_feature = st.sidebar.radio(
    "Select a Feature:",
    [
        "Ask Questions",
        "Summarize Document",
        "Image Captioning"
    ]
)

# Map selected feature to corresponding functionality
if selected_feature == "Ask Questions":
    ask_questions_page()

elif selected_feature == "Summarize Document":
    summarize_document_page()

elif selected_feature == "Image Captioning":
    image_folder = "data/uploads"
    image_captioning_page(image_folder) 