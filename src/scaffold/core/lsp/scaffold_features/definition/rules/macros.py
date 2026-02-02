# Path: core/lsp/scaffold_features/definition/rules/macros.py
# -----------------------------------------------------------

import re
from typing import Optional
from ....base.features.definition.contracts import DefinitionRule
from ....base.features.definition.models import Location, Range, Position
from ....base.document import TextDocument
from ....base.utils.text import WordInfo


class MacroRule(DefinitionRule):
    """
    [THE MACRO-MANCER]
    Jumps from an @call or macro usage to its @macro definition.
    """

    @property
    def name(self) -> str:
        return "Macro"

    @property
    def priority(self) -> int:
        return 95  # High priority, second only to Variables

    def matches(self, info: WordInfo) -> bool:
        # Matches tokens that look like function calls or follow @call
        return "@call" in info.line_text or "(" in info.text

    def resolve(self, doc: TextDocument, info: WordInfo) -> Optional[Location]:
        # 1. Purify the Macro Name
        # e.g., @call my_macro(args) -> my_macro
        name = info.text.split('(')[0].replace('@call', '').strip()
        if not name: return None

        # 2. LOCAL SCAN (Immediate Reality)
        # Search for: @macro name
        pattern = re.compile(rf'^\s*@macro\s+{re.escape(name)}\b')

        lines = doc.text.splitlines()
        for i, line in enumerate(lines):
            if pattern.search(line):
                return Location(
                    uri=doc.uri,
                    range=Range(start=Position(line=i, character=0), end=Position(line=i, character=0))
                )

        # 3. GLOBAL FALLBACK (The Mirror)
        # If not found locally, we poll the Daemon via the GlobalCortexRule
        # (which should be registered after this one).
        return None