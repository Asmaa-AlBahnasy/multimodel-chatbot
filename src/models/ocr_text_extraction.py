import os
import requests

def extract_text_from_image(image_path):
    """
    Extracts text from an image using Hugging Face OCR models.
    Args:
        image_path (str): Path to the image file.
    Returns:
        str: Extracted text from the image.
    """
    # API endpoint for Hugging Face's OCR model
    api_url = "https://api-inference.huggingface.co/models/microsoft/trocr-base-handwritten"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}"}

    # Read the image in binary format
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Make the POST request to the Hugging Face API
    response = requests.post(api_url, headers=headers, data=image_data)

    # Handle the response
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list):  # Check if result is a list
            return result[0].get("generated_text", "No text extracted.") if result else "No text extracted."
        return result.get("generated_text", "No text extracted.")
    elif response.status_code == 503:
        raise Exception("OCR API request failed: Model is still loading. Please retry later.")
    else:
        raise Exception(f"OCR API request failed: {response.status_code}, {response.text}")
