import logging
from typing import Any

from ....core.artisan import BaseArtisan
from ....interfaces.requests import SheetRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy

from .domains.google import GoogleSheetEngine
from .domains.airtable import AirtableEngine

Logger = logging.getLogger("SheetArtisan")


class SheetArtisan(BaseArtisan[SheetRequest]):
    """
    =============================================================================
    == THE GRID MASTER (V-Ω-SPREADSHEET-SOVEREIGN)                             ==
    =============================================================================
    LIF: ∞ | ROLE: DATA_GRID_INTEGRATOR

    Reads and writes to the business world's database (Sheets/Airtable).
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        self.google = GoogleSheetEngine()
        self.airtable = AirtableEngine()

    def execute(self, request: SheetRequest) -> ScaffoldResult:
        try:
            result = None

            if request.provider == "google":
                result = self.google.execute(request)
            elif request.provider == "airtable":
                result = self.airtable.execute(request)
            else:
                return self.engine.failure(f"Unknown Provider: {request.provider}")

            return self.engine.success(
                f"Grid Rite ({request.provider} -> {request.action}) Complete.",
                data=result
            )

        except Exception as e:
            Logger.error(f"Grid Fracture: {e}", exc_info=True)
            return self.engine.failure(f"Sheet Protocol Failed: {str(e)}")