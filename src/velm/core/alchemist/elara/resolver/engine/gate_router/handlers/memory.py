# Path: core/alchemist/elara/resolver/engine/gate_router/handlers/memory.py
# --------------------------------------------------------------------------

from typing import List, TYPE_CHECKING
from .....contracts.atoms import ASTNode, GnosticToken
from ....context import LexicalScope
from ....pipeline import FilterPipeline
from ........logger import Scribe

if TYPE_CHECKING:
    from ...spooler import LaminarStreamSpooler
    from ...resolver import RecursiveResolver

Logger = Scribe("MemoryHandlers")


class MemoryHandlers:
    """Handles set, with, and export variable states."""

    @staticmethod
    def handle_set(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                   spooler: 'LaminarStreamSpooler'):
        """[GAP 1]: The 'Set Block' Heresy. Allows {% set x %}...{% endset %}"""
        expression = node.metadata.get("expression", "")

        # Scenario A: Inline Assignment ({% set x = 5 %})
        if '=' in expression:
            k, v = [x.strip() for x in expression.split('=', 1)]
            try:
                val = FilterPipeline.execute(v, scope)
                scope.set_local(k, val)
            except Exception as e:
                Logger.warn(f"L{node.token.line_num}: Set Assignment fractured: {e}")
            return

        # Scenario B: Block Assignment ({% set x %}...{% endset %})
        var_name = expression.strip()
        if not var_name: return

        block_output = []
        set_scope = scope.spawn_child(name=f"set_{var_name}")

        for child in node.children:
            resolver._walk(child, set_scope, block_output, spooler)

        # Stringify the captured AST block and bind it
        captured_matter = "".join(str(t.content) for t in block_output if t.content is not None)
        scope.set_local(var_name, captured_matter)

    @staticmethod
    def handle_with(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                    spooler: 'LaminarStreamSpooler'):
        """[GAP 2]: The 'With Scope' Paradox. Ephemeral state isolation."""
        expression = node.metadata.get("expression", "")
        with_scope = scope.spawn_child(name=f"with_block_{node.token.line_num}")

        if expression:
            parts = [p.strip() for p in expression.split(',')]
            for part in parts:
                if '=' in part:
                    k, v = [x.strip() for x in part.split('=', 1)]
                    try:
                        val = FilterPipeline.execute(v, scope)
                        with_scope.set_local(k, val)
                    except:
                        pass

        for child in node.children:
            resolver._walk(child, with_scope, output, spooler)

    @staticmethod
    def handle_export(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                      spooler: 'LaminarStreamSpooler'):
        expression = node.metadata.get("expression", "")
        if '=' in expression:
            k, v = [x.strip() for x in expression.split('=', 1)]
            try:
                val = FilterPipeline.execute(v, scope)
                scope.set_global(k, val)
            except Exception as e:
                Logger.warn(f"L{node.token.line_num}: Global Export fractured: {e}")