"""
caption_model_loader.py
Loads the HuggingFace image captioning pipeline for image-to-text.
"""
from transformers import pipeline


class CaptionModelLoader:
    def __init__(self, model_name: str = "nlpconnect/vit-gpt2-image-captioning"):
        self.model_name = model_name

    def load(self):
        """
        Load and return the image-to-text pipeline.
        """
        return pipeline("image-to-text", model=self.model_name)
