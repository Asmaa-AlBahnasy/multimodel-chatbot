import os
from preprocessors.arxiv_processor import download_arxiv_pdf, extract_arxiv_text
from preprocessors.pdf_processor import extract_pdf_text
from preprocessors.csv_processor import extract_csv_text

def process_uploaded_file(file_path):
    """
    Processes uploaded files (PDF or CSV).
    Args:
        file_path (str): Path to the uploaded file.
    Returns:
        str: Extracted text from the file.
    """
    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)
    elif file_path.endswith(".csv"):
        return extract_csv_text(file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and CSV are allowed.")

def process_arxiv_url(arxiv_url):
    """
    Processes an ArXiv URL and extracts text.
    Args:
        arxiv_url (str): URL to the ArXiv paper.
    Returns:
        str: Extracted text from the ArXiv PDF.
    """
    pdf_stream = download_arxiv_pdf(arxiv_url)
    return extract_arxiv_text(pdf_stream)
