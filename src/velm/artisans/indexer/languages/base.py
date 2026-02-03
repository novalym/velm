# Path: artisans/indexer/languages/base.py
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Pattern
from ....core.cortex.contracts import SymbolEntry, SymbolKind


class BaseLanguageParser(ABC):
    """
    The Immutable Contract for Language Parsing.
    """

    @abstractmethod
    def parse(self, content: str, path: Path) -> List[SymbolEntry]:
        pass

    def _extract(self, pattern: Pattern, content: str, path: Path, kind: SymbolKind) -> List[SymbolEntry]:
        """High-speed regex extraction helper."""
        results = []
        for match in pattern.finditer(content):
            name = match.group(1)
            # O(N) line counting is acceptable for indexing speed vs AST overhead
            line_num = content.count('\n', 0, match.start())

            results.append(SymbolEntry(
                name=name,
                path=path,
                kind=kind,
                line=line_num,
                column=match.start() - content.rfind('\n', 0, match.start()) - 1
            ))
        return results