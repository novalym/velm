# Path: parser_core/parser/ast_weaver/stack_manager/alignment.py
# --------------------------------------------------------------

import time
from typing import Optional

from .state import StackState
from .adjudicator import SiblingAdjudicator
from .....contracts.data_contracts import GnosticLineType, ScaffoldItem
from .....logger import Scribe

Logger = Scribe("ASTAlignmentOracle")


class AlignmentOracle:
    """
    =============================================================================
    == THE GEOMETRIC ALIGNMENT ORACLE (V-Ω-UNIVERSAL-SIBLING-SUTURE)           ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: TOPOLOGICAL_PHYSICIST

    Contains the pure algorithmic loop that aligns a new item into the AST based
    on its visual depth (indentation) and its semantic meaning.
    """

    def __init__(self, state: StackState):
        self.state = state
        self.adjudicator = SiblingAdjudicator()

    def adjust(self, item: ScaffoldItem):
        """
        [THE GRAND RITE OF ALIGNMENT]
        Loops continuously, adjusting the stack depth until perfect equilibrium
        is achieved with the incoming item.
        """
        # [ASCENSION 22]: Metabolic Tomography
        start_ns = time.perf_counter_ns()

        while True:
            top = self.state.current_frame

            # 1. Root Guard: Never pop the absolute root.
            if top.is_root:
                break

            # 2. Child Case: Item is deeper than current top -> We are inside it.
            if item.original_indent > top.indent:
                # [ASCENSION 17]: Semantic Indentation Validation
                # If the jump is massive (e.g., 20 spaces deeper suddenly), we could warn,
                # but structurally, it's valid as a child.
                break

            # 3. Dedent Case: Item is shallower -> Pop stack to find parent.
            if item.original_indent < top.indent:
                self.state.pop(f"Dedent ({item.original_indent} < {top.indent})")
                continue

            # =========================================================================
            # == 4. THE UNIVERSAL SIBLING CONVERGENCE (THE ASCENDED CURE)            ==
            # =========================================================================
            # [ASCENSION 1]: If the new item has the EXACT same indentation as the
            # current active block, it CANNOT be a child of that block. It MUST be
            # popped to become a sibling.
            if item.original_indent == top.indent:

                # A. The Logic Suture: Check if this new item explicitly CLOSES the
                # current logic block (e.g., an @else closing an @if).
                if self.adjudicator.is_closing_tag_for(item, top.node):
                    self.state.pop(f"Logic Closure ({item.raw_scripture.strip()} closes {top.node.name})")
                    continue

                # B. The Form Exorcism: [ASCENSION 8]
                if top.node.item and top.node.item.line_type == GnosticLineType.FORM:
                    # A file cannot have children. Even if a user messes up indentation,
                    # we enforce that a file is a leaf node.
                    self.state.pop("Form Sibling Convergence")
                    continue

                # C. The Universal Law of Siblings
                # If it's not a closing tag, but they share exact indentation, the active
                # block is implicitly closed. We MUST POP to ensure the new item attaches
                # to the parent, creating a true sibling relationship.
                # Example:
                # @if foo:
                #    >> command_1
                # >> command_2 (This must be a sibling to @if, not a child!)
                self.state.pop(f"Universal Sibling Convergence (Indent: {item.original_indent})")
                continue

            # If we somehow fall through the topological matrix, we break to avoid infinity.
            break

        # Record Metric
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if duration_ms > 5.0:
            Logger.warn(f"Heavy Topological Alignment: {duration_ms:.2f}ms for '{item.path}'")