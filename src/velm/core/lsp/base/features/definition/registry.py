# Path: core/lsp/features/definition/registry.py
# --------------------------------------------

from typing import List
from .contracts import DefinitionRule

class RuleRegistry:
    """
    [THE HALL OF RECORDS]
    Manages the collection of prioritized navigation strategies.
    """
    def __init__(self):
        self._rules: List[DefinitionRule] = []

    def add(self, rule: DefinitionRule):
        self._rules.append(rule)

    def get_all(self) -> List[DefinitionRule]:
        return sorted(self._rules, key=lambda x: x.priority, reverse=True)