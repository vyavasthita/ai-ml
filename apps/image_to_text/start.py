"""
image_to_text/start.py
Entry point for the Image to Text Streamlit UI app.
Handles all UI logic for image upload and caption generation.
"""
import streamlit as st
from utils.file_helper import FileHelper
from image_to_text.ui.image_upload_ui import ImageUploadTranscribeUI
from image_to_text.services.model_loader import CaptionModelLoader

# ---------- Setup Functions ----------

def setup_image_to_text_header():
    """
    Display Image to Text app subtitle.
    """
    st.header("Image to Text Converter")


def setup_file_helper():
    """
    Initialize FileHelper once at app startup and store in session_state.
    """
    if "image_file_helper" not in st.session_state:
        st.session_state["image_file_helper"] = FileHelper("image_to_text")


def setup_image_caption_model():
    """
    Load the HuggingFace image captioning model and store in session_state.
    """
    if "image_caption_model" not in st.session_state:
        st.session_state["image_caption_model"] = CaptionModelLoader().load()

# ---------- App Initialization ----------

def initialize_image_to_text_app():
    setup_image_to_text_header()
    setup_file_helper()
    setup_image_caption_model()

# ---------- Main Application Logic ----------

def run_image_to_text_ui():
    """
    Render UI for image upload and caption generation.
    """
    image_ui = ImageUploadTranscribeUI()
    image_ui.display()

# ---------- Entry Point for Import ----------

def main():
    initialize_image_to_text_app()
    run_image_to_text_ui()

if __name__ == "__main__":
    main()
