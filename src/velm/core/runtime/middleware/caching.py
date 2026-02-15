# Path: core/runtime/middleware/caching.py
# ----------------------------------------
# LIF: 100x | AUTH_CODE: Ω_CHRONOCACHE_V12
# =================================================================================

import hashlib
import json
import time
import sys
import gzip
import os
import random
from pathlib import Path
from typing import Dict, Any, Optional, Callable

from .contract import Middleware
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import BaseRequest, DistillRequest, AnalyzeRequest, VerifyRequest, InspectRequest, ProjectRequest

# --- CONFIGURATION ---
CACHE_VERSION = "v2"  # Bump to invalidate old caches
L1_CACHE_SIZE = 50  # Max items in RAM
PRUNE_CHANCE = 0.01  # 1% chance to run cleanup on write


class LRUCache:
    """A humble in-memory store."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[str, Any] = {}
        self.access: Dict[str, float] = {}

    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            self.access[key] = time.time()
            return self.cache[key]
        return None

    def put(self, key: str, value: Any):
        if len(self.cache) >= self.capacity:
            # Evict oldest
            oldest = min(self.access, key=self.access.get)
            del self.cache[oldest]
            del self.access[oldest]
        self.cache[key] = value
        self.access[key] = time.time()


# Singleton L1 Cache (Module Level)
_L1_MEMORY = LRUCache(L1_CACHE_SIZE)


class CachingMiddleware(Middleware):
    """
    =============================================================================
    == THE KEEPER OF ECHOES (V-Ω-ZERO-LATENCY-COMPRESSED)                      ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: TEMPORAL_GOVERNOR

    Intercepts pure, idempotent requests and returns cached Gnosis.
    Features L1/L2 caching, compression, and robust invalidation.
    """

    # The Grimoire of Cacheable Rites & TTLs (Seconds)
    CACHEABLE_RITES = {
        DistillRequest: 3600,  # 1 Hour
        AnalyzeRequest: 600,  # 10 Minutes
        VerifyRequest: 30,  # 30 Seconds
        InspectRequest: 86400,  # 24 Hours
    }

    def handle(self, request: BaseRequest, next_handler: Callable[[BaseRequest], ScaffoldResult]) -> ScaffoldResult:
        # [ASCENSION 11]: DIAGNOSTIC ECHO
        sys.stderr.write(f"[PIPE] Entering Chronocache for {type(request).__name__}\n")

        # 1. THE TRIAGE OF PURITY (BYPASS CHECK)
        if self._should_bypass(request):
            self.logger.verbose(
                f"Interactive/Volatile rite detected ({type(request).__name__}). Bypassing Chronocache.")
            sys.stderr.write("[PIPE] -> Caching Bypassed (Volatile). Executing.\n")

            # [ASCENSION 12]: THE VOID WARD
            result = next_handler(request)
            if result is None:
                sys.stderr.write("[PIPE] !!! CRITICAL: Next Handler returned NONE in Caching Bypass.\n")
            return result

        try:
            # 2. THE KEY GENERATION
            cache_key = self._forge_cache_key(request)
            ttl = self.CACHEABLE_RITES.get(type(request), 60)

            # 3. L1 CACHE PROBE (RAM)
            l1_hit = _L1_MEMORY.get(cache_key)
            if l1_hit:
                sys.stderr.write("[PIPE] -> L1 Cache Hit (RAM). Returning.\n")
                return self._hydrate_result(l1_hit, source="L1_RAM")

            # 4. L2 CACHE PROBE (DISK)
            cache_path = self._get_cache_path(request.project_root, cache_key)
            if self._is_valid_disk_cache(cache_path, ttl):
                data = self._read_disk_cache(cache_path)
                if data:
                    sys.stderr.write("[PIPE] -> L2 Cache Hit (Disk). Returning.\n")
                    # Promote to L1
                    _L1_MEMORY.put(cache_key, data)
                    return self._hydrate_result(data, source="L2_DISK")

            # 5. EXECUTION (MISS)
            sys.stderr.write("[PIPE] -> Cache Miss. Executing.\n")
            result = next_handler(request)

            # 6. INSCRIPTION
            if result and result.success:
                # [ASCENSION 8]: FALLBACK CIRCUIT
                try:
                    payload = result.model_dump(mode='json')
                    _L1_MEMORY.put(cache_key, payload)
                    self._write_disk_cache(cache_path, payload)

                    # [ASCENSION 6]: THE PRUNING SCYTHE
                    if random.random() < PRUNE_CHANCE:
                        self._prune_graveyard(cache_path.parent)

                except Exception as e:
                    self.logger.warn(f"Cache Inscription Failed (Non-Critical): {e}")

            return result

        except Exception as e:
            # [ASCENSION 8]: FALLBACK CIRCUIT
            # If caching logic crashes, fail open and execute the rite
            sys.stderr.write(f"[PIPE] !! Caching System Fracture: {e}. Bypassing.\n")
            return next_handler(request)

    def _should_bypass(self, request: BaseRequest) -> bool:
        """Determines if the rite is too volatile for the timeline."""
        # Type Check
        if type(request) not in self.CACHEABLE_RITES:
            return True

        # Forced Refresh
        if request.force or request.variables.get('--no-cache'):
            return True

        # [ASCENSION 3]: INTERACTIVITY CHECK
        # TUI pads, Wizard modes, and REPLs must never be cached.
        if getattr(request, 'pad', False) or getattr(request, 'interactive', False):
            return True

        # CLI overrides
        if os.environ.get("SCAFFOLD_NO_CACHE") == "1":
            return True

        return False

    def _forge_cache_key(self, request: BaseRequest) -> str:
        """
        [ASCENSION 5]: THE MERKLE FINGERPRINT
        Forges a unique hash based on Request, Content, and Environment.
        """
        # 1. Serialize Request
        data = request.model_dump(
            exclude={'request_id', 'session_id', 'force', 'verbose', 'silent'},
            mode='json'
        )

        # 2. [ASCENSION 10]: STRICT TYPE HEALING
        # Ensure paths are strings
        if 'project_root' in data and data['project_root']:
            data['project_root'] = str(data['project_root'])

        # 3. [ASCENSION 5]: CONTENT HASHING (If file target exists)
        # If the request targets a specific file, hash its mtime/size/content
        # to ensure we don't return stale analysis of a changed file.
        content_sig = "VOID"
        target_path = getattr(request, 'file_path', None) or getattr(request, 'path_to_scripture', None)

        if target_path:
            try:
                # Resolve relative to root if needed
                root = Path(request.project_root or ".")
                p = Path(target_path)
                if not p.is_absolute():
                    p = root / p

                if p.exists() and p.is_file():
                    stat = p.stat()
                    # We use mtime + size as a fast proxy for content hash
                    content_sig = f"{stat.st_mtime_ns}:{stat.st_size}"
            except Exception:
                pass  # Fail safe to string path

        # 4. Canonicalize
        payload = f"{CACHE_VERSION}:{json.dumps(data, sort_keys=True)}:{content_sig}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def _get_cache_path(self, root: Optional[Path], key: str) -> Path:
        # [ASCENSION 7]: CONTEXTUAL ISOLATION
        # Cache is stored per-project to avoid collisions
        anchor = root or Path.cwd()
        cache_dir = anchor / ".scaffold" / "cache" / "middleware" / key[:2]  # Sharding
        return cache_dir / f"{key}.json.gz"

    def _is_valid_disk_cache(self, path: Path, ttl: int) -> bool:
        if not path.exists(): return False
        age = time.time() - path.stat().st_mtime
        return age < ttl

    def _read_disk_cache(self, path: Path) -> Optional[Dict]:
        """[ASCENSION 2]: DECOMPRESSION RITE"""
        try:
            with gzip.open(path, 'rt', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    def _write_disk_cache(self, path: Path, data: Dict):
        """[ASCENSION 4 & 2]: ATOMIC COMPRESSED INSCRIPTION"""
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = path.with_suffix(".tmp")
        with gzip.open(temp_path, 'wt', encoding='utf-8') as f:
            json.dump(data, f)

        temp_path.replace(path)

    def _hydrate_result(self, data: Dict, source: str) -> ScaffoldResult:
        """[ASCENSION 9]: TRACE INJECTION"""
        res = ScaffoldResult.model_validate(data)
        # Inject metadata to let the UI know this is a Time Echo
        if not res.data: res.data = {}
        if isinstance(res.data, dict):
            res.data['_cache_meta'] = {
                "source": source,
                "timestamp": time.time(),
                "age": "timeless"
            }
        return res

    def _prune_graveyard(self, cache_dir: Path):
        """[ASCENSION 6]: THE PRUNING SCYTHE"""
        try:
            now = time.time()
            # Delete files older than 24 hours
            MAX_AGE = 86400
            for f in cache_dir.glob("*.gz"):
                if now - f.stat().st_mtime > MAX_AGE:
                    f.unlink()
        except Exception:
            pass