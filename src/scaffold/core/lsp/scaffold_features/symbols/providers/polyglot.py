# Path: core/lsp/scaffold_features/symbols/providers/polyglot.py
# --------------------------------------------------------------

import re
from typing import Optional
from ....base.types import DocumentSymbol, SymbolKind
from .base import BaseSymbolProvider

class PolyglotProvider(BaseSymbolProvider):
    """
    [THE TOWER OF BABEL]
    Maps embedded language blocks (python:, rust:, etc.).
    """

    PATTERN = re.compile(r'^\s*([a-z]+):(?:\s*)$')
    LANGS = {'py', 'python', 'js', 'node', 'ts', 'rs', 'rust', 'go', 'sh', 'bash', 'sql'}

    def extract(self, line_num: int, raw_line: str, stripped: str) -> Optional[DocumentSymbol]:
        match = self.PATTERN.match(raw_line)
        if match:
            lang = match.group(1).lower()
            if lang in self.LANGS:
                return self.forge_vessel(
                    name=f"Polyglot: {lang}",
                    detail="Foreign Logic Block",
                    kind=SymbolKind.Module,
                    line=line_num,
                    start_col=raw_line.find(lang),
                    length=len(lang) + 1
                )
        return None