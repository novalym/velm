# Path: scaffold/artisans/distill/core/slicer/weavers/contracts.py
# ----------------------------------------------------------------

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

from ..contracts import CodeSegment, RelevanceLevel, SymbolNode

@dataclass(frozen=True)
class WeaveContext:
    """
    The Gnostic Vessel of Weaving.
    It carries the complete, immutable state of the scripture and the
    Architect's will into the heart of a Weaving Strategy.
    """
    file_path: Path
    lines: List[str]
    scores: Dict[str, RelevanceLevel]
    graph_roots: List[SymbolNode]
    merged_segments: List[CodeSegment]