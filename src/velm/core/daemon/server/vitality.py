# Path: core/daemon/server/vitality.py
# ------------------------------------

import os
import time
import json
import random
import psutil
import threading
from pathlib import Path
from typing import Optional, Dict, Any, Union

from ....logger import Scribe

# [LIF: 100X] [RANK: GOD_TIER]
Logger = Scribe("VitalityCortex")


class VitalityMonitor:
    """
    =================================================================================
    == THE VITALITY CORTEX (V-Ω-TOTALITY-METABOLIC-V3)                             ==
    =================================================================================
    LIF: ∞ | auth_code: Ω_HEARTBEAT_BIFURCATED_FINAL

    The supreme lifecycle governor. It manages the dual-channel pulse system:
    1. THE LEASH (Inbound): Watched for Parent (Electron) signals.
    2. THE PULSE (Outbound): Written to signal Daemon health to the Cockpit.
    =================================================================================
    """

    def __init__(self, parent_pid: Optional[int], watch_path: Optional[str]):
        """
        [ASCENSION 1]: Biphasic Initialization.
        """
        self.parent_pid = parent_pid
        # The file Electron writes to keep us alive
        self.watch_file = Path(watch_path) if watch_path else None

        # [THE CURE]: The file WE write to tell Electron we are alive.
        # This prevents WinError 5 Access Denied by separating Write/Read handles.
        if self.watch_file:
            self.pulse_file = self.watch_file.parent / "daemon.pulse"
            self.grace_file = self.watch_file.parent / "daemon.grace"
        else:
            self.pulse_file = None
            self.grace_file = None

        self._creator_process = None
        self._last_metabolic_tick = time.time()
        self._metabolic_rate = 2.0  # Default 2s

        # [ASCENSION 5]: Memory Limit (1GB Default)
        self._memory_ceiling_mb = 1024.0

        if self.parent_pid:
            try:
                self._creator_process = psutil.Process(self.parent_pid)
                # [ASCENSION 11]: Lower I/O priority for the monitor
                if os.name == 'nt':
                    self._creator_process.ionice(psutil.IOPRIO_VERYLOW)
            except (psutil.NoSuchProcess, Exception):
                Logger.warn(f"Creator (PID {self.parent_pid}) was dead on arrival.")

    def check_vitals(self) -> bool:
        """
        [THE GRAND ADJUDICATION]
        Performs a multi-vector liveness check.
        """
        # 1. Physical PID Check
        if self.parent_pid and not self._is_parent_alive():
            Logger.critical(f"Creator (PID {self.parent_pid}) has dissolved. Aborting.")
            return False

        # 2. File-Based Leash Check
        if self.watch_file and not self._check_leash_integrity():
            return False

        # 3. [ASCENSION 5]: Internal Health Audit (Memory)
        if not self._audit_internal_memory():
            return False

        return True

    def write_pulse(self, metadata: Dict[str, Any] = None):
        """
        [ASCENSION 2 & 14]: ATOMIC LOCK-BREAKER
        Inscribes our presence to the pulse file with Windows Contention Guard.
        """
        if not self.pulse_file:
            return

        # [ASCENSION 9]: Entropy Pulse (±5% jitter)
        jitter = (random.random() - 0.5) * 0.1
        metadata = metadata or {}
        metadata["jitter_delta"] = jitter

        temp_path = self.pulse_file.with_suffix('.tmp')

        # [ASCENSION 7]: High-Density Payload
        data = {
            "pid": os.getpid(),
            "timestamp": time.time(),
            "status": "ALIVE",
            "meta": metadata,
            "metabolic_rate": self._metabolic_rate
        }

        try:
            # Atomic Inscription
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f)

            # [ASCENSION 2]: Exponential Jitter Backoff for Windows Handle Locks
            max_retries = 5
            for i in range(max_retries):
                try:
                    # [THE FIX]: os.replace is atomic on both Win/Nix
                    os.replace(temp_path, self.pulse_file)
                    break
                except PermissionError:
                    if i == max_retries - 1:
                        raise
                    # Backoff logic: 50ms, 100ms, 150ms...
                    time.sleep(0.05 * (i + 1))
        except Exception as e:
            Logger.error(f"Vitality Inscription Fracture: {e}")

    def proclaim_grace(self):
        """
        [ASCENSION 6]: THE PHOENIX SIGNAL
        Writes a final grace-note so the UI knows the shutdown was intentional.
        """
        if not self.pulse_file:
            return
        try:
            grace_data = {"status": "VOID_GRACE", "timestamp": time.time()}
            with open(self.pulse_file, 'w', encoding='utf-8') as f:
                json.dump(grace_data, f)
        except:
            pass

    def _is_parent_alive(self) -> bool:
        """[ASCENSION 8]: Direct Syscall Fallback."""
        if not self._creator_process:
            return False
        try:
            # Check if running and not a zombie
            if not self._creator_process.is_running():
                return False
            if self._creator_process.status() == psutil.STATUS_ZOMBIE:
                return False
            return True
        except (psutil.NoSuchProcess, Exception):
            # Fallback to zero-kill signal
            try:
                os.kill(self.parent_pid, 0)
                return True
            except OSError:
                return False

    def _check_leash_integrity(self) -> bool:
        """
        [ASCENSION 10]: Socratic Check.
        Verifies the Electron leash is present and not stale.
        """
        if not self.watch_file.exists():
            Logger.warn(f"Leash handle {self.watch_file.name} vanished.")
            return False

        try:
            # Check modification time
            mtime = self.watch_file.stat().st_mtime
            age = time.time() - mtime

            # [ASCENSION 3]: Adaptive Aging.
            # If the leash hasn't updated in 10s, the Cockpit is frozen.
            if age > 10.0:
                Logger.critical(f"Leash has flatlined (Age: {age:.2f}s). Terminating.")
                return False

            return True
        except Exception as e:
            # On Windows, PermissionError often means the file is being written to.
            # We treat "Busy" as "Alive".
            return True

    def _audit_internal_memory(self) -> bool:
        """
        [ASCENSION 5]: The Memory Sentry.
        """
        try:
            me = psutil.Process(os.getpid())
            rss_mb = me.memory_info().rss / 1024 / 1024
            if rss_mb > self._memory_ceiling_mb:
                Logger.critical(f"Memory Heresy: RSS ({rss_mb:.1f}MB) exceeds ceiling.")
                return False
            return True
        except:
            return True

    def adjust_metabolism(self, active_tasks: int):
        """
        [ASCENSION 3]: Adaptive Metabolic Rate.
        active_tasks > 0 -> Adrenaline (1s)
        active_tasks == 0 -> Zen (3s)
        """
        if active_tasks > 0:
            self._metabolic_rate = 1.0
        else:
            self._metabolic_rate = 3.0
        return self._metabolic_rate