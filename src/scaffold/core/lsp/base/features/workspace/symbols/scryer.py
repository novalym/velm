# Path: core/lsp/features/workspace/symbols/scryer.py
# ----------------------------------------------------
import re
from typing import List
from .models import WorkspaceSymbol
from ....types.primitives import Location, Range, Position
from ....types.symbols import SymbolKind


class LocalScryer:
    """[THE RADIANT SCANNER] Scans the current active buffer and local roots."""

    def __init__(self, server):
        self.server = server
        # Regex for Scaffold particles: $$ var, let var, @macro name
        self.VAR_PATTERN = re.compile(r'^\s*(\$\$|let|def|const|@macro)\s+([a-zA-Z_]\w*)')

    def scan(self, query: str) -> List[WorkspaceSymbol]:
        results = []
        q_lower = query.lower()

        # Scan all open documents (The most current reality)
        for uri in self.server.documents.open_uris:
            doc = self.server.documents.get(uri)
            if not doc: continue

            lines = doc.text.splitlines()
            for i, line in enumerate(lines):
                match = self.VAR_PATTERN.match(line)
                if match:
                    sigil, name = match.groups()
                    if q_lower in name.lower():
                        results.append(WorkspaceSymbol(
                            name=name,
                            kind=SymbolKind.Variable if sigil != "@macro" else SymbolKind.Function,
                            location=Location(
                                uri=uri,
                                range=Range(
                                    start=Position(line=i, character=line.find(name)),
                                    end=Position(line=i, character=line.find(name) + len(name))
                                )
                            ),
                            score=1.0 if name.lower().startswith(q_lower) else 0.8,
                            source="LOCAL"
                        ))
        return results