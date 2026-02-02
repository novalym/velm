# Path: core/lsp/features/symbols/engine.py
# -----------------------------------------

import time
import logging
from typing import List, Tuple, Optional, Any
from .contracts import SymbolProvider
from .models import DocumentSymbol

Logger = logging.getLogger("SymbolEngine")


class SymbolEngine:
    """
    =============================================================================
    == THE HIGH MAPPER (V-Ω-TOTALITY-STACK-ENGINE)                             ==
    =============================================================================
    LIF: 10,000,000 | ROLE: TOPOLOGICAL_RECONSTRUCTOR

    The central intelligence that orchestrates specialized providers and
    reconstructs the document's hierarchical tree using indentation physics.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[SymbolProvider] = []

    def register(self, provider: SymbolProvider):
        """Consecrates a new mapping provider."""
        self.providers.append(provider)
        Logger.debug(f"Symbol Cartographer Registered: {type(provider).__name__}")

    def map_scripture(self, uri: str) -> List[DocumentSymbol]:
        """
        [THE RITE OF CARTOGRAPHY]
        Performs a single-pass hierarchical scan of the document.
        """
        start_time = time.perf_counter()

        doc = self.server.documents.get(uri)
        if not doc: return []

        root_symbols: List[DocumentSymbol] = []

        # [ASCENSION 1]: THE INDENTATION STACK
        # List[Tuple[indent_level, symbol_object]]
        stack: List[Tuple[int, DocumentSymbol]] = []

        lines = doc.text.splitlines()

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped: continue

            # [ASCENSION 6]: CALCULATE GEOMETRIC DEPTH
            # Normalize tabs to 4 spaces for calculation
            indent_str = line[:len(line) - len(stripped)]
            indent_level = len(indent_str.replace('\t', '    '))

            # 1. DIVINE SYMBOL (Polling Providers)
            symbol = self._scry_line(i, line, stripped)

            if symbol:
                # [ASCENSION 2 & 7]: HIERARCHICAL RECONSTRUCTION
                # Pop symbols from stack that are at the same or deeper level
                while stack and stack[-1][0] >= indent_level:
                    stack.pop()

                if stack:
                    # We are a child of the current stack top
                    parent = stack[-1][1]
                    parent.children.append(symbol)

                    # [ASCENSION 4]: DYNAMIC BLOCK EXPANSION
                    # We update the parent's total range to include this child
                    parent.range.end.line = symbol.range.end.line
                    parent.range.end.character = symbol.range.end.character
                else:
                    # We are a root node
                    root_symbols.append(symbol)

                # Push self to stack to potentially capture children
                stack.append((indent_level, symbol))

        duration = (time.perf_counter() - start_time) * 1000
        Logger.debug(f"Cartography of {uri.split('/')[-1]} complete in {duration:.2f}ms.")

        return root_symbols

    def _scry_line(self, line_num: int, raw_line: str, stripped: str) -> Optional[DocumentSymbol]:
        """Ask providers to identify a symbol on this line."""
        for provider in self.providers:
            try:
                symbol = provider.extract(line_num, raw_line, stripped)
                if symbol:
                    return symbol
            except Exception as e:
                Logger.error(f"Provider {type(provider).__name__} failed line {line_num}: {e}")
        return None