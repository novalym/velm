# Path: core/lsp/scaffold_features/symbols/providers/logic.py
# -----------------------------------------------------------

import re
from typing import Optional
from ....base.types import DocumentSymbol, SymbolKind
from .base import BaseSymbolProvider

class LogicProvider(BaseSymbolProvider):
    """
    [THE LOGIC GEOMETER]
    Maps control flow directives (@if, @for, @macro).
    """

    # Matches: @if condition, @for item in list, @macro name(args)
    PATTERN = re.compile(r'^\s*@([a-zA-Z_]\w*)(?:\s+(.*))?')

    def extract(self, line_num: int, raw_line: str, stripped: str) -> Optional[DocumentSymbol]:
        if not stripped.startswith("@"): return None

        match = self.PATTERN.match(raw_line)
        if not match: return None

        directive, args = match.groups()
        args = args or ""

        # Ignore closing tags to prevent clutter
        if directive.startswith("end") or directive in ("else", "elif"): return None

        name = f"@{directive}"
        detail = "Logic Gate"
        kind = SymbolKind.Interface

        if directive == "if":
            kind = SymbolKind.Boolean
            detail = f"Condition: {args.strip()}"
        elif directive == "for":
            kind = SymbolKind.Array
            detail = f"Loop: {args.strip()}"
        elif directive == "macro":
            kind = SymbolKind.Function
            macro_name = args.split('(')[0].strip()
            name = f"Macro: {macro_name}"
            detail = "Definition"
        elif directive == "include":
            kind = SymbolKind.Module
            include_path = args.strip().strip("'\"")
            name = f"Include: {include_path}"
            detail = "Composition"

        return self.forge_vessel(
            name=name,
            detail=detail,
            kind=kind,
            line=line_num,
            start_col=raw_line.find("@"),
            length=len(name)
        )