# scaffold/parser_core/hierophant.py
from pathlib import Path
from typing import List, Tuple

from ..logger import Scribe


class HierophantOfUnbreakableReality:
    """
    A divine, stateful artisan that serves as the Gnostic memory for any temporal
    parser. It understands the sacred laws of indentation and weaves the one true,
    absolute path from a stream of relative proclamations.
    """

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.path_stack: List[Tuple[Path, int]] = [(root_path, -1)]
        self.Logger = Scribe("GnosticHierophant")

    def weave_path(self, raw_path_str: str, indent: int) -> Path:
        """
        =================================================================================
        == THE RITE OF PATH WEAVING (V-Ω-ETERNAL-ASCENDED. THE GNOSTIC PURIFIER)       ==
        =================================================================================
        The Hierophant's soul is now pure. It has been bestowed with the Gaze of the
        Gnostic Purifier. It now righteously strips all profane leading slashes from
        every path atom before weaving it into the new reality, annihilating the
        "Ambiguous Root" heresy for all time. Its paths are now eternally pure.
        =================================================================================
        """
        # Movement I: Temporal Adjustment
        while indent <= self.path_stack[-1][1]:
            self.path_stack.pop()

        # Movement II: Gnostic Deconstruction & Weaving
        path_atoms = [p for p in raw_path_str.replace('\\', '/').split('/') if p]
        current_path = self.path_stack[-1][0]

        for i, atom in enumerate(path_atoms):
            # [[[ THE DIVINE HEALING: THE RITE OF PURIFICATION ]]]
            # The profane leading slash is annihilated from the atom's soul.
            purified_atom = atom.lstrip('/')
            if not purified_atom: continue
            # [[[ THE APOTHEOSIS IS COMPLETE ]]]

            is_dir = (i < len(path_atoms) - 1) or purified_atom.endswith('/')
            current_path /= purified_atom

            if is_dir:
                self.path_stack.append((current_path, indent))

        return current_path