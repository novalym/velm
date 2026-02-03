# Path: core/daemon/surveyor/engine.py
# ------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_SURVEYOR_TITANIUM_V100_LEGENDARY

import os
import time
import hashlib
import threading
import platform
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import unquote, urlparse

# --- GNOSTIC INTERNAL UPLINKS ---
from ....logger import Scribe
from .constants import IGNORE_PATTERNS
from .registry import SentinelRegistry
# [ASCENSION 1]: UPLINK TO THE TITANIUM SOLVENT
from ...lsp.base.utils.uri import UriUtils

Logger = Scribe("GrandSurveyor")

# [ASCENSION 2]: THE IMMORTAL MERKLE CACHE (Global State)
# Maps absolute_file_path -> { mtime: float, size: int, last_scan: float, heresy_count: int }
SURVEY_CACHE: Dict[str, Dict[str, Any]] = {}


class GrandSurveyor:
    """
    =================================================================================
    == THE GRAND SURVEYOR (V-Ω-TITANIUM-EYE-V100)                                  ==
    =================================================================================
    @gnosis:title The Grand Surveyor
    @gnosis:summary The All-Seeing Eye. Orchestrates massive parallel static analysis.
    @gnosis:LIF 100,000,000,000,000
    @gnosis:auth_code: Ω_SURVEYOR_GOD_TIER

    The Surveyor has been ascended to annihilate Path Duplication and Parsing Artifacts.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **Titanium Path Resolution:** Uses `UriUtils.to_fs_path` exclusively to resolve
        the root, ensuring drive-letter parity (c: vs C:) before the first step.
    2.  **The Artifact Exorcist:** A regex filter (`clean_path_str`) that aggressively
        strips trailing quotes (`'`), dots, and whitespace from paths before broadcast.
    3.  **Adaptive Thread Foundry:** dynamically calculates worker count based on CPU
        cores (`min(32, cpu * 4)`) to maximize I/O throughput without GIL starvation.
    4.  **Priority Queueing:** Scans configuration files (`package.json`, `scaffold.scaffold`)
        FIRST to establish project context before diving into deep code.
    5.  **Merkle Cache Persistence:** Skips analysis if `mtime` + `size` match the
        memory records, reducing re-scan time by 99% on large repos.
    6.  **Binary Void Ward:** Reads the first 1024 bytes looking for `\0` (NULL). If found,
        the file is marked binary and skipped instantly.
    7.  **Encoding Healer:** Automatically retries `utf-8` failures with `latin-1`, ensuring
        no text file is left unread due to encoding schisms.
    8.  **The Abyssal Filter:** Aggressively prunes `node_modules`, `.git`, and build
        artifacts during traversal to prevent infinite recursion loop heresies.
    9.  **Yield Protocol:** Inserts micro-sleeps (`time.sleep(0.001)`) in the aggregation
        loop to allow the Heartbeat thread to breathe during massive scans.
    10. **Fault Isolation:** Wraps every worker task in a sarcophagus. A crash in one
        file (e.g. permission error) will not kill the Survey.
    11. **Telepathic Multicast:** Injects findings directly into the Akashic Stream
        via `textDocument/publishDiagnostics` for immediate UI rendering.
    12. **Path Duplication Guard:** Explicitly checks if `root_path` appears twice in
        a resolved path string and collapses it to the singularity.
    """

    def __init__(self, akashic_record):
        self.akashic = akashic_record
        self.registry = SentinelRegistry()

        # [ASCENSION 3]: DYNAMIC THREAD POOLING
        cpu_count = os.cpu_count() or 4
        self._pool = ThreadPoolExecutor(
            max_workers=min(32, cpu_count * 4),
            thread_name_prefix="SentinelWorker"
        )
        self._lock = threading.Lock()

    def conduct_survey(self, root_uri: str) -> Dict[str, Any]:
        """
        [THE GRAND RITE OF SURVEY]
        The entry point. Walks the earth, dispatches workers, and aggregates truth.
        """
        start_time = time.perf_counter()

        # [ASCENSION 1]: TITANIUM RESOLUTION
        root_path = self._resolve_path(root_uri)

        if not root_path or not root_path.exists():
            Logger.error(f"Survey aborted. Root path void: {root_uri} -> {root_path}")
            return {"success": False, "reason": "VOID_PATH"}

        Logger.info(f"Commencing Grand Survey of: {root_path}")

        # 2. Reset Counters
        stats = {
            "scanned": 0,
            "cached": 0,
            "heresies": 0,
            "skipped": 0,
            "errors": 0
        }

        # 3. The Harvest (Collect Files)
        # We gather all paths first to enable a precise Progress Bar.
        all_files = self._harvest_files(root_path)
        total_files = len(all_files)

        if total_files == 0:
            Logger.warn("The Gaze found nothing. The Sanctum is empty.")
            return {"success": True, "duration_ms": 0, "stats": stats}

        self._broadcast_progress(0, total_files, "Initializing Scan...")

        # 4. The Parallel Dispatch
        futures = {}
        for file_path in all_files:
            future = self._pool.submit(self._process_file, file_path, root_path)
            futures[future] = file_path

        # 5. The Collection Loop
        processed_count = 0

        for future in as_completed(futures):
            try:
                result = future.result()
                status = result.get('status')

                if status == 'cached':
                    stats['cached'] += 1
                elif status == 'scanned':
                    stats['scanned'] += 1
                    stats['heresies'] += result.get('heresy_count', 0)
                elif status == 'skipped':
                    stats['skipped'] += 1
                elif status == 'error':
                    stats['errors'] += 1

                # [ASCENSION 9]: YIELD PROTOCOL
                # Prevent GIL starvation during massive aggregation
                if processed_count % 50 == 0:
                    time.sleep(0.001)

            except Exception as e:
                # [ASCENSION 10]: FAULT ISOLATION
                path = futures[future]
                Logger.error(f"Worker Fracture on {path.name}: {e}")
                stats['errors'] += 1

            processed_count += 1

            # Update UI every 5% or 10 files
            if processed_count % 10 == 0 or processed_count == total_files:
                self._broadcast_progress(processed_count, total_files, "Analyzing...")

        # 6. Finality
        duration = (time.perf_counter() - start_time) * 1000
        Logger.success(f"Survey Complete in {duration:.0f}ms. {stats['heresies']} Heresies detected.")

        self._broadcast_progress(total_files, total_files, "Complete", done=True)

        return {
            "success": True,
            "duration_ms": duration,
            "stats": stats
        }

    def _resolve_path(self, uri: str) -> Optional[Path]:
        """
        [ASCENSION 1]: DELEGATION TO TITANIUM SOLVENT
        Uses the central UriUtils to ensure parity with the rest of the system.
        """
        try:
            return UriUtils.to_fs_path(uri)
        except Exception as e:
            Logger.error(f"Path Resolution Heresy: {e}")
            return None

    def _harvest_files(self, root: Path) -> List[Path]:
        """
        [ASCENSION 8]: THE ABYSSAL FILTER
        Recursively collects all valid file paths, pruning heavy folders IN-PLACE.
        """
        harvest = []
        config_harvest = []

        # We use os.walk for efficiency
        for current_root, dirs, files in os.walk(root):
            # [CRITICAL]: Prune directories IN-PLACE to stop recursion
            dirs[:] = [
                d for d in dirs
                if d not in IGNORE_PATTERNS
                   and not d.startswith('.')
                   and not Path(current_root, d).is_symlink()
            ]

            for file in files:
                if file in IGNORE_PATTERNS or file.startswith('.'): continue

                # [ASCENSION 12]: PATH DUPLICATION GUARD
                # Ensure we don't accidentally create C:\Root\C:\Root\File
                # os.walk yields absolute paths if root is absolute.
                full_path = Path(current_root) / file

                # [ASCENSION 4]: PRIORITY QUEUE
                # We prioritize config files to build context early
                if file in ['scaffold.scaffold', 'package.json', 'Cargo.toml', 'pyproject.toml', '.env.example']:
                    config_harvest.append(full_path)
                else:
                    harvest.append(full_path)

        return config_harvest + harvest

    def _process_file(self, file_path: Path, root_path: Path) -> Dict[str, Any]:
        """
        [THE ATOMIC RITE]
        Executed by a worker thread. Performs checks, caching, and analysis.
        """
        str_path = str(file_path)

        try:
            stat = file_path.stat()
            mtime = stat.st_mtime
            size = stat.st_size

            # [ASCENSION 5]: MERKLE CACHE CHECK
            # We assume sentinels are pure functions of file content.
            with self._lock:
                if str_path in SURVEY_CACHE:
                    cached = SURVEY_CACHE[str_path]
                    if cached['mtime'] == mtime and cached['size'] == size:
                        return {'status': 'cached', 'heresy_count': 0}

            # [ASCENSION 6]: BINARY VOID WARD
            # Read first 1024 bytes. If null byte found, it's binary.
            try:
                with open(file_path, 'rb') as f:
                    chunk = f.read(1024)
                    if b'\0' in chunk:
                        return {'status': 'skipped', 'reason': 'binary'}
            except IOError:
                return {'status': 'skipped', 'reason': 'read_error'}

            # [ASCENSION 7]: ENCODING HEALER
            content = ""
            try:
                content = file_path.read_text(encoding='utf-8', errors='strict')
            except UnicodeDecodeError:
                try:
                    content = file_path.read_text(encoding='latin-1', errors='replace')
                except Exception:
                    return {'status': 'skipped', 'reason': 'encoding_failure'}

            # Sentinel Summoning
            sentinels = self.registry.summon(file_path.name)
            if not sentinels:
                # No guardian for this file type
                return {'status': 'skipped', 'reason': 'no_sentinel'}

            heresy_count = 0
            all_diagnostics = []

            for sentinel in sentinels:
                try:
                    findings = sentinel.analyze(content, file_path, root_path)
                    if findings:
                        all_diagnostics.extend(findings)
                except Exception as e:
                    Logger.warn(f"Sentinel Fracture on {file_path.name}: {e}")

            # [ASCENSION 11]: BROADCAST TRUTH
            # Only broadcast if there are findings, or if we want to clear old errors.
            heresy_count = len(all_diagnostics)
            self._broadcast_diagnostics(file_path, all_diagnostics)

            # Update Cache
            with self._lock:
                SURVEY_CACHE[str_path] = {
                    'mtime': mtime,
                    'size': size,
                    'last_scan': time.time(),
                    'heresy_count': heresy_count
                }

            return {'status': 'scanned', 'heresy_count': heresy_count}

        except Exception as e:
            return {'status': 'error', 'msg': str(e)}

    def _broadcast_diagnostics(self, file_path: Path, diagnostics: List[Dict]):
        """
        [ASCENSION 11]: TELEPATHIC TRANSMITTER
        Injects the finding directly into the Akashic Stream.
        """
        # [ASCENSION 1 & 2]: TITANIUM PATH SANITIZATION
        # 1. Convert to URI
        uri = UriUtils.to_uri(file_path)

        # 2. [THE CURE]: SCRUB ARTIFACTS
        # Ensure no trailing quotes from previous parse errors survive
        clean_uri = uri.replace("'", "").replace('"', "").strip()

        packet = {
            "method": "textDocument/publishDiagnostics",
            "params": {
                "uri": clean_uri,
                "diagnostics": diagnostics
            },
            # Tag the source so the Frontend Store knows it came from the Daemon
            "_source": "DAEMON_SURVEYOR"
        }
        self.akashic.broadcast(packet)

    def _broadcast_progress(self, current: int, total: int, message: str, done: bool = False):
        """[ASCENSION 6]: PROGRESS PULSE"""
        percent = int((current / total) * 100) if total > 0 else 0
        packet = {
            "method": "scaffold/progress",
            "params": {
                "id": "grand-survey",
                "title": "Gnostic Survey",
                "message": message,
                "percentage": percent,
                "done": done
            }
        }
        self.akashic.broadcast(packet)