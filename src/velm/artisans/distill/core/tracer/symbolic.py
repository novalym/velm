# Path: artisans/distill/core/tracer/symbolic.py
# ----------------------------------------------

from typing import Set, List
from core.cortex.contracts import CortexMemory

class SymbolicExecutor:
    """
    =============================================================================
    == THE GNOSTIC LINKER (V-Ω-SYMBOL-WALKER)                                  ==
    =============================================================================
    This artisan bridges the gap between Abstract Symbols (e.g., 'User') and
    Concrete Files. It hooks into the CortexMemory to perform O(1) lookups.
    """

    def __init__(self, memory: CortexMemory):
        self.memory = memory

    def find_usages(self, symbol_name: str) -> Set[str]:
        """
        Finds files that likely use a specific symbol.
        Leverages the 'imported_symbols' field in FileGnosis.
        """
        users = set()
        # We iterate the inventory to find who imports this symbol.
        # This relies on the GraphBuilder having populated 'imported_symbols'
        for file in self.memory.inventory:
            if symbol_name in file.imported_symbols:
                users.add(str(file.path).replace('\\', '/'))
        return users

    def resolve_definition(self, symbol_name: str) -> Set[str]:
        """
        Finds the file(s) where a symbol is defined.
        Uses the Cortex's pre-computed symbol_multimap.
        """
        # This relies on the symbol_multimap built by GraphBuilder
        return set(self.memory.symbol_multimap.get(symbol_name, []))