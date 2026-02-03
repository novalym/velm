# Path: core/lsp/scaffold_features/symbols/providers/matter.py
# ------------------------------------------------------------

import re
from typing import Optional
from ....base.types import DocumentSymbol, SymbolKind
from .base import BaseSymbolProvider

class MatterProvider(BaseSymbolProvider):
    """
    [THE MATTER GEOMETER]
    Maps physical filesystem operations (Creation, Seeding, Linking).
    """

    # Matches: path/to/file :: "content", path << seed, link -> target
    # Excludes lines starting with Gnostic Sigils ($$, %%, @)
    PATTERN = re.compile(
        r'^\s*(?P<path>[\w\.\-\/\{\}\$\@]+)(?:\s*)'
        r'(?P<op>::|<<|->|\+=|-=|~=|\^=)'
        r'(?:\s*)(?P<target>.*)?$'
    )

    def extract(self, line_num: int, raw_line: str, stripped: str) -> Optional[DocumentSymbol]:
        if stripped.startswith(("$", "@", "%", "#")): return None

        match = self.PATTERN.match(raw_line)
        if not match:
            # Check for bare directory blocks (path ending in :)
            if stripped.endswith(":") and not any(s in stripped for s in ('::', '<<')):
                name = stripped.rstrip(":")
                return self.forge_vessel(
                    name=name + "/",
                    detail="Sanctum",
                    kind=SymbolKind.Package,
                    line=line_num,
                    start_col=raw_line.find(name),
                    length=len(name)
                )
            return None

        path, op, target = match.groups()
        name = path.strip().strip("'\"")

        kind = SymbolKind.File
        detail = "Scripture"

        if op == "::":
            detail = "Inline Genesis"
        elif op == "<<":
            detail = "Celestial Seed"
        elif op == "->":
            kind = SymbolKind.Event
            detail = f"Link -> {target.strip()[:20]}"
        elif op in ("+=", "-=", "~=", "^="):
            kind = SymbolKind.Operator
            detail = "Mutation"

        return self.forge_vessel(
            name=name,
            detail=detail,
            kind=kind,
            line=line_num,
            start_col=raw_line.find(path),
            length=len(path)
        )