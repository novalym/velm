# Path: scaffold/creator/io_controller/path_alchemist.py
from __future__ import annotations
from pathlib import Path
from typing import Union, Dict, Any

from ...core.alchemist import get_alchemist
from ...contracts.heresy_contracts import ArtisanHeresy


class PathAlchemist:
    """
    =================================================================================
    == THE ALCHEMIST OF PATHS (V-Ω-TRANSMUTATION-ENGINE)                           ==
    =================================================================================
    A specialist artisan whose one true purpose is to transmute the Gnostic variables
    (e.g., `{{project_slug}}`) within a path string into their final, concrete form.
    It is the mind that perceives the final destination before the journey begins.
    =================================================================================
    """

    def __init__(self, gnosis: Dict[str, Any]):
        self.gnosis = gnosis
        self.alchemist = get_alchemist()

    def transmute(self, logical_path: Union[str, Path]) -> str:
        """
        Performs the Rite of Path Transmutation.
        Raises a Heresy if the path contains untransmuted Gnosis after the rite.
        """
        path_str = str(logical_path)

        # The Gaze of Prudence: a swift check to avoid unnecessary rites.
        if "{{" not in path_str:
            return path_str

        transmuted_path = self.alchemist.transmute(path_str, self.gnosis)

        # The Final Adjudication: a check for Gnostic residue.
        if "{{" in transmuted_path or "}}" in transmuted_path:
            raise ArtisanHeresy(
                f"Transmutation Heresy: The path '{str(logical_path)}' contains untransmuted Gnosis after final alchemy.",
                suggestion="Ensure all variables used in the path are defined in the Gnostic Context."
            )

        return transmuted_path