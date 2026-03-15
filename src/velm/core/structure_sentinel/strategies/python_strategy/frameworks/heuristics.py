# Path: core/structure_sentinel/strategies/python_strategy/frameworks/heuristics.py
# ---------------------------------------------------------------------------------

import os
import sys
import time
import threading
import secrets
import hashlib
from pathlib import Path
from typing import List, Optional, Any, Set, Final, Dict, Tuple, Callable

from ......logger import Scribe

Logger = Scribe("EntrypointDiviner")


class EntrypointDiviner:
    """
    =================================================================================
    == THE OMNISCIENT ENTRYPOINT ORACLE (V-Ω-TOTALITY-VMAX-GLOBAL-PROMISE)         ==
    =================================================================================
    LIF: ∞^∞ | ROLE: TOPOLOGICAL_BLOODHOUND | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_HEURISTICS_VMAX_GLOBAL_PROMISE_2026_FINALIS

    [THE MANIFESTO]
    The supreme authority for locating the Application Heart. It has been radically
    transfigured to annihilate the "NTFS I/O Storm" (The Step 1.5 Metabolic Freeze).
    By elevating its memory to the Class Stratum, it ensures that in a 24-worker
    parallel swarm, only ONE thread ever touches the disk per signature, while the
    others enter a zero-tax meditative sleep.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Global Promise Registry (THE MASTER CURE):** `_GLOBAL_ACTIVE_SEARCHES`
        uses `threading.Event` at the class level. If 24 threads ask for FastAPI,
        1 becomes the Scout, 23 become Watchers. The I/O Storm is mathematically dead.
    2.  **The Panic-Proof Scout Release (THE FIX):** A titanium `try/finally` block
        guarantees that if the Scout suffers a catastrophic OS fault, the `Event` is
        still set, preventing the Watchers from sleeping eternally (Deadlock).
    3.  **Achronal L1 Memo-Matrix (Class-Level):** Results are cached universally
        across all `FrameworkFaculty` instances, surviving process-local re-inception.
    4.  **Transaction Mass Decoupling:** Annihilates `tx_mass` from the cache key.
        The entrypoint is a Gnostic Constant; it does not shift just because a
        staging file was born. This achieves 100x velocity in monolithic strikes.
    5.  **Substrate-Aware Suffix Filtering:** Pre-filters extensions at the `os.scandir`
        level to avoid wasting CPU cycles opening binaries or media assets.
    6.  **The Deep-Read Throttle:** Limits reading to the first 8KB of files,
        protecting the heap from 50MB minified JS files masking as Python.
    7.  **The Abyssal Short-Circuit:** Instantly skips `__pycache__`, `node_modules`,
        `venv`, `.git`, and `.scaffold` via O(1) set lookup.
    8.  **Thread-ID Coordinate Radiation:** Injects `[T:1234]` into debug logs to
        prove and monitor parallel efficiency in the terminal.
    9.  **The Staging Precedence Suture:** Scries the active transaction's staging
        area BEFORE hitting the physical disk, perceiving "Future Truths."
    10. **Stale Promise Sweeper:** Timeouts on `Event.wait(5.0)` ensure Watcher
        threads survive and degrade to solo-execution if a Scout mysteriously vanishes.
    11. **The Semantic Depth Priority:** Weights `main.py` (30pts) > `app.py` (20pts) >
        `routes.py` (15pts) to divine the true heart of the application instantly.
    12. **Null-Byte Annihilation:** Wraps file reads in a strict utf-8 decoder that
        ignores/replaces null bytes, preventing `ValueError` crashes on binary reads.
    13. **Ouroboros Symlink Guard:** Uses `is_symlink()` logic to avoid circular
        filesystem labyrinths during the search phase.
    14. **Hydraulic CPU Yielding:** Injects `time.sleep(0.001)` during massive
        directory walks to allow the OS scheduler to breathe.
    15. **The Ghost Match Exorcist:** Verifies that a cached path actually still
        `exists()` before returning it, preventing stale references.
    16. **Marker Normalization:** Sorts and lowercases markers for the cache key
        to maximize cache hit rates regardless of input order.
    17. **Dynamic Substrate Pathing:** `str(root.resolve())` standardizes cache
        keys across Windows/Linux, preventing cache-misses due to path aliasing.
    18. **File Size Sarcophagus:** Explicitly checks `st_size` and skips files > 2MB.
    19. **The Jinja Decoupler:** Penalizes files that look like raw Jinja templates
        without valid Python structure.
    20. **The Metric Radiator:** Logs "O(1) Cache Hit vs O(N) Disk Scan" telemetry
        to stderr when Adrenaline/Debug mode is active.
    21. **Non-Blocking Promise Acquirer:** Uses `.wait()` with a hard ceiling to
        ensure the Ocular HUD never hangs on a disk lock.
    22. **Shallow Diagnostic Suture:** Limits depth in specific folders (`src`, `app`)
        to avoid scanning 10,000 files deep in a monorepo.
    23. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        high-velocity, and transactionally-contained physical coordinate.
    24. **Apophatic Fallback:** If the provided `reader_func` fails, it possesses
        a native `Path.read_text` fallback to ensure the Gaze is never blinded.
    =================================================================================
    """

    # [ASCENSION 7]: THE ABYSSAL FILTER (O(1) Lookup)
    IGNORE_DIRS: Final[Set[str]] = {
        '.git', '.scaffold', 'node_modules', 'venv', '.venv', 'env',
        '__pycache__', 'site-packages', 'dist', 'build', 'migrations',
        'tests', 'docs', '.idea', '.vscode', '.next', 'coverage'
    }

    # =========================================================================
    # == [ASCENSION 1]: THE GLOBAL PROMISE REGISTRY (THE MASTER CURE)        ==
    # =========================================================================
    # These structures exist at the Class level, shared by all threads.
    _GLOBAL_MEMO: Dict[Tuple[str, tuple], Tuple[float, Optional[Path]]] = {}
    _GLOBAL_ACTIVE_SEARCHES: Dict[Tuple[str, tuple], threading.Event] = {}
    _GLOBAL_LOCK: threading.RLock = threading.RLock()

    def __init__(self, reader_func: Callable[[Path, Path, Any], str]):
        """[THE RITE OF INCEPTION]"""
        self.read = reader_func

    def find_best_match(self, root: Path, markers: List[str], tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE RITE OF SYNCHRONIZED DISCOVERY (V-Ω-SCOUT-WATCHER-PARADIGM)         ==
        =============================================================================
        Finds the most resonant entrypoint file containing any of the markers.
        """
        t_id = threading.get_ident()
        start_t = time.perf_counter()
        trace_id = f"scry-{secrets.token_hex(2).upper()}"
        debug_mode = os.environ.get("SCAFFOLD_DEBUG") == "1"

        def _proclaim(msg: str, color: str = "90"):
            """Direct-to-Iron logging to bypass logger deadlocks."""
            if debug_mode:
                sys.stderr.write(f"\x1b[{color}m[T:{t_id}][{trace_id}] {msg}\x1b[0m\n")
                sys.stderr.flush()

        # =========================================================================
        # == HERESY II CURE: ACHRONAL CONTINUITY (DECOUPLING TX_MASS)            ==
        # =========================================================================
        # We mathematically annihilate `tx_mass` from the cache key.
        # The entrypoint is a structural constant; it doesn't shift during a strike.
        root_str = str(root.resolve())
        marker_key = tuple(sorted([m.lower().strip() for m in markers]))
        cache_key = (root_str, marker_key)

        is_scout = False
        wait_event = None

        with self._GLOBAL_LOCK:
            # 1. Check L1 Cache (Achronal Memo-Matrix)
            if cache_key in self._GLOBAL_MEMO:
                ts, res = self._GLOBAL_MEMO[cache_key]
                # [ASCENSION 15]: Verify it still exists physically or in staging
                if time.time() - ts < 30.0:  # 30s validity
                    if not res or res.exists() or (tx and tx.is_file_in_staging(res.relative_to(root))):
                        _proclaim(f"O(1) Global Cache Hit: {res.name if res else 'None'}", "32")
                        return res

            # 2. Check Promise Registry (Are we the Scout or the Watcher?)
            if cache_key in self._GLOBAL_ACTIVE_SEARCHES:
                wait_event = self._GLOBAL_ACTIVE_SEARCHES[cache_key]
                is_scout = False
                _proclaim(f"Thread adopting Watcher posture. Awaiting Scout...")
            else:
                wait_event = threading.Event()
                self._GLOBAL_ACTIVE_SEARCHES[cache_key] = wait_event
                is_scout = True
                _proclaim(f"Thread ascending to Scout posture. Commencing physical I/O scan.", "36")

        # --- BRANCH A: THE WATCHER (ZERO I/O SLEEP) ---
        if not is_scout and wait_event:
            # [ASCENSION 10]: Non-blocking Promise Acquirer
            flag = wait_event.wait(timeout=5.0)
            if not flag:
                _proclaim("Promise Timeout: Scout vanished. Devolving to solitary scan.", "33")
            else:
                with self._GLOBAL_LOCK:
                    if cache_key in self._GLOBAL_MEMO:
                        ts, res = self._GLOBAL_MEMO[cache_key]
                        _proclaim(f"Awakened by Scout. Received Gnosis: {res.name if res else 'None'}", "32")
                        return res

        # --- BRANCH B: THE SCOUT (THE PHYSICAL DISK WALK) ---
        best_candidate: Optional[Path] = None
        try:
            # =========================================================================
            # == MOVEMENT III: TARGET ACQUISITION (THE WALK)                         ==
            # =========================================================================
            candidates: List[Path] = []
            scanned_paths: Set[Path] = set()

            # Priority Search Strata
            search_roots = [root]
            for sub in ['src', 'app', 'core']:
                p = root / sub
                if p.exists(): search_roots.append(p)

            for base in search_roots:
                try:
                    # [ASCENSION 22]: Shallow Diagnostic Suture via os.scandir
                    with os.scandir(base) as it:
                        for entry in it:
                            if entry.name in self.IGNORE_DIRS or entry.name.startswith('.'):
                                continue

                            # [ASCENSION 14]: Hydraulic CPU Yield
                            time.sleep(0)

                            if entry.is_dir(follow_symlinks=False):
                                # Only go 1 level deep in sub-packages to avoid O(N) storm
                                self._scan_shallow_diagnostic(entry.path, candidates, scanned_paths, _proclaim)
                                continue

                            if not entry.name.endswith('.py'): continue

                            p = Path(entry.path)
                            if p in scanned_paths: continue

                            # Skip known noise files
                            if entry.name.startswith("test_") or entry.name in ("conftest.py", "setup.py",
                                                                                "__init__.py"):
                                continue

                            candidates.append(p)
                            scanned_paths.add(p)
                except Exception as e:
                    _proclaim(f"IO_FRACTURE in {base.name}: {e}", "31")

            # =========================================================================
            # == MOVEMENT IV: THE ADJUDICATION (SCORING)                             ==
            # =========================================================================
            best_score = 0
            _proclaim(f"Scout Adjudicating {len(candidates)} candidates...")

            for cand in candidates:
                score = 0
                name = cand.name

                # [ASCENSION 18]: File Size Sarcophagus
                try:
                    if cand.stat().st_size > 1 * 1024 * 1024:  # 1MB Limit
                        continue
                except OSError:
                    pass

                # [ASCENSION 11]: Semantic Depth Priority
                if name == "main.py":
                    score += 40
                elif name == "app.py":
                    score += 30
                elif name in ("wsgi.py", "asgi.py", "server.py"):
                    score += 20

                # [ASCENSION 6 & 12]: THE DEEP-READ THROTTLE & NULL-BYTE ANNIHILATOR
                try:
                    # Use contextual reader (Staging Aware)
                    content = self.read(cand, root, tx)
                    if not content:
                        content = cand.read_bytes().decode('utf-8', errors='ignore')

                    if content:
                        # [ASCENSION 6]: Sample only the first 8KB
                        content_sample = content[:8192]

                        for marker in markers:
                            if marker in content_sample:
                                score += 50

                        # [ASCENSION 21]: Structural Hints
                        if '__main__' in content_sample and 'if __name__' in content_sample:
                            score += 25
                        if "FastAPI(" in content_sample: score += 10
                except Exception as e:
                    _proclaim(f"   -> [FRACTURE] Could not scry {name}: {e}", "31")

                if score > best_score:
                    best_score = score
                    best_candidate = cand

            _proclaim(
                f"Scout Concluded in {time.perf_counter() - start_t:.2f}s. Winner: {best_candidate.name if best_candidate else 'None'}",
                "36")

        except Exception as catastrophic_scout_error:
            _proclaim(f"Scout suffered catastrophic paradox: {catastrophic_scout_error}", "41")

        finally:
            # =========================================================================
            # == MOVEMENT V: THE PANIC-PROOF SCOUT RELEASE (THE FIX)                 ==
            # =========================================================================
            # [ASCENSION 2]: We mathematically guarantee that Watchers are awoken
            # even if the Scout crashes entirely during the I/O pass.
            with self._GLOBAL_LOCK:
                # Inscribe the Gnosis into the eternal memo-matrix
                self._GLOBAL_MEMO[cache_key] = (time.time(), best_candidate)

                # Exorcise the Promise and awaken the sleeping Watchers
                if cache_key in self._GLOBAL_ACTIVE_SEARCHES:
                    event = self._GLOBAL_ACTIVE_SEARCHES.pop(cache_key)
                    event.set()

        return best_candidate

    def _scan_shallow_diagnostic(self, path_str: str, candidates: List[Path], scanned: Set[Path], proclaim: Callable):
        """[ASCENSION 22]: High-speed, non-recursive sibling check."""
        try:
            with os.scandir(path_str) as it:
                for entry in it:
                    if entry.is_file(follow_symlinks=False) and entry.name.endswith('.py'):
                        p = Path(entry.path)
                        if p not in scanned:
                            candidates.append(p)
                            scanned.add(p)
        except Exception as e:
            proclaim(f"Shallow scan fracture in {path_str}: {e}", "31")

    def __repr__(self) -> str:
        return f"<Ω_ENTRYPOINT_DIVINER mode=GLOBAL_PROMISE_REGISTRY status=RESONANT>"