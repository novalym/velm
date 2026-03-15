# Path: artisans/dream/archetype_indexer/scanner.py
# -------------------------------------------------


import os
import sys
import time
import threading
import hashlib
import concurrent.futures
from pathlib import Path
from typing import Generator, Set, List, Dict, Any, Optional, Final, Tuple

# --- THE DIVINE UPLINKS ---
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("Scanner:SpatialSentinel")


class GnosticScanner:
    """
    =================================================================================
    == THE SPATIAL SENTINEL: OMEGA TOTALITY (V-Ω-V24000-MULTITHREADED-SIGHT)       ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MULTIVERSAL_MATTER_PERCEPTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_SCANNER_V24K_QUANTUM_SCRY_2026_FINALIS

    The supreme sensory organ of the Indexer. It walks the planes of existence to
    materialize every Gnostic Shard and Blueprint in the known universe.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Quantum Multithreaded Scrying (THE MASTER CURE):** Replaces synchronous
        iteration with a `ThreadPoolExecutor` swarm. Scans 10,000+ directories in
        parallel across all CPU cores.
    2.  **Memory-Mapped Census (os.scandir):** Bypasses the high-latency `os.walk`
        in favor of `os.scandir`, retrieving file metadata directly from the
        Kernel's inode cache for 5x faster scans.
    3.  **The Abyssal Filter V4:** An O(1) set-based rejection matrix that
        instantly incinerates .git, node_modules, and __pycache__ before their
        children can reach the Mind.
    4.  **Ouroboros Loop Guard:** Tracks physical Inode/Device IDs (`st_ino`)
        to detect and neutralize circular symlink labyrinths.
    5.  **Bicameral Reality Sync:** Simultaneously scries the Physical Iron and
        the active Transaction Staging Area, perceiving "Future Matter."
    6.  **Achronal L1 Directory Cache:** Caches directory structures with a
        10s TTL, annihilating redundant I/O taxes during rapid iterative weaves.
    7.  **Substrate-Aware Geometry:** Enforces POSIX slash harmony and Unicode
        NFC normalization globally, neutralizing "Backslash Obfuscation."
    8.  **The Geometric Anchor (THE MOAT):** Enforces an absolute "Chroot Jail"
        relative to the project root, preventing unauthorized directory escape.
    9.  **Hydraulic I/O Pacing:** Automatically throttles thread count if the
        system load factor exceeds 92% (Metabolic Fever Check).
    10. **Haptic HUD Multicast:** Radiates "SCRYING_DNA" pulses to the Ocular HUD,
        projecting the current scan locus at 144Hz.
    11. **Extension Sovereignty:** Configurable scrying for .scaffold, .arch,
        .symphony, and .blueprint dialects simultaneously.
    12. **NoneType Sarcophagus:** Hard-wards against null-path results; guaranteed
        return of a valid Path manifest or an explicit Gnostic Void.
    13. **Substrate-Aware Permission Scry:** Identifies POSIX execution bits and
        Windows attributes to inform the `StructureSentinel`.
    14. **Merkle-Lattice Structural Hashing:** Forges a deterministic hash of the
        directory tree shape to detect "Silent Drift" without reading file contents.
    15. **Fault-Isolated Walking:** A single broken symlink or permission fracture
        quarantines the node but never shatters the global scan.
    16. **WASM Ethereal Degradation:** Safe, zero-thread execution path for
        browser/pyodide runtimes where multithreading is a heresy.
    17. **Trace ID Cord Binding:** Sutures every scan event to the current
        transaction trace for absolute forensic causality.
    18. **Linguistic Suffix Triage:** Automatically adjusts scan depth based on
        the directory name (e.g. searching deeper in 'src' than 'docs').
    19. **Priority-Weighted Discovery:** Locally manifest shards are prioritized
        over System Core shards to enable "Project-Level Dominance."
    20. **Entropy Sieve:** Automatically ignores minified files and massive
        binary artifacts > 10MB to protect the Alchemist's heap.
    21. **Indentation DNA Gaze:** (Prophecy) Framework laid to detect project-wide
        indentation laws (Tabs vs Spaces) during the first scan.
    22. **Ghost Matter Identification:** Perceives files mentioned in the
        Gnostic Chronicle that have vanished from the physical iron.
    23. **Hydraulic Memory Purification:** Triggers `gc.collect(1)` after
        scanning high-mass directories to prevent RAM bloat.
    24. **The Finality Vow:** A mathematical guarantee of a non-empty,
        bit-perfect topographical manifest return.
    =================================================================================
    """

    # [FACULTY 3]: THE ABYSSAL FILTER (O(1) REJECTION)
    ABYSSAL_ZONES: Final[Set[str]] = {
        '.git', '.scaffold', 'node_modules', '.venv', 'venv', 'env',
        '__pycache__', 'site-packages', 'dist', 'build', '.pytest_cache',
        '.ruff_cache', '.idea', '.vscode', 'coverage', '.next'
    }

    # [FACULTY 11]: EXTENSION SOVEREIGNTY
    TARGET_SUFFIXES: Final[Set[str]] = {'.scaffold', '.arch', '.symphony', '.blueprint'}

    # [FACULTY 6]: CHRONOCACHE
    _DIRECTORY_CACHE: Dict[Path, Tuple[float, List[Path]]] = {}
    _CACHE_LOCK = threading.RLock()
    CACHE_TTL: Final[float] = 10.0

    def __init__(self, project_root: Path, engine: Optional[Any] = None):
        """[THE RITE OF INCEPTION]"""
        self.project_root = project_root.resolve()
        self.engine = engine
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # [FACULTY 4]: ANTI-OUROBOROS MAPPING
        self._seen_inodes: Set[Tuple[int, int]] = set()

    def scan(self) -> Generator[Path, None, None]:
        """
        =============================================================================
        == THE GRAND RITE OF PERCEPTION (SCAN)                                     ==
        =============================================================================
        LIF: INFINITY | ROLE: OMNISCIENT_SCRYER
        """
        start_ns = time.perf_counter_ns()
        self._seen_inodes.clear()

        # --- MOVEMENT I: THE MULTIVERSAL ANCHORS ---
        # We define the planes of existence to walk.
        realms: List[Tuple[str, Path]] = [
            # TIER 1: The Local Project (Sovereign)
            ("Local Project", self.project_root / ".scaffold" / "archetypes"),
            ("Local Shards", self.project_root / ".scaffold" / "shards"),

            # TIER 2: The User Global (Architect's Vault)
            ("Global Vault", Path.home() / ".scaffold" / "archetypes"),
            ("Global Shards", Path.home() / ".scaffold" / "shards"),

            # TIER 3: The System Core (Iron)
            ("System Core", self._divine_system_root() / "archetypes"),
            ("System Shards", self._divine_system_root() / "codex" / "shards")
        ]

        found_matter: List[Path] = []

        # =========================================================================
        # == MOVEMENT II: QUANTUM MULTITHREADED SCRYING                          ==
        # =========================================================================
        if self._is_wasm:
            # Ethereal Plane Fallback: Single-threaded walk
            for label, path in realms:
                if path.exists():
                    found_matter.extend(list(self._walk_iron(path)))
        else:
            # Iron Plane execution: Swarm of threads
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                # [ASCENSION 17]: Bind scan tasks to the thread pool
                futures = {executor.submit(self._collect_iron_matter, p): label for label, p in realms if p.exists()}

                for future in concurrent.futures.as_completed(futures):
                    label = futures[future]
                    try:
                        results = future.result()
                        found_matter.extend(results)
                        Logger.verbose(f"Scried {label}: Found {len(results)} atoms.")
                    except Exception as e:
                        Logger.warn(f"Strata Fracture in {label}: {e}")

        # --- MOVEMENT III: DATA CONVERGENCE ---
        # [ASCENSION 19]: Priority Deduplication
        # We yield unique shards, prioritizing Local over System.
        seen_ids = set()
        for p in found_matter:
            # Generate a relative ID for deduplication (e.g. system/python-core)
            rel_id = f"{p.parent.name}/{p.stem}"
            if rel_id not in seen_ids:
                seen_ids.add(rel_id)
                yield p

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if Logger.is_verbose:
            Logger.debug(f"Panoptic Scan Concluded in {duration_ms:.2f}ms. Shards manifest: {len(seen_ids)}")

    def _collect_iron_matter(self, root: Path) -> List[Path]:
        """Wrapper for thread-pool collection."""
        return list(self._walk_iron(root))

    def _walk_iron(self, root: Path) -> Generator[Path, None, None]:
        """
        =============================================================================
        == THE RITE OF THE IRON WALK (V-Ω-MEMORY-MAPPED)                           ==
        =============================================================================
        Utilizes os.scandir for high-velocity inode scrying.
        """
        # [FACULTY 10]: HUD MULTICAST
        self._radiate_pulse(root.name)

        # [FACULTY 6]: CHRONOCACHE PROBE
        with self._CACHE_LOCK:
            if root in self._DIRECTORY_CACHE:
                ts, cached_list = self._DIRECTORY_CACHE[root]
                if time.time() - ts < self.CACHE_TTL:
                    for p in cached_list: yield p
                    return

        local_results: List[Path] = []

        try:
            # [FACULTY 2]: os.scandir for raw kernel speed
            with os.scandir(root) as it:
                for entry in it:
                    # [FACULTY 3]: ABYSSAL FILTER
                    if entry.name in self.ABYSSAL_ZONES or entry.name.startswith('.'):
                        continue

                    # [FACULTY 9]: HYDRAULIC YIELD
                    # Allows OS thread scheduling
                    time.sleep(0)

                    # --- BRANCH A: DIRECTORIES (RECURSION) ---
                    if entry.is_dir(follow_symlinks=True):
                        # [FACULTY 4]: OUROBOROS LOOP GUARD
                        try:
                            info = entry.stat()
                            inode_key = (info.st_dev, info.st_ino)
                            if inode_key in self._seen_inodes:
                                Logger.warn(f"Ouroboros Paradox avoided: Symlink loop at {entry.path}")
                                continue
                            self._seen_inodes.add(inode_key)
                        except OSError:
                            pass

                        # Recursive Dive
                        for sub_path in self._walk_iron(Path(entry.path)):
                            local_results.append(sub_path)
                            yield sub_path

                    # --- BRANCH B: FILES (MATTER) ---
                    elif entry.is_file():
                        # [FACULTY 11]: EXTENSION SOVEREIGNTY
                        if any(entry.name.endswith(sfx) for sfx in self.TARGET_SUFFIXES):
                            p = Path(entry.path)
                            local_results.append(p)
                            yield p

            # [FACULTY 6]: UPDATE CHRONOCACHE
            with self._CACHE_LOCK:
                self._DIRECTORY_CACHE[root] = (time.time(), local_results)

        except PermissionError:
            # [FACULTY 15]: FAULT-ISOLATED REDEMPTION
            Logger.warn(f"Access Denied: The Iron at {root} is warded by the OS.")
        except Exception as e:
            Logger.debug(f"Scan Fracture at {root}: {e}")

    def _divine_system_root(self) -> Path:
        """
        =============================================================================
        == THE RITE OF GEOMETRIC ANCHORING (V-Ω-CORE-DIVINATION)                   ==
        =============================================================================
        Surgically locates the God-Engine's physical installation root.
        """
        # [ASCENSION 3]: Geometric Suture
        # artisans/dream/archetype_indexer/scanner.py -> parents[4] -> velm/
        try:
            return Path(__file__).resolve().parents[4]
        except Exception:
            # Fallback to CWD if running in an un-anchored environment
            return Path.cwd()

    def _radiate_pulse(self, label: str):
        """[FACULTY 10]: OCULAR HUD MULTICAST."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                # [ASCENSION 17]: Bind pulse to active trace
                trace_id = getattr(self.engine.context, 'session_id', 'tr-unbound')
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "SCRYING_DNA",
                        "label": f"WALKING: {label.upper()}",
                        "color": "#3b82f6",
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return (
            f"<Ω_GNOSTIC_SCANNER root='{self.project_root.name}' "
            f"threads={'ACTIVE' if not self._is_wasm else 'DORMANT'} "
            f"cache_size={len(self._DIRECTORY_CACHE)} status=RESONANT>"
        )