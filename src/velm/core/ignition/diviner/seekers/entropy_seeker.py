# Path: scaffold/core/ignition/diviner/seekers/entropy_seeker.py
# -------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_ENTROPY_SEEKER_V7

import os
from pathlib import Path
from typing import Optional, Dict
from .base import BaseSeeker


class EntropySeeker(BaseSeeker):
    """
    =============================================================================
    == THE ENTROPY SEEKER (V-Ω-DENSITY-MAPPING)                                ==
    =============================================================================
    [ASCENSION 11]: Analyzes where the 'Work' is happening.
    Finds directories with the highest concentration of source code.
    """

    SOURCE_EXTS = {
        ".ts", ".tsx", ".js", ".jsx", ".py",
        ".rs", ".go", ".c", ".cpp", ".java",
        ".php", ".rb", ".swift", ".kt"
    }

    def scan(self, target: Optional[Path] = None) -> Optional[Path]:
        """Hunts for the folder containing the most actual code."""
        start_node = target or self.root
        candidates: Dict[Path, int] = {}

        # Perform a breadth-limited walk
        for root, dirs, files in os.walk(start_node):
            # [ASCENSION 2]: ABYSSAL THROTTLING
            dirs[:] = [d for d in dirs if d not in self.ABYSS and not d.startswith('.')]

            p_root = Path(root)
            # Limit depth to 4 to prevent runaway recursion
            if len(p_root.relative_to(start_node).parts) > 4:
                dirs[:] = []
                continue

            code_count = sum(1 for f in files if Path(f).suffix in self.SOURCE_EXTS)

            if code_count > 0:
                # [ASCENSION 27]: SEMANTIC FOLDER DIVINATION
                # Reward folders like 'src' or 'lib' as roots
                if p_root.name in {"src", "lib", "app", "source"}:
                    candidates[p_root.parent] = candidates.get(p_root.parent, 0) + (code_count * 2)
                else:
                    candidates[p_root] = candidates.get(p_root, 0) + code_count

        if not candidates:
            return None

        # Return the candidate with the highest entropy (code mass)
        winner = max(candidates, key=candidates.get)
        return winner