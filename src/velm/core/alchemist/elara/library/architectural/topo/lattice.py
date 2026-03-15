# Path: core/alchemist/elara/library/architectural/topo/lattice.py
# ----------------------------------------------------------------

from typing import List, Any

class LatticeOracle:
    """
    =============================================================================
    == THE LATTICE ORACLE (V-Ω-TOTALITY)                                       ==
    =============================================================================
    LIF: ∞ | ROLE: DAG_AND_CAUSAL_SCRYER

    [ASCENSIONS 9-12]:
    9. Global Symbol Table introspection.
    10. Downstream Blast-Radius computation.
    11. Dead-Code Branch Isolation.
    12. Ouroboros Loop Detection in dependency graphs.
    """
    def __init__(self, engine_ref: Any):
        self.engine = engine_ref

    def is_imported(self, symbol_name: str) -> bool:
        """[ASCENSION 9]: Verifies if a symbol is bound to the Causal Mind."""
        if not self.engine or not hasattr(self.engine, 'cortex'): return False
        try:
            return symbol_name in self.engine.cortex.get_global_symbols()
        except: return False

    def dependents(self, path_str: str) -> List[str]:
        """[ASCENSION 10]: Calculates the blast radius if this file is mutated."""
        if not self.engine or not hasattr(self.engine, 'cortex'): return[]
        try:
            return self.engine.cortex.get_dependents(path_str)
        except: return[]

    def is_circular(self) -> bool:
        """[ASCENSION 12]: Senses topological deadlock in current generation."""
        # Integrates with the Tarjan Scryer in the Causal Linker
        if hasattr(self.engine, 'transactions'):
            return getattr(self.engine.transactions, 'has_cycle', False)
        return False