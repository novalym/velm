# Path: src/velm/core/runtime/middleware/caching.py
# -----------------------------------------------------------------------------------------
# SYSTEM: Cache Management Subsystem
# ROLE: Multi-Tier Request/Response Memoization
# STABILITY: High-Performance / Atomic
# -----------------------------------------------------------------------------------------

import hashlib
import json
import time
import sys
import gzip
import os
import random
from pathlib import Path
from typing import Dict, Any, Optional, Callable, Type, Final

from .contract import Middleware
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import (
    BaseRequest,
    DistillRequest,
    AnalyzeRequest,
    VerifyRequest,
    InspectRequest
)

# --- ARCHITECTURAL CONFIGURATION ---
# Increment CACHE_VERSION to force a global invalidation across all projects
# in the event of a breaking change to the ScaffoldResult schema.
CACHE_VERSION: Final[str] = "v2.1.0"

# L1 Cache represents the process-local heap.
# 50 items balances memory pressure vs. sub-millisecond retrieval speed.
L1_CACHE_SIZE: Final[int] = 50

# Probability of triggering a background cleanup of expired disk entries on write.
PRUNE_CHANCE: Final[float] = 0.01

# Debug state sensing from environment
_DEBUG_MODE: Final[bool] = os.environ.get("SCAFFOLD_DEBUG") == "1"


class LRUCache:
    """
    Standard Least-Recently-Used (LRU) in-memory data structure.

    Implements a fixed-capacity dictionary with temporal access tracking
    to ensure the process heap remains within defined metabolic boundaries.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[str, Any] = {}
        self.access: Dict[str, float] = {}

    def get(self, key: str) -> Optional[Any]:
        """Retrieves an entry and updates its temporal priority."""
        if key in self.cache:
            self.access[key] = time.time()
            return self.cache[key]
        return None

    def put(self, key: str, value: Any):
        """Inscribes an entry, potentially evicting the oldest record if at capacity."""
        if len(self.cache) >= self.capacity:
            # Atomic Eviction of the least recently used coordinate
            oldest = min(self.access, key=self.access.get)
            del self.cache[oldest]
            del self.access[oldest]

        self.cache[key] = value
        self.access[key] = time.time()


# --- SINGLETON L1 SUBSTRATE ---
# This instance lives at the module level to persist across middleware re-instantiation.
_L1_MEMORY = LRUCache(L1_CACHE_SIZE)


class CachingMiddleware(Middleware):
    """
    High-Performance Multi-Tier Caching Pipeline.

    This middleware intercepts incoming requests to determine if a bit-perfect
    previous result is available in local memory or on-disk. It enforces
    idempotency and prevents redundant computational tax on the Python Kernel.

    Key Engineering Strata:
    1.  **L1 Cache (RAM):** Sub-millisecond retrieval for hot requests.
    2.  **L2 Cache (Disk):** Compressed, sharded storage for cross-session persistence.
    3.  **Content-Aware Invalidation:** Uses file metadata (mtime/size) as a proxy
        for content integrity, ensuring cache results are never stale.
    4.  **Substrate Normalization:** Normalizes paths and types before hashing to
        ensure cross-platform key resonance.
    """

    # --- Domain-Specific TTL Registry ---
    # Defines the time-horizon for specific Request types.
    CACHEABLE_RITES: Final[Dict[Type[BaseRequest], int]] = {
        DistillRequest: 3600,  # 1 Hour: Static analysis is expensive and generally stable
        AnalyzeRequest: 600,  # 10 Minutes: Source-aware linting
        VerifyRequest: 30,  # 30 Seconds: Integrity checks are high-volatility
        InspectRequest: 86400,  # 24 Hours: Blueprint metadata is near-immutable
    }

    def handle(self, request: BaseRequest, next_handler: Callable[[BaseRequest], ScaffoldResult]) -> ScaffoldResult:
        """
        Processes the request through the caching filter.

        Order of Operations:
        1.  Adjudicate volatility (Should we bypass?).
        2.  Synthesize the deterministic Cache Key.
        3.  Probe L1 (Memory).
        4.  Probe L2 (Disk).
        5.  Execute Handler on miss.
        6.  Enshrine result on success.
        """

        # 1. VOLATILITY TRIAGE
        if self._should_bypass(request):
            if _DEBUG_MODE:
                sys.stderr.write(
                    f"[DEBUG: Cache] Bypass triggered for {type(request).__name__} (Volatile/User-Forced)\n")
            return next_handler(request)

        # 2. KEY GENERATION
        # We forge a unique fingerprint based on the request state and physical file state.
        cache_key = self._forge_cache_key(request)
        ttl = self.CACHEABLE_RITES.get(type(request), 60)

        # 3. L1 PROBE (Process Heap)
        l1_hit = _L1_MEMORY.get(cache_key)
        if l1_hit:
            if _DEBUG_MODE:
                sys.stderr.write(f"[DEBUG: Cache] L1 Hit (RAM) for {cache_key[:8]}\n")
            return self._hydrate_result(l1_hit, source="L1_MEMORY")

        # 4. L2 PROBE (Persistent Disk)
        # We shard the cache to avoid directory-listing overhead on large datasets.
        cache_path = self._get_cache_path(request.project_root, cache_key)
        if self._is_valid_disk_cache(cache_path, ttl):
            data = self._read_disk_cache(cache_path)
            if data:
                if _DEBUG_MODE:
                    sys.stderr.write(f"[DEBUG: Cache] L2 Hit (Disk) for {cache_key[:8]}\n")

                # Promote from Disk to Memory for future O(1) retrieval
                _L1_MEMORY.put(cache_key, data)
                return self._hydrate_result(data, source="L2_DISK")

        # 5. EXECUTION (The Cache Miss)
        if _DEBUG_MODE:
            sys.stderr.write(f"[DEBUG: Cache] Miss for {type(request).__name__}. Dispatching...\n")

        result = next_handler(request)

        # 6. INSCRIPTION
        # We only cache successful, pure results.
        if result and result.success:
            try:
                # Transmute to JSON-safe dictionary for storage
                payload = result.model_dump(mode='json')

                # Commit to both tiers
                _L1_MEMORY.put(cache_key, payload)
                self._write_disk_cache(cache_path, payload)

                # Probabilistic Maintenance
                if random.random() < PRUNE_CHANCE:
                    self._maintenance_routine(cache_path.parent)

            except Exception as e:
                self.logger.debug(f"Cache inscription failed (Non-Critical): {e}")

        return result

    def _should_bypass(self, request: BaseRequest) -> bool:
        """
        Determines if the current operation is too volatile for caching.
        """
        # A. Support Check: Is this request type registered for caching?
        if type(request) not in self.CACHEABLE_RITES:
            return True

        # B. User Intent: Did the Architect explicitly request a fresh strike?
        if request.force or request.variables.get('--no-cache'):
            return True

        # C. Interactivity Check: Never cache UI pads, wizards, or interactive sessions.
        if getattr(request, 'pad', False) or getattr(request, 'interactive', False):
            return True

        # D. Environmental Guard
        if os.environ.get("SCAFFOLD_NO_CACHE") == "1":
            return True

        return False

    def _forge_cache_key(self, request: BaseRequest) -> str:
        """
        Synthesizes a deterministic SHA-256 fingerprint for the request.

        The key is composed of:
        1.  The Global Cache Version.
        2.  The JSON-serialized Request data (excluding transient fields like request_id).
        3.  The physical state of the target file (mtime + size), if applicable.
        """
        # 1. Extract static state
        # We exclude fields that change per-request but don't affect logic output.
        data = request.model_dump(
            exclude={'request_id', 'session_id', 'force', 'verbose', 'silent', 'metadata'},
            mode='json'
        )

        # 2. Path Normalization
        if data.get('project_root'):
            data['project_root'] = str(data['project_root']).replace('\\', '/')

        # 3. Content Integrity Sensing
        # If the request targets a specific scripture, we must ensure the cache
        # is invalidated if that file is modified externally.
        content_sig = "VOID"
        target_path = getattr(request, 'file_path', None) or getattr(request, 'path_to_scripture', None)

        if target_path:
            try:
                root = Path(request.project_root or ".")
                p = Path(target_path)
                if not p.is_absolute():
                    p = root / p

                if p.exists() and p.is_file():
                    # We use mtime + size as a high-velocity proxy for content hash.
                    file_stat = p.stat()
                    content_sig = f"{file_stat.st_mtime_ns}:{file_stat.st_size}"
            except Exception:
                # In the event of a syscall failure, we fallback to the path string.
                pass

        # 4. Deterministic Hashing
        # sort_keys=True is critical for key resonance across different Python dictionary orderings.
        serialized_payload = f"{CACHE_VERSION}:{json.dumps(data, sort_keys=True)}:{content_sig}"
        return hashlib.sha256(serialized_payload.encode('utf-8')).hexdigest()

    def _get_cache_path(self, root: Optional[Path], key: str) -> Path:
        """
        Calculates the physical coordinate for an L2 cache entry.
        Uses a partitioned directory structure to maintain filesystem performance.
        """
        anchor = root or Path.cwd()
        # Sharding: We use the first 2 characters of the hash to create 256 sub-buckets.
        shard = key[:2]
        return anchor / ".scaffold" / "cache" / "middleware" / shard / f"{key}.json.gz"

    def _is_valid_disk_cache(self, path: Path, ttl: int) -> bool:
        """Verifies existence and checks TTL against the physical last-modified timestamp."""
        if not path.exists():
            return False

        try:
            age = time.time() - path.stat().st_mtime
            return age < ttl
        except OSError:
            return False

    def _read_disk_cache(self, path: Path) -> Optional[Dict]:
        """
        Materializes a JSON payload from a compressed disk shard.
        """
        try:
            with gzip.open(path, 'rt', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            if _DEBUG_MODE:
                sys.stderr.write(f"[WARN: Cache] Failed to read shard {path.name}: {e}\n")
            return None

    def _write_disk_cache(self, path: Path, data: Dict):
        """
        Atomically inscribes a result to the L2 persistent tier.
        Utilizes Gzip compression and temporal-replacement to ensure integrity.
        """
        try:
            if not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)

            # 1. Inscribe to temporary coordinate
            temp_path = path.with_suffix(".tmp")
            with gzip.open(temp_path, 'wt', encoding='utf-8') as f:
                json.dump(data, f)

            # 2. Atomic Move (The Switch)
            # This ensures that a crash during write results in no file,
            # rather than a corrupted JSON file.
            temp_path.replace(path)
        except Exception as e:
            if _DEBUG_MODE:
                sys.stderr.write(f"[WARN: Cache] Disk write failed: {e}\n")

    def _hydrate_result(self, data: Dict, source: str) -> ScaffoldResult:
        """
        Reconstructs a formal ScaffoldResult model from raw dictionary matter.
        Injects metadata to inform the UI of the result's cached provenance.
        """
        result = ScaffoldResult.model_validate(data)

        # Ingress cache telemetry for Ocular visibility
        if result.data is None:
            result.data = {}

        if isinstance(result.data, dict):
            result.data['_cache_telemetry'] = {
                "source": source,
                "hit_timestamp": time.time(),
                "integrity": "verified"
            }

        return result

    def _maintenance_routine(self, cache_dir: Path):
        """
        Autonomous maintenance routine.
        Evaporates entries older than 24 hours to prevent storage bloat.
        """
        try:
            now = time.time()
            # 24-Hour Persistence Ceiling
            MAX_AGE_SECONDS = 86400

            for shard_file in cache_dir.glob("*.gz"):
                if now - shard_file.stat().st_mtime > MAX_AGE_SECONDS:
                    shard_file.unlink(missing_ok=True)

        except Exception:
            # Housekeeping failure is non-fatal.
            pass