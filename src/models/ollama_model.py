import os
import requests
import time

# Load Hugging Face API key from environment variable
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")

import requests
import time

def summarize_text(text, max_length=150, min_length=30, max_retries=5):
    """
    Summarizes the given text using Hugging Face's summarization model with retry logic.
    Args:
        text (str): The text to summarize.
        max_length (int): Maximum length of the summary.
        min_length (int): Minimum length of the summary.
        max_retries (int): Maximum number of retries if the model is loading.
    Returns:
        str: The summarized text.
    """
    # Truncate text to a safe length
    max_input_length = 1024  # Limit input size to avoid errors
    truncated_text = text[:max_input_length]

    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": truncated_text,
        "parameters": {"min_length": min_length, "max_length": max_length},
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()[0]["summary_text"]
            elif response.status_code == 503:
                estimated_time = response.json().get("estimated_time", 10)
                print(f"Model is loading. Retrying in {estimated_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(estimated_time)
            else:
                raise Exception(f"Summarization API request failed: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
            time.sleep(5)  # Wait before retrying

    return "Error: Model did not load in time. Please try again later."



def answer_question(context, question):
    """
    Answers a question based on the given context using Hugging Face's Inference API.
    Args:
        context (str): The context in which to find the answer.
        question (str): The question to answer.
    Returns:
        str: The answer to the question or an error message.
    """
    api_url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-distilled-squad"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": {
            "question": question,
            "context": context,
        }
    }

    max_retries = 5  # Maximum number of retries
    wait_time = 10  # Initial wait time in seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                # Successful response
                return response.json().get("answer", "No answer found.")
            
            elif response.status_code == 503:
                # Model is loading
                estimated_time = response.json().get("estimated_time", wait_time)
                print(f"Model loading. Retrying in {estimated_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(estimated_time)
            else:
                # Other errors
                raise Exception(f"API request failed: {response.status_code}, {response.text}")
        
        except requests.RequestException as e:
            # Network-related errors
            print(f"Request failed: {e}")
            time.sleep(wait_time)

    return "Error: The model did not load in time. Please try again later."
