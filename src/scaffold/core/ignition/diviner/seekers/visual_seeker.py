# Path: scaffold/core/ignition/diviner/seekers/visual_seeker.py
# ------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_VISUAL_SEEKER_V7

from pathlib import Path
from typing import Optional
from .base import BaseSeeker


class VisualSeeker(BaseSeeker):
    """
    =============================================================================
    == THE OCULAR SEEKER (V-Ω-TOTALITY-FINAL-V2.0-HOMING)                      ==
    =============================================================================
    [ASCENSION 6]: Prioritizes the 'Visible Realm' (HTML) for manifestation.
    """

    # [ASCENSION 6]: THE PRIORITY MATRIX
    # Gravitational mass of standard web-roots.
    WEB_ROOT_SCORES = {
        "dist": 100,
        "build": 95,
        "out": 90,
        "public": 85,
        "www": 80,
        "web": 80,
        "site": 70,
        "client": 60,
        "frontend": 60
    }

    VALID_SEEDS = ["index.html", "index.htm", "main.html", "app.html"]

    def scan(self, target: Optional[Path] = None) -> Path:
        curr = target or self.root

        # 1. Primary Inquest (Current Node)
        if self._has_seed(curr):
            return curr

        # 2. Neighborhood Scoring (Children)
        candidates = []
        for item in self.safe_iter(curr):
            if item.is_dir() and not self.is_abyssal(item):
                score = self.WEB_ROOT_SCORES.get(item.name.lower(), 0)
                if self._has_seed(item):
                    candidates.append((item, 50 + score))

        if candidates:
            # Sort by Gnostic Weight (Highest Score first)
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]

        # 3. Ultimate Fallback
        return curr

    def _has_seed(self, path: Path) -> bool:
        return any((path / s).exists() for s in self.VALID_SEEDS)