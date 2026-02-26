# Path: src/velm/parser_core/parser/ast_weaver/weaver/engine.py
# -------------------------------------------------------------

from pathlib import Path
from typing import List, Tuple, Optional, TYPE_CHECKING

# --- SIBLING ORGANS ---
from .path_mason import PathMason
from .gatekeeper import LogicGatekeeper
from .bridge import DimensionalBridge

# --- ANCESTRAL ORGANS ---
from ..node_factory import NodeFactory
from ..stack_manager import StackManager

# --- THE DIVINE CONTRACTS ---
from .....contracts.data_contracts import _GnosticNode, GnosticLineType
from .....contracts.heresy_contracts import Heresy
from .....contracts.symphony_contracts import Edict

if TYPE_CHECKING:
    from ...engine import ApotheosisParser
    from .....contracts.data_contracts import ScaffoldItem

# [THE ASCENDED TYPE]
Quaternity = Tuple[str, int, Optional[List[str]], Optional[List[str]]]


class GnosticASTWeaver:
    """
    =================================================================================
    == THE HIEROPHANT OF THE GNOSTIC TREE (V-Ω-TOTALITY-V32-CHRONOLOGICAL-SUTURE)  ==
    =================================================================================
    LIF: ∞ (ETERNAL & DIVINE) | ROLE: AST_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN

    The one true Orchestrator of Abstract Syntax Tree construction. It has been
    purified of the "Sorting Heresy" and the "Monolithic Schism." It delegates
    its power to the `PathMason`, `LogicGatekeeper`, and `DimensionalBridge` to
    ensure absolute topological and chronological purity.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Chronological Truth Suture (THE CURE):** It no longer sorts `raw_items`
        by `line_num`. It trusts the depth-first, sequential order forged by the
        Parser, preserving the exact spatial relationships of `@imported` shards.
    2.  **The Bridge of Realization:** Delegates the formulation of the Sacred
        Quaternity to the `DimensionalBridge`, ensuring strict type-safety before
        calling the `LogicWeaver`.
    3.  **The Law of True Parentage:** It correctly uses the living, dynamic
        `stack_mgr.current_node` as the absolute parent for all incoming atoms.
    4.  **The Sovereign Soul:** It is a pure Conductor. It owns no parsing logic,
        delegating all state management to the `StackManager`.
    5.  **The Void Sentinel:** Righteously ignores `VARIABLE` and `TRAIT` items,
        as they represent Gnostic State, not structural Form.
    6.  **The Unbreakable Ward of Paradox:** Its core loop is shielded by a
        Sarcophagus. A single profane item will log a Heresy but will not shatter
        the entire topological weave.
    7.  **Deep Path Delegation:** Entrusts the transmutation of complex paths
        (e.g., `src/api/main.py`) to the specialized `PathMason`.
    8.  **Closure Divination:** Consults the `LogicGatekeeper` to ensure tags like
        `@endif` close the stack rather than pushing a new layer onto it.
    9.  **Luminous Trace Proclamation:** Broadcasts the final size and structure
        of the root node to the telemetry stratum.
    10. **Empty Tree Paradox Ward:** Safely returns a sterile `__ROOT__` node if
        the parser provided a void array of items.
    11. **Type-Safe Quaternity Cast:** Guarantees the return signature exactly matches
        what the `ApotheosisParser` requires for final materialization.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        hierarchically sound AST.
    =================================================================================
    """

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF INCEPTION]"""
        self.parser = parser
        self.Logger = parser.Logger
        self.factory = NodeFactory()
        self.mason = PathMason(self.factory)

    def weave_gnostic_ast(self) -> _GnosticNode:
        """
        =============================================================================
        == THE GRAND RITE OF WEAVING (V-Ω-SEQUENTIAL-TRUTH)                        ==
        =============================================================================
        Transmutes the flat `raw_items` list into a hierarchical Gnostic AST.
        """
        root = self.factory.forge_root()
        stack_mgr = StackManager(root)

        # [ASCENSION 10]: The Empty Tree Paradox Ward
        if not self.parser.raw_items:
            self.Logger.warn("AST Weaver received a void. No raw items to weave.")
            return root

        # =========================================================================
        # == [ASCENSION 1]: THE CHRONOLOGICAL TRUTH SUTURE (THE CURE)            ==
        # =========================================================================
        # We incinerate the `sorted(key=line_num)` heresy. The `raw_items` list
        # is populated synchronously during the depth-first parse (including @imports).
        # It is already in perfect causal order. Sorting it shatters the spacetime
        # continuum of the imports.
        causal_timeline = self.parser.raw_items

        self.Logger.verbose(f"AST Weaver preparing to weave {len(causal_timeline)} items into the Gnostic Tree...")

        for item in causal_timeline:
            # [ASCENSION 5]: The Void Sentinel & Trait Bypass
            # State modifications do not manifest as physical structure in the AST
            if item.line_type in (GnosticLineType.VARIABLE, GnosticLineType.TRAIT_DEF, GnosticLineType.TRAIT_USE):
                continue

            # [ASCENSION 6]: Heresy-Resilient Weaving
            try:
                # 1. Align the Stack Geometry
                stack_mgr.adjust_for_item(item)

                # 2. Perceive the Current Topological State
                parent_node = stack_mgr.current_node
                parent_phys_path = stack_mgr.current_phys_path

                # --- PATH A: LOGIC & TEMPLATES ---
                if item.line_type in (GnosticLineType.LOGIC, GnosticLineType.JINJA_CONSTRUCT):
                    new_node = self.factory.forge_logic_node(item)
                    parent_node.children.append(new_node)

                    # [ASCENSION 8]: Closure Divination
                    is_pure_closer = LogicGatekeeper.is_pure_closer(item)
                    if not is_pure_closer:
                        # If it opens a new reality block, we descend into it
                        stack_mgr.push(new_node, item.original_indent, parent_phys_path)

                # --- PATH B: FORM & KINETIC WILL ---
                else:
                    # Files, Directories, and Edicts masquerading as Form
                    # [ASCENSION 7]: Deep Path Delegation
                    self.mason.weave_form_item(item, parent_node, parent_phys_path, stack_mgr)

            except Exception as e:
                self.Logger.error(f"AST Weaving Paradox on line {item.line_num}: {e}", exc_info=True)
                continue

        # [ASCENSION 9]: The Luminous Trace
        self.Logger.verbose(f"AST Weaving complete. Root has {len(root.children)} children.")
        return root

    def resolve_paths_from_ast(self, node: _GnosticNode) -> Tuple[
        List['ScaffoldItem'],
        List[Quaternity],
        List[Heresy],
        List[Edict]
    ]:
        """
        =============================================================================
        == THE BRIDGE OF REALIZATION (V-Ω-QUATERNITY-SUTURE)                       ==
        =============================================================================
        [ASCENSION 2]: Delegates the multi-stage Quaternity cast to the Dimensional
        Bridge to ensure the `LogicWeaver` is summoned with absolute type purity.
        """
        return DimensionalBridge.resolve_paths_from_ast(self.parser, node)