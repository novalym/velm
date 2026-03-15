# Path: core/alchemist/elara/resolver/inclusion/resolver.py
# -----------------------------------------------------------

import os
from pathlib import Path
from typing import Optional, Any, TYPE_CHECKING
from ......logger import Scribe

if TYPE_CHECKING:
    from ..context import LexicalScope

Logger = Scribe("Inclusion:Compass")


class InclusionResolver:
    """
    =============================================================================
    == THE INCLUSION COMPASS (V-Ω-TOTALITY)                                    ==
    =============================================================================
    LIF: 50,000x | ROLE: TOPOGRAPHICAL_SCRYER
    Surgically locates physical matter across the Multiverse strata.
    """

    @classmethod
    def scry_iron(cls, path_str: str, scope: 'LexicalScope') -> Optional[str]:
        """[ASCENSION 45]: Tiered search through physical Iron."""
        # 1. Access the Iron Proxy (Physical Sensory)
        iron = scope.get("iron")
        if not iron:
            # Fallback to direct OS scry if proxy is unmanifest
            project_root = scope.global_ctx.project_root or Path.cwd()
            target = (project_root / path_str).resolve()
            if target.exists() and target.is_file():
                return target.read_text(encoding='utf-8', errors='ignore')
            return None

        # 2. Project Local
        if iron.exists(path_str):
            return iron.read(path_str)

        # 3. Library Stratum
        lib_path = f".scaffold/library/{path_str}"
        if iron.exists(lib_path):
            return iron.read(lib_path)

        # 4. System Stratum (Iron Core)
        # (Prophecy: Logic for velm/codex/shards lookup)

        return None