"""
ImageUploadTranscribeUI
UI class for uploading images and generating captions using HuggingFace pipeline.
"""
import streamlit as st
from image_to_text.services.image_caption_service import ImageCaptionService


class ImageUploadTranscribeUI:
    def __init__(self):
        self.file_helper = st.session_state.get("image_file_helper")
        self.model = st.session_state.get("image_caption_model")
        self.caption_service = ImageCaptionService(self.model) if self.model else None

    def display(self):
        st.subheader("Upload an image or provide a URL")
        img = self._get_image_input()
        self._show_image(img)
        self._caption_and_save(img)

    def _get_image_input(self):
        image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        image_url = st.text_input("Or paste an image URL")
        img = None
        if image_file:
            img = self.caption_service.load_image_from_file(image_file)
        elif image_url:
            try:
                img = self.caption_service.load_image_from_url(image_url)
            except Exception:
                st.error("Could not load image from URL.")
        return img

    def _show_image(self, img):
        if img:
            st.image(img, caption="Selected Image", width='stretch')

    def _caption_and_save(self, img):
        if not (img and self.caption_service):
            return
        caption = self.caption_service.generate_caption(img)
        st.success(f"Caption: {caption}")
        if self.file_helper:
            self.file_helper.write_text_file("captions", "caption.txt", caption)
