"""
image_caption_service.py
Service class for image loading and caption generation.
"""
from PIL import Image
import requests
from io import BytesIO


class ImageCaptionService:
    def __init__(self, model):
        self.model = model

    def load_image_from_file(self, image_file):
        """Load image from uploaded file."""
        return Image.open(image_file)

    def load_image_from_url(self, url: str):
        """Load image from a URL."""
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    def generate_caption(self, img):
        """Generate caption for the given image using the model."""
        result = self.model(img)
        return result[0]["generated_text"] if result and "generated_text" in result[0] else ""
