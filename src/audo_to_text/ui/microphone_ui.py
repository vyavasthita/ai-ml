import tempfile
from pathlib import Path
import streamlit as st
from .export_ui import export_buttons, download_button
from src.audo_to_text.services.model_loader import ModelLoader
from src.audo_to_text.services.audio_transcriber import AudioFileTranscriber
from src.audo_to_text.services.speech_transcriber import SpeechTranscriber


class MicrophoneTranscribeUI:
    """
    Handles microphone input (single-shot recording and future streaming).
    - Loads Whisper and speech transcriber models
    - Records and saves audio clips
    - Runs transcription
    - Persists and writes transcript
    - Offers download/export options
    """

    def __init__(self):
        # Load models if not already in session
        if "speech_transcriber" not in st.session_state:
            st.session_state["speech_transcriber"] = SpeechTranscriber(model_name="tiny")
        if "whisper_model" not in st.session_state:
            st.session_state["whisper_model"] = ModelLoader("tiny").load()

    def audio_recorder(self):
        """Show microphone audio recorder widget."""
        return st.audio_input("Record speech")

    def save_clip(self, clip):
        """Save recorded audio clip to temp path."""
        if not clip:
            return None
        suffix = self.determine_suffix(clip)
        data = clip.read()  # read once
        return self.write_temp_file(data, suffix)

    def determine_suffix(self, clip) -> str:
        """Infer file suffix from mime type; default wav."""
        suffix = ".wav"
        ctype = getattr(clip, "type", None) or ""
        if "mpeg" in ctype:
            suffix = ".mp3"
        elif "ogg" in ctype:
            suffix = ".ogg"
        return suffix

    def write_temp_file(self, data: bytes, suffix: str) -> Path:
        """Write bytes to a temp file and return its Path."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            return Path(tmp.name)

    def transcribe_clip(self, path: Path):
        """Run Whisper transcription on saved clip."""
        if not path:
            return None, ""
        
        model = st.session_state["whisper_model"]
        transcriber = AudioFileTranscriber(audio_path=path, model=model)
        lang, text = transcriber.transcribe()
        return lang, text

    def display_single_shot(self):
        """Main display logic for microphone tab."""
        clip = self.audio_recorder()
        if not clip:
            st.info("Press 'Record speech' to capture audio.")
            return
        col_info, col_btn = st.columns([1, 1])
        with col_btn:
            if self.transcribe_action():
                self.process_clip(clip)

    def transcribe_action(self) -> bool:
        """Show transcribe button widget."""
        return st.button("Transcribe Recording", key="mic_transcribe_btn")

    def process_clip(self, clip):
        """Handle clip saving, transcription, and render results."""
        path = self.save_clip(clip)
        if not path:
            st.error("Failed to save recording.")
            return
        try:
            lang, text = self.transcribe_clip(path)
            self.render_transcription(lang, text, audio_path=path)
        finally:
            if path.exists():
                path.unlink(missing_ok=True)

    def render_transcription(self, lang: str, text: str, audio_path=None):
        """Show transcription, audio playback, and export buttons."""
        st.success(f"Detected language: {lang if lang else 'unknown'}")
        st.text_area("Microphone Transcription", value=text, height=180)
        if audio_path:
            st.audio(str(audio_path), format="audio/wav")
        self.persist_last_transcript(text)
        file_path = self.write_transcription_to_file(text)
        self.download_button(text, file_path)
        export_buttons(text)

    def persist_last_transcript(self, text: str):
        """Store last transcript in session state."""
        st.session_state["last_mic_transcript"] = text

    def write_transcription_to_file(self, text: str):
        """Write transcript to disk for download."""
        out_dir = Path("transcriptions")
        out_dir.mkdir(exist_ok=True)
        file_path = out_dir / "microphone_transcription.txt"
        file_path.write_text(text, encoding="utf-8")
        return file_path

    def download_button(self, text: str, file_path: Path):
        """Show download button for transcript text."""
        download_button(text, file_path)

    def display(self):
        """Entry point for microphone tab UI."""
        st.subheader("Microphone Speech Recognition")
        self.display_single_shot()
        # ...existing code...
