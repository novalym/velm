# Path: src/velm/parser_core/logic_weaver/traversal.py
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
    == THE WALKER OF WORLDS (V-Ω-QUATERNITY-ASCENDED)                              ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    This is the kinetic engine of the Logic Weaver. It walks the Gnostic AST,
    evaluating logic gates (@if), expanding templates ({{ }}), and—most critically—
    resolving the references to the Maestro's Will.

    [THE ASCENSION]:
    It has been taught the sacred, four-fold tongue. It now stores the complete
    Gnostic Quaternity `(Command, Line, Undo, Heresy)` in its memory map, ensuring
    that the seeds of Redemption (`on-heresy`) travel safely from the Parser to
    the CPU.
    """

    MAX_RECURSION_DEPTH = 100

    def __init__(
            self,
            context: GnosticContext,
            alchemist: DivineAlchemist,
            parser_edicts: List[Edict],
            # [ASCENSION]: The Sacred 4-Tuple Input Type
            parser_post_run: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]]
    ):
        """
        The Rite of Memory Allocation.
        """
        self.gnostic_context = context
        self.alchemist = alchemist
        self.adjudicator = forge_adjudicator(context.raw)

        # --- THE MEMORY OF THE ENGINE ---
        self.items: List[ScaffoldItem] = []

        # [ASCENSION]: The Storage of the Quaternity
        # Holds the resolved list of commands to be executed, in order.
        self.post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []

        self.edicts: List[Edict] = []
        self.heresies: List[Heresy] = []
        self.visibility_map: Dict[int, bool] = {}

        # --- THE MAPS OF RESOLUTION ---
        self.edict_map: Dict[int, Edict] = {e.line_num: e for e in parser_edicts}

        # [ASCENSION]: The Map of Will
        # Indexes the 4-tuples by their line number for O(1) retrieval during traversal.
        self.post_run_map: Dict[int, Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = {
            cmd_tuple[1]: cmd_tuple for cmd_tuple in parser_post_run
        }

        self._materialized_paths: Dict[str, int] = {}

    def traverse(self, node: _GnosticNode, current_path: Path):
        """Entry point for the recursive gaze."""
        if Logger.is_verbose:
            self._dump_ast(node)
        self._recurse(node, current_path, LogicScope(parent_visible=True), depth=0, breadcrumb="ROOT")

    def _dump_ast(self, node: _GnosticNode, depth: int = 0):
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

        # Sort children by line number to preserve temporal order
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

            # [THE GNOSTIC EDICT LINKER]
            elif line_type == GnosticLineType.FORM and hasattr(child.item,
                                                               'edict_type') and child.item.edict_type is not None:
                if scope.parent_visible:
                    edict_soul = self.edict_map.get(child.item.line_num)
                    if edict_soul:
                        self.edicts.append(edict_soul)
                    else:
                        Logger.warn(
                            f"A Gnostic Anchor for an Edict was found at L{child.item.line_num}, but its soul is a void.")

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
        condition = node.item.condition
        if not condition: return True
        try:
            return self.adjudicator.judge_condition(condition, self.gnostic_context.raw)
        except Exception as e:
            Logger.error(f"Logic Heresy at L{node.item.line_num}: {e}")
            self._record_heresy(node, "LOGIC_PARADOX", str(e))
            return False

    def _process_form_node(self, node: _GnosticNode, parent_path: Path, scope: LogicScope, depth: int, breadcrumb: str):
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
        == THE ORACLE OF THE MAESTRO'S WILL (V-Ω-QUATERNITY-RETRIEVAL)                 ==
        =================================================================================
        This is the rite in its final, eternal form.
        It reads the sacred map of line numbers from the AST node and performs a
        high-performant Gaze into its own memory (`post_run_map`) to resurrect the
        one true, four-fold scripture of Will (Cmd, Line, Undo, Heresy).
        """
        if not node.item or not node.item.content:
            return

        import json
        try:
            # The node content is a JSON list of line numbers (the anchors)
            command_line_numbers = json.loads(node.item.content)

            for line_num in command_line_numbers:
                # O(1) Gaze into memory
                command_tuple = self.post_run_map.get(line_num)
                if command_tuple:
                    # [ASCENSION]: We append the full 4-Tuple to the execution plan
                    self.post_run_commands.append(command_tuple)
                else:
                    # Silent resilience for unmatched anchors
                    pass
        except (json.JSONDecodeError, TypeError) as e:
            self.Logger.error(
                f"A paradox occurred while reading the Maestro's Gnostic Map at line {node.item.line_num}: {e}")

    def _record_heresy(self, node: _GnosticNode, key: str, details: str):
        line = node.item.line_num if node.item else 0
        content = node.item.raw_scripture if node.item else node.name
        self.heresies.append(
            Heresy(message=key, line_num=line, line_content=content, details=details, severity=HeresySeverity.CRITICAL))