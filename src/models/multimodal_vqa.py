import requests

def get_vqa_answer(image_binary, question, api_token):
    """
    Sends the image and question to a Visual Question Answering (VQA) API.

    Args:
        image_binary (bytes): The binary content of the image file.
        question (str): The question about the image.
        api_token (str): Hugging Face API token.

    Returns:
        str: The generated answer from the VQA model.
    """
    api_url = "https://api-inference.huggingface.co/models/Salesforce/blip-vqa-base"
    headers = {"Authorization": f"Bearer {api_token}"}

    # Correct multipart/form-data format
    files = {
        "image": ("image.jpg", image_binary, "application/octet-stream")
    }
    data = {
        "question": question
    }

    # Send the POST request
    response = requests.post(api_url, headers=headers, files=files, data=data)

    # Handle the response
    if response.status_code == 200:
        return response.json().get("generated_text", "No answer found.")
    else:
        raise Exception(
            f"VQA API request failed: {response.status_code}, {response.text}"
        )
