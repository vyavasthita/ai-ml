"""
Export and download UI utilities for transcription app.
Provides PDF, SRT, and text download via dropdown for Streamlit UI.
"""

from fpdf import FPDF
import streamlit as st


__all__ = ["ExportUI", "export_dropdown"]


def export_pdf_button(text: str):
    """Show a single Download PDF button for exporting transcription as PDF."""
    ExportUI(text).show_pdf_download()


class ExportUI:
    """Class-based export and download UI utilities for transcription app."""

    def __init__(self, text: str):
        self.text = text

    def get_pdf_lines(self) -> list:
        """Return lines for PDF, ensuring at least one line."""
        lines = self.text.splitlines()
        if not lines or all(not line.strip() for line in lines):
            return ["(No transcription)"]
        return lines

    def show_pdf_download(self):
        """Render a download button for PDF export."""
        pdf_bytes = self.generate_pdf_bytes()
        st.download_button("Download PDF", data=pdf_bytes, file_name="transcription.pdf", mime="application/pdf")

    # Removed SRT, text, and dropdown export logic

    def generate_pdf_bytes(self) -> bytes:
        """Generate PDF bytes from transcription text (robust, with wrapping and encoding)."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in self.get_pdf_lines():
            pdf.multi_cell(0, 10, txt=line)
        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        return pdf_bytes

    def transcription_to_srt(self) -> str:
        """Convert plain text transcription to minimal SRT format."""
        # Minimal SRT: one block, no timestamps
        return "1\n00:00:00,000 --> 00:00:10,000\n" + self.text + "\n"
