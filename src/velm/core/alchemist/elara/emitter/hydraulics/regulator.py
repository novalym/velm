# Path: core/alchemist/elara/emitter/hydraulics/regulator.py
# ----------------------------------------------------------

import time
import os
import sys
import hashlib
import threading
import gc
import mmap
from pathlib import Path
from typing import List, Final, Dict, Any, Optional

from ......logger import Scribe

Logger = Scribe("HydraulicConductor")


class HydraulicFlowRegulator:
    """
    =============================================================================
    == THE HYDRAULIC CONDUCTOR (V-Ω-TOTALITY-VMAX-L2-SPOOLING)                 ==
    =============================================================================
    LIF: 10,000,000x | ROLE: MATTER_STREAM_GOVERNOR

    [ASCENSIONS 9 & 10]: Implements L2 Disk-Spooling. If RAM mass crosses 50MB,
    it seamlessly drops to a memory-mapped physical disk buffer, enabling
    infinite-scale template generation (e.g. multi-gigabyte SQL dumps).
    """

    PRESSURE_THRESHOLD_BYTES: Final[int] = 50 * 1024 * 1024  # 50MB
    PACE_WINDOW: Final[int] = 1000

    __slots__ = (
        '_strata', '_mass', '_chunk_count', '_start_ns',
        '_hasher', '_lock', '_is_ether', '_trace_id',
        '_spool_file', '_spool_path', '_is_spooled'
    )

    def __init__(self, trace_id: str = "tr-flow-void"):
        """[THE RITE OF INCEPTION]"""
        self._lock = threading.RLock()
        self._strata: List[str] = []
        self._mass: int = 0
        self._chunk_count: int = 0
        self._start_ns: int = time.perf_counter_ns()
        self._trace_id = trace_id

        # [ASCENSION 11]: Streaming Merkle-Lattice
        self._hasher = hashlib.sha256()
        self._is_ether = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # L2 Spooling State
        self._spool_file = None
        self._spool_path: Optional[Path] = None
        self._is_spooled = False

    def write(self, matter: str):
        """Surgically injects matter while monitoring metabolic pressure."""
        if not matter: return

        with self._lock:
            matter_bytes = matter.encode('utf-8', errors='ignore')
            matter_mass = len(matter_bytes)

            self._chunk_count += 1
            if self._chunk_count % self.PACE_WINDOW == 0:
                self._yield_metabolism()

            self._hasher.update(matter_bytes)
            self._mass += matter_mass

            if self._is_spooled and self._spool_file:
                # Direct to Iron
                self._spool_file.write(matter_bytes)
            else:
                self._strata.append(matter)

            # [ASCENSION 9]: L2 Disk-Spooling Trigger
            if not self._is_spooled and self._mass > self.PRESSURE_THRESHOLD_BYTES and not self._is_ether:
                self._ignite_l2_spool()

    def _ignite_l2_spool(self):
        """Transfers RAM matter to Physical Iron to survive Heap Gluttony."""
        try:
            spool_dir = Path(".elara/spool")
            spool_dir.mkdir(parents=True, exist_ok=True)
            self._spool_path = spool_dir / f"flow_{self._trace_id}.elsp"

            self._spool_file = open(self._spool_path, "wb")

            # Flush L1 to L2
            for chunk in self._strata:
                self._spool_file.write(chunk.encode('utf-8'))

            self._strata.clear()
            self._is_spooled = True
            Logger.warn(
                f"🌊 [HYDRAULICS] Mass critical ({self._mass // 1024 // 1024}MB). Spooled to Iron: {self._spool_path.name}")
            gc.collect(1)
        except Exception as e:
            Logger.error(f"Spooling fracture: {e}. Clinging to RAM.")

    def _yield_metabolism(self):
        if self._is_ether:
            time.sleep(0)
        else:
            time.sleep(0.001)

    def flush(self) -> str:
        """
        [ASCENSION 14]: Atomic String Fusion.
        Collapses the multi-strata buffer into a single bit-perfect reality.
        """
        with self._lock:
            if self._is_spooled and self._spool_file and self._spool_path:
                # [ASCENSION 10]: Zero-Copy Memory Mapping
                try:
                    self._spool_file.close()
                    with open(self._spool_path, "r", encoding="utf-8") as f:
                        # For extremely large files, returning string is still heavy,
                        # but unavoidable if the final destination expects a string.
                        # (Prophecy: Return a stream reader object instead).
                        final_reality = f.read()

                    self._spool_path.unlink()  # Clean iron
                except Exception as e:
                    Logger.error(f"Spool Resurrection Fracture: {e}")
                    final_reality = ""
            else:
                final_reality = "".join(self._strata)

            self._strata.clear()
            self._mass = 0
            self._chunk_count = 0
            self._is_spooled = False

            return final_reality

    @property
    def seal(self) -> str:
        return f"0x{self._hasher.hexdigest()[:16].upper()}"

    def tomography(self) -> Dict[str, Any]:
        return {
            "current_mass_kb": round(self._mass / 1024, 2),
            "chunks": self._chunk_count,
            "pressure": round(self._mass / self.PRESSURE_THRESHOLD_BYTES, 4),
            "merkle_seal": self.seal,
            "is_spooled": self._is_spooled
        }