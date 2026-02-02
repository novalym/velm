import logging
from ....core.artisan import BaseArtisan
from ....interfaces.requests import BrowserRequest
from ....interfaces.base import ScaffoldResult
from .engine import ChromeEngine

Logger = logging.getLogger("BrowserArtisan")


class BrowserArtisan(BaseArtisan[BrowserRequest]):
    """
    [THE NAVIGATOR]
    Orchestrates headless browser interactions.
    """

    def __init__(self, engine):
        super().__init__(engine)
        self.chrome = ChromeEngine()

    def execute(self, request: BrowserRequest) -> ScaffoldResult:
        try:
            result = self.chrome.execute(request)

            # Handle Binary Artifacts (Screenshot/PDF)
            if isinstance(result, dict) and "binary" in result:
                # We don't return raw bytes in JSON; we save or return metadata
                # Ideally, we write to a temp file or upload to StorageArtisan
                # For now, we return summary and assume caller handles bytes via other means if needed
                # or we write to disk if output_path is implied.

                # Simple implementation: Write to CWD/output
                ext = "png" if result['mime'] == "image/png" else "pdf"
                filename = f"browser_output.{ext}"
                with open(filename, "wb") as f:
                    f.write(result['binary'])

                return self.engine.success(
                    f"Browser Rite ({request.action}) Complete.",
                    data={"path": filename, "mime": result['mime']}
                )

            return self.engine.success(
                f"Browser Rite ({request.action}) Complete.",
                data=result
            )

        except Exception as e:
            Logger.error(f"Browser Fracture: {e}", exc_info=True)
            return self.engine.failure(f"Navigation Failed: {e}")