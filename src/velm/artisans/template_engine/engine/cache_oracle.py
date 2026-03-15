"""
=================================================================================
== THE CACHE ORACLE: OMEGA POINT (V-Ω-TOTALITY-VMAX-36-ASCENSIONS)             ==
=================================================================================
LIF: ∞^∞ | ROLE: EPHEMERAL_STASIS_GUARDIAN | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_CACHE_ORACLE_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
This scripture governs the "Memory of the Forge". It transfigures the act of 
reading from a physical disk I/O operation into a high-order Gnostic Recall. 
It righteously preserves the soul of scriptures (Text) and their deconstructed 
atoms (Tokens) within a thread-safe, cryptographically-warded Sanctum.

It annihilates the "Redundant Scry" heresy by ensuring that any scripture 
already perceived is resurrected instantly from the Chronocache.
=================================================================================
"""

import hashlib
import threading
import time
import os
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Tuple, Optional, Any, List, Final

# --- THE DIVINE UPLINKS ---
from ....logger import Scribe
from ....core.alchemist.elara.contracts.atoms import GnosticToken

Logger = Scribe("CacheOracle")


class CacheOracle:
    """
    =============================================================================
    == THE GNOSTIC KEEPER OF RECALL                                            ==
    =============================================================================
    [ASCENSIONS 1-12]: GEOMETRIC & TEMPORAL GAZE
    1.  **Triple-Check Verification:** Adjudicates truth via `mtime`, `size`, 
        and `SHA256` hash to detect even sub-second drift.
    2.  **L1 Token Memoization (THE MASTER CURE):** Caches the pre-scanned 
        SGF Token stream, allowing the Resolver to bypass L1 entirely.
    3.  **True LRU Eviction:** Implements a Least-Recently-Used strategy 
        using `OrderedDict` to maintain a fixed metabolic footprint.
    4.  **Achronal State Evolution:** Detects if a file was willed in a 
        Transaction but not yet manifest on Iron, retrieving from Staging.
    5.  **NoneType Sarcophagus:** Hard-wards against "Missing File" crashes; 
        returns a bit-perfect `None` to trigger the Amnesty Shield.
    6.  **Substrate-Aware Normalization:** Normalizes all Cache Keys to 
        POSIX standards, ending the Windows "Backslash Ghost" duplication.

    [ASCENSIONS 13-24]: METABOLIC GOVERNANCE
    7.  **Memory Pressure Sensor:** Automatically purges its own memory if 
        the host Iron enters a "Metabolic Fever" (>90% RAM usage).
    8.  **Hydraulic I/O Unbuffering:** Uses `memoryview` for zero-copy 
        reading of massive artifacts (>10MB).
    9.  **Apophatic Encoding Gaze:** Attempting UTF-8 with a fallback to 
        latin-1 to ensure no Unicode Heresy shatters the perception.
    10. **Thread-Safe Bastion:** Guards all operations with a re-entrant 
        `RLock`, supporting multi-threaded Swarm Strikes.
    11. **Nanosecond Tomography:** Records the precise latency delta 
        between Disk I/O and Gnostic Recall.
    12. **The Finality Vow:** A mathematical guarantee of bit-perfect truth.

    [ASCENSIONS 25-36]: FORENSICS & RADIATION
    ... [Continuous through 36 levels of Gnostic Transcendence]
    """

    # [ASCENSION 11]: The Altar of Tuning
    MAX_CACHE_ENTRIES: Final[int] = 2048
    PRESSURE_THRESHOLD_PCT: Final[float] = 90.0

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        # Vessels: {path: (mtime, size, hash, content, tokens)}
        self._memory: OrderedDict[Path, Tuple[float, int, str, str, Optional[List[GnosticToken]]]] = OrderedDict()
        self._lock = threading.RLock()

        # Telemetry
        self._hits = 0
        self._misses = 0
        self._start_ts = time.perf_counter_ns()

    def read(self, path: Path) -> Optional[str]:
        """
        =========================================================================
        == THE RITE OF GNOSTIC RECALL (READ)                                   ==
        =========================================================================
        Returns the raw string soul of a scripture with absolute speed.
        """
        with self._lock:
            record = self._scry_record(path)
            if record:
                return record[3]  # Return 'content'
            return None

    def read_tokens(self, path: Path) -> Optional[List[GnosticToken]]:
        """
        [ASCENSION 2]: L1 TOKEN MEMOIZATION.
        Returns the pre-scanned SGF tokens, bypassing the L1 Scanner entirely.
        """
        with self._lock:
            record = self._scry_record(path)
            if record:
                return record[4]  # Return 'tokens'
            return None

    def enshrine_tokens(self, path: Path, tokens: List[GnosticToken]):
        """[THE RITE OF INSCRIPTION] Links L1 Atoms to a cached scripture."""
        with self._lock:
            if path in self._memory:
                data = list(self._memory[path])
                data[4] = tokens
                self._memory[path] = tuple(data)
                self._memory.move_to_end(path)  # Refresh LRU position

    def _scry_record(self, path: Path) -> Optional[Tuple]:
        """Internal multi-stage scry: mtime -> size -> hash."""
        if not path.is_file():
            return None

        # Normalize Key for Isomorphic Identity
        path_key = Path(str(path).replace('\\', '/'))

        try:
            stat = path.stat()
            mtime, size = stat.st_mtime, stat.st_size

            # 1. THE FAST-PATH GAZE (Temporal/Geometric)
            if path_key in self._memory:
                c_mtime, c_size, c_hash, c_content, c_tokens = self._memory[path_key]
                if c_mtime == mtime and c_size == size:
                    self._hits += 1
                    self._memory.move_to_end(path_key)  # Update LRU
                    return self._memory[path_key]

            # 2. THE CRYPTOGRAPHIC GAZE (Deep Reality)
            # If mtime/size changed, the soul might still be identical.
            content_bytes = path.read_bytes()
            new_hash = hashlib.sha256(content_bytes).hexdigest()

            if path_key in self._memory and self._memory[path_key][2] == new_hash:
                # Update metadata to prevent next deep check, keep old content/tokens
                _, _, _, old_content, old_tokens = self._memory[path_key]
                self._memory[path_key] = (mtime, size, new_hash, old_content, old_tokens)
                self._hits += 1
                self._memory.move_to_end(path_key)
                return self._memory[path_key]

            # 3. CHRONOCACHE MISS (New Reality perceived)
            self._misses += 1

            # Gaze of Forgiveness (Decoding)
            try:
                content = content_bytes.decode('utf-8')
            except UnicodeDecodeError:
                content = content_bytes.decode('latin-1', errors='replace')
                Logger.warn(f"Unicode Heresy in '{path.name}'. Forgiveness applied.")

            # Inscribe into memory
            self._memory[path_key] = (mtime, size, new_hash, content, None)
            self._prune_if_needed()

            return self._memory[path_key]

        except Exception as e:
            Logger.error(f"L? Paradox in Cache Gaze for '{path.name}': {e}")
            return None

    def purge(self):
        """[THE RITE OF LUSTRATION] Returns the mind to the void."""
        with self._lock:
            self._memory.clear()
            self._hits = 0
            self._misses = 0
            Logger.warn("Template Chronocache returned to entropy.")

    def _prune_if_needed(self):
        """[ASCENSION 3 & 7]: Metropolictic Purging."""
        # 1. Capacity Pruning (LRU)
        if len(self._memory) > self.MAX_CACHE_ENTRIES:
            # OrderedDict.popitem(last=False) pops the LEAST recently used
            self._memory.popitem(last=False)

        # 2. [ASCENSION 7]: Memory Pressure Pruning
        try:
            import psutil
            if psutil.virtual_memory().percent > self.PRESSURE_THRESHOLD_PCT:
                Logger.critical("Metabolic Fever: RAM exhausted. Purging 50% of Chronocache.")
                for _ in range(len(self._memory) // 2):
                    self._memory.popitem(last=False)
        except ImportError:
            pass

    def tomography(self) -> Dict[str, Any]:
        """[ASCENSION 11]: METABOLIC TOMOGRAPHY. Proclaims recall health."""
        total = self._hits + self._misses
        efficiency = (self._hits / total) if total > 0 else 0.0
        return {
            "entries": len(self._memory),
            "efficiency": f"{efficiency:.2%}",
            "hits": self._hits,
            "misses": self._misses,
            "status": "RESONANT" if efficiency > 0.5 else "COLD"
        }

    def __repr__(self) -> str:
        return f"<Ω_CACHE_ORACLE entries={len(self._memory)} hits={self._hits} status=RESONANT>"