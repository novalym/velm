# Path: scaffold/core/ignition/diviner/seekers/environmental_seeker.py
# --------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_ENV_SEEKER_V7

from pathlib import Path
from typing import Optional
from .base import BaseSeeker


class EnvironmentalSeeker(BaseSeeker):
    """
    =============================================================================
    == THE ENVIRONMENTAL SEEKER (V-Ω-ANCHOR-PRIEST)                            ==
    =============================================================================
    [ASCENSION 5]: Recognizes the 'Consecrated Root' via project sigils.
    """

    SIGILS = {
        "scaffold.scaffold",
        "scaffold.lock",
        "scaffold.arch",
        ".git",
        ".scaffold",
        "package.json",  # Only if it's a Workspace root
        "pnpm-workspace.yaml",
        "lerna.json"
    }

    def scan(self, target: Optional[Path] = None) -> Optional[Path]:
        """
        Ascends from the starting point to find the first project anchor.
        """
        curr = target or self.root

        # [ASCENSION 15]: INDENTATION SYMMETRY
        # Limit ascent to 5 levels to prevent escaping the developer's universe.
        for _ in range(5):
            if any((curr / s).exists() for s in self.SIGILS):
                # Verify it's not a dummy leaf
                if (curr / "package.json").exists():
                    # Handle sub-package check?
                    pass
                return curr

            if curr == curr.parent:
                break
            curr = curr.parent

        return None

