import tempfile
from pathlib import Path
import streamlit as st
from src.audo_to_text.services.model_loader import ModelLoader
from src.audo_to_text.services.audio_transcriber import AudioFileTranscriber, DEFAULT_MODEL_NAME


class TranscribeUI:
	"""
	Minimal Streamlit UI for audio transcription.
	Handles file upload, model selection, and result display.
	Future: microphone input integration.
	"""

	def __init__(self):
		# Set up Streamlit page config and header
		st.set_page_config(page_title="Transcribe", layout="centered")
		st.title("Minimal Audio Transcription UI")
		st.caption("Prototype: upload a file and transcribe. Microphone support coming later.")

	def model_selector(self):
		"""Model selection dropdown."""
		return st.selectbox("Model", ["tiny", "base", "small"], index=0)

	def file_uploader(self):
		"""Audio file uploader widget."""
		return st.file_uploader("Upload audio file (wav/mp3)", type=["wav", "mp3"], accept_multiple_files=False)

	def transcribe_button(self):
		"""Transcribe button widget."""
		return st.button("Transcribe")

	def transcribe_file(self, uploaded, model_name):
		"""
		Handle file upload, model loading, transcription, and result display.
		Args:
			uploaded: Uploaded file object from Streamlit
			model_name: Selected Whisper model name
		"""
		if not uploaded:
			st.warning("Please upload an audio file first.")
			return

		# Save uploaded file to a temporary path for whisper.load_audio
		suffix = Path(uploaded.name).suffix or ".wav"
		with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
			tmp.write(uploaded.read())
			tmp_path = Path(tmp.name)

		try:
			# Load model (could cache in st.session_state for performance)
			model = ModelLoader(model_name).load()
			transcriber = AudioFileTranscriber(audio_path=tmp_path, model=model)
			lang, text = transcriber.transcribe()
			st.success(f"Detected language: {lang}")
			st.text_area("Transcription", value=text, height=180)
		finally:
			# Clean up temp file
			if tmp_path.exists():
				tmp_path.unlink(missing_ok=True)

	def microphone_placeholder(self):
		"""Display placeholder for future microphone input integration."""
		st.divider()
		st.subheader("Microphone Input")
		st.caption("Placeholder – will integrate WebRTC / Streamlit audio recorder in future.")
		st.info("Microphone streaming not implemented yet.")

	def footer(self):
		"""Footer/debug info."""
		st.caption("v0 minimal stub")

	def run(self):
		"""Main UI runner."""
		model_name = self.model_selector()
		uploaded = self.file_uploader()
		transcribe_btn = self.transcribe_button()
		
		if transcribe_btn:
			self.transcribe_file(uploaded, model_name)
			
		self.microphone_placeholder()
		self.footer()


if __name__ == "__main__":
	# For Streamlit, this block is not used, but allows local testing
	TranscribeUI().run()
