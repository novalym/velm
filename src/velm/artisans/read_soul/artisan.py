# Path: scaffold/artisans/read_soul/artisan.py
# (Content is identical to the previous `read_soul_artisan.py`)

from pathlib import Path
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import ReadSoulRequest
from ...contracts.heresy_contracts import ArtisanHeresy
from ...help_registry import register_artisan


@register_artisan("read-soul")
class ReadSoulArtisan(BaseArtisan[ReadSoulRequest]):
    """The artisan that reads a file's soul for the AI."""

    def execute(self, request: ReadSoulRequest) -> ScaffoldResult:
        try:
            target_path = (self.project_root / request.path_to_scripture).resolve()

            if not target_path.is_file():
                raise ArtisanHeresy(f"The scripture is a void: {target_path}")

            content = target_path.read_text(encoding='utf-8', errors='ignore')

            # Proclaim the raw soul to stdout for the Sentinel to capture.
            print(content)

            return self.success("The soul has been proclaimed.")
        except Exception as e:
            raise ArtisanHeresy(f"Gaze upon the soul failed: {e}", child_heresy=e)