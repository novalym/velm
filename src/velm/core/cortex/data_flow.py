# === [scaffold/core/cortex/data_flow.py] - SECTION 1 of 1: The Taint Tracker ===
import re
from typing import List, Dict, Set, Optional
from pathlib import Path
from .contracts import CortexMemory
from ...logger import Scribe

Logger = Scribe("DataFlowEngine")


class DataFlowEngine:
    """
    =============================================================================
    == THE RIVER OF DATA (V-Ω-SYMBOLIC-TAINT-TRACKER)                          ==
    =============================================================================
    LIF: 10,000,000,000

    Traces the flow of 'Tainted Symbols' (variables of interest) across the
    codebase. It uses the Gnostic Cortex's symbol map to jump from file to file.

    Logic:
    1. Find definition of Symbol S.
    2. Find all files that Import S.
    3. Find all files that use S string-wise (heuristic resonance).
    """

    def __init__(self, memory: CortexMemory):
        self.memory = memory

    def trace(self, symbols: List[str]) -> Dict[str, int]:
        """
        Returns a map of {file_path: score_boost}.
        """
        impact_map: Dict[str, int] = {}

        for symbol in symbols:
            Logger.info(f"Tracing the flow of data: [cyan]'{symbol}'[/cyan]...")

            # 1. Direct Definition (Where is it born?)
            # symbol_multimap maps "User" -> ["src/models/user.py"]
            origins = self.memory.symbol_multimap.get(symbol, [])

            # Also check for qualified names e.g. "auth.SECRET_KEY"
            if not origins and "." in symbol:
                simple_name = symbol.split(".")[-1]
                origins = self.memory.symbol_multimap.get(simple_name, [])

            if not origins:
                Logger.verbose(f"   -> Symbol '{symbol}' origin not found in Cortex.")

            # 2. Causality Expansion (Where does it go?)
            tainted_files = set(origins)

            # Scan inventory for usage
            # This is a heuristic scan. A full DFG requires deep AST analysis of every file.
            # We use the "Resonance Judge" logic here: text search in AST-aware context.

            for gnosis in self.memory.inventory:
                path_str = str(gnosis.path).replace('\\', '/')

                # Skip if already tainted (origin)
                if path_str in tainted_files:
                    impact_map[path_str] = impact_map.get(path_str, 0) + 100  # High boost for origin
                    continue

                # Check Imports (Strong Link)
                # If file imports the symbol explicitly
                if symbol in gnosis.imported_symbols:
                    impact_map[path_str] = impact_map.get(path_str, 0) + 50
                    tainted_files.add(path_str)
                    continue

                # Check Content Resonance (Weak Link)
                # Does the file contain the string?
                # We use the pre-computed semantic_tags or check content if available (slow)
                # Fast check: symbol name in AST metrics
                is_used = False
                if gnosis.ast_metrics:
                    # Check function arguments for data passing
                    for func in gnosis.ast_metrics.get('functions', []):
                        if symbol in func.get('args_list', []):
                            is_used = True
                            break

                if is_used:
                    impact_map[path_str] = impact_map.get(path_str, 0) + 25
                    tainted_files.add(path_str)

        Logger.success(f"Data Flow Analysis complete. {len(impact_map)} files touched by the river.")
        return impact_map

