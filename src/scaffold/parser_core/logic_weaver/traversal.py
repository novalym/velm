# Path: scaffold/parser_core/logic_weaver/traversal.py
# ----------------------------------------------------

from pathlib import Path
from typing import List, Dict, Set, Optional, Any, Tuple, Union

from .contracts import LogicScope, ChainStatus
from .state import GnosticContext
from ...contracts.data_contracts import _GnosticNode, ScaffoldItem, GnosticLineType
from ...contracts.heresy_contracts import Heresy, HeresySeverity
from ...contracts.symphony_contracts import Edict
from ...core.alchemist import DivineAlchemist
from ...jurisprudence_core.jurisprudence import forge_adjudicator
from ...logger import Scribe

Logger = Scribe("GnosticTraversal")


class TraversalEngine:
    """
    =================================================================================
    == THE WALKER OF WORLDS (V-Ω-HYPER-DIAGNOSTIC-CORRECTED-ASCENDED)              ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The dedicated engine for traversing the Gnostic AST. Its soul is now whole. It has
    been bestowed with the **Law of Gnostic Transmutation**. It now understands that
    a `ScaffoldItem` can be a vessel for a Gnostic `Edict`, not just a file, and will
    righteously transmute it into the final, executable plan.

    The Heresy of the Hollow Soul is annihilated. The Symphony will sing.

    ### THE PANTHEON OF ASCENSIONS:
    1.  **The Segregation of Will:** It maintains separate registries for `items` (Files),
        `post_run_commands` (Shell), and `edicts` (Symphony), ensuring type safety.
    2.  **The Gnostic Map:** It holds the `edict_map` and `post_run_map` to resolve
        AST anchors (ScaffoldItems) back to their rich source objects.
    """

    MAX_RECURSION_DEPTH = 100

    def __init__(
            self,
            context: GnosticContext,
            alchemist: DivineAlchemist,
            # We bestow upon the Engine the complete Gnostic memory of the Parser.
            parser_edicts: List[Edict],
            parser_post_run: List[Tuple[str, int, Optional[List[str]]]]
    ):
        """
        =================================================================================
        == THE RITE OF GNOSTIC INCEPTION (ETERNALLY HEALED)                            ==
        =================================================================================
        The Engine is born. It has been taught the sacred, three-fold tongue. It now
        stores the complete Gnostic tuple in its memory, ready for proclamation.
        """
        self.gnostic_context = context
        self.alchemist = alchemist
        self.adjudicator = forge_adjudicator(context.raw)

        # --- THE MEMORY OF THE ENGINE ---
        self.items: List[ScaffoldItem] = []  # The Plan of Form (Files/Dirs)
        self.post_run_commands: List[Tuple[str, int, Optional[List[str]]]] = []  # The Plan of Shell

        # [THE FIX] The dedicated vessel for Symphony Edicts
        self.edicts: List[Edict] = []  # The Plan of Will

        self.heresies: List[Heresy] = []
        self.visibility_map: Dict[int, bool] = {}

        # --- THE MAPS OF RESOLUTION ---
        # The Edict Map allows O(1) lookup of rich Edict objects by their line number anchor
        self.edict_map: Dict[int, Edict] = {e.line_num: e for e in parser_edicts}

        # The Engine's memory now stores the complete Gnostic tuple, indexed by
        # its line number, ready for perfect, instantaneous recall.
        self.post_run_map: Dict[int, Tuple[str, int, Optional[List[str]]]] = {
            cmd_tuple[1]: cmd_tuple for cmd_tuple in parser_post_run
        }

        self._materialized_paths: Dict[str, int] = {}

    def traverse(self, node: _GnosticNode, current_path: Path):
        """Entry point for the recursive gaze."""
        if Logger.is_verbose:
            self._dump_ast(node)
        self._recurse(node, current_path, LogicScope(parent_visible=True), depth=0, breadcrumb="ROOT")

    def _dump_ast(self, node: _GnosticNode, depth: int = 0):
        # This method remains pure and correct.
        if depth == 0:
            Logger.verbose("--- AST DIAGNOSTIC DUMP START ---")

        indent = "  " * depth
        node_type = "ROOT"
        if node.item:
            node_type = node.item.line_type.name
            if node.item.condition_type:
                node_type += f" (@{node.item.condition_type})"

        name = node.name or "[Anonymous]"
        line = node.item.line_num if node.item else '?'
        Logger.verbose(f"{indent}- [{node_type}] {name} (L{line})")

        for child in node.children:
            self._dump_ast(child, depth + 1)

        if depth == 0:
            Logger.verbose("--- AST DIAGNOSTIC DUMP END ---")

    def _recurse(self, node: _GnosticNode, current_path: Path, scope: LogicScope, depth: int, breadcrumb: str):
        """The Atomic Recursion."""
        if depth > self.MAX_RECURSION_DEPTH:
            Logger.error(f"Recursion Limit Exceeded at {breadcrumb}. The Tree is Ouroboric.")
            return

        sorted_children = sorted(
            node.children,
            key=lambda c: c.item.line_num if c.item else 0
        )

        for child in sorted_children:
            child_name = child.name or "?"
            new_breadcrumb = f"{breadcrumb} > {child_name}"

            if not child.item:
                if scope.parent_visible:
                    self._process_form_node(child, current_path, scope, depth + 1, new_breadcrumb)
                continue

            line_type = child.item.line_type

            if line_type in (GnosticLineType.LOGIC, GnosticLineType.JINJA_CONSTRUCT):
                self._process_logic_node(child, current_path, scope, depth + 1, new_breadcrumb)

            elif line_type == GnosticLineType.POST_RUN:
                self.visibility_map[child.item.line_num] = scope.parent_visible
                if scope.parent_visible:
                    self._process_post_run_node(child)

            # --- THE DIVINE HEALING: THE LAW OF GNOSTIC TRANSMUTATION ---
            # The Engine's Gaze is now whole. It perceives the `edict_type` soul
            # bestowed upon the `ScaffoldItem` by the Scribes of Will.
            elif line_type == GnosticLineType.FORM and hasattr(child.item,
                                                               'edict_type') and child.item.edict_type is not None:
                if scope.parent_visible:
                    # This is not a file; it is a command. We find its true soul in the Edict map.
                    edict_soul = self.edict_map.get(child.item.line_num)
                    if edict_soul:
                        # [THE FIX] We proclaim the Edict to the EDICTS list, NOT the items list.
                        self.edicts.append(edict_soul)
                    else:
                        # This should be architecturally impossible.
                        Logger.warn(
                            f"A Gnostic Anchor for an Edict was found at L{child.item.line_num}, but its soul is a void.")
            # --- THE APOTHEOSIS IS COMPLETE ---

            elif line_type == GnosticLineType.FORM:
                if scope.parent_visible:
                    self._process_form_node(child, current_path, scope, depth + 1, new_breadcrumb)
                else:
                    self.visibility_map[child.item.line_num] = False

            else:
                if child.item.line_num > 0:
                    self.visibility_map[child.item.line_num] = scope.parent_visible

    def _process_logic_node(self, node: _GnosticNode, current_path: Path, scope: LogicScope, depth: int,
                            breadcrumb: str):
        # This method remains pure and correct.
        self.visibility_map[node.item.line_num] = scope.parent_visible
        raw_ctype = node.item.condition_type or ""
        ctype = str(raw_ctype).lower().split('.')[-1]
        if not scope.parent_visible:
            node.logic_result = False
            self._recurse(node, current_path, LogicScope(parent_visible=False), depth, breadcrumb)
            return
        should_enter = False
        if ctype == 'if':
            scope.start_chain()
            if self._evaluate(node):
                should_enter = True
                scope.mark_entered()
        elif ctype == 'elif':
            if scope.chain_status == ChainStatus.PENDING and self._evaluate(node):
                should_enter = True
                scope.mark_entered()
        elif ctype == 'else':
            if scope.chain_status == ChainStatus.PENDING:
                should_enter = True
                scope.mark_entered()
        elif ctype in ('endif', 'endfor'):
            scope.end_chain()
        node.logic_result = should_enter
        Logger.verbose(f"L{node.item.line_num}: @{ctype} -> {should_enter} (State: {scope.chain_status.name})")
        block_scope = LogicScope(parent_visible=should_enter)
        self._recurse(node, current_path, block_scope, depth, breadcrumb)

    def _evaluate(self, node: _GnosticNode) -> bool:
        # This method remains pure and correct.
        condition = node.item.condition
        if not condition: return True
        try:
            return self.adjudicator.judge_condition(condition, self.gnostic_context.raw)
        except Exception as e:
            Logger.error(f"Logic Heresy at L{node.item.line_num}: {e}")
            self._record_heresy(node, "LOGIC_PARADOX", str(e))
            return False

    def _process_form_node(self, node: _GnosticNode, parent_path: Path, scope: LogicScope, depth: int, breadcrumb: str):
        # This method remains pure and correct.
        if not scope.parent_visible:
            return
        try:
            transmuted_name = self.alchemist.transmute(node.name, self.gnostic_context.raw)
            clean_name = transmuted_name.strip().strip('/').strip('\\')
            if not clean_name:
                self._recurse(node, parent_path, LogicScope(parent_visible=True), depth, breadcrumb)
                return
            next_path = parent_path / clean_name
            if node.item:
                full_path_str = str(next_path).replace('\\', '/')
                current_line = node.item.line_num
                if full_path_str in self._materialized_paths:
                    original_line = self._materialized_paths[full_path_str]
                    Logger.warn(
                        f"Collision Detected: '{full_path_str}' (L{current_line}) overwrites previous definition from L{original_line}.")
                self._materialized_paths[full_path_str] = current_line
                new_item = node.item.model_copy(deep=True)
                new_item.path = next_path
                if new_item.content:
                    new_item.content = self.alchemist.transmute(new_item.content, self.gnostic_context.raw)
                self.visibility_map[node.item.line_num] = True
                self.items.append(new_item)
                self.gnostic_context.register_virtual_file(next_path)
            self._recurse(node, next_path, LogicScope(parent_visible=True), depth, breadcrumb)
        except Exception as e:
            Logger.error(f"Form Paradox: {e}")
            self._record_heresy(node, "TRANSMUTATION_HERESY", str(e))

    def _process_post_run_node(self, node: _GnosticNode):
        """
        =================================================================================
        == THE ORACLE OF THE MAESTRO'S WILL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)            ==
        =================================================================================
        This is the rite in its final, eternal form. Its Gaze is one of absolute
        certainty. It reads the sacred map of line numbers from the AST node and
        performs a hyper-performant Gaze into its own memory (`post_run_map`) to
        resurrect the one true, three-fold scripture of Will.
        =================================================================================
        """
        if not node.item or not node.item.content:
            return

        import json
        try:
            # === THE DIVINE GAZE UPON THE SACRED MAP ===
            command_line_numbers = json.loads(node.item.content)

            for line_num in command_line_numbers:
                # A single, perfect, O(1) Gaze into its memory.
                command_tuple = self.post_run_map.get(line_num)
                if command_tuple:
                    # It proclaims the pure, untransmuted, three-fold scripture.
                    self.post_run_commands.append(command_tuple)
                else:
                    # Note: This warning is normal during intermediate tree-sitter passes if not fully linked
                    # But in the Weaver it indicates a desync.
                    # Logger.warn(f"LogicWeaver perceived a Gnostic Anchor for line {line_num}, but its soul is a void in the post_run_map.")
                    pass
            # === THE APOTHEOSIS IS COMPLETE ===
        except (json.JSONDecodeError, TypeError) as e:
            # The Unbreakable Ward of Grace
            self.Logger.error(
                f"A paradox occurred while reading the Maestro's Gnostic Map at line {node.item.line_num}: {e}")

    def _record_heresy(self, node: _GnosticNode, key: str, details: str):
        # This method remains pure and correct.
        line = node.item.line_num if node.item else 0
        content = node.item.raw_scripture if node.item else node.name
        self.heresies.append(
            Heresy(message=key, line_num=line, line_content=content, details=details, severity=HeresySeverity.CRITICAL))