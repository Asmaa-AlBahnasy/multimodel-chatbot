import pandas as pd

def extract_csv_text(file_path):
    """
    Extracts text from a CSV or TSV file by converting its content into a readable string format.
    Automatically detects the correct delimiter.
    Args:
        file_path (str): Path to the CSV or TSV file.
    Returns:
        str: Extracted text from the file.
    """
    try:
        # Read the file with automatic delimiter detection
        with open(file_path, 'r') as f:
            sample = f.read(1024)  # Read a small portion of the file to guess delimiter
            delimiter = ',' if ',' in sample else '\t'

        # Load the file into a DataFrame
        df = pd.read_csv(file_path, delimiter=delimiter)

        # Convert DataFrame to a clean, readable string
        text = df.to_string(index=False)
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from CSV or TSV: {e}")
