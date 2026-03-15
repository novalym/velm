# Path: parser_core/parser/ast_weaver/weaver/engine.py
# ----------------------------------------------------


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

# [THE ASCENDED TYPE]: The Sacred Quaternity
Quaternity = Tuple[str, int, Optional[List[str]], Optional[List[str]]]


class GnosticASTWeaver:
    """
    =================================================================================
    == THE HIEROPHANT OF THE GNOSTIC TREE (V-Ω-TOTALITY-V45-ENUM-EXORCIST)         ==
    =================================================================================
    LIF: ∞ | ROLE: TOPOLOGICAL_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_AST_WEAVER_V45_ENUM_EXORCIST_FINALIS_2026

    The supreme architect of the Abstract Syntax Tree. It has been ascended to
    enforce the **Law of Spatial Resonance**, annihilating the 'Ghost Directory'
    paradox by synchronizing the Mind with the Map.

    ### THE PANTHEON OF 13 NEW LEGENDARY ASCENSIONS:
    13. **The Omni-Enum Exorcist (THE MASTER CURE):** Mathematically annihilates
        the Stringification Heresy by comparing normalized string values,
        regardless of how Pydantic or JSON-RPC mangled the original Enum object.
    [... prior 12 ascensions retained ...]
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
        == THE GRAND RITE OF WEAVING (V-Ω-SPATIAL-SYNC-V45)                        ==
        =============================================================================
        Transmutes the flat `raw_items` list into a hierarchical Gnostic AST.
        """
        root = self.factory.forge_root()
        stack_mgr = StackManager(root)

        if not self.parser.raw_items:
            self.Logger.warn("AST Weaver received a void. No raw items to weave.")
            return root

        # Trust the sequential, depth-first order from the initial parse
        causal_timeline = self.parser.raw_items

        self.Logger.verbose(f"AST Weaver: Orchestrating spatial resonance for {len(causal_timeline)} atoms...")

        for item in causal_timeline:

            # =========================================================================
            # == [ASCENSION 13]: THE OMNI-ENUM EXORCIST (THE MASTER CURE)            ==
            # =========================================================================
            line_type_name = "UNKNOWN"
            if hasattr(item.line_type, 'name'):
                line_type_name = item.line_type.name
            elif isinstance(item.line_type, str):
                line_type_name = item.line_type.split('.')[-1].upper()
            elif isinstance(item.line_type, int):
                try:
                    line_type_name = GnosticLineType(item.line_type).name
                except Exception:
                    pass

            # 1. THE VOID SENTINEL
            # Variables and Traits are state definitions, not physical matter.
            if line_type_name in ("VARIABLE", "TRAIT_DEF", "TRAIT_USE"):
                continue

            # 2. [ASCENSION 32]: THE RESILIENCE WARD
            try:
                # A. ALIGN THE GEOMETRY
                stack_mgr.adjust_for_item(item)

                # B. PERCEIVE THE LOCUS
                parent_node = stack_mgr.current_node
                parent_phys_path = stack_mgr.current_phys_path

                # =========================================================================
                # == [ASCENSION 33]: THE SPATIAL ANCHOR SYNC                             ==
                # =========================================================================
                posix_parent = str(parent_phys_path).replace('\\', '/')
                if posix_parent == ".": posix_parent = ""

                # Suture the anchor into the Parser's variable space
                self.parser.variables["__current_dir__"] = posix_parent

                if item.path:
                    posix_file = str(item.path).replace('\\', '/')
                    self.parser.variables["__current_file__"] = posix_file
                # =========================================================================

                # --- PATH A: LOGIC & TEMPLATES ---
                if line_type_name in ("LOGIC", "SGF_CONSTRUCT"):
                    new_node = self.factory.forge_logic_node(item)
                    parent_node.children.append(new_node)

                    # [ASCENSION 9]: Closure Divination
                    is_pure_closer = LogicGatekeeper.is_pure_closer(item)
                    if not is_pure_closer:
                        # Descend into the logic branch
                        stack_mgr.push(new_node, item.original_indent, parent_phys_path)

                # --- PATH B: FORM & KINETIC WILL ---
                else:
                    # Files, Directories, and Edicts masquerading as Form
                    self.mason.weave_form_item(item, parent_node, parent_phys_path, stack_mgr)

            except Exception as paradox:
                self.Logger.error(f"L{item.line_num}: AST Weaving Paradox: {paradox}")
                continue

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
        """
        # [ASCENSION 10]: Delegates to the specialized bridge to ensure type purity.
        return DimensionalBridge.resolve_paths_from_ast(self.parser, node)

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_AST_WEAVER anchor={self.parser.project_root.name} status=RESONANT>"