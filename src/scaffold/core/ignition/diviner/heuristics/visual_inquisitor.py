# Path: scaffold/core/ignition/diviner/heuristics/visual_inquisitor.py
# -------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_VISUAL_INQUISITOR_V1

from pathlib import Path
from typing import Tuple, List
from .base import BaseInquisitor
from ...contracts import IgnitionAura

class VisualInquisitor(BaseInquisitor):
    """Detects purely visual/static realities."""

    def analyze(self, root: Path) -> Tuple[IgnitionAura, float, List[str]]:
        if (root / "index.html").exists():
            # [ASCENSION 8]: ARTIFACT FORENSICS
            # If there's an index.html in a dist/build folder, it's very likely static
            is_artifact = root.name in ["dist", "build", "out", "public"]
            confidence = 0.9 if is_artifact else 0.4
            return IgnitionAura.STATIC, confidence, [f"Static HTML seed found in {root.name}."]

        return IgnitionAura.GENERIC, 0.0, []