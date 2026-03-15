# Path: core/alchemist/elara/library/architectural/substrate/vitals.py
# --------------------------------------------------------------------

import os
import sys
import shutil
import platform
import multiprocessing

class SystemVitals:
    """
    =============================================================================
    == THE SYSTEM VITALS (V-Ω-TOTALITY)                                        ==
    =============================================================================
    LIF: ∞ | ROLE: HARDWARE_PHYSICS_SENSOR

    [ASCENSIONS 25-28]:
    25. Dynamic CPU core detection.
    26. OS/Architecture mapping (ARM64 vs x86_64).
    27. GPU / Tensor-Core detection (CUDA/MPS).
    28. Executable verification (`which` proxy).
    """

    @property
    def cpu_cores(self) -> int:
        return multiprocessing.cpu_count()

    @property
    def optimal_workers(self) -> int:
        """[ASCENSION 25]: Recommends Uvicorn/Gunicorn worker count."""
        return (self.cpu_cores * 2) + 1

    @property
    def has_gpu(self) -> bool:
        """[ASCENSION 27]: Scries for NVIDIA/AMD iron."""
        # Simple heuristic: is nvidia-smi manifest?
        return shutil.which("nvidia-smi") is not None

    def can_run(self, binary: str) -> bool:
        """[ASCENSION 28]: Verifies artisan presence in the system PATH."""
        return shutil.which(binary) is not None

    @property
    def arch(self) -> str:
        """[ASCENSION 26]: Returns 'arm64' or 'x86_64'."""
        return platform.machine().lower()