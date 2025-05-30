import os
import requests
import streamlit as st
from models.image_captioning import get_image_caption

def image_captioning_page(documents_directory):
    """
    Handles image upload and caption generation.
    """
    st.header("Image Captioning Feature")

    # File Upload Section
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png"])
    if not uploaded_image:
        st.error("Please upload an image first.")
    else:
        try:
            # Save the uploaded image
            file_path = os.path.join(documents_directory, uploaded_image.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_image.read())

            # Display the uploaded image
            st.image(file_path, caption="Uploaded Image", use_container_width=True)

            # Generate caption
            caption = get_image_caption(file_path)
            st.subheader("Generated Caption")
            st.write(f"Caption: {caption}")
        except Exception as e:
            st.error(f"Error processing the image: {e}")
