import os
from preprocessors.arxiv_processor import download_arxiv_pdf, extract_arxiv_text
from preprocessors.pdf_processor import extract_pdf_text
from preprocessors.csv_processor import extract_csv_text


def process_uploaded_file(file):
    """
    Process the uploaded file based on its type.
    Args:
        file: Uploaded file object from Streamlit.
    Returns:
        str: Extracted text from the file.
    """
    file_path = os.path.join("data/uploads", file.name)
    with open(file_path, "wb") as f:
        f.write(file.read())

    if file.name.endswith(".pdf"):
        return extract_pdf_text(file_path)
    elif file.name.endswith(".csv"):
        return extract_csv_text(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and CSV are allowed.")


def process_arxiv_url(arxiv_url):
    """
    Process a given ArXiv URL and extract its text.
    Args:
        arxiv_url (str): The ArXiv URL.
    Returns:
        str: Extracted text from the ArXiv document.
    """
    pdf_stream = download_arxiv_pdf(arxiv_url)
    return extract_arxiv_text(pdf_stream)
