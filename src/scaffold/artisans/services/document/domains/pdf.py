import logging
from typing import Any, Dict


class PdfEngine:
    """[THE PDF FORGE] Uses WeasyPrint or ReportLab."""

    def generate(self, html_content: str, output_path: str) -> str:
        try:
            from weasyprint import HTML
            HTML(string=html_content).write_pdf(output_path)
            return output_path
        except ImportError:
            raise ImportError("WeasyPrint not found. Run `pip install weasyprint`.")