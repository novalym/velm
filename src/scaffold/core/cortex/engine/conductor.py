# Path: core/cortex/engine/conductor.py
# -------------------------------------

import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Set

# --- THE DIVINE SUMMONS ---
from .perception import PerceptionEngine
from .analysis import AnalysisEngine
from ..contracts import CortexMemory, SymbolEntry
from ..vector import VectorCortex
from ....logger import Scribe

Logger = Scribe("GnosticCortex")


class GnosticCortex:
    """
    =================================================================================
    == THE GNOSTIC CORTEX (V-Ω-NEURAL-HIVE-MIND)                                   ==
    =================================================================================
    @gnosis:title The Gnostic Cortex
    @gnosis:LIF INFINITY

    The Central Intelligence.
    It holds the **Structural Graph** (Files) and the **Symbolic Lattice** (Definitions).

    [ASCENDED CAPABILITIES]:
    1.  **Instant Symbol Resolution:** O(1) lookup for "Where is 'UserClass' defined?"
    2.  **Lazy Gaze:** Subsystems (Vector, Analysis) awake only when summoned.
    3.  **Fractal Memory:** State is preserved across rites via the `_memory` vessel.
    """

    def __init__(self, project_root: Path):
        self.logger = Logger
        self.root = project_root.resolve()

        # --- Organs ---
        self._perception_engine: Optional[PerceptionEngine] = None
        self._analysis_engine: Optional[AnalysisEngine] = None
        self._vector_cortex_instance: Optional[VectorCortex] = None

        # --- The Akashic Memory ---
        self._memory: Optional[CortexMemory] = None

        # [ASCENSION 1]: THE SYMBOLIC LATTICE
        # Map[SymbolName, List[SymbolEntry]]
        # Allows instant jump-to-definition across the entire project.
        self._symbol_index: Dict[str, List[SymbolEntry]] = {}
        self._indexed_files: Set[Path] = set()

    # --- CONFIGURATION RITES ---

    def configure_filters(self, ignore: List[str] = None, include: List[str] = None):
        """Configures the Gaze of Aversion."""
        self.perception_engine.configure_filters(ignore=ignore, include=include)

    # --- LAZY FACULTIES ---

    @property
    def perception_engine(self) -> PerceptionEngine:
        if self._perception_engine is None:
            self._perception_engine = PerceptionEngine(self.root)
        return self._perception_engine

    @property
    def analysis_engine(self) -> AnalysisEngine:
        if self._analysis_engine is None:
            if self._memory is None: self.perceive()
            self._analysis_engine = AnalysisEngine(self.root, self._memory)
        return self._analysis_engine

    @property
    def vector_cortex(self) -> VectorCortex:
        if self._vector_cortex_instance is None:
            self._vector_cortex_instance = VectorCortex(self.root)
        return self._vector_cortex_instance

    # --- PRIMARY RITES ---

    def perceive(self, force_refresh: bool = False) -> CortexMemory:
        """
        [THE RITE OF AWAKENING]
        Scans the physical reality to build the Structural Graph.
        Does NOT parse content (that is for the Indexer).
        """
        if self._memory and not force_refresh:
            return self._memory

        Logger.info(f"The Cortex awakens. Mapping topology of '{self.root.name}'...")
        start_time = time.monotonic()

        self._memory = self.perception_engine.perceive()

        duration = time.monotonic() - start_time
        Logger.success(f"Topology Mapped in {duration:.2f}s. {len(self._memory.inventory)} nodes active.")
        return self._memory

    # --- SYMBOLIC INTELLIGENCE (THE PYCHARM KILLER) ---

    def memorize_symbols(self, file_path: Path, symbols: List[SymbolEntry]):
        """
        [THE RITE OF INSCRIPTION]
        Called by the IndexerArtisan to inject knowledge into the Hive Mind.
        """
        # 1. Clear old symbols for this file (Re-indexing)
        # (Optimization: We could track reverse map, but for V1 we just append)
        # In a real heavy system, we'd remove old entries first.

        for sym in symbols:
            if sym.name not in self._symbol_index:
                self._symbol_index[sym.name] = []
            self._symbol_index[sym.name].append(sym)

        self._indexed_files.add(file_path)

    def locate_symbol(self, name: str) -> List[SymbolEntry]:
        """
        [THE RITE OF RECALL]
        Instant O(1) lookup for a symbol definition.
        """
        return self._symbol_index.get(name, [])

    def is_indexed(self, path: Path) -> bool:
        """Checks if a file's soul has been consumed."""
        return path in self._indexed_files

    # --- HEALING & MAINTENANCE ---

    def ingest_file(self, path: Path):
        """Incremental update of structure."""
        if not self._memory: self.perceive()
        self._memory = self.perception_engine.ingest_file(path, self._memory)
        # Note: We do not auto-index here. The Watchdog triggers the Indexer.

    def forget_file(self, path: Path):
        """Surgical oblivion."""
        if not self._memory: return
        self._memory = self.perception_engine.forget_file(path, self._memory)
        if path in self._indexed_files:
            self._indexed_files.remove(path)
            # Pruning the symbol index is expensive O(N), so we let it drift slightly
            # or handle it in a background gc cycle.