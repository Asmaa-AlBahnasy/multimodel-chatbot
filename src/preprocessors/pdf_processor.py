import re
from pdfminer.high_level import extract_text

def extract_pdf_text(file_path):
    """
    Extracts and cleans text from a PDF file.
    Args:
        file_path (str): Path to the PDF file.
    Returns:
        str: Cleaned text extracted from the PDF.
    """
    try:
        # Extract raw text from PDF
        raw_text = extract_text(file_path)

        # Clean the extracted text
        cleaned_text = re.sub(r'\s+', ' ', raw_text)  # Replace multiple spaces/newlines with a single space
        cleaned_text = re.sub(r'', '-', cleaned_text)  # Replace bullet points with a dash
        cleaned_text = re.sub(r'•', '-', cleaned_text)  # Replace another type of bullet point with a dash
        cleaned_text = re.sub(r'\n+', '\n', cleaned_text)  # Normalize newlines for paragraphs
        cleaned_text = re.sub(r'\s*-\s*', '- ', cleaned_text)  # Normalize spacing around dashes

        return cleaned_text.strip()
    except Exception as e:
        raise Exception(f"Error extracting and cleaning text from PDF: {e}")
