# Path: src/velm/core/cortex/file_discoverer.py
# ---------------------------------------------


import os
import time
import json
import fnmatch
import hashlib
import threading
import concurrent.futures
from pathlib import Path
from typing import List, Set, Optional, Iterator, Dict, Any, Final, Tuple, Iterable

# --- GNOSTIC UPLINKS ---
from .knowledge import KnowledgeBase
from .contracts import GnosticPath
from ...logger import Scribe
from ...utils import get_ignore_spec

# --- SUBSTRATE SENSING ---
try:
    from pathspec import PathSpec

    PATHSPEC_AVAILABLE = True
except ImportError:
    PATHSPEC_AVAILABLE = False

try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    scaffold_core_rs = None
    RUST_AVAILABLE = False

Logger = Scribe("GnosticPathfinder")


class TopologyCache:
    """
    =============================================================================
    == THE TOPOLOGICAL CHRONOCACHE (V-Ω-MEMORY-PERSISTENCE)                    ==
    =============================================================================
    Persists the map of reality to disk to allow for O(1) warm-boot discovery.
    Uses directory mtimes as validity keys.
    """
    CACHE_VERSION: Final[str] = "2.0-STREAMING"

    def __init__(self, root: Path):
        self.root = root
        self.cache_path = root / ".scaffold" / "cache" / "topology.json"
        self._memory: Dict[str, Any] = {}
        self._dirty = False

    def load(self):
        """Resurrects the memory from disk."""
        if not self.cache_path.exists():
            return
        try:
            data = json.loads(self.cache_path.read_text(encoding='utf-8'))
            if data.get("__version__") == self.CACHE_VERSION:
                self._memory = data.get("tree", {})
        except Exception:
            # If memory is corrupt, we start with a clean slate
            self._memory = {}

    def save(self):
        """Inscribes the memory to disk."""
        if not self._dirty: return
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "__version__": self.CACHE_VERSION,
                "timestamp": time.time(),
                "tree": self._memory
            }
            # Atomic write
            temp = self.cache_path.with_suffix(".tmp")
            temp.write_text(json.dumps(data), encoding='utf-8')
            os.replace(temp, self.cache_path)
        except Exception:
            pass

    def get_cached_files(self, dir_path: str, current_mtime: float) -> Optional[List[Dict]]:
        """
        Returns cached files for a directory if the mtime matches.
        Returns None if cache is stale or missing.
        """
        entry = self._memory.get(dir_path)
        if entry and abs(entry.get("mtime", 0) - current_mtime) < 0.1:
            return entry.get("files")
        return None

    def update_dir(self, dir_path: str, current_mtime: float, files: List[Dict]):
        """Updates the cache for a specific directory node."""
        self._memory[dir_path] = {
            "mtime": current_mtime,
            "files": files
        }
        self._dirty = True


class FileDiscoverer:
    """
    =================================================================================
    == THE GNOSTIC PATHFINDER (V-Ω-STREAMING-TURBO-PARALLEL)                       ==
    =================================================================================
    LIF: 100,000,000,000,000 | ROLE: OMNISCIENT_SCOUT

    The All-Seeing Eye of the Filesystem. It has been ascended to perform
    **Hydraulic Parallel Scanning**, **Streaming Yields**, and **Topological Caching**.

    It does not wait for the world to be mapped; it reports discoveries the moment
    they are perceived.
    """

    _iron_core_disabled = False

    # The Grimoire of Shadow Files (Kernel-level Ignore)
    SHADOW_FILES: Final[Set[str]] = {
        '.DS_Store', 'Thumbs.db', 'desktop.ini', '$RECYCLE.BIN',
        '.spotlight-V100', '.Trashes', 'ehthumbs.db'
    }

    # The Grimoire of Ancestral Keystones
    ANCESTRAL_KEYSTONES: Final[Set[str]] = {
        "README.md", "ARCHITECTURE.md", "CONTRIBUTING.md", "LICENSE",
        "package.json", "pyproject.toml", "Cargo.toml", "go.mod"
    }

    def __init__(
            self,
            root: Path,
            ignore_patterns: Optional[List[str]] = None,
            include_patterns: Optional[List[str]] = None,
            use_cache: bool = True
    ):
        self.root = root.resolve()

        # [ASCENSION 1]: The Ignore Specification
        self.ignore_spec = get_ignore_spec(self.root, extra_patterns=ignore_patterns or [])

        # [ASCENSION 2]: Inode Loop Protection
        self.visited_inodes: Set[int] = set()

        # [ASCENSION 3]: Rust Acceleration Detection
        self.use_iron_core = RUST_AVAILABLE and not FileDiscoverer._iron_core_disabled

        # [ASCENSION 4]: Inclusion Logic
        self.include_spec = None
        self.simple_include_patterns = include_patterns or []
        if self.simple_include_patterns and PATHSPEC_AVAILABLE:
            self.include_spec = PathSpec.from_lines("gitwildmatch", self.simple_include_patterns)

        # [ASCENSION 5]: Topological Caching
        self.use_cache = use_cache
        self.cache = TopologyCache(self.root)
        if self.use_cache:
            self.cache.load()

    def discover(self) -> List[Path]:
        """
        Legacy Interface: Consumes the stream into a list.
        For maximum velocity, use `stream_discovery()` instead.
        """
        return list(self.stream_discovery())

    def stream_discovery(self) -> Iterator[Path]:
        """
        =============================================================================
        == THE RITE OF THE FLOWING RIVER (STREAMING)                               ==
        =============================================================================
        Yields paths instantly as they are discovered.
        Combines Iron Core (Rust), Parallel Python, and Ancestral Gazing.
        """
        Logger.verbose(f"The Gnostic Pathfinder awakens... (Iron Core: {self.use_iron_core})")

        # 1. THE ANCESTRAL GAZE (Yield immediately)
        # We look upwards first to anchor the project in its lineage.
        for ancestor in self._gaze_upon_ancestry():
            yield ancestor

        # 2. THE CORE DISCOVERY
        if self.use_iron_core:
            yield from self._stream_with_iron_core()
        else:
            yield from self._stream_with_parallel_python()

        # 3. FINALITY
        if self.use_cache:
            self.cache.save()

    def _stream_with_iron_core(self) -> Iterator[Path]:
        """Rust-Accelerated Scanning."""
        try:
            # scaffold_core_rs typically returns a full list.
            # Ideally, we'd bind to a Rust iterator, but list is fast enough for Rust.
            records = scaffold_core_rs.scan_directory(str(self.root), False)

            for record in records:
                path_str = record.path
                # Construct GnosticPath to avoid re-statting later
                path = GnosticPath(path_str)
                path.init_gnosis(size=record.size, mtime=record.mtime, is_binary=record.is_binary)

                if self._should_yield_file(path):
                    yield path

        except Exception as e:
            Logger.error(f"The Iron Core faltered: {e}. Falling back to Pythonic Parallelism.")
            FileDiscoverer._iron_core_disabled = True
            self.use_iron_core = False
            yield from self._stream_with_parallel_python()

    def _stream_with_parallel_python(self) -> Iterator[Path]:
        """
        =============================================================================
        == THE HYDRAULIC SCANNER (PARALLEL WALK)                                   ==
        =============================================================================
        Uses a ThreadPool to scan multiple directories simultaneously.
        Yields results to the main thread via a Queue.
        """
        import queue

        # [CONFIGURATION]: Parallelism Physics
        # Disk IO latency usually allows for high thread counts.
        MAX_WORKERS = min(32, (os.cpu_count() or 1) * 4)

        # The Frontier: Directories waiting to be scanned
        # We use a set for dedup and a list for tasks
        dir_queue: List[Path] = [self.root]

        # The Result Stream
        result_queue = queue.Queue(maxsize=1000)

        # Sentinel for completion
        SENTINEL = None

        # Active scanners count
        active_scanners = 0
        lock = threading.Lock()

        def _scan_worker(dir_path: Path):
            """The atomic unit of scanning work."""
            sub_dirs = []
            files_found = []

            try:
                # [OPTIMIZATION]: Fast statting via os.scandir
                # [CACHE CHECK]
                rel_dir = self._to_rel_str(dir_path)
                cached_files = None

                # Try to get dir mtime for cache validation
                try:
                    dir_stat = dir_path.stat()
                    dir_mtime = dir_stat.st_mtime
                    if self.use_cache:
                        cached_files = self.cache.get_cached_files(rel_dir, dir_mtime)
                except OSError:
                    pass

                if cached_files is not None:
                    # CACHE HIT: Reconstruct paths from memory
                    for f_meta in cached_files:
                        f_path = dir_path / f_meta["name"]
                        # We still need to create the Path object, but we skip disk I/O
                        if f_meta["is_dir"]:
                            # Add to sub_dirs for recursion (we still need to walk the structure)
                            # Or do we? If we cache the whole tree structure, we could skip.
                            # But hybrid approach is safer. We recurse to check mtimes down the tree.
                            if not self._is_dir_ignored(dir_path, f_meta["name"]):
                                sub_dirs.append(f_path)
                        else:
                            # Rehydrate GnosticPath
                            gp = GnosticPath(f_path)
                            gp.init_gnosis(f_meta["size"], f_meta["mtime"], f_meta.get("is_binary", False))
                            if self._should_yield_file(gp,
                                                       skip_ignore_check=True):  # Already ignored in cache? No, spec changes.
                                files_found.append(gp)
                else:
                    # CACHE MISS: Physical Scan
                    cacheable_files = []

                    with os.scandir(dir_path) as entries:
                        for entry in entries:
                            name = entry.name

                            # 1. Shadow Ban
                            if name in self.SHADOW_FILES: continue

                            try:
                                is_dir = entry.is_dir(follow_symlinks=False)
                            except OSError:
                                continue

                            if is_dir:
                                if name in KnowledgeBase.ABYSS_DIRECTORIES: continue
                                if self._is_dir_ignored(dir_path, name): continue
                                sub_dirs.append(Path(entry.path))
                                cacheable_files.append({"name": name, "is_dir": True, "size": 0, "mtime": 0})
                            else:
                                # File processing
                                gp = GnosticPath(entry.path)
                                try:
                                    stat_res = entry.stat(follow_symlinks=False)
                                    gp.init_gnosis(stat_res.st_size, stat_res.st_mtime, False)  # Binary check deferred

                                    if self._should_yield_file(gp):
                                        files_found.append(gp)

                                    cacheable_files.append({
                                        "name": name, "is_dir": False,
                                        "size": stat_res.st_size, "mtime": stat_res.st_mtime
                                    })
                                except OSError:
                                    pass

                    # Update Cache
                    if self.use_cache:
                        with lock:
                            self.cache.update_dir(rel_dir, dir_mtime, cacheable_files)

            except Exception as e:
                # Permission errors, etc.
                pass

            return sub_dirs, files_found

        # THE ORCHESTRATOR LOOP
        # We process directories breadth-first using the thread pool

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = set()

            # Seed the pool
            futures.add(executor.submit(_scan_worker, self.root))

            while futures:
                # Wait for at least one future to complete
                done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

                for fut in done:
                    futures.remove(fut)
                    try:
                        new_dirs, new_files = fut.result()

                        # Yield files immediately
                        for f in new_files:
                            yield f

                        # Schedule new directories
                        for d in new_dirs:
                            # Inode Loop Check (if not cached)
                            if self._safe_inode_check(d):
                                futures.add(executor.submit(_scan_worker, d))

                    except Exception as e:
                        Logger.debug(f"Scan worker failed: {e}")

                # If queue is empty but workers are busy?
                # wait() handles this. If futures is not empty, we loop.

    def _safe_inode_check(self, path: Path) -> bool:
        """Thread-safe inode check."""
        try:
            st = path.stat()
            ino = st.st_ino
            # We don't need a lock for set.add on CPython (atomic),
            # but for logic correctness we should be careful.
            # Actually, visited_inodes is not critical for correctness, just loop prevention.
            if ino in self.visited_inodes:
                return False
            self.visited_inodes.add(ino)
            return True
        except Exception:
            return False

    def _should_yield_file(self, path: Path, skip_ignore_check: bool = False) -> bool:
        """The Grand Filter."""
        if path.name in KnowledgeBase.ABYSS_DIRECTORIES: return False

        # 1. Inclusion Check (Whitelist)
        if not self._is_file_included(path): return False

        # 2. Exclusion Check (Blacklist)
        if not skip_ignore_check and self._is_file_ignored(path): return False

        return True

    def _gaze_upon_ancestry(self) -> Set[Path]:
        """
        [PILLAR II] The Ancestral Gaze (Healed).
        Looks upwards for keystones, but stops at repository boundaries.
        """
        ancestors = set()
        current = self.root

        # Stop condition: .git or filesystem root
        limit = current
        for _ in range(4):  # Max 4 levels up
            if (limit / ".git").exists(): break
            if limit.parent == limit: break
            limit = limit.parent

        temp = current.parent
        while temp != limit.parent:  # Iterate up to limit
            for name in self.ANCESTRAL_KEYSTONES:
                candidate = temp / name
                if candidate.is_file() and candidate.exists():
                    # Only include if not ignored by global specs (optional)
                    ancestors.add(candidate)

            if temp.parent == temp: break
            temp = temp.parent

        return ancestors

    def _is_dir_ignored(self, parent: Path, dir_name: str) -> bool:
        if dir_name in KnowledgeBase.ABYSS_DIRECTORIES: return True
        if self.ignore_spec:
            # Construct relative path string ending in /
            # Optimization: Don't resolve fully if we can construct string cheaply
            try:
                # rel_parent = parent.relative_to(self.root) # Expensive?
                # Faster:
                rel_path = self._to_rel_str(parent / dir_name) + "/"
                if self.ignore_spec.match_file(rel_path): return True
            except ValueError:
                pass
        return False

    def _is_file_ignored(self, path: Path) -> bool:
        # [ASCENSION]: Sacred internal files
        if "simulacrum_pkg" in str(path): return False

        if path.name in KnowledgeBase.ABYSS_DIRECTORIES: return True

        if self.ignore_spec:
            try:
                rel_path = self._to_rel_str(path)
                if self.ignore_spec.match_file(rel_path): return True
            except ValueError:
                # Path outside root (Ancestral) - verify name only
                if path.name.startswith('.'): return True

        return False

    def _is_file_included(self, path: Path) -> bool:
        if not self.include_spec and not self.simple_include_patterns: return True
        try:
            rel_path = self._to_rel_str(path)
            if self.include_spec: return self.include_spec.match_file(rel_path)

            # Simple fnmatch fallback
            for pat in self.simple_include_patterns:
                if fnmatch.fnmatch(rel_path, pat): return True
            return False
        except ValueError:
            # Ancestral files are included if they match name pattern
            for pat in self.simple_include_patterns:
                if fnmatch.fnmatch(path.name, pat): return True
            return False

    def _to_rel_str(self, path: Path) -> str:
        """High-speed path relativizer."""
        # pathlib.relative_to can be slow. String manipulation is faster if safe.
        s_path = str(path)
        s_root = str(self.root)
        if s_path.startswith(s_root):
            return s_path[len(s_root):].lstrip(os.sep).replace('\\', '/')
        return path.name  # Fallback