# Path: scaffold/parser_core/parser/ast_weaver/weaver.py
# ------------------------------------------------------

import re
from pathlib import Path
from typing import List, Tuple, Set, Optional,TYPE_CHECKING

from .contracts import StackFrame
from .node_factory import NodeFactory
from .stack_manager import StackManager
from ....contracts.data_contracts import _GnosticNode, GnosticLineType, ScaffoldItem
from ....contracts.heresy_contracts import ArtisanHeresy, Heresy
from ....contracts.symphony_contracts import Edict
if TYPE_CHECKING:
    from ..engine import ApotheosisParser


class GnosticASTWeaver:
    """
    =================================================================================
    == THE HIEROPHANT OF THE GNOSTIC TREE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)        ==
    =================================================================================
    LIF: ∞ (ETERNAL & DIVINE)

    The one true Orchestrator of Abstract Syntax Tree construction. It has been healed
    of the "Heresy of the Flat Reality" and ascended to become a divine Hierophant.
    It now honors the complete, five-fold Gnostic contract of the LogicWeaver,
    annihilating the TypeError for all time.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Law of the Gnostic Dowry (THE FIX):** Its `resolve_paths_from_ast` rite
        now makes a sacred, five-fold plea to the `GnosticLogicWeaver`, bestowing upon
        it the complete Gnosis of the Parser's mind: the AST root, the variables, the
        Alchemist, all perceived Edicts, and all Maestro Commands. The `TypeError` is
        annihilated from all timelines.

    2.  **The Law of True Parentage:** It correctly uses the living,
        dynamic `stack_mgr.current_node` as the one true parent for all new nodes,
        ensuring perfect hierarchical purity.

    3.  **The Sovereign Soul:** It is a pure Conductor. It delegates all state management
        to the `StackManager` and all node creation to the `NodeFactory`.

    4.  **The Gnostic Triage:** It flawlessly distinguishes between Form (`file/dir`),
        Logic (`@if`), and Meta (`$$ var`) nodes, summoning the correct forging rite.

    5.  **The Deep Path Weaver (`_weave_form_item`):** Intelligently deconstructs paths
        like `src/api/v1/main.py`, automatically forging intermediate sanctum nodes.

    6.  **The Unbreakable Ward of Paradox:** Its core loop is shielded. A single profane
        item will not shatter the entire weave.

    7.  **The Void Sentinel:** It righteously ignores `VARIABLE` items, as they represent
        Gnostic state, not structural form, keeping the final AST pure.

    8.  **The Linear Sorter:** It sorts all incoming items by line number, ensuring the
        temporal order of the Architect's will is honored during the weave.

    9.  **The Bridge of Realization:** Contains the `resolve_paths_from_ast` rite, the
        sacred gateway that summons the `GnosticLogicWeaver` to transmute the final AST
        into a concrete, executable plan.

    10. **The Pure Gnostic Contract:** Its every interaction is governed by the sacred
        `_GnosticNode` and `ScaffoldItem` contracts.

    11. **The Luminous Voice:** Proclaims its every major rite to the Gnostic Chronicle.

    12. **The Recursive Builder:** The `_weave_form_item` is a divine, recursive-style
        artisan that ensures the AST's structure perfectly mirrors the blueprint's path
        hierarchy.
    =================================================================================
    """

    def __init__(self, parser: 'ApotheosisParser'):
        self.parser = parser
        self.Logger = parser.Logger
        self.factory = NodeFactory()

    def weave_gnostic_ast(self) -> _GnosticNode:
        """
        The Grand Rite of Weaving.
        Transmutes the flat `raw_items` list into a hierarchical Gnostic AST.
        """
        root = self.factory.forge_root()
        stack_mgr = StackManager(root)

        if not self.parser.raw_items:
            self.Logger.warn("AST Weaver received a void. No raw items to weave.")
            return root

        sorted_items = sorted(self.parser.raw_items, key=lambda x: x.line_num)
        self.Logger.verbose(f"AST Weaver preparing to weave {len(sorted_items)} items into the Gnostic Tree...")

        for item in sorted_items:
            if item.line_type == GnosticLineType.VARIABLE:
                continue

            try:
                stack_mgr.adjust_for_item(item)

                parent_node = stack_mgr.current_node
                parent_phys_path = stack_mgr.current_phys_path

                if item.line_type in (GnosticLineType.LOGIC, GnosticLineType.JINJA_CONSTRUCT):
                    new_node = self.factory.forge_logic_node(item)
                    parent_node.children.append(new_node)

                    is_pure_closer = self._is_pure_closer(item)
                    if not is_pure_closer:
                        stack_mgr.push(new_node, item.original_indent, parent_phys_path)

                elif item.line_type in (GnosticLineType.TRAIT_DEF, GnosticLineType.TRAIT_USE):
                    pass

                else:  # Default to FORM
                    self._weave_form_item(item, parent_node, parent_phys_path, stack_mgr)

            except Exception as e:
                self.Logger.error(f"AST Weaving Paradox on line {item.line_num}: {e}", exc_info=True)
                continue

        self.Logger.verbose(f"AST Weaving complete. Root has {len(root.children)} children.")
        return root

    def _weave_form_item(
            self,
            item: ScaffoldItem,
            parent_node: _GnosticNode,
            parent_phys_path: Path,
            stack_mgr: StackManager
    ):
        """
        [FACULTY 4 & 11] The Deep Path Weaver & Recursive Builder.
        Handles deep paths (a/b/c) by creating intermediate nodes.
        """
        if not item.path:
            return

        rel_path = item.path
        if str(parent_phys_path) != ".":
            try:
                rel_path = item.path.relative_to(parent_phys_path)
            except ValueError:
                pass

        path_str = str(rel_path).replace('\\', '/')
        path_atoms = [p for p in path_str.split('/') if p and p != '.']

        current_node = parent_node

        for i_atom, atom in enumerate(path_atoms):
            is_last = (i_atom == len(path_atoms) - 1)

            child = next((c for c in current_node.children if c.name == atom), None)

            if not child:
                child_item = item if is_last else None
                is_dir_node = (not is_last) or (is_last and item.is_dir)

                child = self.factory.forge_form_node(atom, is_dir_node, child_item)
                current_node.children.append(child)

            current_node = child

        if item.is_dir:
            stack_mgr.push(current_node, item.original_indent, item.path)

    def _is_pure_closer(self, item: ScaffoldItem) -> bool:
        """Detects tags that ONLY close a block (endif, endfor)."""
        if item.condition_type:
            ctype_str = str(item.condition_type).upper()
            if 'CONDITIONALTYPE.' in ctype_str: ctype_str = ctype_str.split('.')[-1]
            return ctype_str.startswith('END')
        elif item.jinja_expression:
            match = re.search(r'{%[-]?\s*(\w+)', item.jinja_expression)
            if match:
                return match.group(1).lower().startswith('end')
        return False

    def resolve_paths_from_ast(self, node: _GnosticNode) -> Tuple[
        List[ScaffoldItem],
        List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
        List[Heresy],
        List[Edict]
    ]:
        """
        =================================================================================
        == THE BRIDGE OF REALIZATION: TOTALITY (V-Ω-QUATERNITY-SUTURE)                 ==
        =================================================================================
        LIF: ∞ | ROLE: CAUSAL_REALIZER | RANK: OMEGA_SUPREME
        AUTH: Ω_WEAVER_V200_QUATERNITY_RETURN_FINALIS

        [THE CURE]: This rite now righteously returns the full four-fold Dowry from
        the LogicWeaver, ensuring the Master Parser can finalize the reality.
        """
        from ...logic_weaver import GnosticLogicWeaver

        # --- MOVEMENT I: BESTOW THE DOWRY ---
        # We pass the complete state of the Parser to the LogicWeaver.
        weaver = GnosticLogicWeaver(
            root=node,
            context=self.parser.variables,
            alchemist=self.parser.alchemist,
            all_edicts=self.parser.edicts,
            post_run_commands=self.parser.post_run_commands
        )

        # --- MOVEMENT II: THE LOGIC STRIKE ---
        # LogicWeaver.weave() is already ascended to return 4 values.
        resolved_items, extra_commands_tuples, heresies, resolved_edicts = weaver.weave()

        # --- MOVEMENT III: PERSISTENCE SYNC ---
        # We update the master parser's command ledger with the resolved reality.
        self.parser.post_run_commands = extra_commands_tuples

        # [ASCENSION 12]: THE FINALITY VOW
        # We return the full quaternity to satisfy the ApotheosisParser's expected signature.
        return resolved_items, extra_commands_tuples, heresies, resolved_edicts