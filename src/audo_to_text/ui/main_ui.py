"""
Main UI entry point for audio/speech transcription app.
Provides tabbed interface for file upload and microphone input.
"""
import streamlit as st
from src.audo_to_text.ui.audio_upload_ui import AudioUploadTranscribeUI
from src.audo_to_text.ui.microphone_ui import MicrophoneTranscribeUI

# Setup Streamlit page configuration and header

def setup_ui():
    """Configure Streamlit page and display main header/caption."""
    st.set_page_config(page_title="Transcribe", layout="centered")
    st.title("Minimal Audio Transcription UI")
    st.caption("Upload audio or record speech for transcription.")

setup_ui()

# Main application logic

def main():
    """Render tabbed UI for audio upload and microphone transcription."""
    upload_ui = AudioUploadTranscribeUI()  # UI for file upload
    mic_ui = MicrophoneTranscribeUI()      # UI for microphone input
    
    tab_upload, tab_mic = st.tabs(["Upload Audio", "Microphone"])
    
    with tab_upload:
        upload_ui.display()  # Show upload UI
    
    with tab_mic:
        mic_ui.display()     # Show microphone UI

if __name__ == "__main__":
    main()