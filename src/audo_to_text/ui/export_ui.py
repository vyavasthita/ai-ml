"""
Export and download UI utilities for transcription app.
Provides PDF, SRT, and text export/download buttons for Streamlit UI.
"""
from fpdf import FPDF
import streamlit as st
from pathlib import Path


def download_button(text: str, file_path: Path, label: str = "Export as TEXT"):
    """Reusable download button for transcription text."""
    st.download_button(
        label=label,
        data=text,
        file_name=file_path.name,
        mime="text/plain",
        help="Save the transcription locally"
    )


def export_buttons(text: str):
    """Show export buttons for PDF and SRT formats."""
    # PDF export
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.splitlines():
        pdf.cell(200, 10, txt=line, ln=1)
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    st.download_button("Export as PDF", data=pdf_bytes, file_name="transcription.pdf", mime="application/pdf")
    # SRT export
    srt_text = transcription_to_srt(text)
    st.download_button("Export as SRT", data=srt_text, file_name="transcription.srt", mime="text/plain")


def transcription_to_srt(text: str) -> str:
    """Convert plain text transcription to minimal SRT format."""
    # Minimal SRT: one block, no timestamps
    return "1\n00:00:00,000 --> 00:00:10,000\n" + text + "\n"
