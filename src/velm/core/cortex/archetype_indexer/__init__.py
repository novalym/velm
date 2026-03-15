# Path: artisans/dream/archetype_indexer/__init__.py
# --------------------------------------------------

"""
=================================================================================
== THE OMNISCIENT INDEXER (V-Ω-DEEP-TISSUE-SCANNER)                            ==
=================================================================================
@gnosis:title The Archetype Indexer
@gnosis:summary The sensory organ that digitizes the available blueprints into
                 searchable Gnostic Souls.
@gnosis:LIF INFINITY

It unifies:
1.  **The Scanner:** Locates blueprints across the Multiverse (System/User/Local).
2.  **The Extractor:** Performs Regex Surgery to extract metadata.
3.  **The Biologist:** Analyzes the structural DNA (files created) to infer tags.
"""

from .manager import ArchetypeIndexer
from .contracts import ArchetypeSoul

__all__ = ["ArchetypeIndexer", "ArchetypeSoul"]