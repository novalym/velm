# Path: scaffold/artisans/lint/engine.py
# --------------------------------------
from typing import List, Dict, Type
from .contracts import LintContext, LintIssue
from .rules.base import GnosticRule
from .rules.graph import OrphanRule, OuroborosRule
from .rules.structural import PropheticStructureRule


class GnosticLintEngine:
    """The Engine that drives the Adjudication."""

    def __init__(self):
        self.rules: List[GnosticRule] = [
            OrphanRule(),
            OuroborosRule(),
            PropheticStructureRule()
        ]

    def register_rule(self, rule: GnosticRule):
        self.rules.append(rule)

    def conduct_inquest(self, context: LintContext) -> List[LintIssue]:
        issues = []
        for rule in self.rules:
            # Future: Filter by context.category if requested
            issues.extend(list(rule.check(context)))
        return issues