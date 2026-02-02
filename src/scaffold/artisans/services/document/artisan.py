import logging
import os
from typing import Any

from ....core.artisan import BaseArtisan
from ....interfaces.requests import DocumentRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy

from .domains.pdf import PdfEngine
from .domains.data import DataEngine

Logger = logging.getLogger("DocumentArtisan")


class DocumentArtisan(BaseArtisan[DocumentRequest]):
    """
    =============================================================================
    == THE SCRIBE OF MATTER (V-Ω-DOC-AUTOMATION)                               ==
    =============================================================================
    LIF: ∞ | ROLE: FILE_GENERATOR
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        self.pdf = PdfEngine()
        self.data = DataEngine()

    def execute(self, request: DocumentRequest) -> ScaffoldResult:
        try:
            output_path = request.output_path or f"output.{request.format.value}"

            # --- RITE 1: GENERATION ---
            if request.action == "generate":
                if request.format == "pdf":
                    # 1. Render Template
                    if not request.template_path: return self.engine.failure("PDF requires template_path.")

                    html = self.engine.alchemist.render_file(request.template_path, request.data or {})
                    self.pdf.generate(html, output_path)

                elif request.format in ["csv", "xlsx"]:
                    if not request.data: return self.engine.failure("Data required for spreadsheet generation.")
                    self.data.generate(request.data, output_path, request.format.value)

                return self.engine.success(f"Generated {request.format.value}", data={"path": output_path})

            # --- RITE 2: PARSING ---
            elif request.action == "parse":
                if not request.source_path: return self.engine.failure("Source path required.")

                result_data = self.data.parse(request.source_path, request.format.value)
                return self.engine.success(
                    f"Parsed {len(result_data)} rows.",
                    data=result_data  # CAUTION: Can be large
                )

            # --- RITE 3: MERGING (Future) ---
            # Use PyPDF2 to merge PDFs?

            else:
                return self.engine.failure(f"Unknown Document Action: {request.action}")

        except Exception as e:
            Logger.error(f"Document Fracture: {e}", exc_info=True)
            return self.engine.failure(f"Document Rite Failed: {str(e)}")