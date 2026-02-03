# Path: scaffold/artisans/run/prophet/rite_adjudicator.py
# -------------------------------------------------------

"""
=================================================================================
== THE RITE ADJUDICATOR (V-Ω-LEGENDARY-JUDGE)                                  ==
=================================================================================
A pure Judge that receives a prophesied language and adjudicates the final,
correct rite based on the scripture's form and the state of reality.
=================================================================================
"""
from pathlib import Path

from .grimoire import TEST_FILE_PATTERNS
from ....logger import Scribe


class RiteAdjudicator:
    """The Judge of Rites."""

    def __init__(self, logger: Scribe):
        self.logger = logger

    def adjudicate(self, language: str, project_root: Path) -> str:
        """
        The one true rite of adjudication.
        """
        # Gaze 1: The Gaze of the Chronicle (The Genesis/Transmute Schism)
        if language == 'form':
            is_managed = (project_root / "scaffold.lock").exists()
            final_rite = "transmute" if is_managed else "genesis"
            self.logger.verbose(
                f"  -> Adjudicator's Gaze: Reality is {'Managed' if is_managed else 'Unmanaged'}. Rite is '{final_rite}'.")
            return final_rite

        # Gaze 2: The Gaze of the Inquisitor (Test vs. Run)
        # This is a prophecy for a future ascension where we pass the path here.
        # For now, we assume this logic lives in the Language Oracle based on filename.
        # But this is its true, rightful home.

        return language