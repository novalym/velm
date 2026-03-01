# Path: src/velm/core/cortex/file_discoverer.py
# ---------------------------------------------

import os
import time
import json
import fnmatch
import hashlib
import threading
import concurrent.futures
import sys
from pathlib import Path
from typing import List, Set, Optional, Iterator, Dict, Any, Final, Tuple

# --- Core Dependencies ---
from .knowledge import KnowledgeBase
from .contracts import GnosticPath
from ...logger import Scribe
from ...utils import get_ignore_spec

# --- Optional Acceleration Modules ---
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

Logger = Scribe("FileDiscoverer")


class TopologyCache:
    """
    Persists directory state to disk to enable O(1) warm-boot discovery.
    Utilizes directory mtime as a validity key for cache entries.

    Attributes:
        CACHE_VERSION (str): Schema version identifier for cache invalidation.
        root (Path): The project root directory.
        cache_path (Path): Physical location of the cache file.
        _memory (Dict[str, Any]): In-memory representation of the cached tree structure.
        _dirty (bool): Flag indicating if in-memory state differs from disk.
    """
    CACHE_VERSION: Final[str] = "2.0-STREAMING"

    def __init__(self, root: Path):
        self.root = root
        self.cache_path = root / ".scaffold" / "cache" / "topology.json"
        self._memory: Dict[str, Any] = {}
        self._dirty = False

    def load(self) -> None:
        """
        Loads the cache from disk. Validates schema version to prevent corruption.
        """
        if not self.cache_path.exists():
            return
        try:
            data = json.loads(self.cache_path.read_text(encoding='utf-8'))
            if data.get("__version__") == self.CACHE_VERSION:
                self._memory = data.get("tree", {})
            else:
                self._memory = {}  # Schema mismatch, start fresh
        except (json.JSONDecodeError, OSError):
            self._memory = {}  # Corrupt cache file, start fresh

    def save(self) -> None:
        """
        Persists the cache to disk using an atomic write strategy.
        """
        if not self._dirty:
            return
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "__version__": self.CACHE_VERSION,
                "timestamp": time.time(),
                "tree": self._memory
            }
            # Atomic write via temporary file
            temp = self.cache_path.with_suffix(".tmp")
            temp.write_text(json.dumps(data), encoding='utf-8')
            os.replace(temp, self.cache_path)
            self._dirty = False
        except OSError:
            pass  # Suppress IO errors during cache write to prioritize main execution flow

    def get_cached_files(self, dir_path: str, current_mtime: float) -> Optional[List[Dict]]:
        """
        Retrieves cached file entries for a directory if the mtime matches.

        Args:
            dir_path: Relative path string of the directory.
            current_mtime: Current modification timestamp from filesystem.

        Returns:
            List of file dictionaries if cache is valid, None otherwise.
        """
        entry = self._memory.get(dir_path)
        # Check mtime with a small epsilon for float comparison stability
        if entry and abs(entry.get("mtime", 0) - current_mtime) < 0.1:
            return entry.get("files")
        return None

    def update_dir(self, dir_path: str, current_mtime: float, files: List[Dict]) -> None:
        """
        Updates the cache entry for a specific directory.

        Args:
            dir_path: Relative path string of the directory.
            current_mtime: Current modification timestamp.
            files: List of file dictionaries present in the directory.
        """
        self._memory[dir_path] = {
            "mtime": current_mtime,
            "files": files
        }
        self._dirty = True


class FileDiscoverer:
    """
    High-performance file system scanner designed for rapid ingestion of large codebases.

    Features:
    - **Hybrid Execution:** Automatically switches between Rust-accelerated scanning (via `scaffold_core_rs`)
      and optimized Python implementations based on availability and environment.
    - **Substrate Awareness:** Detects WASM environments to enforce synchronous execution, preventing threading crashes.
    - **Parallelism:** Utilizes `ThreadPoolExecutor` for parallel directory scanning on native systems.
    - **Topological Caching:** Caches directory contents keyed by mtime to skip redundant IO on subsequent runs.
    - **Ancestral Lookups:** Scans parent directories for critical configuration files (e.g., git config, package manifests)
      up to repository boundaries.
    - **Robust Filtering:** Applies `.gitignore` logic and custom inclusion/exclusion patterns.
    """

    _iron_core_disabled = False

    # Directories that are universally ignored for performance and relevance.
    SHADOW_FILES: Final[Set[str]] = {
        '.DS_Store', 'Thumbs.db', 'desktop.ini', '$RECYCLE.BIN',
        '.spotlight-V100', '.Trashes', 'ehthumbs.db'
    }

    # Configuration files looked for in parent directories.
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

        # Initialize ignore specifications (gitignore logic)
        self.ignore_spec = get_ignore_spec(self.root, extra_patterns=ignore_patterns or [])

        # Inode tracking to prevent infinite loops with symlinks
        self.visited_inodes: Set[int] = set()

        # Determine availability of Rust acceleration
        self.use_iron_core = RUST_AVAILABLE and not FileDiscoverer._iron_core_disabled

        # Initialize inclusion specifications
        self.include_spec = None
        self.simple_include_patterns = include_patterns or []
        if self.simple_include_patterns and PATHSPEC_AVAILABLE:
            self.include_spec = PathSpec.from_lines("gitwildmatch", self.simple_include_patterns)

        # Initialize caching subsystem
        self.use_cache = use_cache
        self.cache = TopologyCache(self.root)
        if self.use_cache:
            self.cache.load()

    def discover(self) -> List[Path]:
        """
        Synchronously consumes the discovery stream into a list.
        Convenience wrapper around `stream_discovery`.
        """
        return list(self.stream_discovery())

    def stream_discovery(self) -> Iterator[Path]:
        """
        Yields file paths as they are discovered.
        Orchestrates the scanning strategy based on environment capabilities.
        """
        Logger.verbose(f"Initializing discovery stream. Root: {self.root} | Acceleration: {self.use_iron_core}")

        # 1. Ancestral Lookup: Scan upwards for context
        for ancestor in self._gaze_upon_ancestry():
            yield ancestor

        # 2. Core Discovery: Execute scanning strategy
        if self.use_iron_core:
            yield from self._stream_with_iron_core()
        else:
            yield from self._stream_python_dynamic()

        # 3. Finalization: Persist cache state
        if self.use_cache:
            self.cache.save()

    def _stream_with_iron_core(self) -> Iterator[Path]:
        """
        Executes scanning using the Rust extension module for maximum throughput.
        Falls back to Python implementation on failure.
        """
        try:
            # scaffold_core_rs returns a list of FileRecord objects
            records = scaffold_core_rs.scan_directory(str(self.root), False)

            for record in records:
                path = GnosticPath(record.path)
                # Pre-populate stat cache on GnosticPath to avoid re-statting
                path.init_gnosis(size=record.size, mtime=record.mtime, is_binary=record.is_binary)

                if self._should_yield_file(path):
                    yield path

        except Exception as e:
            Logger.error(f"Rust acceleration failed: {e}. Disabling acceleration and falling back to Python.")
            FileDiscoverer._iron_core_disabled = True
            self.use_iron_core = False
            yield from self._stream_python_dynamic()

    def _stream_python_dynamic(self) -> Iterator[Path]:
        """
        Selects the appropriate Python scanning strategy based on the runtime environment.
        """
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        if is_wasm:
            # WASM environments (browser main thread/web worker) typically do not support
            # true threading primitives or fork(), so we must run synchronously.
            yield from self._stream_synchronously()
        else:
            # Native environments can leverage multi-threading for IO-bound directory traversal.
            yield from self._stream_with_parallel_python()

    def _stream_synchronously(self) -> Iterator[Path]:
        """
        Synchronous directory walker for environments without threading support (e.g., WASM).
        """
        dir_queue = [self.root]

        while dir_queue:
            current_dir = dir_queue.pop(0)
            try:
                rel_dir = self._to_rel_str(current_dir)
                try:
                    dir_mtime = current_dir.stat().st_mtime
                except OSError:
                    dir_mtime = 0

                cacheable_files = []

                # Check cache first if enabled (logic inside loop for simplicity of integration with scandir pattern)
                # Note: Full cache logic integration would require refactoring to check cache *before* scandir.
                # For this implementation, we proceed with scandir but use cache for update.
                # Optimization: Could check cache validity here and skip scandir if valid.

                cached_files = None
                if self.use_cache:
                    cached_files = self.cache.get_cached_files(rel_dir, dir_mtime)

                if cached_files is not None:
                    # Serve from Cache
                    for f_meta in cached_files:
                        f_path = current_dir / f_meta["name"]
                        if f_meta["is_dir"]:
                            if not self._is_dir_ignored(current_dir, f_meta["name"]):
                                dir_queue.append(f_path)
                        else:
                            gp = GnosticPath(f_path)
                            gp.init_gnosis(f_meta["size"], f_meta["mtime"],
                                           False)  # Binary status not in V1 cache schema
                            if self._should_yield_file(gp, skip_ignore_check=True):
                                yield gp
                else:
                    # Scan Disk
                    with os.scandir(current_dir) as entries:
                        for entry in entries:
                            name = entry.name
                            if name in self.SHADOW_FILES: continue

                            try:
                                is_dir = entry.is_dir(follow_symlinks=False)
                            except OSError:
                                continue

                            if is_dir:
                                if name in KnowledgeBase.ABYSS_DIRECTORIES: continue
                                if self._is_dir_ignored(current_dir, name): continue
                                dir_queue.append(Path(entry.path))
                                cacheable_files.append({"name": name, "is_dir": True, "size": 0, "mtime": 0})
                            else:
                                gp = GnosticPath(entry.path)
                                try:
                                    stat_res = entry.stat(follow_symlinks=False)
                                    gp.init_gnosis(stat_res.st_size, stat_res.st_mtime, False)
                                    if self._should_yield_file(gp):
                                        yield gp
                                    cacheable_files.append({"name": name, "is_dir": False, "size": stat_res.st_size,
                                                            "mtime": stat_res.st_mtime})
                                except OSError:
                                    pass

                    if self.use_cache:
                        self.cache.update_dir(rel_dir, dir_mtime, cacheable_files)

            except Exception:
                pass  # Gracefully handle permissions/IO errors on directory access

    def _stream_with_parallel_python(self) -> Iterator[Path]:
        """
        Parallel directory walker using a ThreadPoolExecutor.
        Scales worker count based on CPU cores.
        """
        import queue

        MAX_WORKERS = min(32, (os.cpu_count() or 1) * 4)
        lock = threading.Lock()

        def _scan_worker(dir_path: Path):
            sub_dirs = []
            files_found = []
            try:
                rel_dir = self._to_rel_str(dir_path)
                try:
                    dir_mtime = dir_path.stat().st_mtime
                except OSError:
                    dir_mtime = 0

                cached_files = None
                if self.use_cache:
                    cached_files = self.cache.get_cached_files(rel_dir, dir_mtime)

                if cached_files is not None:
                    for f_meta in cached_files:
                        f_path = dir_path / f_meta["name"]
                        if f_meta["is_dir"]:
                            if not self._is_dir_ignored(dir_path, f_meta["name"]):
                                sub_dirs.append(f_path)
                        else:
                            gp = GnosticPath(f_path)
                            gp.init_gnosis(f_meta["size"], f_meta["mtime"], False)
                            if self._should_yield_file(gp, skip_ignore_check=True):
                                files_found.append(gp)
                else:
                    cacheable_files = []
                    with os.scandir(dir_path) as entries:
                        for entry in entries:
                            name = entry.name
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
                                gp = GnosticPath(entry.path)
                                try:
                                    stat_res = entry.stat(follow_symlinks=False)
                                    gp.init_gnosis(stat_res.st_size, stat_res.st_mtime, False)
                                    if self._should_yield_file(gp): files_found.append(gp)
                                    cacheable_files.append({"name": name, "is_dir": False, "size": stat_res.st_size,
                                                            "mtime": stat_res.st_mtime})
                                except OSError:
                                    pass

                    if self.use_cache:
                        with lock: self.cache.update_dir(rel_dir, dir_mtime, cacheable_files)
            except Exception:
                pass
            return sub_dirs, files_found

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Seed the pool with the root directory
            futures = set([executor.submit(_scan_worker, self.root)])

            while futures:
                # Wait for at least one future to complete
                done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

                for fut in done:
                    futures.remove(fut)
                    try:
                        new_dirs, new_files = fut.result()

                        # Yield files immediately to the consumer
                        for f in new_files: yield f

                        # Schedule scans for subdirectories
                        for d in new_dirs:
                            if self._safe_inode_check(d):
                                futures.add(executor.submit(_scan_worker, d))
                    except Exception as e:
                        Logger.debug(f"Scan worker exception: {e}")

    def _safe_inode_check(self, path: Path) -> bool:
        """
        Thread-safe check for inode visitation to prevent cycles.
        Returns True if path should be visited (new inode), False otherwise.
        """
        try:
            st = path.stat()
            ino = st.st_ino
            # Note: set.add is atomic in CPython, but explicit locking might be needed for other implementations.
            # Given the GIL, this is generally safe for simple sets.
            if ino in self.visited_inodes:
                return False
            self.visited_inodes.add(ino)
            return True
        except Exception:
            return False

    def _should_yield_file(self, path: Path, skip_ignore_check: bool = False) -> bool:
        """
        Determines if a file should be included in the discovery output based on configured rules.
        """
        if path.name in KnowledgeBase.ABYSS_DIRECTORIES: return False

        # 1. Inclusion Check (Whitelist)
        if not self._is_file_included(path): return False

        # 2. Exclusion Check (Blacklist)
        if not skip_ignore_check and self._is_file_ignored(path): return False

        return True

    def _gaze_upon_ancestry(self) -> Set[Path]:
        """
        Scans parent directories for repository keystones (e.g. .git, package.json).
        Stops at filesystem boundaries or git roots.
        """
        ancestors = set()
        current = self.root

        # Determine traversal limit
        limit = current
        for _ in range(4):  # Max 4 levels up
            if (limit / ".git").exists(): break
            if limit.parent == limit: break
            limit = limit.parent

        # Walk upwards
        temp = current.parent
        while temp != limit.parent:
            for name in self.ANCESTRAL_KEYSTONES:
                candidate = temp / name
                if candidate.is_file() and candidate.exists():
                    ancestors.add(candidate)

            if temp.parent == temp: break
            temp = temp.parent

        return ancestors

    def _is_dir_ignored(self, parent: Path, dir_name: str) -> bool:
        """Checks if a directory matches exclusion rules."""
        if dir_name in KnowledgeBase.ABYSS_DIRECTORIES: return True
        if self.ignore_spec:
            try:
                rel_path = self._to_rel_str(parent / dir_name) + "/"
                if self.ignore_spec.match_file(rel_path): return True
            except ValueError:
                pass
        return False

    def _is_file_ignored(self, path: Path) -> bool:
        """Checks if a file matches exclusion rules."""
        if "simulacrum_pkg" in str(path): return False  # Internal override
        if path.name in KnowledgeBase.ABYSS_DIRECTORIES: return True

        if self.ignore_spec:
            try:
                rel_path = self._to_rel_str(path)
                if self.ignore_spec.match_file(rel_path): return True
            except ValueError:
                # Handle paths outside root (Ancestral) - verify name only against common patterns
                if path.name.startswith('.'): return True
        return False

    def _is_file_included(self, path: Path) -> bool:
        """Checks if a file matches inclusion rules (if any are set)."""
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
        """
        Optimized path relativizer.
        Uses string manipulation instead of pathlib for speed in hot loops.
        """
        s_path = str(path)
        s_root = str(self.root)
        if s_path.startswith(s_root):
            return s_path[len(s_root):].lstrip(os.sep).replace('\\', '/')
        return path.name  # Fallback for external paths