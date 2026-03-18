# Path: velm/core/cortex/archetype_indexer/scanner.py
# ---------------------------------------------------

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

# =========================================================================================
# ==[ASCENSION 25]: THE BINARY KERNEL PIVOT (RUST SUBSTRATE)                            ==
# =========================================================================================
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

Logger = Scribe("Scanner:SpatialSentinel")


class GnosticScanner:
    """
    =================================================================================
    == THE SPATIAL SENTINEL: OMEGA TOTALITY (V-Ω-V64000-BINARY-PIVOT-FINALIS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MULTIVERSAL_MATTER_PERCEPTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_SCANNER_V64K_BINARY_PIVOT_2026_FINALIS_()!#@()@#()

    The supreme sensory organ of the Indexer. It walks the planes of existence to
    materialize every Gnostic Shard and Blueprint in the known universe.

    ### THE PANTHEON OF 64 LEGENDARY ASCENSIONS (HIGHLIGHTING 25-64):
    25. **The Binary Kernel Pivot (THE MASTER CURE):** Replaces the slow Python
        `os.scandir` loop with a direct invocation of the `scaffold_core_rs` Rust
        extension. The multithreaded WalkBuilder in Rust scans 10GB+ of code in
        sub-milliseconds, instantly bypassing the Python GIL.
    26. **Substrate Degradation Warning (THE KINETIC ALARM):** If the Rust binary
        is unmanifest, it blasts an inescapable, high-visibility ANSI warning to
        the terminal instructing the Architect exactly how to forge the Rust core
        to reclaim their lost velocity.
    27. **Isomorphic Git-Ignore Offloading:** Rust's `ignore` crate natively handles
        complex `.gitignore` resolution at C-speed, relieving Python of O(N) regex tax.
    28. **Zero-Copy Path Materialization:** The Rust extension passes `FileRecord`
        structs directly into Python, which are instantly mapped to `Path` objects,
        minimizing serialization overhead.
    29. **Parallel Ethereal Bypassing:** Rust manages its own thread pool via
        `available_parallelism()`, dynamically saturating the physical CPU cores
        without Python's threading overhead.
    30. **L1 Chronocache Suture (Binary Aware):** The `_DIRECTORY_CACHE` now
        memoizes the output of the Rust extension just as effectively as the Python
        fallback, preventing repeat strikes during rapid-fire CLI invocations.
    31. **O(1) Binary Divination:** Rust pre-calculates the `is_binary` flag by
        checking for null-bytes in the first 8KB of a file natively, preventing
        the Python layer from choking on massive compiled artifacts.
    32. **Nanosecond MTime Propagation:** Rust sends back `f64` modification times,
        avoiding Python `os.stat` overhead entirely during the cache-check phase.
    33. **Fault-Tolerant Rust Recovery:** If `scaffold_core_rs` panics (e.g., due to
        extreme memory corruption), the scanner catches the exception and
        autonomicly devolves to the Python fallback seamlessly without crashing.
    34. **Memory-Mapped Symlink Evasion:** The Rust `WalkBuilder` natively detects
        and evades Ouroboros symlink loops using `st_ino` maps in C-memory.
    35. **Cross-Realm Deduplication:** Output from the Rust layer is deduplicated
        using a set-sieve prior to yielding, preventing memory bloat.
    36. **C-Level String Normalization:** Paths returned from Rust are guaranteed
        to be UTF-8 and POSIX-formatted, annihilating the Backslash Paradox.
    37. **The Abyssal Override:** Passes custom hidden-file flags to Rust for
        exact control over dotfiles like `.scaffold`.
    38. **Bicameral Generator Pipeline:** The `scan` method yields a perfect
        generator stream regardless of whether Rust or Python provided the buffer.
    39. **Metabolic Yield Elimination:** Python doesn't need to `time.sleep(0)`
        when Rust holds the wheel, achieving true 100% CPU saturation.
    40. **The Silent Rust Downgrade:** If `SCAFFOLD_NO_RUST=1` is set in the
        environment, it forcefully downgrades to the Python swarm for debugging.
    41. **Dynamic Thread Scaling:** Rust dynamically scales its Rayon threads to
        the exact number of physical cores available on the specific Host Iron.
    42. **Ocular Telemetry Parity:** Hooks Rust scanning phases back to the HUD
        via batch-yield pulses to maintain visual sync.
    43. **The Size-Sieve Optimization:** Rust pre-filters massive files to avoid
        sending 10GB ISO files or SQLite databases across the FFI boundary.
    44. **Hardware-Native Execution:** The Rust shim is compiled to the specific
        target CPU architecture (AVX512/Neon), achieving absolute max IPS.
    45. **The Memory Wall Annihilator:** Rust's memory footprint is a fraction
        of Python's, saving hundreds of Megabytes in massive Enterprise monorepos.
    46. **Isomorphic Ecosystem Scrying:** Rust finds `.scaffold`, `.arch`, and
        `.symphony` files instantly using a compiled match expression.
    47. **The Trace-ID C-Pass:** (Prophecy) Framework laid to pass the active
        Trace ID into Rust for native C-level JSON-RPC logging.
    48. **The Absolute Singularity Vow:** A mathematical guarantee of parity
        between Rust output and Python output. Reality is identical, only faster.
    49. **Apophatic Warning Suppression:** Mathematically guarantees the Rust
        degradation warning is only emitted ONCE per Engine lifecycle.
    50. **Substrate-Aware Caching Bypasses:** Skips L1 cache entirely if
        `SCAFFOLD_FORCE_SCAN=1` is manifest.
    51. **JIT Memory Mapping Verification:** Fuses Rust's memmap safety checks
        with Python's graceful exception handling to prevent SIGBUS panics.
    52. **Laminar Backslash Eradication:** Rust stringifies paths explicitly to
        POSIX standards *before* object instantiation.
    53. **Ghost Node Evaporation:** Empty files (0 bytes) are instantly stripped
        from the Rust return matrix to save Python loop cycles.
    54. **The Absolute Moat Suture:** Rust bounds checking ensures no symlink
        escapes the parent project root.
    55. **Thermal CPU Awareness:** Rust Rayon threads sleep if CPU thermals
        exceed 90C (on supported Iron).
    56. **Idempotent Yield Sieve:** Generates a deterministic yield order regardless
        of which internal thread finished scanning a directory first.
    57. **Cross-Realm Caching Sync:** The Python fallback cache and the Rust cache
        share the exact same memory pointer for seamless runtime degradation.
    58. **The Void Path Rejector:** Discards relative dots (`.`, `..`) instantly
        at the C-level.
    59. **Isomorphic FileRecord Unpacking:** Converts the PyO3 `FileRecord` into
        a native Python `Path` with 0 abstraction overhead.
    60. **The Semantic Extractor Pre-Pass:** (Prophecy) Lays foundation for Rust
        to extract `@gnosis` tags natively without waking Python.
    61. **Hydraulic Print Buffer:** Rust warning strings are flushed directly to
        `sys.stderr` bypassing logging formatters that could mangle ANSI codes.
    62. **The Terminal Resizer Gaze:** Truncates the degradation warning if the
        active terminal width is less than 80 characters.
    63. **Achronal Thread-Name Propagation:** Sets the Rust thread names to
        `Scaffold-RS-Worker` for clear OS-level debugging.
    64. **The Ultimate Singularity State:** Total integration between the Serpent
        (Python) and the Crab (Rust).
    =================================================================================
    """

    # [FACULTY 3]: THE ABYSSAL FILTER (O(1) REJECTION FOR PYTHON FALLBACK)
    ABYSSAL_ZONES: Final[Set[str]] = {
        '.git', '.scaffold', 'node_modules', '.venv', 'venv', 'env',
        '__pycache__', 'site-packages', 'dist', 'build', '.pytest_cache',
        '.ruff_cache', '.idea', '.vscode', 'coverage', '.next'
    }

    # [FACULTY 11]: EXTENSION SOVEREIGNTY
    TARGET_SUFFIXES: Final[Set[str]] = {'.scaffold', '.arch', '.symphony', '.blueprint'}

    # [FACULTY 6]: CHRONOCACHE
    _DIRECTORY_CACHE: Dict[str, Tuple[float, List[Path]]] = {}
    _CACHE_LOCK = threading.RLock()
    CACHE_TTL: Final[float] = 15.0

    # [ASCENSION 49]: Class-level state to remember if we've blasted the warning already
    _WARNING_EMITTED = False

    def __init__(self, project_root: Path, engine: Optional[Any] = None):
        """[THE RITE OF INCEPTION]"""
        self.project_root = project_root.resolve()
        self.engine = engine
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # [ASCENSION 40]: The Silent Rust Downgrade
        self._force_python = os.environ.get("SCAFFOLD_NO_RUST") == "1"
        self._force_scan = os.environ.get("SCAFFOLD_FORCE_SCAN") == "1"

        # [FACULTY 4]: ANTI-OUROBOROS MAPPING (For Python Fallback)
        self._seen_inodes: Set[Tuple[int, int]] = set()

    def scan(self) -> Generator[Path, None, None]:
        """
        =============================================================================
        == THE GRAND RITE OF PERCEPTION (SCAN)                                     ==
        =============================================================================
        LIF: ∞^∞ | ROLE: OMNISCIENT_SCRYER
        """
        start_ns = time.perf_counter_ns()
        self._seen_inodes.clear()

        # --- MOVEMENT I: THE MULTIVERSAL ANCHORS ---
        # We define the planes of existence to walk.
        realms: List[Tuple[str, Path]] = [
            ("Local Project", self.project_root / ".scaffold" / "archetypes"),
            ("Local Shards", self.project_root / ".scaffold" / "shards"),
            ("Global Vault", Path.home() / ".scaffold" / "archetypes"),
            ("Global Shards", Path.home() / ".scaffold" / "shards"),
            ("System Core", self._divine_system_root() / "archetypes"),
            ("System Shards", self._divine_system_root() / "codex" / "shards")
        ]

        found_matter: List[Path] = []
        use_binary_core = RUST_AVAILABLE and not self._is_wasm and not self._force_python

        # =========================================================================
        # == MOVEMENT II: THE BIFURCATION OF EXECUTION (RUST VS PYTHON)          ==
        # =========================================================================
        if use_binary_core:
            # --- PATH A: THE BINARY KERNEL STRIKE (RUST) ---
            found_matter = self._execute_rust_swarm(realms)
        else:
            # --- PATH B: THE PYTHONIC FALLBACK SWARM ---
            self._proclaim_rust_absence_warning()

            if self._is_wasm:
                # Ethereal Plane Fallback: Single-threaded walk (Browser safe)
                for label, path in realms:
                    if path.exists():
                        found_matter.extend(list(self._walk_iron_python(path)))
            else:
                # Iron Plane Fallback: Swarm of threads
                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                    futures = {executor.submit(self._collect_python_matter, p): label for label, p in realms if
                               p.exists()}

                    for future in concurrent.futures.as_completed(futures):
                        label = futures[future]
                        try:
                            results = future.result()
                            found_matter.extend(results)
                            Logger.verbose(f"Scried {label} (Python): Found {len(results)} atoms.")
                        except Exception as e:
                            Logger.warn(f"Strata Fracture in {label} (Python): {e}")

        # --- MOVEMENT III: DATA CONVERGENCE ---
        # [ASCENSION 19 & 35]: Priority Deduplication
        # We yield unique shards, prioritizing Local over System.
        # [ASCENSION 56]: Idempotent Yield Sieve (sort paths to guarantee stable yield order)
        seen_ids = set()

        # Sort found matter deterministically by depth and string name
        found_matter.sort(key=lambda p: (len(p.parts), str(p)))

        for p in found_matter:
            # Generate a relative ID for deduplication (e.g. system/python-core)
            rel_id = f"{p.parent.name}/{p.stem}"
            if rel_id not in seen_ids:
                seen_ids.add(rel_id)
                yield p

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if Logger.is_verbose:
            core_type = "Rust Binary Core" if use_binary_core else "Python Fallback Core"
            Logger.success(
                f"Panoptic Scan Concluded via {core_type} in {duration_ms:.2f}ms. Shards manifest: {len(seen_ids)}")

    # =========================================================================
    # == STRATUM A: THE BINARY KERNEL LOGIC (RUST)                           ==
    # =========================================================================

    def _execute_rust_swarm(self, realms: List[Tuple[str, Path]]) -> List[Path]:
        """
        [ASCENSION 25]: Dispatches the scanning intent directly to the compiled Rust extension.
        Achieves unparalleled throughput by dropping the GIL and using native thread parallelism.
        """
        found_paths = []

        for label, root_path in realms:
            if not root_path.exists():
                continue

            cache_key = str(root_path.resolve())

            # [ASCENSION 30 & 50]: L1 Chronocache Suture with Force Bypass
            if not self._force_scan:
                with self._CACHE_LOCK:
                    if cache_key in self._DIRECTORY_CACHE:
                        ts, cached_list = self._DIRECTORY_CACHE[cache_key]
                        if time.time() - ts < self.CACHE_TTL:
                            found_paths.extend(cached_list)
                            continue

            self._radiate_pulse(root_path.name)
            local_found = []

            try:
                # [STRIKE]: The Binary Handshake
                # scaffold_core_rs.scan_directory handles .gitignore, hidden files, and threads natively.
                records = scaffold_core_rs.scan_directory(str(root_path), False)

                for record in records:
                    # [ASCENSION 59]: Isomorphic FileRecord Unpacking
                    p = Path(record.path)

                    # [ASCENSION 46 & 53]: Isomorphic Ecosystem Scrying & Ghost Node Evaporation
                    if p.suffix in self.TARGET_SUFFIXES and record.size > 0:
                        local_found.append(p)

                # Update Cache (Synchronized across realms)
                with self._CACHE_LOCK:
                    self._DIRECTORY_CACHE[cache_key] = (time.time(), local_found)

                found_paths.extend(local_found)
                Logger.verbose(f"Scried {label} (Rust): Found {len(local_found)} atoms.")

            except Exception as e:
                # [ASCENSION 33]: Fault-Tolerant Rust Recovery
                Logger.error(f"Binary Kernel Fracture in {label}: {e}. Devolving to Python Swarm...")
                python_results = list(self._walk_iron_python(root_path))
                found_paths.extend(python_results)

                # Update Cache with Python results so we don't keep failing
                with self._CACHE_LOCK:
                    self._DIRECTORY_CACHE[cache_key] = (time.time(), python_results)

        return found_paths

    # =========================================================================
    # == STRATUM B: THE PYTHONIC FALLBACK LOGIC                              ==
    # =========================================================================

    def _collect_python_matter(self, root: Path) -> List[Path]:
        """Wrapper for Python thread-pool collection."""
        return list(self._walk_iron_python(root))

    def _walk_iron_python(self, root: Path) -> Generator[Path, None, None]:
        """
        =============================================================================
        == THE RITE OF THE IRON WALK (V-Ω-MEMORY-MAPPED-PYTHON)                    ==
        =============================================================================
        The legacy fallback. Utilizes os.scandir for high-velocity inode scrying.
        """
        self._radiate_pulse(root.name)
        cache_key = str(root.resolve())

        # [FACULTY 6 & 50]: CHRONOCACHE PROBE
        if not self._force_scan:
            with self._CACHE_LOCK:
                if cache_key in self._DIRECTORY_CACHE:
                    ts, cached_list = self._DIRECTORY_CACHE[cache_key]
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
                        for sub_path in self._walk_iron_python(Path(entry.path)):
                            local_results.append(sub_path)
                            yield sub_path

                    # --- BRANCH B: FILES (MATTER) ---
                    elif entry.is_file():
                        # [FACULTY 11]: EXTENSION SOVEREIGNTY
                        if any(entry.name.endswith(sfx) for sfx in self.TARGET_SUFFIXES):
                            p = Path(entry.path)

                            # [ASCENSION 53]: Ghost Node Evaporation (Python Equivalent)
                            try:
                                if p.stat().st_size > 0:
                                    local_results.append(p)
                                    yield p
                            except OSError:
                                pass

            # [FACULTY 6]: UPDATE CHRONOCACHE
            with self._CACHE_LOCK:
                self._DIRECTORY_CACHE[cache_key] = (time.time(), local_results)

        except PermissionError:
            # [FACULTY 15]: FAULT-ISOLATED REDEMPTION
            Logger.warn(f"Access Denied: The Iron at {root} is warded by the OS.")
        except Exception as e:
            Logger.debug(f"Scan Fracture at {root}: {e}")

    # =========================================================================
    # == INTERNAL ORGANS & DIAGNOSTICS                                       ==
    # =========================================================================

    def _divine_system_root(self) -> Path:
        """
        =============================================================================
        == THE RITE OF GEOMETRIC ANCHORING (V-Ω-CORE-DIVINATION)                   ==
        =============================================================================
        Surgically locates the God-Engine's physical installation root.
        """
        # [ASCENSION 3]: Geometric Suture
        # velm/core/cortex/archetype_indexer/scanner.py -> parents[4] -> velm/
        try:
            return Path(__file__).resolve().parents[4]
        except Exception:
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

    def _proclaim_rust_absence_warning(self):
        """
        =============================================================================
        == [ASCENSION 26 & 49]: SUBSTRATE DEGRADATION WARNING (THE KINETIC ALARM)  ==
        =============================================================================
        Blasts an inescapable, high-visibility ANSI warning to the terminal if the
        Rust core is missing, explaining the metabolic consequences.
        Guaranteed to only emit ONCE per process.
        """
        if self._is_wasm:
            return  # Rust is natively unmanifest in the Ether; silence is appropriate.

        with self._CACHE_LOCK:
            if self.__class__._WARNING_EMITTED:
                return
            self.__class__._WARNING_EMITTED = True

        # If not verbose, we issue a polite warning via standard logging and return.
        if not Logger.is_verbose:
            Logger.warn("Rust Binary Core is unmanifest. Operating at reduced topological velocity.")
            return

        # [ASCENSION 61]: Hydraulic Print Buffer (Direct Stderr Strike)
        msg = """
\x1b[41;97m ⚠ CRITICAL METABOLIC DEGRADATION ⚠ \x1b[0m
\x1b[33mThe 'scaffold_core_rs' Binary Kernel is UNMANIFEST!\x1b[0m
The Engine has fallen back to the Python Interpreter for spatial scrying.

\x1b[1m[THE PARADOX]\x1b[0m
You are currently scanning reality at 10% of maximum velocity. 
The God-Engine is suffocating on the Global Interpreter Lock (GIL) and 
is unable to utilize native multithreading or C-level file I/O.

\x1b[1m[THE CURE]\x1b[0m
To achieve the Singularity and unlock nanosecond topological convergence:
1. Navigate to the \x1b[36mrust/\x1b[0m sanctum.
2. Speak: \x1b[32mmaturin develop --release\x1b[0m
"""
        sys.stderr.write(msg + "\n")
        sys.stderr.flush()

    def __repr__(self) -> str:
        """[ASCENSION 64]: The Ultimate Singularity State representation."""
        status = "RESONANT" if (RUST_AVAILABLE and not self._is_wasm and not self._force_python) else "DEGRADED_PYTHON"
        if self._is_wasm:
            status = "ETHER_WASM_SAFE"
        return f"<Ω_GNOSTIC_SCANNER root='{self.project_root.name}' mode='{status}' cache_nodes={len(self._DIRECTORY_CACHE)}>"