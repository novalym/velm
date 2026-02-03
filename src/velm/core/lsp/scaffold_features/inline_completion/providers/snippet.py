# Path: core/lsp/scaffold_features/inline_completion/providers/snippet.py
# -----------------------------------------------------------------------

import re
from typing import List
from ....base.features.inline_completion.contracts import InlineCompletionProvider
from ....base.features.inline_completion.models import InlineCompletionItem, InlineCompletionParams


class SnippetProphet(InlineCompletionProvider):
    """
    [THE REFLEX]
    Fast, local heuristics (autoclose, common patterns).
    """

    @property
    def name(self) -> str:
        return "Reflex"

    @property
    def priority(self) -> int:
        return 100

    def prophesy(self, params: InlineCompletionParams) -> List[InlineCompletionItem]:
        uri = str(params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc: return []

        line = doc.get_line(params.position.line)
        prefix = line[:params.position.character]

        # 1. AUTOCLOSE JINJA
        if prefix.endswith("{{ ") and "}}" not in line:
            return [InlineCompletionItem(insertText=" }}")]

        # 2. AUTOCLOSE BLOCK
        if prefix.strip() == "%%" and "post-run" not in line:
            return [InlineCompletionItem(insertText=" post-run")]

        return []