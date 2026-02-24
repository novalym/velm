# Path: artisans/dream/archetype_indexer/scanner.py
# -------------------------------------------------

import os
from pathlib import Path
from typing import Generator


class GnosticScanner:
    """
    =============================================================================
    == THE SPATIAL SENTINEL (V-Ω-MULTIVERSAL-WALKER)                           ==
    =============================================================================
    Walks the three planes of existence to find Blueprints:
    1. The Local Sanctum (Project Root)
    2. The User's Grimoire (~/.scaffold)
    3. The System Core (Bundled)
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def scan(self) -> Generator[Path, None, None]:
        """Yields paths to every .scaffold file in the known universe."""

        # 1. Local Project
        yield from self._walk(self.project_root / ".scaffold" / "archetypes")

        # 2. User Global
        yield from self._walk(Path.home() / ".scaffold" / "archetypes")

        # 3. System Bundled (Relative to the package install)
        # We ascend from this file to find the root 'archetypes' folder
        try:
            # artisans/dream/archetype_indexer/scanner.py -> ... -> velm/archetypes
            system_root = Path(__file__).parents[4] / "archetypes"
            if system_root.exists():
                yield from self._walk(system_root)
        except Exception:
            pass

    def _walk(self, root: Path) -> Generator[Path, None, None]:
        if not root.exists(): return

        # We use os.walk for speed and control
        for dirpath, _, filenames in os.walk(root):
            for f in filenames:
                if f.endswith((".scaffold", ".arch")):
                    yield Path(dirpath) / f