# Path: scaffold/core/ignition/diviner/sentinel/biology.py
# --------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: SENTINEL_BIOLOGY_V1

import sys
from pathlib import Path
from typing import List
from ..contracts import IgnitionAura


class BiologicalAuditor:
    """
    =============================================================================
    == THE BIOLOGICAL AUDITOR (V-Ω-LATTICE-HEALTH)                             ==
    =============================================================================
    [ASCENSION 16]: Checks for project-bound dependency artifacts.
    """

    @classmethod
    def audit_lungs(cls, root: Path, aura: IgnitionAura) -> List[str]:
        missing = []

        # NODE BIOLOGY
        node_auras = {IgnitionAura.VITE, IgnitionAura.NEXT, IgnitionAura.NUXT, IgnitionAura.ASTRO}
        if aura in node_auras:
            if not (root / "node_modules").is_dir():
                missing.append("node_modules")

        # PYTHON BIOLOGY
        python_auras = {IgnitionAura.FASTAPI, IgnitionAura.FLASK, IgnitionAura.DJANGO}
        if aura in python_auras:
            has_venv = any((root / d).is_dir() for d in [".venv", "venv", "env"])
            # Check if we are outside a virtual reality
            if not has_venv and sys.prefix == sys.base_prefix:
                missing.append("virtual_environment")

        return missing