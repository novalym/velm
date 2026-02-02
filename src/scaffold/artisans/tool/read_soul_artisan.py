# Path: scaffold/artisans/tool/read_soul_artisan.py
# -----------------------------------------------
"""
=================================================================================
== THE SCRIBE OF THE PURE SOUL (V-Ω-SENTINEL-CONDUIT)                          ==
=================================================================================
This artisan is a pure, unbreakable conduit. Its one true purpose is to receive a
plea for a scripture's soul from the Sentinel, gaze upon that scripture in the
mortal realm, and proclaim its raw, untransmuted content to stdout. It is the
sensory organ for the AI's Gnostic Gaze.
=================================================================================
"""
from pathlib import Path
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import ReadSoulRequest
from ...contracts.heresy_contracts import ArtisanHeresy


# This artisan does not need a dedicated registration in the LAZY_RITE_MAP
# because it is a sub-command of 'tool', which is already registered.
# The ToolArtisan will summon it.

class ReadSoulArtisan(BaseArtisan[ReadSoulRequest]):
    """The artisan that reads a file's soul for the AI."""

    def execute(self, request: ReadSoulRequest) -> ScaffoldResult:
        try:
            target_path = (self.project_root / request.path_to_scripture).resolve()

            if not target_path.is_file():
                # We return a failure result, and the Sentinel will see the non-zero exit code.
                raise ArtisanHeresy(f"The scripture is a void: {target_path}")

            content = target_path.read_text(encoding='utf-8', errors='ignore')

            # Proclaim the raw soul to stdout for the Sentinel to capture.
            print(content)

            return self.success("The soul has been proclaimed.")
        except Exception as e:
            # We must ensure any failure is loud for the Sentinel.
            raise ArtisanHeresy(f"Gaze upon the soul failed: {e}", child_heresy=e)