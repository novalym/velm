# Path: artisans/dream/archetype_indexer/contracts.py
# ---------------------------------------------------

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Set


@dataclass
class ArchetypeSoul:
    """
    =============================================================================
    == THE SOUL OF THE BLUEPRINT (V-Ω-METADATA-VESSEL)                         ==
    =============================================================================
    A distilled, searchable representation of a .scaffold file.
    """
    id: str  # Unique slug (e.g. "python/fastapi-basic")
    path: Path  # Physical location

    # --- EXPLICIT GNOSIS (From Headers) ---
    title: str = ""
    summary: str = ""
    tags: Set[str] = field(default_factory=set)
    author: str = "Unknown"

    # --- IMPLICIT GNOSIS (From Structural DNA) ---
    inferred_tags: Set[str] = field(default_factory=set)
    file_signatures: Set[str] = field(default_factory=set)  # e.g. {"Dockerfile", "cargo.toml"}

    # --- KINETIC REQUIREMENTS ---
    required_vars: List[str] = field(default_factory=list)

    # --- THE SEARCH VECTOR ---
    lexical_corpus: str = ""  # The flattened string for BM25 indexing

    def merge_tags(self):
        """Unifies explicit and inferred tags for the search index."""
        return self.tags.union(self.inferred_tags)


