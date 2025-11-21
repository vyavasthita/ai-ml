import streamlit as st
from pathlib import Path

def download_button(text: str, file_path: Path, label: str = "Download Transcription"):
    """Reusable download button for transcription text."""
    st.download_button(
        label=label,
        data=text,
        file_name=file_path.name,
        mime="text/plain",
        help="Save the transcription locally"
    )
