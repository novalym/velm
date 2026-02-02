# Path: scaffold/artisans/distill/core/slicer/contracts.py
# --------------------------------------------------------


from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Set, Optional, Dict, Any


class RelevanceLevel(Enum):
    """The Gnostic Weight of a code segment."""
    IRRELEVANT = 0  # Cut completely
    STRUCTURAL = 1  # Keep signature/skeleton (Parent containers)
    DEPENDENCY = 5  # Keep because a focused symbol needs it
    FOCUSED = 10  # The target itself (Full Fidelity)


@dataclass
class SymbolNode:
    """A node in the file's internal dependency graph."""
    name: str
    type: str  # function, class, method, import, var
    start_line: int
    end_line: int
    start_byte: int
    end_byte: int
    children: List['SymbolNode'] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)  # Names of symbols this node uses
    parent_name: Optional[str] = None

    @property
    def signature_end_line(self) -> int:
        """Heuristic for where the signature ends (for skeletonization)."""
        # A more advanced adapter would parse this precisely.
        # For Python, this is often the same as the start_line if it ends with a colon.
        return self.start_line


@dataclass
class CodeSegment:
    """
    =============================================================================
    == THE VESSEL OF SURGICAL INTENT (V-Ω-HEALED)                              ==
    =============================================================================
    A slice of the file to be preserved. It has been healed to carry not just
    the location of the scripture, but the very Gnostic Node that it represents,
    allowing the Weaver to perform more intelligent reconstruction.
    =============================================================================
    """
    start_line: int
    end_line: int
    content: str
    relevance: RelevanceLevel
    # [THE FIX] The vessel is now whole. It can carry the SymbolNode.
    node: Optional[SymbolNode] = None

    def overlaps(self, other: 'CodeSegment') -> bool:
        return max(self.start_line, other.start_line) <= min(self.end_line, other.end_line)

    def merge(self, other: 'CodeSegment') -> 'CodeSegment':
        """Fuses two overlapping segments into a larger reality."""
        new_start = min(self.start_line, other.start_line)
        new_end = max(self.end_line, other.end_line)
        highest_relevance = max(self.relevance.value, other.relevance.value)
        # The first node in a merged sequence is kept as the representative
        return CodeSegment(new_start, new_end, "", RelevanceLevel(highest_relevance), self.node or other.node)


@dataclass
class SliceProfile:
    """Configuration for the surgery."""
    focus_symbols: List[str]
    context_lines: int = 0
    include_imports: bool = True
    skeletonize_remainder: bool = True  # If False, remove remainder entirely

