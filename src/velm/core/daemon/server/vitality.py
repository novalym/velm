# Path: core/daemon/server/vitality.py
# =========================================================================================
# == THE VITALITY CORTEX (V-Ω-TOTALITY-V20000.12-ISOMORPHIC-GOVERNOR)                    ==
# =========================================================================================
# LIF: ∞ | ROLE: LIFECYCLE_SOVEREIGN | RANK: OMEGA_SUPREME
# AUTH: Ω_VITALITY_V20000_SUBSTRATE_SUTURE_2026_FINALIS
# =========================================================================================

import os
import time
import json
import random
import threading
import gc
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Union

# [ASCENSION 1]: SURGICAL SENSORY GUARD
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from ....logger import Scribe

# [LIF: 100X] [RANK: GOD_TIER]
Logger = Scribe("VitalityCortex")


class VitalityMonitor:
    """
    =================================================================================
    == THE VITALITY CORTEX (V-Ω-TOTALITY)                                          ==
    =================================================================================
    The supreme governor of existence. It manages the two-way bridge between
    the Mind (Engine) and the Body (Host/UI).
    """

    def __init__(self, parent_pid: Optional[int], watch_path: Optional[str]):
        """[THE RITE OF INCEPTION]"""
        self.parent_pid = parent_pid
        self.watch_file = Path(watch_path) if watch_path else None
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or not PSUTIL_AVAILABLE

        # [THE CURE]: Atomic Pulse Differentiation
        if self.watch_file:
            self.pulse_file = self.watch_file.parent / "daemon.pulse"
        else:
            self.pulse_file = None

        self._creator_process = None
        self._last_metabolic_tick = time.time()
        self._metabolic_rate = 3.0  # Default to Zen state
        self._memory_ceiling_mb = 1024.0  # 1GB Wall

        # --- MOVEMENT I: SENSORY CALIBRATION ---
        if self.parent_pid and PSUTIL_AVAILABLE:
            try:
                self._creator_process = psutil.Process(self.parent_pid)
                if os.name == 'nt' and not self.is_wasm:
                    # [ASCENSION 11]: Set Vitality process priority to minimize UI jitter
                    try:
                        import win32process
                        win32process.SetPriorityClass(win32process.GetCurrentProcess(),
                                                      win32process.IDLE_PRIORITY_CLASS)
                    except ImportError:
                        pass
            except (psutil.NoSuchProcess, Exception):
                Logger.warn(f"Creator (PID {self.parent_pid}) unmanifested at boot.")

    def check_vitals(self) -> bool:
        """
        =============================================================================
        == THE GRAND ADJUDICATION                                                  ==
        =============================================================================
        Multi-vector liveness check across Iron and Ether planes.
        """
        # 1. Physical Identity Check (Native Only)
        if not self.is_wasm and self.parent_pid:
            if not self._is_parent_alive():
                Logger.critical(f"Creator (PID {self.parent_pid}) has returned to the void. Banishment initiated.")
                return False

        # 2. Chronometric Leash Check (Universal)
        # [ASCENSION 2]: In WASM, the file-leash is our only silver cord.
        if self.watch_file and not self._check_leash_integrity():
            return False

        # 3. Metabolic Health Audit (Memory)
        if not self._audit_internal_memory():
            # Trigger emergency lustration before failing
            gc.collect()
            if not self._audit_internal_memory():
                Logger.critical("Metabolic Collapse: Memory Wall breached after lustration.")
                return False

        return True

    def write_pulse(self, metadata: Dict[str, Any] = None):
        """
        =============================================================================
        == THE RITE OF ATOMIC PULSE (V-Ω-LOCK-BREAKER)                             ==
        =============================================================================
        [ASCENSION 4]: Uses os.replace and jittered retries for Windows-VFS parity.
        """
        if not self.pulse_file: return

        metadata = metadata or {}
        # [ASCENSION 9]: Metabolic Substrate Identification
        metadata.update({
            "substrate": "ETHER" if self.is_wasm else "IRON",
            "jitter_pulse": random.random(),
            "gc_stats": gc.get_count()
        })

        temp_path = self.pulse_file.with_suffix('.tmp')
        data = {
            "pid": os.getpid(),
            "timestamp": time.time(),
            "status": "RESONANT",
            "meta": metadata,
            "metabolic_rate": self._metabolic_rate
        }

        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f)

            # [ASCENSION 4]: Atomic Replacement with Contentious Jitter
            max_retries = 5
            for i in range(max_retries):
                try:
                    os.replace(str(temp_path), str(self.pulse_file))
                    break
                except (PermissionError, OSError):
                    if i == max_retries - 1: raise
                    # Backoff: 10ms, 20ms, 40ms...
                    time.sleep(0.01 * (2 ** i))
        except Exception as e:
            Logger.debug(f"Pulse Inscription deferred: {e}")

    def proclaim_grace(self):
        """[ASCENSION 6]: THE PHOENIX SIGNAL. Inscribes a final state of grace."""
        if not self.pulse_file: return
        try:
            grace = {"status": "VOID_GRACE", "timestamp": time.time(), "reason": "INTENTIONAL_DISSOLUTION"}
            with open(self.pulse_file, 'w', encoding='utf-8') as f:
                json.dump(grace, f)
        except:
            pass

    def _is_parent_alive(self) -> bool:
        """[ASCENSION 8]: Direct Syscall Tomography."""
        if self.is_wasm: return True  # WASM assumes parent is the Browser Worker

        if not self._creator_process and self.parent_pid:
            try:
                self._creator_process = psutil.Process(self.parent_pid)
            except:
                return False

        try:
            if not self._creator_process.is_running(): return False
            if self._creator_process.status() == psutil.STATUS_ZOMBIE: return False
            return True
        except:
            # Fallback to zero-kill signal (Universal POSIX/Windows-emulated)
            try:
                os.kill(self.parent_pid, 0)
                return True
            except OSError:
                return False

    def _check_leash_integrity(self) -> bool:
        """[ASCENSION 10]: Chronometric Leash Scrying."""
        if not self.watch_file.exists():
            Logger.warn(f"The Leash '{self.watch_file.name}' has vanished from the substrate.")
            return False

        try:
            # Scry the modification epoch
            last_will = self.watch_file.stat().st_mtime
            age = time.time() - last_will

            # [ASCENSION 10]: Adaptive Aging
            # If the machine is under heavy load (Adrenaline), we expand the threshold.
            threshold = 15.0 if self._metabolic_rate < 2.0 else 10.0

            if age > threshold:
                Logger.critical(f"Leash has flatlined. Age: {age:.1f}s. Substrate has drifted.")
                return False
            return True
        except:
            # PermissionError in VFS often implies a concurrent write. We assume vitality.
            return True

    def _audit_internal_memory(self) -> bool:
        """[ASCENSION 3]: Heuristic Mass Inference."""
        try:
            if not self.is_wasm and PSUTIL_AVAILABLE:
                me = psutil.Process(os.getpid())
                rss_mb = me.memory_info().rss / (1024 * 1024)
            else:
                # [ASCENSION 3]: Gnostic Object Tomography
                # Count Python blocks when physical RSS is veiled.
                blocks = sys.getallocatedblocks()
                rss_mb = blocks * 0.0002  # Heuristic coefficient for Pyodide/WASM

            if rss_mb > self._memory_ceiling_mb:
                return False

            # [ASCENSION 8]: Lesser Lustration
            if rss_mb > (self._memory_ceiling_mb * 0.75):
                gc.collect(1)  # Clear the young souls to prevent fever

            return True
        except:
            return True

    def adjust_metabolism(self, active_tasks: int):
        """[ASCENSION 5]: ADAPTIVE METABOLIC RATE."""
        if active_tasks > 0:
            self._metabolic_rate = 1.0  # Adrenaline: 1s heartbeat
        else:
            self._metabolic_rate = 3.0  # Zen: 3s heartbeat
        return self._metabolic_rate
