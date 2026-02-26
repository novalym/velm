# Path: parser_core/parser/ast_weaver/stack_manager/engine.py
# -----------------------------------------------------------

from pathlib import Path
from typing import List, Tuple

from ..contracts import StackFrame
from .state import StackState
from .alignment import AlignmentOracle
from .....contracts.data_contracts import _GnosticNode, ScaffoldItem
from .....logger import Scribe

Logger = Scribe("ASTStackManager")


class StackManager:
    """
    =============================================================================
    == THE SOVEREIGN OF THE STACK (V-Ω-TOTALITY-FACADE)                        ==
    =============================================================================
    LIF: ∞ | ROLE: TOPOLOGICAL_COORDINATOR | RANK: OMEGA_SOVEREIGN

    The unified public gateway to the newly ascended Directory Sanctum.
    It orchestrates the `StackState` and the `AlignmentOracle` to provide a
    seamless, indestructible API for the `GnosticASTWeaver`.
    """

    def __init__(self, root_node: _GnosticNode):
        """[THE RITE OF INCEPTION] Forges the memory and the algorithm."""
        self._state = StackState(root_node)
        self._oracle = AlignmentOracle(self._state)

    # --- THE PUBLIC PROPERTIES (O(1) PROXY) ---

    @property
    def current_frame(self) -> StackFrame:
        return self._state.current_frame

    @property
    def current_node(self) -> _GnosticNode:
        """[ASCENSION 24]: The Finality Vow. Always returns a valid GnosticNode."""
        return self._state.current_node

    @property
    def current_phys_path(self) -> Path:
        return self._state.current_phys_path

    # --- THE KINETIC RITES ---

    def adjust_for_item(self, item: ScaffoldItem):
        """
        The Grand Rite of Alignment.
        Delegates the complex spatial mathematics to the AlignmentOracle.
        """
        # [ASCENSION 20]: Heresy-Resilient Fallback
        try:
            self._oracle.adjust(item)
        except Exception as e:
            Logger.error(f"Topological Fracture during alignment: {e}. Defaulting to Root.")
            # Emergency Reset to Root to save the Weaver
            while not self._state.current_frame.is_root:
                self._state.pop("Emergency Reset")

    def push(self, node: _GnosticNode, indent: int, path_context: Path):
        """Delegates the push operation to the State organ."""
        self._state.push(node, indent, path_context)

    def __repr__(self) -> str:
        return f"<Ω_STACK_MANAGER facade_active state={self._state}>"