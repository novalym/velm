# Path: artisans/dream/archetype_indexer/manager.py
# -------------------------------------------------

from pathlib import Path
from typing import Dict

from .scanner import GnosticScanner
from .extractor import SoulExtractor
from .contracts import ArchetypeSoul
from ....logger import Scribe

Logger = Scribe("Dream:ArchetypeManager")


class ArchetypeIndexer:
    """
    =============================================================================
    == THE INDEX MANAGER (V-Ω-TOTALITY)                                        ==
    =============================================================================
    The Sovereign Interface for the Indexing subsystem.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.scanner = GnosticScanner(project_root)
        self.extractor = SoulExtractor()
        self._cache: Dict[str, ArchetypeSoul] = {}

    def conduct_census(self) -> Dict[str, ArchetypeSoul]:
        """
        Performs the Grand Census.
        Returns a map of {id: Soul}.
        """
        if self._cache: return self._cache

        Logger.debug("Commencing Archetype Census...")
        count = 0

        for path in self.scanner.scan():
            # Generate a relative ID based on its name or parent folder
            # e.g. .../archetypes/api/fastapi.scaffold -> "api/fastapi"
            # This is heuristic; for now we use stem or parent/stem

            # Simple ID strategy: just the filename stem for uniqueness?
            # Better: If in a subdir of 'archetypes', include subdir.
            # For robustness, we use the filename stem as the primary key suffix.
            # Collisions are possible but rare in default sets.
            # V2: Use relative path from the 'archetypes' anchor.

            _id = path.stem
            # If parent is not 'archetypes', prepend it for context (e.g. "cloud/aws")
            if path.parent.name != "archetypes":
                _id = f"{path.parent.name}/{path.stem}"

            if _id not in self._cache:
                soul = self.extractor.extract(path, _id)
                self._cache[_id] = soul
                count += 1

        Logger.debug(f"Census Complete. {count} blueprints indexed.")
        return self._cache