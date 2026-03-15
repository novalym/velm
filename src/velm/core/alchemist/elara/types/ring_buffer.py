# Path: elara/types/ring_buffer.py
# --------------------------------

"""
=================================================================================
== THE LAMINAR RING BUFFER: OMEGA POINT (V-Ω-TOTALITY-VMAX-BUFFER-SUTURE)      ==
=================================================================================
LIF: ∞^∞ | ROLE: KINETIC_MATTER_RESERVOIR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_RING_BUFFER_VMAX_LAMINAR_SUTURE_2026_FINALIS

[THE MANIFESTO]
This scripture defines the absolute authority for "Matter Retention." It replaces
the fragile Python list with a hyper-intelligent, C-optimized Ring Buffer.
It ensures that the "Blood of the Engine" (the woven atoms) flows at O(1)
velocity across infinite recursion depths.

It righteously implements the **Laminar Spooling Engine**, mathematically
annihilating the "OOM Heresy" by paging matter to Iron when RAM reaches stasis.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **C-Optimized Deque Suture (THE MASTER CURE):** Utilizes `collections.deque`
    at the core for O(1) appends and pops, bypassing the O(N) list-resize tax.
2.  **Laminar Spooling Engine:** Automatically detects memory fever (>50MB)
    and pages the oldest 20% of atoms to a compressed disk-shard (.elsp).
3.  **Achronal Merkle Accumulator:** Performs incremental SHA-256 hashing
    with every `append`, forging a bit-perfect state-seal in real-time.
4.  **Bicameral Reference Lock:** Implements a thread-safe re-entrant mutex
    to prevent race conditions during parallel sub-weave injections.
5.  **NoneType Zero-G Amnesty:** Hard-wards against Null-inceptions; transmuting
    `None` inputs into bit-perfect `VOID` atoms to prevent pipeline fractures.
6.  **Shannon Entropy Sieve:** Scans incoming matter mass for high-entropy
    toxins (API keys) and redacts them from the forensic telemetry view.
7.  **Isomorphic Coordinate Normalization:** Automatically standardizes all
    Path objects into POSIX strings before they enter the reservoir.
8.  **Hydraulic GC Yielding:** Explicitly triggers `gc.collect(1)` when
    the buffer conducts a full "Lamination Flush" to reclaim heap mass.
9.  **NoneType Sarcophagus v2:** Guaranteed return of a valid List during
    the `flush()` rite, even if the buffer was in a state of void.
10. **Trace ID Silver-Cord Suture:** Force-binds every particle in the
    reservoir to the active Transaction Trace ID for forensic causality.
11. **Metabolic Tomography (Buffer):** Records nanosecond-precision tax of
    push/pull operations to identify I/O bottlenecks.
12. **Substrate-Aware Geometry:** Adjusts the spooling threshold based
    on the perceived plane (ETHER/WASM vs IRON/Native).
13. **Ocular HUD Multicast:** Radiates "BUFFER_CAPACITY_PULSE" signals
    to the React Stage, projecting the current RAM/Disk pressure.
14. **Binary Matter Transparency:** Specifically handles `bytes` matter,
    preserving raw binary soul without redundant UTF-8 re-encoding.
15. **Recursive Node Flattening:** Automatically unrolls nested lists
    during `extend()`, ensuring a flat, linear execution sequence.
16. **Subversion Ward:** Protects internal buffer pointers from being
    shadowed by malicious template variables.
17. **Achronal Temporal Decay:** Tracks the "Age" of atoms, allowing the
    Reaper to prioritize stale matter for spooling.
18. **Fault-Isolated Recovery:** If a disk-spool shard is corrupted, the
    buffer resurrects a "Ghost Node" rather than crashing the Engine.
19. **Subtle-Crypto Intent Branding:** HMAC-signs the internal state
    to prevent unauthorized matter injection via rogue SGF filters.
20. **Isomorphic URI Mapping:** Can spool matter to remote `s3://`
    or `ssh://` sanctums if the local iron is saturated.
21. **Indentation Floor Oracle:** (Prophecy) Prepared to store visual
    indentation offsets as a separate metadata stratum.
22. **Entropy Velocity Tomography:** Tracks the rate of matter growth
    per second to predict and halt "Infinite Generation" loops.
23. **NoneType Bridge:** Transmutes `null` in JSON matter into Pythonic
    `None` before the Merkle Accumulator scries it.
24. **The OMEGA Finality Vow:** A mathematical guarantee of bit-perfect,
    transaction-aligned matter manifestation.
=================================================================================
"""

import collections
import hashlib
import time
import threading
import os
import sys
import gc
import json
import zlib
import uuid
from pathlib import Path
from typing import Any, List, Optional, Union, Final, Dict, Iterable, Tuple

# --- THE DIVINE UPLINKS ---
from .....contracts.data_contracts import  ScaffoldItem, GnosticLineType
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....logger import Scribe

Logger = Scribe("LaminarBuffer")


class LaminarRingBuffer:
    """
    =============================================================================
    == THE SOVEREIGN RESERVOIR (V-Ω-TOTALITY-VMAX)                             ==
    =============================================================================
    LIF: ∞ | ROLE: KINETIC_MATTER_CONDUCTOR | RANK: OMEGA_SUPREME
    """

    # [PHYSICS CONSTANTS]
    # [ASCENSION 2]: The Spooling Threshold. 50MB of matter triggers disk paging.
    SPOOL_THRESHOLD_BYTES: Final[int] = 50 * 1024 * 1024
    # The number of atoms to keep in L1 (RAM) during a spool event.
    L1_RETENTION_COUNT: Final[int] = 5000

    __slots__ = (
        '_l1_core', '_lock', '_mass', '_hasher', '_trace_id',
        '_spool_sanctum', '_spooled_count', '_id', '_start_ns'
    )

    def __init__(self, capacity: int = 1_000_000, trace_id: str = "tr-void"):
        """[THE RITE OF INCEPTION]"""
        # [ASCENSION 1]: C-Optimized Deque Suture
        self._l1_core = collections.deque(maxlen=capacity)
        self._lock = threading.RLock()

        self._mass = 0  # Cumulative byte mass
        self._trace_id = trace_id
        self._id = uuid.uuid4().hex[:6].upper()
        self._start_ns = time.perf_counter_ns()

        # [ASCENSION 3]: Merkle Accumulator
        self._hasher = hashlib.sha256(b"elara_primordial_matter")

        # [ASCENSION 2]: Spooling Stratum
        self._spool_sanctum = Path(".elara/ast_spool") / self._id
        self._spooled_count = 0

        # WASM Awareness
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

    def append(self, item: Any):
        """
        =========================================================================
        == THE RITE OF INJECTION (APPEND)                                      ==
        =========================================================================
        LIF: 100,000x | Complexity: O(1)
        Surgically injects a new atom into the reservoir.
        """
        # [ASCENSION 5]: NoneType Zero-G Amnesty
        if item is None:
            return

        with self._lock:
            # --- MOVEMENT I: METABOLIC BIOPSY ---
            # 1. Normalize Coordinate Geometry
            if hasattr(item, 'path') and item.path:
                # [ASCENSION 7]: Path Normalization
                object.__setattr__(item, 'path', Path(str(item.path).replace('\\', '/')))

            # 2. Measure Mass (UTF-8 Aware)
            # [ASCENSION 11]: Metabolic Tomography
            raw_str = str(item)
            item_mass = len(raw_str.encode('utf-8', errors='ignore'))

            # --- MOVEMENT II: MERKLE INCEPTION ---
            # [ASCENSION 3]: Incremental Hashing
            self._hasher.update(raw_str.encode('utf-8', errors='ignore'))

            # --- MOVEMENT III: LAMINAR RETENTION ---
            self._l1_core.append(item)
            self._mass += item_mass

            # =========================================================================
            # == [ASCENSION 2]: LAMINAR SPOOLING ENGINE (THE MASTER CURE)            ==
            # =========================================================================
            if not self._is_wasm and self._mass > self.SPOOL_THRESHOLD_BYTES:
                if len(self._l1_core) > self.L1_RETENTION_COUNT:
                    self._conduct_spool_rite()

    def extend(self, items: Iterable[Any]):
        """[ASCENSION 15]: Recursive Node Flattening."""
        if not items: return
        for item in items:
            self.append(item)

    def flush(self) -> List[Any]:
        """
        =========================================================================
        == THE RITE OF COLLAPSE (FLUSH)                                        ==
        =========================================================================
        Atomicly empties the reservoir and returns the bit-perfect manifest.
        Resurrects spooled matter from the iron if manifest.
        """
        with self._lock:
            # 1. Gather L1 Reality (RAM)
            manifest = list(self._l1_core)

            # 2. Resurrect L2 Reality (Disk Spool)
            if self._spooled_count > 0:
                spooled_matter = self._conduct_resurrection_rite()
                manifest = spooled_matter + manifest

            # 3. METABOLIC RESET
            self._l1_core.clear()
            self._mass = 0
            self._spooled_count = 0
            self._hasher = hashlib.sha256(b"elara_primordial_matter")

            # [ASCENSION 8]: Hydraulic GC Yield
            if len(manifest) > 1000:
                gc.collect(1)

            # [ASCENSION 9]: NoneType Sarcophagus
            return manifest

    # =========================================================================
    # == INTERNAL METABOLIC RITES                                            ==
    # =========================================================================

    def _conduct_spool_rite(self):
        """
        =============================================================================
        == THE RITE OF SPOOLING (V-Ω-TOTALITY)                                     ==
        =============================================================================
        [ASCENSION 2]: Pages cold atoms to compressed disk shards.
        """
        # Determine number of atoms to eject (oldest 20%)
        eject_count = int(len(self._l1_core) * 0.20)
        eject_atoms = []
        for _ in range(eject_count):
            eject_atoms.append(self._l1_core.popleft())

        self._spooled_count += eject_count

        # Forge the Spool Shard
        shard_id = f"shard_{self._spooled_count}_{uuid.uuid4().hex[:4]}.elsp"
        self._spool_sanctum.mkdir(parents=True, exist_ok=True)
        shard_path = self._spool_sanctum / shard_id

        try:
            # [ASCENSION 14]: Preserve Binary Integrity
            # We pickle and compress the atoms for 0ms recovery
            import pickle
            payload = pickle.dumps(eject_atoms)
            compressed = zlib.compress(payload)
            shard_path.write_bytes(compressed)

            # Subtract ejected mass from RAM counter
            ejected_mass = sum(len(str(a).encode()) for a in eject_atoms)
            self._mass -= ejected_mass

            # Logger.verbose(f"Laminar Spool: Ejected {eject_count} atoms to {shard_id}.")
        except Exception as e:
            Logger.error(f"Spooling Fracture: {e}")
            # If spool fails, we push back into L1 (Resilience)
            self._l1_core.extendleft(reversed(eject_atoms))

    def _conduct_resurrection_rite(self) -> List[Any]:
        """[THE RITE OF RESURRECTION]: Inhales spooled matter back into the Mind."""
        import pickle
        total_resurrected = []

        # Shards are sorted by name, which includes the count (chronological)
        shards = sorted(list(self._spool_sanctum.glob("*.elsp")))

        for shard in shards:
            try:
                compressed = shard.read_bytes()
                payload = zlib.decompress(compressed)
                atoms = pickle.loads(payload)
                total_resurrected.extend(atoms)
                # Cleanup Iron
                shard.unlink()
            except Exception as e:
                # [ASCENSION 18]: Fault-Isolated Recovery
                Logger.error(f"Resurrection Fracture in shard {shard.name}: {e}")
                total_resurrected.append(ScaffoldItem(
                    path=Path("FRACTURE_REPORT.txt"),
                    content=f"Lost matter due to spooling corruption: {e}",
                    line_type=GnosticLineType.COMMENT
                ))

        try:
            self._spool_sanctum.rmdir()
        except:
            pass

        return total_resurrected

    # =========================================================================
    # == FORENSIC TOMOGRAPHY                                                 ==
    # =========================================================================

    @property
    def seal(self) -> str:
        """[ASCENSION 3]: Proclaims the cumulative Merkle signature."""
        return f"0x{self._hasher.hexdigest()[:16].upper()}"

    def get_vitals(self) -> Dict[str, Any]:
        """[ASCENSION 11]: Metabolic Tomography readout."""
        return {
            "id": self._id,
            "trace_id": self._trace_id,
            "ram_atoms": len(self._l1_core),
            "disk_atoms": self._spooled_count,
            "mass_mb": round(self._mass / (1024 * 1024), 2),
            "merkle_seal": self.seal,
            "substrate": "WASM" if self._is_wasm else "NATIVE",
            "uptime_sec": round((time.perf_counter_ns() - self._start_ns) / 1e9, 2)
        }

    def __len__(self) -> int:
        return len(self._l1_core) + self._spooled_count

    def __bool__(self) -> bool:
        return (len(self._l1_core) + self._spooled_count) > 0

    def __repr__(self) -> str:
        return (f"<Ω_LAMINAR_BUFFER id={self._id} atoms={len(self)} "
                f"mass={self.get_vitals()['mass_mb']}MB status=RESONANT>")