# Path: core/cortex/scanner.py
# ----------------------------

import concurrent.futures
import json
import os
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Set

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
    =================================================================================
    == THE PANOPTICON (V-Ω-TELEMETRIC-HEARTBEAT)                                   ==
    =================================================================================
    LIF: 100,000,000,000,000

    The All-Seeing Eye.
    [HEALED]: Now broadcasts its progress to the Architect, preventing the
    "Silent Freeze" heresy.
    """

    CACHE_FILE = ".scaffold/cache/distill_gnosis.json"
    CACHE_SCHEMA_VERSION = "8.2"

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

        self.old_cache: Dict[str, Any] = self._load_cache()
        self.new_cache: Dict[str, Any] = {
            "__meta__": {"version": self.CACHE_SCHEMA_VERSION, "timestamp": time.time()}
        }
        self.project_gnosis: Dict[str, Dict[str, Any]] = {}
        self.metrics = {"start_time": time.time(), "total_files": 0, "cache_hits": 0, "fresh_scans": 0, "errors": 0}

        self.git_historian = GitHistorian(self.root)
        self.file_discoverer = FileDiscoverer(self.root, self.ignore_patterns, self.include_patterns)

    def scan(self) -> Tuple[List[FileGnosis], Dict[str, Any]]:
        """The Grand Rite of Differential Perception."""
        start_time = time.monotonic()

        Logger.info("Initiating file discovery (The Pathfinder)...")
        files_on_disk: List[Path] = self.file_discoverer.discover()
        self.metrics["total_files"] = len(files_on_disk)

        Logger.info(f"Pathfinder identified {len(files_on_disk)} candidate scriptures. Engaging Historian...")
        self.git_historian.inquire_all()

        files_to_interrogate: List[Path] = []
        final_inventory: List[FileGnosis] = []
        cached_entries = {k: v for k, v in self.old_cache.items() if k != "__meta__"}

        Logger.verbose("Verifying cache integrity...")
        for path in files_on_disk:
            try:
                rel_path_str = os.path.relpath(path, self.root).replace('\\', '/')
            except ValueError:
                rel_path_str = path.as_posix()

            cached_data = cached_entries.get(rel_path_str)
            is_valid = False

            if cached_data:
                try:
                    stat = path.stat()
                    # Stage 1: Fast Temporal Check
                    if (abs(stat.st_mtime - cached_data.get('mtime', 0)) < 0.1 and
                            stat.st_size == cached_data.get('size', -1)):
                        is_valid = True
                    # Stage 2: Cryptographic Check
                    elif 'gnosis' in cached_data and 'hash_signature' in cached_data['gnosis']:
                        current_hash = hash_file(path)
                        if current_hash == cached_data['gnosis']['hash_signature']:
                            is_valid = True

                    if is_valid:
                        # [THE FIX: IMMUTABLE COPY]
                        gnosis_data = cached_data.get('gnosis', {}).copy()
                        ast_data = cached_data.get('project_gnosis')

                        if gnosis_data:
                            # Mutate the COPY for runtime usage
                            gnosis_data['path'] = Path(rel_path_str)
                            file_gnosis = FileGnosis(**gnosis_data)
                            final_inventory.append(file_gnosis)

                            if ast_data:
                                self.project_gnosis[rel_path_str] = ast_data

                            # Store the ORIGINAL (safe) data in the new cache
                            self.new_cache[rel_path_str] = cached_data
                            self.metrics["cache_hits"] += 1
                except (OSError, ValueError):
                    pass

            if not is_valid:
                files_to_interrogate.append(path)

        if files_to_interrogate:
            Logger.info(f"Deep Scanning {len(files_to_interrogate)} modified/new scriptures...")
            interrogator = FileInterrogator(
                root=self.root,
                economist=self.economist,
                git_historian=self.git_historian,
                cache=self.old_cache,
                new_cache=self.new_cache,
                workspace_root=self.root
            )

            max_workers = min(32, (os.cpu_count() or 1) + 4)
            processed_count = 0

            # [ASCENSION]: HEARTBEAT LOGGING
            # We log every 50 files so you can see if it hangs on 'node_modules'
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_path = {executor.submit(interrogator.interrogate, p): p for p in files_to_interrogate}

                for future in concurrent.futures.as_completed(future_to_path):
                    path = future_to_path[future]
                    processed_count += 1

                    if processed_count % 50 == 0:
                        Logger.verbose(f"   -> Scanned {processed_count}/{len(files_to_interrogate)}: {path.name}")

                    try:
                        result = future.result()
                        if not result: continue
                        gnosis, ast_dossier = result
                        if gnosis:
                            final_inventory.append(gnosis)
                            self.metrics["fresh_scans"] += 1
                            try:
                                path_str = os.path.relpath(gnosis.path, ".").replace('\\', '/')
                            except ValueError:
                                path_str = str(gnosis.path).replace('\\', '/')
                            if ast_dossier and "error" not in ast_dossier:
                                self.project_gnosis[path_str] = ast_dossier
                    except Exception as e:
                        self.metrics["errors"] += 1
                        Logger.warn(f"Paradox scanning '{path.name}': {e}")

        self._save_cache()
        return final_inventory, self.project_gnosis

    def _load_cache(self) -> Dict[str, Any]:
        if not self.cache_path.exists(): return {}
        try:
            content = self.cache_path.read_text(encoding='utf-8')
            if not content.strip(): return {}
            data = json.loads(content)
            if data.get("__meta__", {}).get("version") != self.CACHE_SCHEMA_VERSION:
                return {}
            return data
        except Exception:
            return {}

    def _save_cache(self):
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = self.cache_path.with_suffix(".tmp")

            def json_default(obj):
                if isinstance(obj, Path): return str(obj).replace('\\', '/')
                if isinstance(obj, set): return list(obj)
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(self.new_cache, f, indent=None, default=json_default)
            os.replace(temp_path, self.cache_path)
        except Exception as e:
            Logger.error(f"Failed to persist cache: {e}")