# Path: core/lsp/scaffold_features/symbols/providers/maestro.py
# -------------------------------------------------------------

import re
from typing import Optional
from ....base.types import DocumentSymbol, SymbolKind
from .base import BaseSymbolProvider

class MaestroProvider(BaseSymbolProvider):
    """
    [THE WILL OF THE MAESTRO]
    Maps %% edicts (Lifecycle hooks, Traits).
    """

    PATTERN = re.compile(r'^\s*%%\s+([\w\-\s]+)')

    def extract(self, line_num: int, raw_line: str, stripped: str) -> Optional[DocumentSymbol]:
        match = self.PATTERN.match(raw_line)
        if match:
            name = match.group(1).strip()
            detail = "Kinetic Will"
            kind = SymbolKind.Namespace

            if name.startswith("trait"):
                kind = SymbolKind.Class
                detail = "Architectural Trait"
                name = name.replace("trait", "").strip()
            elif name.startswith("use"):
                kind = SymbolKind.Interface
                detail = "Trait Injection"
                name = name.replace("use", "").strip()

            return self.forge_vessel(
                name=f"Edict: {name}",
                detail=detail,
                kind=kind,
                line=line_num,
                start_col=raw_line.find("%%"),
                length=len(stripped)
            )
        return None