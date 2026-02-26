# Path: core/cortex/engine/conductor.py
# -------------------------------------

import time
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Set, Union

# --- THE DIVINE SUMMONS ---
from .perception import PerceptionEngine
from .analysis import AnalysisEngine
from ..contracts import CortexMemory, SymbolEntry
from ..vector import VectorCortex
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("GnosticCortex")


class GnosticCortex:
    """
    =================================================================================
    == THE GNOSTIC CORTEX (V-Ω-TOTALITY-V5000-CONDUCTOR-ASCENDED)                  ==
    =================================================================================
    @gnosis:title The Gnostic Cortex
    @gnosis:LIF INFINITY | ROLE: CENTRAL_INTELLIGENCE_GOVERNOR

    The supreme orchestrator of perception and memory.
    It holds the **Structural Graph** (Files) and the **Symbolic Lattice** (Definitions).
    Now ascended with **Forensic Fingerprinting** to detect dimensional drift.
    =================================================================================
    """

    def __init__(self, project_root: Path):
        """[THE RITE OF INCEPTION]"""
        self.logger = Logger
        self.root = project_root.resolve()

        # --- ORGANS (LAZY MATERIALIZATION) ---
        self._perception_engine: Optional[PerceptionEngine] = None
        self._analysis_engine: Optional[AnalysisEngine] = None
        self._vector_cortex_instance: Optional[VectorCortex] = None

        # --- THE AKASHIC MEMORY ---
        self._memory: Optional[CortexMemory] = None

        # [ASCENSION 1]: THE SYMBOLIC LATTICE
        self._symbol_index: Dict[str, List[SymbolEntry]] = {}
        self._indexed_files: Set[Path] = set()

        # [ASCENSION 8]: THE FINGERPRINT CACHE
        self._hash_cache: Dict[Path, str] = {}

    # =========================================================================
    # == SECTION I: THE GAZE OF ESSENCE (FINGERPRINTING)                     ==
    # =========================================================================

    def scry_hash(self, path: Union[str, Path]) -> str:
        """
        =============================================================================
        == THE ORACLE OF ESSENCE (V-Ω-TOTALITY-SCRY-HASH)                          ==
        =============================================================================
        LIF: 100x | ROLE: FORENSIC_BIOPSY | RANK: OMEGA

        Performs a cryptographic biopsy of a scripture's soul (content).
        Returns a SHA-256 fingerprint. Warded against existence paradoxes.
        """
        target = Path(path).resolve() if isinstance(path, str) else path.resolve()

        # 1. THE VOID CHECK
        if not target.exists() or not target.is_file():
            return "0xVOID"

        # 2. CHRONOCACHE PROBE
        # We scry the cache to see if the soul is already known.
        # (Future: Compare mtime for cache invalidation)
        if target in self._hash_cache:
            return self._hash_cache[target]

        # 3. THE KINETIC STRIKE (HASHING)
        try:
            hasher = hashlib.sha256()
            # We read in 64KB shards to preserve heap memory during heavy scrying
            with open(target, 'rb') as f:
                for shard in iter(lambda: f.read(65536), b""):
                    hasher.update(shard)

            fingerprint = hasher.hexdigest()
            self._hash_cache[target] = fingerprint
            return fingerprint

        except Exception as e:
            self.logger.warn(f"Gaze clouded on essence of '{target.name}': {e}")
            return "0xHERESY"

    def scry_diff(self, path_a: Path, path_b: Path) -> bool:
        """
        [ASCENSION 3]: THE DUAL-REALITY MIRROR.
        Adjudicates if two scriptures share the same soul.
        True if bit-perfect congruent, False if divergent.
        """
        return self.scry_hash(path_a) == self.scry_hash(path_b)

    def scry_mass(self, path: Path) -> int:
        """[ASCENSION 2]: APOPHATIC MASS TOMOGRAPHY."""
        if not path.exists(): return 0
        return path.stat().st_size

    # =========================================================================
    # == SECTION II: LAZY FACULTIES & PERCEPTION                             ==
    # =========================================================================

    @property
    def perception_engine(self) -> PerceptionEngine:
        if self._perception_engine is None:
            self._perception_engine = PerceptionEngine(self.root)
        return self._perception_engine

    @property
    def analysis_engine(self) -> AnalysisEngine:
        if self._analysis_engine is None:
            self._ensure_memory()
            self._analysis_engine = AnalysisEngine(self.root, self._memory)
        return self._analysis_engine

    @property
    def vector_cortex(self) -> VectorCortex:
        if self._vector_cortex_instance is None:
            self._vector_cortex_instance = VectorCortex(self.root)
        return self._vector_cortex_instance

    def perceive(self, force_refresh: bool = False, deep_scan: bool = False) -> CortexMemory:
        """
        [THE RITE OF AWAKENING]
        Scans physical reality to build the Structural Graph.
        """
        if self._memory and not force_refresh:
            return self._memory

        self.logger.info(f"The Cortex awakens. Mapping topology of '{self.root.name}'...")
        start_time = time.monotonic()

        self._memory = self.perception_engine.perceive()

        # [ASCENSION 9]: HYDRAULIC CACHE WARMING
        if deep_scan:
            self.logger.verbose("Initiating Deep Tissue Biopsy (Hashing Entire Project)...")
            for node in self._memory.inventory:
                if not node.is_dir:
                    self.scry_hash(node.path)

        duration = time.monotonic() - start_time
        self.logger.success(f"Topology Mapped in {duration:.2f}s. {len(self._memory.inventory)} nodes active.")
        return self._memory

    def _ensure_memory(self):
        """[ASCENSION 4]: NONETYPE SARCOPHAGUS."""
        if self._memory is None:
            self.perceive()

    # =========================================================================
    # == SECTION III: SYMBOLIC INTELLIGENCE                                  ==
    # =========================================================================

    def memorize_symbols(self, file_path: Path, symbols: List[SymbolEntry]):
        """[THE RITE OF INSCRIPTION]"""
        # [ASCENSION 10]: Deduplication Ward
        # Remove old symbols for this specific path to allow for re-indexing
        for sym_list in self._symbol_index.values():
            # Filter in-place
            sym_list[:] = [s for s in sym_list if s.path != file_path]

        for sym in symbols:
            if sym.name not in self._symbol_index:
                self._symbol_index[sym.name] = []
            self._symbol_index[sym.name].append(sym)

        self._indexed_files.add(file_path)

    def locate_symbol(self, name: str) -> List[SymbolEntry]:
        """[THE RITE OF RECALL] O(1) definition lookup."""
        return self._symbol_index.get(name, [])

    # =========================================================================
    # == SECTION IV: HEALING & MAINTENANCE                                   ==
    # =========================================================================

    def ingest_file(self, path: Path):
        """Incremental update of structure."""
        self._ensure_memory()
        self._memory = self.perception_engine.ingest_file(path, self._memory)
        # Invalidate hash cache for this path
        self._hash_cache.pop(path, None)

    def forget_file(self, path: Path):
        """Surgical oblivion."""
        if not self._memory: return
        self._memory = self.perception_engine.forget_file(path, self._memory)
        self._hash_cache.pop(path, None)
        if path in self._indexed_files:
            self._indexed_files.remove(path)

    def forget_affected_areas(self, artifacts: List[Any]):
        """
        [ASCENSION 8]: THE GHOST-SHARD PURGE.
        Called after a major transmutation (refactor) to clear stale memories.
        """
        for art in artifacts:
            p = Path(art.path) if hasattr(art, 'path') else Path(str(art))
            self.forget_file(p)

    def configure_filters(self, ignore: List[str] = None, include: List[str] = None):
        """Configures the Gaze of Aversion."""
        self.perception_engine.configure_filters(ignore=ignore, include=include)

    def __repr__(self) -> str:
        status = "RESONANT" if self._memory else "COLD"
        return f"<Ω_GNOSTIC_CORTEX status={status} root={self.root.name} indexed={len(self._indexed_files)}>"

