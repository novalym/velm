# Path: parser_core/parser/ast_weaver/stack_manager/state.py
# ----------------------------------------------------------

import threading
from pathlib import Path
from typing import List, Optional, Deque
from collections import deque

from ..contracts import StackFrame
from .....contracts.data_contracts import _GnosticNode
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....logger import Scribe

Logger = Scribe("StackState")


class StackState:
    """
    =============================================================================
    == THE KEEPER OF DIMENSIONS (V-Ω-THREAD-SAFE-MEMORY)                       ==
    =============================================================================
    Manages the raw memory array of the AST hierarchy.
    It guarantees Absolute Root Warding and Thread-Safe Mutability.
    """

    # [ASCENSION 13]: Depth-Limit Sarcophagus
    MAX_STACK_DEPTH = 256

    def __init__(self, root_node: _GnosticNode):
        self._lock = threading.RLock()

        # The Living Timeline
        self._stack: List[StackFrame] = [
            StackFrame(node=root_node, indent=-1, physical_path=Path("."))
        ]

        # [ASCENSION 7]: Temporal Frame Preservation (Forensic Trail)
        self._ghost_trail: Deque[StackFrame] = deque(maxlen=10)

    @property
    def current_frame(self) -> StackFrame:
        """[ASCENSION 3]: O(1) Frame Resolution."""
        return self._stack[-1]

    @property
    def current_node(self) -> _GnosticNode:
        return self._stack[-1].node

    @property
    def current_phys_path(self) -> Path:
        return self._stack[-1].physical_path

    @property
    def depth(self) -> int:
        return len(self._stack)

    def push(self, node: _GnosticNode, indent: int, path_context: Path):
        """
        [ASCENSION 14]: State-Machine Purity.
        Safely descends into a deeper topological layer.
        """
        with self._lock:
            if self.depth >= self.MAX_STACK_DEPTH:
                raise ArtisanHeresy(
                    f"Topological Overflow: Maximum AST nesting depth ({self.MAX_STACK_DEPTH}) breached.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Flatten your logic. The God-Engine rejects infinite recursion."
                )

            frame = StackFrame(node, indent, path_context)
            self._stack.append(frame)

    def pop(self, reason: str = "Dedent"):
        """
        [ASCENSION 4]: Absolute Root Warding.
        Safely ascends out of the current topological layer.
        """
        with self._lock:
            if len(self._stack) <= 1:
                Logger.warn(f"Geometric Paradox: Attempted to pop the Eternal Root. Reason: {reason}. Denied.")
                return

            # Eject the soul and add it to the Ghost Trail for forensics
            ghost_frame = self._stack.pop()
            self._ghost_trail.append(ghost_frame)

            # [ASCENSION 11]: Metabolic Logging Triage
            # Logger.verbose(f"   <- Popped '{ghost_frame.node.name}' ({reason})")

    def __repr__(self) -> str:
        return f"<Ω_STACK_STATE depth={self.depth} active_node='{self.current_node.name}'>"