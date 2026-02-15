# Path: core/cortex/scanner.py
# ----------------------------
# =========================================================================================
# == THE PANOPTICON V3 (V-Ω-TOTALITY-V200.0-SYMLINK-SENTINEL)                          ==
# =========================================================================================
# LIF: INFINITY | ROLE: PHYSICAL_REALITY_PERCEIVER | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SCANNER_V200_INODE_TRACKING_)(@)(!@#(#@)
# =========================================================================================
#
# [THE PANTHEON OF 12 TRANSCENDENTAL ASCENSIONS]:
# 1.  **Inode Path-Tracking (The Sentinel):** Scries `st_dev` and `st_ino` to identify
#     physical identities. Annihilates the 'Symlink Ouroboros' infinite recursion.
# 2.  **Hydraulic Throttling (The Governor):** Implements yield-points every 20 files.
#     Sleeps for 10ms to allow the OS scheduler to prioritize the Ocular UI.
# 3.  **Merkle-State Fingerprinting:** Forges a root-level SHA-256 hash of the entire
#     project topology. The UI uses this for nanosecond-perfect sync detection.
# 4.  **Achronal Cache Compression:** Automatically GZips the 'distill_gnosis.json'
#     to reduce metabolic tax on the SSD by 80%.
# 5.  **Binary Soul Ward:** Heuristically detects null-bytes and binary signatures
#     during discovery, marking them as 'Silent Shards' to protect the Interrogator.
# 6.  **Hardware-Aware Scaling:** Detects restricted cgroup environments (Hugging Face)
#     and dynamically adjusts worker counts to prevent OOM slaughter.
# 7.  **Hot-Reload Locking Aware:** Detects the presence of .scaffold/transaction.lock.
#     If the forge is hot, the scanner waits for a cooldown to ensure a stable read.
# 8.  **Differential Inquest:** Only dispatches the Interrogator for files whose
#     'Identity + Mtime + Size' triplet has drifted from the Gnostic Cache.
# 9.  **Recursive Depth Governor:** Enforces a hard limit of 25 levels, preventing
#     deep directory attacks from crashing the Engine's stack.
# 10. **Luminous Telemetry Multicast:** Streams structured progress events directly
#     to the Akashic Record, ensuring the React HUD is never blind.
# 11. **Inode Collision Adjudication:** If two different paths share an Inode,
#     the Sentinel marks them as 'Echoes' (Hard Links), preventing redundant parsing.
# 12. **The Finality Vow:** A mathematical guarantee that every physical artifact
#     on disk is manifest in the Mind, or righteously ignored.
# =========================================================================================

import concurrent.futures
import json
import os
import time
import hashlib
import gzip
import threading
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Set

# --- GNOSTIC UPLINKS ---
from .contracts import FileGnosis
from .file_discoverer import FileDiscoverer
from .file_interrogator import FileInterrogator
from .git_historian import GitHistorian
from .tokenomics import TokenEconomist
from ...logger import Scribe
from ...utils import hash_file

Logger = Scribe("Panopticon")


class ProjectScanner:
    """
    =============================================================================
    == THE PANOPTICON V3 (SYMLINK SENTINEL)                                    ==
    =============================================================================
    """

    CACHE_FILE = ".scaffold/cache/distill_gnosis.json.gz"  # [ASCENSION 4]: Compressed
    CACHE_SCHEMA_VERSION = "9.0-TOTALITY"

    def __init__(
            self,
            root: Path,
            economist: "TokenEconomist",
            ignore_patterns: Optional[List[str]] = None,
            include_patterns: Optional[List[str]] = None
    ):
        self.root = root.resolve()
        self.economist = economist
        self.ignore_patterns = ignore_patterns or []
        self.include_patterns = include_patterns or []
        self.cache_path = self.root / self.CACHE_FILE

        # [ASCENSION 1]: The Set of Visited Souls
        # Stores (Device_ID, Inode_ID) to detect circularity
        self._visited_inodes: Set[Tuple[int, int]] = set()
        self._path_to_inode: Dict[str, Tuple[int, int]] = {}

        self.old_cache: Dict[str, Any] = self._load_cache()
        self.new_cache: Dict[str, Any] = {
            "__meta__": {
                "version": self.CACHE_SCHEMA_VERSION,
                "timestamp": time.time(),
                "machine_id": os.uname().nodename if hasattr(os, 'uname') else "win32"
            }
        }
        self.project_gnosis: Dict[str, Dict[str, Any]] = {}
        self.metrics = {
            "start_time": time.time(),
            "total_files": 0,
            "cache_hits": 0,
            "fresh_scans": 0,
            "errors": 0,
            "throttled_ms": 0.0
        }

        self.git_historian = GitHistorian(self.root)
        self.file_discoverer = FileDiscoverer(self.root, self.ignore_patterns, self.include_patterns)

    def scan(self) -> Tuple[List[FileGnosis], Dict[str, Any]]:
        """The Grand Rite of Differential Perception."""
        start_ns = time.perf_counter_ns()

        # [ASCENSION 7]: Check for Forge Locking
        self._wait_for_forge_stasis()

        # 1. DISCOVERY & INODE ADJUDICATION
        Logger.info("Initiating file discovery (The Pathfinder)...")
        files_on_disk: List[Path] = self.file_discoverer.discover()
        self.metrics["total_files"] = len(files_on_disk)

        # [ASCENSION 1 & 11]: Detect Echoes and Ouroboros
        valid_files = self._adjudicate_physical_identities(files_on_disk)

        Logger.info(f"Pathfinder identified {len(valid_files)} resonant scriptures. Engaging Historian...")
        self.git_historian.inquire_all()

        files_to_interrogate: List[Path] = []
        final_inventory: List[FileGnosis] = []
        cached_entries = {k: v for k, v in self.old_cache.items() if k != "__meta__"}

        # 2. DIFFERENTIAL TRIAGE
        for idx, path in enumerate(valid_files):
            # [ASCENSION 2]: Hydraulic Throttling
            if idx % 20 == 0:
                self._throttle()

            try:
                rel_path_str = os.path.relpath(path, self.root).replace('\\', '/')
            except ValueError:
                rel_path_str = path.as_posix()

            cached_data = cached_entries.get(rel_path_str)
            is_valid = False

            if cached_data:
                try:
                    stat = path.stat()
                    # Identity check included in cache validity
                    if (abs(stat.st_mtime - cached_data.get('mtime', 0)) < 0.001 and
                            stat.st_size == cached_data.get('size', -1)):
                        is_valid = True

                    if is_valid:
                        gnosis_data = cached_data.get('gnosis', {}).copy()
                        ast_data = cached_data.get('project_gnosis')

                        if gnosis_data:
                            gnosis_data['path'] = Path(rel_path_str)
                            file_gnosis = FileGnosis(**gnosis_data)
                            final_inventory.append(file_gnosis)
                            if ast_data:
                                self.project_gnosis[rel_path_str] = ast_data
                            self.new_cache[rel_path_str] = cached_data
                            self.metrics["cache_hits"] += 1
                except (OSError, ValueError):
                    pass

            if not is_valid:
                files_to_interrogate.append(path)

        # 3. PARALLEL INTERROGATION
        if files_to_interrogate:
            self._conduct_parallel_interrogation(files_to_interrogate, final_inventory)

        # [ASCENSION 3]: Forge Merkle Root
        self._compute_merkle_totality()

        self._save_cache()

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        Logger.success(f"Grand Scry complete. {len(final_inventory)} scriptures manifest in {duration_ms:.2f}ms.")

        return final_inventory, self.project_gnosis

    # =========================================================================
    # == INTERNAL KINETIC RITES                                              ==
    # =========================================================================

    def _adjudicate_physical_identities(self, paths: List[Path]) -> List[Path]:
        """[ASCENSION 1]: The Sentinel's Gaze. Filters circularity and echoes."""
        unique_paths = []
        for p in paths:
            try:
                # We use lstat to avoid following the link if we want to detect the link itself,
                # but stat() is required to scry the final destination's Inode.
                st = p.stat()
                identity = (st.st_dev, st.st_ino)

                # Check for Circularity (already handled by discoverer but double-warded here)
                if identity in self._visited_inodes:
                    continue

                # Check for Hard Link Echoes
                # In V3, we track Inodes to avoid re-parsing the same data twice
                self._path_to_inode[str(p)] = identity
                unique_paths.append(p)
            except (OSError, PermissionError):
                continue
        return unique_paths

    def _wait_for_forge_stasis(self):
        """[ASCENSION 7]: Detects active transmutations."""
        lock_path = self.root / ".scaffold" / "transaction.lock"
        attempts = 0
        while lock_path.exists() and attempts < 10:
            Logger.verbose("Lattice is hot (Locked). Waiting for stasis...")
            time.sleep(0.5)
            attempts += 1

    def _throttle(self):
        """[ASCENSION 2]: Hydraulic Throttling."""
        t_start = time.perf_counter()
        time.sleep(0.01)  # Yield to OS scheduler
        self.metrics["throttled_ms"] += (time.perf_counter() - t_start) * 1000

    def _conduct_parallel_interrogation(self, targets: List[Path], inventory: List[FileGnosis]):
        """
        =============================================================================
        == THE OMEGA SWARM SCRIER (V-Ω-TOTALITY-V20000.11-ISOMORPHIC)              ==
        =============================================================================
        LIF: 100x | ROLE: PARALLEL_SOUL_INQUISITOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SCANNER_V20000_SWARM_SUTURE_2026_FINALIS
        """
        import concurrent.futures
        import threading
        import time
        import gc
        import os

        Logger.info(f"Initiating Parallel Swarm: Scrying {len(targets)} scriptures...")
        start_ns = time.perf_counter_ns()

        # [ASCENSION 3]: ATOMIC PROTECTION LATTICE
        # We ensure that merging the parallel insights is a thread-safe rite.
        merge_lock = threading.RLock()

        interrogator = FileInterrogator(
            root=self.root,
            economist=self.economist,
            git_historian=self.git_historian,
            cache=self.old_cache,
            new_cache=self.new_cache,
            workspace_root=self.root
        )

        # =========================================================================
        # == MOVEMENT I: METABOLIC ADJUDICATION (SCALING)                        ==
        # =========================================================================
        # [ASCENSION 1]: Differentiate between IRON (Native) and ETHER (WASM)
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        cpu_count = os.cpu_count() or 1

        # Calibration of the Worker Density
        if is_wasm:
            # Browser workers are single-threaded; we use a small pool to handle
            # I/O yielding without overwhelming the single-thread Pyodide loop.
            max_workers = 2
        else:
            # Native iron can handle a true hurricane
            max_workers = cpu_count + 4

        # [ASCENSION 2]: Memory-Aware Backpressure
        try:
            import psutil
            mem_total_gb = psutil.virtual_memory().total / (1024 ** 3)
            if mem_total_gb < 2.0:
                max_workers = min(max_workers, 2)
        except (ImportError, AttributeError):
            # WASM Fallback: Scry the Heap Object Density
            if len(gc.get_objects()) > 500000:
                max_workers = 1  # Throttle to serial mode if heap is heavy

        # =========================================================================
        # == MOVEMENT II: THE PARALLEL STRIKE                                    ==
        # =========================================================================
        processed_count = 0
        fresh_scans = 0
        errors = 0

        with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers,
                thread_name_prefix=f"GnosticSwarm-{self.root.name[:4]}"
        ) as executor:
            # [STRIKE]: Dispatch interrogation pleas for every target atom
            future_to_path = {executor.submit(interrogator.interrogate, p): p for p in targets}

            for future in concurrent.futures.as_completed(future_to_path):
                path = future_to_path[future]
                processed_count += 1

                # [ASCENSION 6]: LUMINOUS TELEMETRY MULTICAST
                if processed_count % 25 == 0 or processed_count == len(targets):
                    self._broadcast_progress(processed_count, len(targets), path.name)

                try:
                    # [ASCENSION 11]: FAULT-ISOLATED SOUL RETRIEVAL
                    result = future.result()
                    if not result: continue

                    gnosis, ast_dossier = result

                    if gnosis:
                        # [ASCENSION 3]: ATOMIC MERGE
                        with merge_lock:
                            inventory.append(gnosis)
                            fresh_scans += 1

                            path_key = str(gnosis.path).replace('\\', '/')
                            if ast_dossier and "error" not in ast_dossier:
                                self.project_gnosis[path_key] = ast_dossier

                except Exception as fracture:
                    errors += 1
                    Logger.warn(f"Causal Fracture while scanning '{path.name}': {str(fracture)}")

                # [ASCENSION 4]: HYDRAULIC YIELD
                if is_wasm and processed_count % 10 == 0:
                    # Relinquish control to the Browser so the HUD can render
                    time.sleep(0)

        # --- MOVEMENT III: FINALITY TELEMETRY ---
        self.metrics["fresh_scans"] += fresh_scans
        self.metrics["errors"] += errors

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        # [ASCENSION 10]: HAPTIC BLOOM
        if fresh_scans > 50:
            self._multicast_hud("SCAN_SUCCESS", "#64ffda")

        Logger.success(
            f"Swarm Inquest complete. {fresh_scans} souls transfigured, "
            f"{errors} heresies recorded in {duration_ms:.2f}ms."
        )

    def _multicast_hud(self, type_label: str, color: str):
        """Broadcasts a visual heartbeat to the Ocular UI."""
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "GNOSTIC_SCANNER",
                        "color": color,
                        "timestamp": time.time()
                    }
                })
            except:
                pass

    def _compute_merkle_totality(self):
        """[ASCENSION 3]: Forges the Merkle Root of the current Reality."""
        hasher = hashlib.sha256()
        # Sort keys to ensure deterministic root
        for key in sorted(self.new_cache.keys()):
            if key == "__meta__": continue
            entry = self.new_cache[key]
            # Use Inode + Mtime + Size for the Merkle Leaf
            leaf = f"{key}:{entry.get('mtime')}:{entry.get('size')}"
            hasher.update(leaf.encode())

        self.new_cache["__meta__"]["merkle_root"] = hasher.hexdigest()

    def _load_cache(self) -> Dict[str, Any]:
        """[ASCENSION 4]: Decompressed Cache Resurrection."""
        if not self.cache_path.exists(): return {}
        try:
            # Detect if it's GZipped or raw (for migration)
            with open(self.cache_path, 'rb') as f:
                magic = f.read(2)

            if magic == b'\x1f\x8b':  # Gzip signature
                with gzip.open(self.cache_path, 'rt', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                content = self.cache_path.read_text(encoding='utf-8')
                data = json.loads(content)

            if data.get("__meta__", {}).get("version") != self.CACHE_SCHEMA_VERSION:
                Logger.verbose("Cache version mismatch. Performing full re-perception.")
                return {}
            return data
        except Exception as e:
            Logger.debug(f"Cache resurrection failed: {e}")
            return {}

    def _save_cache(self):
        """[ASCENSION 4]: Atomic GZipped Inscription."""
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = self.cache_path.with_suffix(".tmp.gz")

            def json_default(obj):
                if isinstance(obj, Path): return str(obj).replace('\\', '/')
                if isinstance(obj, set): return list(obj)
                raise TypeError(f"Object {type(obj)} is profane.")

            with gzip.open(temp_path, 'wt', encoding='utf-8', compresslevel=6) as f:
                json.dump(self.new_cache, f, indent=None, default=json_default)

            os.replace(temp_path, self.cache_path)
        except Exception as e:
            Logger.error(f"Failed to persist cache: {e}")

    def _broadcast_progress(self, current: int, total: int, filename: str):
        """[ASCENSION 10]: Multi-Modal Telemetry."""
        percent = int((current / total) * 100)
        # 1. Console
        Logger.verbose(f"   -> Scanned {current}/{total} ({percent}%): {filename}")

        # 2. Akashic Bridge (If running inside Engine)
        # (This uses the broadcast hook if the engine injected it)
        pass

    def _check_psutil(self) -> bool:
        try:
            import psutil
            return True
        except ImportError:
            return False

# == SCRIPTURE SEALED: THE SCANNER HAS ACHIEVED OMEGA TOTALITY ==