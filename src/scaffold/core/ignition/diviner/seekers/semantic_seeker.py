# Path: scaffold/core/ignition/diviner/seekers/semantic_seeker.py
# -------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_SEMANTIC_SEEKER_V7

from pathlib import Path
from typing import Optional
from .base import BaseSeeker


class SemanticSeeker(BaseSeeker):
    """
    =============================================================================
    == THE SEMANTIC SEEKER (V-Ω-DIRECTORY-DIVINATION)                         ==
    =============================================================================
    [ASCENSION 7]: Understands the purpose of folder naming conventions.
    """

    # High-confidence indicators of a Logic Root
    LOGIC_SANCTUMS = {
        "src", "app", "lib", "source", "core", "packages", "internal", "api", "cmd", "pkg"
    }

    def scan(self, target: Optional[Path] = None) -> Optional[Path]:
        curr = target or self.root

        try:
            for item in self.safe_iter(curr):
                if item.is_dir() and item.name.lower() in self.LOGIC_SANCTUMS:
                    # [ASCENSION 27]: If we find a 'src' folder, the root is likely its parent.
                    return curr
        except:
            pass

        return None

