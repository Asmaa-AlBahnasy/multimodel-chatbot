import requests
from io import BytesIO
from pdfminer.high_level import extract_text
import re

def download_arxiv_pdf(arxiv_url):
    """
    Downloads a PDF file from an ArXiv URL.
    Args:
        arxiv_url (str): The URL of the ArXiv paper.
    Returns:
        BytesIO: A binary stream of the downloaded PDF.
    """
    try:
        # Convert 'abs' URL to 'pdf' URL if necessary
        if '/abs/' in arxiv_url:
            arxiv_url = arxiv_url.replace('/abs/', '/pdf/') + '.pdf'
        
        response = requests.get(arxiv_url, stream=True)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            raise Exception(f"Failed to download PDF: HTTP {response.status_code}")
    except Exception as e:
        raise Exception(f"Error downloading ArXiv PDF: {e}")


def extract_arxiv_text(pdf_stream):
    """
    Extracts and cleans text from an ArXiv PDF.
    Args:
        pdf_stream (BytesIO): A binary stream of the PDF.
    Returns:
        str: Cleaned text extracted from the PDF.
    """
    try:
        # Extract raw text from PDF
        raw_text = extract_text(pdf_stream)

        # Clean the extracted text
        cleaned_text = re.sub(r'\s+', ' ', raw_text)  # Replace multiple spaces/newlines with a single space
        cleaned_text = re.sub(r'(?<!\S)[a-zA-Z]\s', '', cleaned_text)  # Remove single characters surrounded by spaces
        cleaned_text = re.sub(r'\d+\s+', '', cleaned_text)  # Remove isolated numbers
        cleaned_text = re.sub(r'[^\w\s.,;:\-\'"]+', '', cleaned_text)  # Remove unwanted symbols
        return cleaned_text.strip()
    except Exception as e:
        raise Exception(f"Error extracting and cleaning text from ArXiv PDF: {e}")
