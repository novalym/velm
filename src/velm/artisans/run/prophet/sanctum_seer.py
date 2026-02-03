# Path: scaffold/artisans/run/prophet/sanctum_seer.py
# ---------------------------------------------------

"""
=================================================================================
== THE SANCTUM SEER (V-Ω-LEGENDARY-ARCHAEOLOGIST)                              ==
=================================================================================
A divine artisan that gazes upon a directory's soul (its manifest files) to
divine the Architect's one true intent for its execution.
=================================================================================
"""
from pathlib import Path

from .grimoire import SANCTUM_FINGERPRINTS
from ....logger import Scribe


class SanctumSeer:
    """The Archaeologist of the Sanctum."""

    def __init__(self, logger: Scribe):
        self.logger = logger

    def divine(self, directory: Path) -> str:
        """Performs a Gaze upon a directory's contents."""
        files = {f.name for f in directory.iterdir()}

        for fingerprint in SANCTUM_FINGERPRINTS:
            if fingerprint["manifest"] in files:
                self.logger.verbose(
                    f"  -> Sanctum Seer's Gaze: Found '{fingerprint['manifest']}'. Divining rite as '{fingerprint['rite']}'.")
                return fingerprint["rite"]

        self.logger.warn(f"Sanctum Seer's Gaze on '{directory.name}' is a void. No entry point found.")
        return "unknown_dir"