# Path: parser_core/logic_weaver/traversal/evaluator.py
# -----------------------------------------------------

from typing import Optional
from pathlib import Path

from .context import SpacetimeContext
from ..contracts import LogicScope, ChainStatus
from ....contracts.data_contracts import _GnosticNode
from ....contracts.heresy_contracts import Heresy, HeresySeverity
from ....jurisprudence_core.jurisprudence import forge_adjudicator
from ....logger import Scribe

Logger = Scribe("LogicAdjudicator")


class LogicAdjudicator:
    """
    =============================================================================
    == THE LOGIC ADJUDICATOR (V-Ω-TRUTH-RESOLVER)                              ==
    =============================================================================
    Evaluates Jinja expressions and manages the If/Elif/Else state machine.
    """

    def __init__(self, ctx: SpacetimeContext):
        self.ctx = ctx
        self.adjudicator = forge_adjudicator(ctx.gnostic_context.raw)

    def evaluate_gate(self, node: _GnosticNode, scope: LogicScope) -> bool:
        """
        [THE RITE OF THE GATE]
        Determines if the branch should be entered based on the Chain Status
        and the Jinja condition.
        """
        raw_ctype = node.item.condition_type or ""
        ctype = str(raw_ctype).lower().split('.')[-1]

        should_enter = False

        if ctype == 'if':
            scope.start_chain()
            if self._test_condition(node):
                should_enter = True
                scope.mark_entered()

        elif ctype == 'elif':
            # Only test condition if the chain hasn't been satisfied yet
            if scope.chain_status == ChainStatus.PENDING and self._test_condition(node):
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

        return should_enter

    def _test_condition(self, node: _GnosticNode) -> bool:
        """Invokes the Jinja engine to test the pure condition."""
        condition = node.item.condition
        if not condition:
            return True

        try:
            return self.adjudicator.judge_condition(condition, self.ctx.gnostic_context.raw)
        except Exception as e:
            Logger.error(f"Logic Heresy at L{node.item.line_num}: {e}")
            self.ctx.heresies.append(Heresy(
                message="LOGIC_PARADOX",
                line_num=node.item.line_num,
                line_content=node.item.raw_scripture,
                details=str(e),
                severity=HeresySeverity.CRITICAL
            ))
            return False