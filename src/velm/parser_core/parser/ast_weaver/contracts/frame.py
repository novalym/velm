# Path: parser_core/parser/ast_weaver/contracts/frame.py
# ------------------------------------------------------

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Any

from .....contracts.data_contracts import _GnosticNode


@dataclass(frozen=True)
class StackFrame:
    """
    =============================================================================
    == THE STACK FRAME (V-Ω-IMMUTABLE-GEOMETRY-V3)                             ==
    =============================================================================
    LIF: 1,000,000 | ROLE: TOPOLOGICAL_MEMORY_SLICE | RANK: OMEGA_GUARDIAN

    A single, indestructible slice of the Weaver's memory.
    Holds the Node, its visual indentation level, and the physical path context.

    [ASCENSION 2]: Frozen Integrity. This object can never be mutated once born,
    ensuring the historical stack remains a perfect forensic ledger.
    """

    node: _GnosticNode
    indent: int
    physical_path: Path

    # [ASCENSION 6]: The Holographic Origin Hash
    # Captures the precise nanosecond of this frame's creation for temporal sorting
    _birth_ns: int = field(default_factory=time.perf_counter_ns, compare=False, repr=False)

    def __post_init__(self):
        """
        [ASCENSION 3 & 7]: The Null-Byte Suture & Indentation Guard.
        Guarantees the topological coordinates are physically and logically sound.
        """
        # Validate Indentation Boundary
        if self.indent < -1:
            # We use object.__setattr__ because the dataclass is frozen
            object.__setattr__(self, 'indent', -1)

        # Validate Path Purity
        path_str = str(self.physical_path)
        if '\0' in path_str:
            raise ValueError("Geometric Heresy: Null-byte detected in physical path coordinate.")

        # [ASCENSION 8]: Isomorphic Normalization
        normalized_path = Path(path_str.replace('\\', '/'))
        object.__setattr__(self, 'physical_path', normalized_path)

    @property
    def is_root(self) -> bool:
        """
        [ASCENSION 12]: The Finality Vow.
        O(1) calculation of Root status based on absolute indentation logic.
        """
        return self.indent == -1

    @property
    def age_ns(self) -> int:
        """Returns the chronological age of the frame in nanoseconds."""
        return time.perf_counter_ns() - self._birth_ns

    def __repr__(self) -> str:
        # [ASCENSION 10]: Luminous Trace Representation
        node_name = self.node.name if self.node else "VOID"
        return f"<Ω_FRAME indent={self.indent} node='{node_name}' path='{self.physical_path.name}'>"