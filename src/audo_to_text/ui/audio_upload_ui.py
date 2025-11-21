import tempfile
from pathlib import Path
import streamlit as st
from src.audo_to_text.services.model_loader import ModelLoader
from src.audo_to_text.services.audio_transcriber import AudioFileTranscriber

class AudioUploadHandler:
    """Handles file save, transcription, and download logic for audio uploads."""
    def __init__(self):
        if "whisper_model" not in st.session_state:
            st.session_state["whisper_model"] = ModelLoader("tiny").load()

    def save_uploaded_file(self, uploaded):
        if not uploaded:
            return None
        suffix = Path(uploaded.name).suffix or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded.read())
            return Path(tmp.name)

    def run_transcription(self, tmp_path):
        model = st.session_state["whisper_model"]
        transcriber = AudioFileTranscriber(audio_path=tmp_path, model=model)
        lang, text = transcriber.transcribe()
        return lang, text

    def persist_last_transcript(self, text: str):
        st.session_state["last_upload_transcript"] = text

    def write_transcription_to_file(self, text: str):
        out_dir = Path("transcriptions")
        out_dir.mkdir(exist_ok=True)
        file_path = out_dir / "upload_transcription.txt"
        file_path.write_text(text, encoding="utf-8")
        return file_path

    def download_button(self, text: str, file_path: Path):
        st.download_button(
            label="Download Transcription",
            data=text,
            file_name=file_path.name,
            mime="text/plain",
            help="Save the transcription locally"
        )


class AudioUploadTranscribeUI:
    """Handles audio file upload UI and delegates logic to AudioUploadHandler."""
    def __init__(self):
        self.handler = AudioUploadHandler()

    def file_uploader(self):
        return st.file_uploader("Upload audio file (wav/mp3)", type=["wav", "mp3"], accept_multiple_files=False)

    def transcribe_button(self):
        return st.button("Transcribe", key="upload_transcribe_btn")

    def display(self):
        uploaded = self.file_uploader()
        if self.transcribe_button() and uploaded:
            self.process_uploaded_file(uploaded)
        elif uploaded is None:
            st.info("Upload an audio file to begin.")

    def process_uploaded_file(self, uploaded):
        tmp_path = self.handler.save_uploaded_file(uploaded)
        try:
            lang, text = self.handler.run_transcription(tmp_path)
            self.render_transcription(lang, text)
        finally:
            if tmp_path and tmp_path.exists():
                tmp_path.unlink(missing_ok=True)

    def render_transcription(self, lang, text):
        lang_full = self.language_name(lang)
        st.success(f"Detected language: {lang_full}")
        st.text_area("Transcription", value=text, height=180)
        self.save_and_offer_download(text)

    def save_and_offer_download(self, text):
        self.handler.persist_last_transcript(text)
        file_path = self.handler.write_transcription_to_file(text)
        self.handler.download_button(text, file_path)

    @staticmethod
    def language_name(lang_code):
        """Map language code to full language name."""
        code_map = {
            "en": "English", "hi": "Hindi", "fr": "French", "de": "German", "es": "Spanish", "it": "Italian", "zh": "Chinese", "ja": "Japanese", "ru": "Russian", "ar": "Arabic", "pt": "Portuguese", "bn": "Bengali", "pa": "Punjabi", "te": "Telugu", "ta": "Tamil", "tr": "Turkish", "ko": "Korean", "ur": "Urdu", "fa": "Persian", "pl": "Polish", "nl": "Dutch", "sv": "Swedish", "no": "Norwegian", "fi": "Finnish", "da": "Danish", "el": "Greek", "he": "Hebrew", "id": "Indonesian", "th": "Thai", "vi": "Vietnamese", "uk": "Ukrainian", "ro": "Romanian", "hu": "Hungarian", "cs": "Czech", "sk": "Slovak", "sl": "Slovenian", "hr": "Croatian", "sr": "Serbian", "bg": "Bulgarian", "lt": "Lithuanian", "lv": "Latvian", "et": "Estonian", "ms": "Malay", "fil": "Filipino", "sw": "Swahili", "zu": "Zulu", "af": "Afrikaans", "ca": "Catalan", "eu": "Basque", "gl": "Galician", "is": "Icelandic", "mt": "Maltese", "sq": "Albanian", "mk": "Macedonian", "az": "Azerbaijani", "ka": "Georgian", "hy": "Armenian", "be": "Belarusian", "kk": "Kazakh", "uz": "Uzbek", "mn": "Mongolian", "ky": "Kyrgyz", "tg": "Tajik", "tk": "Turkmen", "ps": "Pashto", "sd": "Sindhi", "si": "Sinhala", "my": "Burmese", "km": "Khmer", "lo": "Lao", "am": "Amharic", "om": "Oromo", "so": "Somali", "ne": "Nepali", "mr": "Marathi", "gu": "Gujarati", "kn": "Kannada", "ml": "Malayalam", "or": "Odia", "sa": "Sanskrit", "as": "Assamese", "mai": "Maithili", "bh": "Bhojpuri", "ta": "Tamil", "te": "Telugu", "ur": "Urdu"
        }
        return code_map.get(lang_code, lang_code)
