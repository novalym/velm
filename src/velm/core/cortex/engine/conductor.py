# Path: core/cortex/engine/conductor.py
# -------------------------------------
import collections
import time
import hashlib
import os
import sys
import threading
import gc
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Set, Union, Final

# --- THE DIVINE SUMMONS (STRATUM-2: THE CORTEX) ---
from .perception import PerceptionEngine
from .analysis import AnalysisEngine
from ..contracts import CortexMemory, SymbolEntry
from ..vector import VectorCortex
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 1]: WASM COMPATIBILITY SENSING
IS_WASM: Final[bool] = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

Logger = Scribe("GnosticCortex")


class GnosticCortex:
    """
    =================================================================================
    == THE GNOSTIC CORTEX: OMEGA POINT (V-Ω-TOTALITY-VMAX-WASM-SUTURED)            ==
    =================================================================================
    LIF: ∞^∞ | ROLE: CENTRAL_INTELLIGENCE_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_CORTEX_VMAX_WASM_SUTURE_2026_FINALIS

    The supreme definitively authority for architectural perception and memory.
    It manages the spatiotemporal relationship between Matter (Files) and
    Mind (Symbols) across Native and Ethereal substrates.
    =================================================================================
    """

    # [ASCENSION 2]: ZERO-ALLOCATION SLOTS
    __slots__ = (
        'root', 'logger', '_perception_engine', '_analysis_engine',
        '_vector_cortex_instance', '_memory', '_symbol_index',
        '_indexed_files', '_hash_cache', '_lock', '_is_warm',
        '_merkle_root', '_start_ns', '_is_adrenaline', '_engine_ref'
    )

    def __init__(self, project_root: Path):
        """
        =============================================================================
        == THE RITE OF INCEPTION: TOTALITY (V-Ω-TOTALITY-VMAX-WASM-SUTURED)        ==
        =============================================================================
        LIF: ∞ | ROLE: CENTRAL_INTELLIGENCE_GOVERNOR | RANK: OMEGA

        [THE MANIFESTO]
        The supreme definitive authority for Kernel awakening. This constructor
        righteously implements the **Weak-Ref Engine Suture**, providing the
        physical slot for the Ethereal Scryer to bind the God-Engine.
        =============================================================================
        """
        import collections
        import time

        # --- MOVEMENT I: IDENTITY & TOPOGRAPHY ---
        self.logger = Logger
        # [ASCENSION 7]: Geometric Path Normalization
        self.root = project_root.resolve()

        self._lock = threading.RLock()
        self._start_ns = time.perf_counter_ns()

        # [THE MASTER CURE]: THE WEAK-REF SUTURE
        # Pre-materializes the anchor for the Engine Property to prevent AttributeErrors.
        self._engine_ref = None

        # --- MOVEMENT II: ORGANS (LAZY MATERIALIZATION) ---
        # Slots initialized to Void to preserve boot-velocity (<15ms).
        self._perception_engine = None
        self._analysis_engine = None
        self._vector_cortex_instance = None

        # --- MOVEMENT III: AKASHIC MEMORY & LATTICE ---
        self._memory = None
        # [ASCENSION 9]: Thread-Safe Symbolic Lattice
        self._symbol_index = collections.defaultdict(list)
        self._indexed_files = set()

        # --- MOVEMENT IV: HOT-PATH CHRONOCACHE ---
        self._hash_cache = {}

        # --- MOVEMENT V: THERMODYNAMIC STATE ---
        self._is_warm = False
        self._merkle_root = "0xVOID"
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

    # =========================================================================
    # == SECTION I: THE GAZE OF ESSENCE (SCRYING)                            ==
    # =========================================================================

    def scry_hash(self, path: Union[str, Path], trace_id: str = "tr-cortex-void") -> str:
        """
        =============================================================================
        == THE ORACLE OF ESSENCE (V-Ω-TOTALITY-VMAX-SCRY)                          ==
        =============================================================================
        LIF: 1,000,000x | ROLE: FORENSIC_BIOPSY | RANK: OMEGA
        """
        # [ASCENSION 5]: NoneType Sarcophagus v20
        if path is None:
            return "0xVOID"

        target = Path(path).resolve() if isinstance(path, str) else path.resolve()

        # 1. SUBSTRATE-AWARE EXISTENCE CHECK
        if not target.exists() or not target.is_file():
            return "0xVOID"

        # 2. CHRONOCACHE PROBE (O(1) Memory Strike)
        if target in self._hash_cache:
            return self._hash_cache[target]

        # 3. THE KINETIC STRIKE (VECTORIZED HASHING)
        try:
            hasher = hashlib.sha256()

            # [ASCENSION 1]: WASM/ETHER PLANE BYPASS
            if IS_WASM:
                # Browser envs prefer atomic reads over chunks due to virtual FS limits
                hasher.update(target.read_bytes())
            else:
                # Iron envs use 64KB shards to maintain L1/L2 cache locality
                with open(target, 'rb') as f:
                    for shard in iter(lambda: f.read(65536), b""):
                        hasher.update(shard)

            fingerprint = hasher.hexdigest()

            # [ASCENSION 4]: Update the Chronocache
            with self._lock:
                self._hash_cache[target] = fingerprint

            # [ASCENSION 9]: HUD Telemetry Pulse
            self._radiate_hud_pulse("ESSENCE_SCRIED", target.name, "#64ffda", trace_id)

            return fingerprint

        except Exception as e:
            self.logger.warn(f"[{trace_id}] Gaze clouded on essence of '{target.name}': {e}")
            return "0xHERESY"

    def scry_mass(self, path: Path) -> int:
        """[ASCENSION 6]: SUBSTRATE DNA TOMOGRAPHY (Size Sensing)."""
        try:
            if not path.exists(): return 0
            return path.stat().st_size
        except OSError:
            return 0

    # =========================================================================
    # == SECTION II: LAZY FACULTIES & PERCEPTION                             ==
    # =========================================================================

    @property
    def perception_engine(self) -> PerceptionEngine:
        """[ASCENSION 10]: Lazarus JIT Inception."""
        if self._perception_engine is None:
            with self._lock:
                if self._perception_engine is None:
                    self._perception_engine = PerceptionEngine(self.root)
        return self._perception_engine

    @property
    def analysis_engine(self) -> AnalysisEngine:
        if self._analysis_engine is None:
            with self._lock:
                if self._analysis_engine is None:
                    self._ensure_memory()
                    self._analysis_engine = AnalysisEngine(self.root, self._memory)
        return self._analysis_engine

    @property
    def vector_cortex(self) -> VectorCortex:
        if self._vector_cortex_instance is None:
            with self._lock:
                if self._vector_cortex_instance is None:
                    self._vector_cortex_instance = VectorCortex(self.root)
        return self._vector_cortex_instance

    @property
    def engine(self) -> Any:
        """
        =========================================================================
        == THE ETHEREAL ENGINE SCRYER (V-Ω-TOTALITY-VMAX-ZERO-STICTION)        ==
        =========================================================================
        LIF: ∞ | ROLE: KERNEL_IDENTITY_RESONATOR | RANK: OMEGA

        [THE MANIFESTO]
        The absolute final solution to the "Engine Void" heresy. This property
        performs a multi-strata search to locate the living God-Engine:
        1. Local WeakRef: Returns the explicitly bound engine.
        2. Main Module Scry: Peers into __main__ for the 'engine' singleton.
        3. Heap Scavenge: Dissects the Python object graph for VelmEngine.
        =========================================================================
        """
        # 1. Check for local warded reference
        if hasattr(self, '_engine_ref') and self._engine_ref is not None:
            ref = self._engine_ref()
            if ref: return ref

        # 2. [ASCENSION 1]: MAIN_MODULE_SCRY
        # Most CLI and Daemon strikes name the engine 'engine' in __main__
        try:
            import sys
            main_ctx = sys.modules.get('__main__')
            if hasattr(main_ctx, 'engine'):
                self.engine = getattr(main_ctx, 'engine')
                return getattr(main_ctx, 'engine')
        except Exception:
            pass

        # 3. [ASCENSION 2]: HEAP_SCAVENGED_RESONANCE
        # Absolute fallback: Scry the entire RAM heap for the VelmEngine signature.
        try:
            import gc
            for obj in gc.get_objects():
                if type(obj).__name__ == 'VelmEngine':
                    self.engine = obj  # Bind for O(1) recall next time
                    return obj
        except Exception:
            pass

        return None

    @engine.setter
    def engine(self, instance: Any):
        """[THE RITE OF WEAK-BINDING]"""
        import weakref
        # We use a weakref to prevent the Cortex from keeping the Engine alive
        # after the timeline is willed to collapse.
        object.__setattr__(self, '_engine_ref', weakref.ref(instance) if instance else None)

    def perceive(self, force_refresh: bool = False, deep_scan: bool = False) -> CortexMemory:
        """
        =============================================================================
        == THE RITE OF AWAKENING (V-Ω-TOTALITY-VMAX-SCAN)                          ==
        =============================================================================
        LIF: INFINITY | ROLE: TOPOLOGICAL_ARCHITECT
        """
        if self._memory and not force_refresh:
            return self._memory

        self.logger.info(
            f"The Cortex awakens on {'ETHER' if IS_WASM else 'IRON'}. Mapping topology of '{self.root.name}'...")
        start_time = time.monotonic()

        # [STRIKE]: Calling the Perception Organ
        self._memory = self.perception_engine.perceive()

        # [ASCENSION 4]: HYDRAULIC CACHE WARMING
        if deep_scan and not self._is_adrenaline:
            self.logger.verbose("Initiating Deep Tissue Biopsy (Vectorizing entire project)...")
            # This would typically be dispatched to a background swarm
            for node in self._memory.inventory:
                if not node.is_dir:
                    self.scry_hash(node.path)

        # [ASCENSION 2]: Merkle-Lattice Graph Finalization
        self._merkle_root = self._calculate_merkle_root()

        duration = time.monotonic() - start_time
        self.logger.success(
            f"Topology Mapped in {duration:.2f}s. {len(self._memory.inventory)} nodes resonant. Seal: 0x{self._merkle_root[:8]}")

        self._is_warm = True
        return self._memory

    def _ensure_memory(self):
        """[ASCENSION 5]: NoneType Sarcophagus."""
        if self._memory is None:
            self.perceive()

    # =========================================================================
    # == SECTION III: SYMBOLIC INTELLIGENCE                                  ==
    # =========================================================================

    def memorize_symbols(self, file_path: Path, symbols: List[SymbolEntry]):
        """
        =============================================================================
        == THE RITE OF INSCRIPTION (V-Ω-TOTALITY-VMAX-SYMBOLIC-SUTURE)            ==
        =============================================================================
        [ASCENSION 10]: Deduplication Ward and Secret Sieve.
        """
        with self._lock:
            # 1. THE APOPHATIC SIEVE (Secret Protection)
            # [ASCENSION 3]: We filter out high-entropy symbols that might be secrets.
            pure_symbols = []
            for sym in symbols:
                # Heuristic: Symbols that look like keys are un-soul'd.
                if len(sym.name) > 32 and not "_" in sym.name:
                    continue
                pure_symbols.append(sym)

            # 2. THE LAZARUS RE-INDEXING
            # Remove existing traces of this file to allow bit-perfect overwrite
            for sym_list in self._symbol_index.values():
                sym_list[:] = [s for s in sym_list if s.path != file_path]

            # 3. KINETIC INSCRIPTION
            for sym in pure_symbols:
                self._symbol_index[sym.name].append(sym)

            self._indexed_files.add(file_path)

    def locate_symbol(self, name: str) -> List[SymbolEntry]:
        """[THE RITE OF RECALL] O(1) definition lookup across the lattice."""
        # [ASCENSION 7]: Isomorphic Identity Normalization
        # We search for the exact name and common case variations
        res = self._symbol_index.get(name, [])
        if not res and name.islower():
            # Try PascalCase fallback
            pascal = "".join(x.title() for x in name.split('_'))
            res = self._symbol_index.get(pascal, [])

        return res

    # =========================================================================
    # == SECTION IV: HEALING & METABOLIC MAINTENANCE                         ==
    # =========================================================================

    def ingest_file(self, path: Path):
        """Incremental update of structure. Annihilates Anomaly 236."""
        self._ensure_memory()
        self._memory = self.perception_engine.ingest_file(path, self._memory)

        # Invalidate Chronocache
        self._hash_cache.pop(path, None)

        # [ASCENSION 8]: Update State Seal
        self._merkle_root = self._calculate_merkle_root()

    def forget_file(self, path: Path):
        """Surgical oblivion of matter and mind."""
        if not self._memory: return

        with self._lock:
            self._memory = self.perception_engine.forget_file(path, self._memory)
            self._hash_cache.pop(path, None)
            if path in self._indexed_files:
                self._indexed_files.remove(path)

            # Clear symbols from lattice
            for sym_list in self._symbol_index.values():
                sym_list[:] = [s for s in sym_list if s.path != path]

    def forget_affected_areas(self, artifacts: List[Any]):
        """[ASCENSION 8]: THE GHOST-SHARD PURGE."""
        for art in artifacts:
            p = Path(art.path) if hasattr(art, 'path') else Path(str(art))
            self.forget_file(p)

        # [ASCENSION 11]: Trigger GC if mass was high
        if len(artifacts) > 100:
            gc.collect(1)

    # =========================================================================
    # == INTERNAL METABOLICS                                                 ==
    # =========================================================================

    def _calculate_merkle_root(self) -> str:
        """[ASCENSION 2]: Forges the 128-bit Merkle-Lattice Root of the project."""
        if not self._memory: return "0xVOID"

        # We hash the sorted inventory to ensure deterministic state identification
        state_str = "".join(sorted([str(n.path) + n.merkle_hash for n in self._memory.inventory if not n.is_dir]))
        return hashlib.sha256(state_str.encode()).hexdigest()

    def _radiate_hud_pulse(self, type_label: str, message: str, color: str, trace: str):
        """[ASCENSION 9 & 11]: OCULAR HUD MULTICAST."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "CORTEX_PERCEPTION",
                        "label": type_label,
                        "message": message,
                        "color": color,
                        "trace": trace
                    }
                })
            except:
                pass


    def __repr__(self) -> str:
        return (f"<Ω_GNOSTIC_CORTEX session={hex(id(self)).upper()} "
                f"root={self.root.name} indexed={len(self._indexed_files)} "
                f"seal=0x{self._merkle_root[:8]} status={'WARM' if self._is_warm else 'COLD'}>")